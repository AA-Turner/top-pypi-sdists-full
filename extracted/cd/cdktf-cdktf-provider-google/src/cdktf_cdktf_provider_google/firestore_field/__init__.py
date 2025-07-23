r'''
# `google_firestore_field`

Refer to the Terraform Registry for docs: [`google_firestore_field`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field).
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


class FirestoreField(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreField",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field google_firestore_field}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        collection: builtins.str,
        field: builtins.str,
        database: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        index_config: typing.Optional[typing.Union["FirestoreFieldIndexConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FirestoreFieldTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl_config: typing.Optional[typing.Union["FirestoreFieldTtlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field google_firestore_field} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param collection: The id of the collection group to configure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#collection FirestoreField#collection}
        :param field: The id of the field to configure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#field FirestoreField#field}
        :param database: The Firestore database id. Defaults to '"(default)"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#database FirestoreField#database}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#id FirestoreField#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_config: index_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#index_config FirestoreField#index_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#project FirestoreField#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#timeouts FirestoreField#timeouts}
        :param ttl_config: ttl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#ttl_config FirestoreField#ttl_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963d659dc64a31ca84e957b83d5f3aac9043f4e7253ddd5cc57a59b745072c37)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FirestoreFieldConfig(
            collection=collection,
            field=field,
            database=database,
            id=id,
            index_config=index_config,
            project=project,
            timeouts=timeouts,
            ttl_config=ttl_config,
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
        '''Generates CDKTF code for importing a FirestoreField resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FirestoreField to import.
        :param import_from_id: The id of the existing FirestoreField that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FirestoreField to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549b0d95c9a91e91685f06103afbd3fe551d6f36a77b274c242f5d2258efe9fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIndexConfig")
    def put_index_config(
        self,
        *,
        indexes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirestoreFieldIndexConfigIndexes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param indexes: indexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#indexes FirestoreField#indexes}
        '''
        value = FirestoreFieldIndexConfig(indexes=indexes)

        return typing.cast(None, jsii.invoke(self, "putIndexConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#create FirestoreField#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#delete FirestoreField#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#update FirestoreField#update}.
        '''
        value = FirestoreFieldTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTtlConfig")
    def put_ttl_config(self) -> None:
        value = FirestoreFieldTtlConfig()

        return typing.cast(None, jsii.invoke(self, "putTtlConfig", [value]))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIndexConfig")
    def reset_index_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTtlConfig")
    def reset_ttl_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtlConfig", []))

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
    @jsii.member(jsii_name="indexConfig")
    def index_config(self) -> "FirestoreFieldIndexConfigOutputReference":
        return typing.cast("FirestoreFieldIndexConfigOutputReference", jsii.get(self, "indexConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FirestoreFieldTimeoutsOutputReference":
        return typing.cast("FirestoreFieldTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="ttlConfig")
    def ttl_config(self) -> "FirestoreFieldTtlConfigOutputReference":
        return typing.cast("FirestoreFieldTtlConfigOutputReference", jsii.get(self, "ttlConfig"))

    @builtins.property
    @jsii.member(jsii_name="collectionInput")
    def collection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexConfigInput")
    def index_config_input(self) -> typing.Optional["FirestoreFieldIndexConfig"]:
        return typing.cast(typing.Optional["FirestoreFieldIndexConfig"], jsii.get(self, "indexConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirestoreFieldTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirestoreFieldTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlConfigInput")
    def ttl_config_input(self) -> typing.Optional["FirestoreFieldTtlConfig"]:
        return typing.cast(typing.Optional["FirestoreFieldTtlConfig"], jsii.get(self, "ttlConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="collection")
    def collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collection"))

    @collection.setter
    def collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6779c47b617cbb3ec04ce260779624eeae35891ec0a6b9b26a402b86e1ae6ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0eab60fd9adf37cfd6f12696523f9dfa344babf723f9428f9d0b6a06d4468b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bbf8f8ab1d00bc496b655680bbca79fadfcd5b822974fd36f19d7e8a79af4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a3d4f47db7263a83edefca38afd575338baa67fae502cacb94116ac749ac90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e48c26294ff835c8ce93b31f78d26a942cbf98f9060abb091bcd55bac37b4fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldConfig",
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
        "field": "field",
        "database": "database",
        "id": "id",
        "index_config": "indexConfig",
        "project": "project",
        "timeouts": "timeouts",
        "ttl_config": "ttlConfig",
    },
)
class FirestoreFieldConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        field: builtins.str,
        database: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        index_config: typing.Optional[typing.Union["FirestoreFieldIndexConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FirestoreFieldTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl_config: typing.Optional[typing.Union["FirestoreFieldTtlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param collection: The id of the collection group to configure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#collection FirestoreField#collection}
        :param field: The id of the field to configure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#field FirestoreField#field}
        :param database: The Firestore database id. Defaults to '"(default)"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#database FirestoreField#database}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#id FirestoreField#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_config: index_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#index_config FirestoreField#index_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#project FirestoreField#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#timeouts FirestoreField#timeouts}
        :param ttl_config: ttl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#ttl_config FirestoreField#ttl_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(index_config, dict):
            index_config = FirestoreFieldIndexConfig(**index_config)
        if isinstance(timeouts, dict):
            timeouts = FirestoreFieldTimeouts(**timeouts)
        if isinstance(ttl_config, dict):
            ttl_config = FirestoreFieldTtlConfig(**ttl_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e318c8728cbce29eaf9378e25a722867ff5257120ed960c3687d709c29a5cd4d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument collection", value=collection, expected_type=type_hints["collection"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index_config", value=index_config, expected_type=type_hints["index_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument ttl_config", value=ttl_config, expected_type=type_hints["ttl_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collection": collection,
            "field": field,
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
        if database is not None:
            self._values["database"] = database
        if id is not None:
            self._values["id"] = id
        if index_config is not None:
            self._values["index_config"] = index_config
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if ttl_config is not None:
            self._values["ttl_config"] = ttl_config

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
        '''The id of the collection group to configure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#collection FirestoreField#collection}
        '''
        result = self._values.get("collection")
        assert result is not None, "Required property 'collection' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field(self) -> builtins.str:
        '''The id of the field to configure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#field FirestoreField#field}
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''The Firestore database id. Defaults to '"(default)"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#database FirestoreField#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#id FirestoreField#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_config(self) -> typing.Optional["FirestoreFieldIndexConfig"]:
        '''index_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#index_config FirestoreField#index_config}
        '''
        result = self._values.get("index_config")
        return typing.cast(typing.Optional["FirestoreFieldIndexConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#project FirestoreField#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FirestoreFieldTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#timeouts FirestoreField#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FirestoreFieldTimeouts"], result)

    @builtins.property
    def ttl_config(self) -> typing.Optional["FirestoreFieldTtlConfig"]:
        '''ttl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#ttl_config FirestoreField#ttl_config}
        '''
        result = self._values.get("ttl_config")
        return typing.cast(typing.Optional["FirestoreFieldTtlConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreFieldConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldIndexConfig",
    jsii_struct_bases=[],
    name_mapping={"indexes": "indexes"},
)
class FirestoreFieldIndexConfig:
    def __init__(
        self,
        *,
        indexes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirestoreFieldIndexConfigIndexes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param indexes: indexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#indexes FirestoreField#indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f1e70903ee5b50c17dee76a0704f1a4d633f4d15a28ddc8be6a5e6b43f1fc1)
            check_type(argname="argument indexes", value=indexes, expected_type=type_hints["indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if indexes is not None:
            self._values["indexes"] = indexes

    @builtins.property
    def indexes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirestoreFieldIndexConfigIndexes"]]]:
        '''indexes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#indexes FirestoreField#indexes}
        '''
        result = self._values.get("indexes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirestoreFieldIndexConfigIndexes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreFieldIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldIndexConfigIndexes",
    jsii_struct_bases=[],
    name_mapping={
        "array_config": "arrayConfig",
        "order": "order",
        "query_scope": "queryScope",
    },
)
class FirestoreFieldIndexConfigIndexes:
    def __init__(
        self,
        *,
        array_config: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        query_scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param array_config: Indicates that this field supports operations on arrayValues. Only one of 'order' and 'arrayConfig' can be specified. Possible values: ["CONTAINS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#array_config FirestoreField#array_config}
        :param order: Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=, !=. Only one of 'order' and 'arrayConfig' can be specified. Possible values: ["ASCENDING", "DESCENDING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#order FirestoreField#order}
        :param query_scope: The scope at which a query is run. Collection scoped queries require you specify the collection at query time. Collection group scope allows queries across all collections with the same id. Default value: "COLLECTION" Possible values: ["COLLECTION", "COLLECTION_GROUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#query_scope FirestoreField#query_scope}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b287c53c78a596a973cedf55dc8adaae287c66d5ea22946b401d0ac56d7b37)
            check_type(argname="argument array_config", value=array_config, expected_type=type_hints["array_config"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument query_scope", value=query_scope, expected_type=type_hints["query_scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if array_config is not None:
            self._values["array_config"] = array_config
        if order is not None:
            self._values["order"] = order
        if query_scope is not None:
            self._values["query_scope"] = query_scope

    @builtins.property
    def array_config(self) -> typing.Optional[builtins.str]:
        '''Indicates that this field supports operations on arrayValues. Only one of 'order' and 'arrayConfig' can be specified. Possible values: ["CONTAINS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#array_config FirestoreField#array_config}
        '''
        result = self._values.get("array_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[builtins.str]:
        '''Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=, !=. Only one of 'order' and 'arrayConfig' can be specified. Possible values: ["ASCENDING", "DESCENDING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#order FirestoreField#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_scope(self) -> typing.Optional[builtins.str]:
        '''The scope at which a query is run.

        Collection scoped queries require you specify
        the collection at query time. Collection group scope allows queries across all
        collections with the same id. Default value: "COLLECTION" Possible values: ["COLLECTION", "COLLECTION_GROUP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#query_scope FirestoreField#query_scope}
        '''
        result = self._values.get("query_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreFieldIndexConfigIndexes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreFieldIndexConfigIndexesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldIndexConfigIndexesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60c3308f32c927b24f2605c8092c9e5321294f4849e4bcec65e3bde9ace44cb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirestoreFieldIndexConfigIndexesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b894ddd738613218eb286e95e08f1d5dbaf617835f96dca838057b885d2cf5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirestoreFieldIndexConfigIndexesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8730467e14c2a146600d4f24e0578b8eadbf97c10ddd0e1e269227e93c71437)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9002a85b1c7d49218e6717a3a31bcdbedf05843b6476a42cadb7766019ae3c1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fed6bfaaca225ee0405f8d289254751c203934266191faed19011bc05ab27733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreFieldIndexConfigIndexes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreFieldIndexConfigIndexes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreFieldIndexConfigIndexes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447e6d3bba40d62dcac0b22a7bbebebb71b1be4dfca924cd5be936f02ff0df64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirestoreFieldIndexConfigIndexesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldIndexConfigIndexesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd93a95142334c3ec5728eba0d57c93632e4725a2d1592d247c0b6ba7fb5ba78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArrayConfig")
    def reset_array_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArrayConfig", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetQueryScope")
    def reset_query_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryScope", []))

    @builtins.property
    @jsii.member(jsii_name="arrayConfigInput")
    def array_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arrayConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="queryScopeInput")
    def query_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayConfig")
    def array_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arrayConfig"))

    @array_config.setter
    def array_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfeb2972b36030e8c75dbb8474dfdfdb7741778f6e4e4eca71344dc015fbacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4191aad012aaf7a9e55296273390238f2d9a943e4b27646d86ce650dcc0b0077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryScope")
    def query_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryScope"))

    @query_scope.setter
    def query_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a8f566bc9766323c08e00f0931600289c2532672c5d48cafb7d0789865dfea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldIndexConfigIndexes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldIndexConfigIndexes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldIndexConfigIndexes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810f91cc7ef7bcff7b36df422a521cbc69d7f88775556e4e2a3d0365c3d748f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirestoreFieldIndexConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldIndexConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a8bc4472941fe8d242691e44674824e122e124e4e19414fcdc5c36be34d79da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIndexes")
    def put_indexes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirestoreFieldIndexConfigIndexes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415791df11b4fcbe55a6489202bac807518f0a2d48c2a954d6e52a5f97dc498b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIndexes", [value]))

    @jsii.member(jsii_name="resetIndexes")
    def reset_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="indexes")
    def indexes(self) -> FirestoreFieldIndexConfigIndexesList:
        return typing.cast(FirestoreFieldIndexConfigIndexesList, jsii.get(self, "indexes"))

    @builtins.property
    @jsii.member(jsii_name="indexesInput")
    def indexes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreFieldIndexConfigIndexes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreFieldIndexConfigIndexes]]], jsii.get(self, "indexesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirestoreFieldIndexConfig]:
        return typing.cast(typing.Optional[FirestoreFieldIndexConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FirestoreFieldIndexConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f0d7a5da310bb8ebd1415701044a94959942794146941ace7e298c9e34c46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FirestoreFieldTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#create FirestoreField#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#delete FirestoreField#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#update FirestoreField#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8fd6a811ed8adfd2f0299a4b4b28b342e0736007a7e9e82173802f5f275cef)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#create FirestoreField#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#delete FirestoreField#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_field#update FirestoreField#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreFieldTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreFieldTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0c32bef156c701ffcf815c9f031ebad7697bc00bb89c9e0885155bdd54fe4c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c63d52606166b45093530f7aa52a54ba1f1b5c8da418a17d8b04db7494b654d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bcf58f178ae7c17258a5d805e7255b5e1c126699a631a85ae67d7352f0dbe9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9763aa94d4e6bb6473d8919af5c915c6f493968e5981c12490a65e1eef6c4855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d75abcee262e3433d13874b9535b800f4c1eea922c792d408ada3d9ab79ba05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldTtlConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirestoreFieldTtlConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreFieldTtlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreFieldTtlConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreField.FirestoreFieldTtlConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bfdd85fa4beffac4e89566958400f0f7c3faa380743f8d548dc97bea181f877)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirestoreFieldTtlConfig]:
        return typing.cast(typing.Optional[FirestoreFieldTtlConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FirestoreFieldTtlConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a554a9d6b39992ff5987a6ae32a9f4aa8fe92879c23b1f6e7a1f7e3103aa601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FirestoreField",
    "FirestoreFieldConfig",
    "FirestoreFieldIndexConfig",
    "FirestoreFieldIndexConfigIndexes",
    "FirestoreFieldIndexConfigIndexesList",
    "FirestoreFieldIndexConfigIndexesOutputReference",
    "FirestoreFieldIndexConfigOutputReference",
    "FirestoreFieldTimeouts",
    "FirestoreFieldTimeoutsOutputReference",
    "FirestoreFieldTtlConfig",
    "FirestoreFieldTtlConfigOutputReference",
]

publication.publish()

def _typecheckingstub__963d659dc64a31ca84e957b83d5f3aac9043f4e7253ddd5cc57a59b745072c37(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    collection: builtins.str,
    field: builtins.str,
    database: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    index_config: typing.Optional[typing.Union[FirestoreFieldIndexConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FirestoreFieldTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl_config: typing.Optional[typing.Union[FirestoreFieldTtlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__549b0d95c9a91e91685f06103afbd3fe551d6f36a77b274c242f5d2258efe9fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6779c47b617cbb3ec04ce260779624eeae35891ec0a6b9b26a402b86e1ae6ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eab60fd9adf37cfd6f12696523f9dfa344babf723f9428f9d0b6a06d4468b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bbf8f8ab1d00bc496b655680bbca79fadfcd5b822974fd36f19d7e8a79af4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a3d4f47db7263a83edefca38afd575338baa67fae502cacb94116ac749ac90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e48c26294ff835c8ce93b31f78d26a942cbf98f9060abb091bcd55bac37b4fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e318c8728cbce29eaf9378e25a722867ff5257120ed960c3687d709c29a5cd4d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    collection: builtins.str,
    field: builtins.str,
    database: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    index_config: typing.Optional[typing.Union[FirestoreFieldIndexConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FirestoreFieldTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl_config: typing.Optional[typing.Union[FirestoreFieldTtlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f1e70903ee5b50c17dee76a0704f1a4d633f4d15a28ddc8be6a5e6b43f1fc1(
    *,
    indexes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirestoreFieldIndexConfigIndexes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b287c53c78a596a973cedf55dc8adaae287c66d5ea22946b401d0ac56d7b37(
    *,
    array_config: typing.Optional[builtins.str] = None,
    order: typing.Optional[builtins.str] = None,
    query_scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c3308f32c927b24f2605c8092c9e5321294f4849e4bcec65e3bde9ace44cb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b894ddd738613218eb286e95e08f1d5dbaf617835f96dca838057b885d2cf5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8730467e14c2a146600d4f24e0578b8eadbf97c10ddd0e1e269227e93c71437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9002a85b1c7d49218e6717a3a31bcdbedf05843b6476a42cadb7766019ae3c1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed6bfaaca225ee0405f8d289254751c203934266191faed19011bc05ab27733(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447e6d3bba40d62dcac0b22a7bbebebb71b1be4dfca924cd5be936f02ff0df64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreFieldIndexConfigIndexes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd93a95142334c3ec5728eba0d57c93632e4725a2d1592d247c0b6ba7fb5ba78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfeb2972b36030e8c75dbb8474dfdfdb7741778f6e4e4eca71344dc015fbacf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4191aad012aaf7a9e55296273390238f2d9a943e4b27646d86ce650dcc0b0077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a8f566bc9766323c08e00f0931600289c2532672c5d48cafb7d0789865dfea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810f91cc7ef7bcff7b36df422a521cbc69d7f88775556e4e2a3d0365c3d748f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldIndexConfigIndexes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8bc4472941fe8d242691e44674824e122e124e4e19414fcdc5c36be34d79da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415791df11b4fcbe55a6489202bac807518f0a2d48c2a954d6e52a5f97dc498b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirestoreFieldIndexConfigIndexes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f0d7a5da310bb8ebd1415701044a94959942794146941ace7e298c9e34c46c(
    value: typing.Optional[FirestoreFieldIndexConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8fd6a811ed8adfd2f0299a4b4b28b342e0736007a7e9e82173802f5f275cef(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c32bef156c701ffcf815c9f031ebad7697bc00bb89c9e0885155bdd54fe4c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c63d52606166b45093530f7aa52a54ba1f1b5c8da418a17d8b04db7494b654d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bcf58f178ae7c17258a5d805e7255b5e1c126699a631a85ae67d7352f0dbe9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9763aa94d4e6bb6473d8919af5c915c6f493968e5981c12490a65e1eef6c4855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d75abcee262e3433d13874b9535b800f4c1eea922c792d408ada3d9ab79ba05(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreFieldTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfdd85fa4beffac4e89566958400f0f7c3faa380743f8d548dc97bea181f877(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a554a9d6b39992ff5987a6ae32a9f4aa8fe92879c23b1f6e7a1f7e3103aa601(
    value: typing.Optional[FirestoreFieldTtlConfig],
) -> None:
    """Type checking stubs"""
    pass
