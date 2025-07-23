r'''
# `google_data_catalog_entry`

Refer to the Terraform Registry for docs: [`google_data_catalog_entry`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry).
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


class DataCatalogEntry(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntry",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry google_data_catalog_entry}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        entry_group: builtins.str,
        entry_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        gcs_fileset_spec: typing.Optional[typing.Union["DataCatalogEntryGcsFilesetSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        linked_resource: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataCatalogEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        user_specified_system: typing.Optional[builtins.str] = None,
        user_specified_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry google_data_catalog_entry} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param entry_group: The name of the entry group this entry is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#entry_group DataCatalogEntry#entry_group}
        :param entry_id: The id of the entry to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#entry_id DataCatalogEntry#entry_id}
        :param description: Entry description, which can consist of several sentences or paragraphs that describe entry contents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#description DataCatalogEntry#description}
        :param display_name: Display information such as title and description. A short name to identify the entry, for example, "Analytics Data - Jan 2011". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#display_name DataCatalogEntry#display_name}
        :param gcs_fileset_spec: gcs_fileset_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#gcs_fileset_spec DataCatalogEntry#gcs_fileset_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#id DataCatalogEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param linked_resource: The resource this metadata entry refers to. For Google Cloud Platform resources, linkedResource is the full name of the resource. For example, the linkedResource for a table resource from BigQuery is: //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId Output only when Entry is of type in the EntryType enum. For entries with userSpecifiedType, this field is optional and defaults to an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#linked_resource DataCatalogEntry#linked_resource}
        :param schema: Schema of the entry (e.g. BigQuery, GoogleSQL, Avro schema), as a json string. An entry might not have any schema attached to it. See https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.entryGroups.entries#schema for what fields this schema can contain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#schema DataCatalogEntry#schema}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#timeouts DataCatalogEntry#timeouts}
        :param type: The type of the entry. Only used for Entries with types in the EntryType enum. Currently, only FILESET enum value is allowed. All other entries created through Data Catalog must use userSpecifiedType. Possible values: ["FILESET"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#type DataCatalogEntry#type}
        :param user_specified_system: This field indicates the entry's source system that Data Catalog does not integrate with. userSpecifiedSystem strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#user_specified_system DataCatalogEntry#user_specified_system}
        :param user_specified_type: Entry type if it does not fit any of the input-allowed values listed in EntryType enum above. When creating an entry, users should check the enum values first, if nothing matches the entry to be created, then provide a custom value, for example "my_special_type". userSpecifiedType strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#user_specified_type DataCatalogEntry#user_specified_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e2aee51c91c9218fe51c1a97af3308c2679403d32bfead0c4defc5a0fbe165)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataCatalogEntryConfig(
            entry_group=entry_group,
            entry_id=entry_id,
            description=description,
            display_name=display_name,
            gcs_fileset_spec=gcs_fileset_spec,
            id=id,
            linked_resource=linked_resource,
            schema=schema,
            timeouts=timeouts,
            type=type,
            user_specified_system=user_specified_system,
            user_specified_type=user_specified_type,
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
        '''Generates CDKTF code for importing a DataCatalogEntry resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataCatalogEntry to import.
        :param import_from_id: The id of the existing DataCatalogEntry that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataCatalogEntry to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb881c8c899075e4d242b5f96e68b8e6d38bbefdd4c9766a55b1fe056f732288)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGcsFilesetSpec")
    def put_gcs_fileset_spec(
        self,
        *,
        file_patterns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param file_patterns: Patterns to identify a set of files in Google Cloud Storage. See `Cloud Storage documentation <https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames>`_ for more information. Note that bucket wildcards are currently not supported. Examples of valid filePatterns: - gs://bucket_name/dir/*: matches all files within bucket_name/dir directory. - gs://bucket_name/dir/**: matches all files in bucket_name/dir spanning all subdirectories. - gs://bucket_name/file*: matches files prefixed by file in bucket_name - gs://bucket_name/??.txt: matches files with two characters followed by .txt in bucket_name - gs://bucket_name/[aeiou].txt: matches files that contain a single vowel character followed by .txt in bucket_name - gs://bucket_name/[a-m].txt: matches files that contain a, b, ... or m followed by .txt in bucket_name - gs://bucket_name/a/* /b: matches all files in bucket_name that match a/* /b pattern, such as a/c/b, a/d/b - gs://another_bucket/a.txt: matches gs://another_bucket/a.txt Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#file_patterns DataCatalogEntry#file_patterns} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DataCatalogEntryGcsFilesetSpec(file_patterns=file_patterns)

        return typing.cast(None, jsii.invoke(self, "putGcsFilesetSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#create DataCatalogEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#delete DataCatalogEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#update DataCatalogEntry#update}.
        '''
        value = DataCatalogEntryTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGcsFilesetSpec")
    def reset_gcs_fileset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsFilesetSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLinkedResource")
    def reset_linked_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedResource", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserSpecifiedSystem")
    def reset_user_specified_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserSpecifiedSystem", []))

    @jsii.member(jsii_name="resetUserSpecifiedType")
    def reset_user_specified_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserSpecifiedType", []))

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
    @jsii.member(jsii_name="bigqueryDateShardedSpec")
    def bigquery_date_sharded_spec(
        self,
    ) -> "DataCatalogEntryBigqueryDateShardedSpecList":
        return typing.cast("DataCatalogEntryBigqueryDateShardedSpecList", jsii.get(self, "bigqueryDateShardedSpec"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryTableSpec")
    def bigquery_table_spec(self) -> "DataCatalogEntryBigqueryTableSpecList":
        return typing.cast("DataCatalogEntryBigqueryTableSpecList", jsii.get(self, "bigqueryTableSpec"))

    @builtins.property
    @jsii.member(jsii_name="gcsFilesetSpec")
    def gcs_fileset_spec(self) -> "DataCatalogEntryGcsFilesetSpecOutputReference":
        return typing.cast("DataCatalogEntryGcsFilesetSpecOutputReference", jsii.get(self, "gcsFilesetSpec"))

    @builtins.property
    @jsii.member(jsii_name="integratedSystem")
    def integrated_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integratedSystem"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataCatalogEntryTimeoutsOutputReference":
        return typing.cast("DataCatalogEntryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="entryGroupInput")
    def entry_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="entryIdInput")
    def entry_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsFilesetSpecInput")
    def gcs_fileset_spec_input(
        self,
    ) -> typing.Optional["DataCatalogEntryGcsFilesetSpec"]:
        return typing.cast(typing.Optional["DataCatalogEntryGcsFilesetSpec"], jsii.get(self, "gcsFilesetSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedResourceInput")
    def linked_resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataCatalogEntryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataCatalogEntryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userSpecifiedSystemInput")
    def user_specified_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userSpecifiedSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="userSpecifiedTypeInput")
    def user_specified_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userSpecifiedTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c1757aa701d330efa5c3151dc4849dbbd4f0177fae32e1d5519e4d1a7ed389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87e13288db8010296f79725624e2c76057986f9b6d81be17c35c67423bce0e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryGroup")
    def entry_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryGroup"))

    @entry_group.setter
    def entry_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d446d4189efbe737e61ac367ea5ad3096d23a746213c5de963e668d695a143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryId")
    def entry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryId"))

    @entry_id.setter
    def entry_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9269ae65a4c11ea49aac8b0ab33989a61658b737a360d74bc43090e05c330f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7006ecb9a1dc1d460c102e589a982e2ec54ba6674f53b75effe637902975d8ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedResource")
    def linked_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedResource"))

    @linked_resource.setter
    def linked_resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f885bd7624d8fb9bdaff05a646e740db3ab6cac68877dae8580cb00bc4893d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83605fcd8cab7bccf4d268312a8cd8b87f1ac628a9cae0562533065cde0cca7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6398a2ad7120a92745dbebc6bc55a8c0f80b9ae901ad509656a484666e5a252a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userSpecifiedSystem")
    def user_specified_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userSpecifiedSystem"))

    @user_specified_system.setter
    def user_specified_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05254197602660acb99dd01f18f2c819ba40847d633c5c25cc3e76648b7b323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSpecifiedSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userSpecifiedType")
    def user_specified_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userSpecifiedType"))

    @user_specified_type.setter
    def user_specified_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a9ebd40e78717f0e2bcdca3fb14853c503016742a4f12bb86741fe77ccd085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSpecifiedType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryDateShardedSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCatalogEntryBigqueryDateShardedSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryBigqueryDateShardedSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogEntryBigqueryDateShardedSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryDateShardedSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04b1f5f1fcacf00386f9d372d864e335856686ebe8c217a1115cf40b74847d0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCatalogEntryBigqueryDateShardedSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4598208dfae8c0defb6bb0ae93f6bb637c727eedba4fc3c19efbc696965f6ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCatalogEntryBigqueryDateShardedSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797dbe9862238be5dc43a2f5a04af40dd9cc90f266dd53cc49bceb2c16481455)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8b3492581fd33079c2c2d4460bb4df72e35a37ec6b50587a7570c05f4756a4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3d00c73f1c941895475a6a1fe43c64a4694b39e07dcd6ac56c64bdba27d1fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataCatalogEntryBigqueryDateShardedSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryDateShardedSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__132f7efdea3caedbf2a3327ec6f228f099131023ee3fe1a141edecb4d958d255)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCatalogEntryBigqueryDateShardedSpec]:
        return typing.cast(typing.Optional[DataCatalogEntryBigqueryDateShardedSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogEntryBigqueryDateShardedSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1820b15e7347d20e1566cd6846511c062edb565f01da934cd47b20c73c196045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCatalogEntryBigqueryTableSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryBigqueryTableSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogEntryBigqueryTableSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f504547451e2a913bef824891c9ccc49464e5417fea1869eb231ee1affeb4c4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCatalogEntryBigqueryTableSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfccdb7aff95bb41526cf6338ba153bb84029a7201556aabfd01bf5596889d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCatalogEntryBigqueryTableSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15efa690b0fd68f2c469f894fcee26aaedffc6bb4455b8b36fb8e88e55473b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a74f136cfb1b67b2e0d0e93e01d3507293970a1c7fad9f335bca93f94bc06ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__791d20181a586aabb20af161daebad473773b98702108f9f754cf5dfc40bfafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataCatalogEntryBigqueryTableSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e559107467b0a7b8c6e9958b3fd2b1131e143dd5e9af7c42eae60e908ee7e96b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="tableSourceType")
    def table_source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableSourceType"))

    @builtins.property
    @jsii.member(jsii_name="tableSpec")
    def table_spec(self) -> "DataCatalogEntryBigqueryTableSpecTableSpecList":
        return typing.cast("DataCatalogEntryBigqueryTableSpecTableSpecList", jsii.get(self, "tableSpec"))

    @builtins.property
    @jsii.member(jsii_name="viewSpec")
    def view_spec(self) -> "DataCatalogEntryBigqueryTableSpecViewSpecList":
        return typing.cast("DataCatalogEntryBigqueryTableSpecViewSpecList", jsii.get(self, "viewSpec"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCatalogEntryBigqueryTableSpec]:
        return typing.cast(typing.Optional[DataCatalogEntryBigqueryTableSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogEntryBigqueryTableSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8a8f9a9bb318a5903e975acff4dbe814e9951e620640b4ef78b963debbc4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecTableSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCatalogEntryBigqueryTableSpecTableSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryBigqueryTableSpecTableSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogEntryBigqueryTableSpecTableSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecTableSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae139a1c048a3d3cd2cd92f5ca097ab9735a309ebf04281be5d0a75337f936d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCatalogEntryBigqueryTableSpecTableSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa33e6e73330dea815086cf3399dad0f99bd327720cf09ce84ff7a767b2f13e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCatalogEntryBigqueryTableSpecTableSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174e923ca221c9444a5871738b99c5b393d90755fc5d9058d7109d8e63f7e1fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__058214646cd3bfa6c4a8a377f495a57e6e90dbbc78e95fa5e36d002aa152548a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5838c2343563a59981f29a14bc4eee2333dcc28239e5afa42fdcea1ba8a22318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataCatalogEntryBigqueryTableSpecTableSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecTableSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ebf8a236145e7798679498fac2699855cf48d983324d9892695995a670ef90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="groupedEntry")
    def grouped_entry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupedEntry"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCatalogEntryBigqueryTableSpecTableSpec]:
        return typing.cast(typing.Optional[DataCatalogEntryBigqueryTableSpecTableSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogEntryBigqueryTableSpecTableSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e750a4816328790bd3ac9fcb123e0843a2f854b3da910eeed753f93072f7c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecViewSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCatalogEntryBigqueryTableSpecViewSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryBigqueryTableSpecViewSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogEntryBigqueryTableSpecViewSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecViewSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc1309c96d4845e979c7cc8b9c6e7402b489f2cce0d8f6cef66ec605ed7b6dd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCatalogEntryBigqueryTableSpecViewSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff536d72efeb22052d74d7a7c20939b199c725e8d0d557f6050c5aa1690c10bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCatalogEntryBigqueryTableSpecViewSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1a96b17e8614541eca2859ae9e43662444b3fa279a789ad7e3dca8a71458ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__002eb552ca29bd0cb1973a4b8b47a097fe3f5c625c8496f1f3cecd5c56740568)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75a56225355436cba5f498d594731cdf84336e631360299f59cf12885b115056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataCatalogEntryBigqueryTableSpecViewSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryBigqueryTableSpecViewSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce4c2513d322d14014ea6c2c9412cc807e68b1b846f57a882086238b2ac6636d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="viewQuery")
    def view_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "viewQuery"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCatalogEntryBigqueryTableSpecViewSpec]:
        return typing.cast(typing.Optional[DataCatalogEntryBigqueryTableSpecViewSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogEntryBigqueryTableSpecViewSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac28a76ecbeda6f48189e9d1c6daf4164de91c2e8b6323f0c784b1d4c2338513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "entry_group": "entryGroup",
        "entry_id": "entryId",
        "description": "description",
        "display_name": "displayName",
        "gcs_fileset_spec": "gcsFilesetSpec",
        "id": "id",
        "linked_resource": "linkedResource",
        "schema": "schema",
        "timeouts": "timeouts",
        "type": "type",
        "user_specified_system": "userSpecifiedSystem",
        "user_specified_type": "userSpecifiedType",
    },
)
class DataCatalogEntryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        entry_group: builtins.str,
        entry_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        gcs_fileset_spec: typing.Optional[typing.Union["DataCatalogEntryGcsFilesetSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        linked_resource: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataCatalogEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        user_specified_system: typing.Optional[builtins.str] = None,
        user_specified_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param entry_group: The name of the entry group this entry is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#entry_group DataCatalogEntry#entry_group}
        :param entry_id: The id of the entry to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#entry_id DataCatalogEntry#entry_id}
        :param description: Entry description, which can consist of several sentences or paragraphs that describe entry contents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#description DataCatalogEntry#description}
        :param display_name: Display information such as title and description. A short name to identify the entry, for example, "Analytics Data - Jan 2011". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#display_name DataCatalogEntry#display_name}
        :param gcs_fileset_spec: gcs_fileset_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#gcs_fileset_spec DataCatalogEntry#gcs_fileset_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#id DataCatalogEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param linked_resource: The resource this metadata entry refers to. For Google Cloud Platform resources, linkedResource is the full name of the resource. For example, the linkedResource for a table resource from BigQuery is: //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId Output only when Entry is of type in the EntryType enum. For entries with userSpecifiedType, this field is optional and defaults to an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#linked_resource DataCatalogEntry#linked_resource}
        :param schema: Schema of the entry (e.g. BigQuery, GoogleSQL, Avro schema), as a json string. An entry might not have any schema attached to it. See https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.entryGroups.entries#schema for what fields this schema can contain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#schema DataCatalogEntry#schema}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#timeouts DataCatalogEntry#timeouts}
        :param type: The type of the entry. Only used for Entries with types in the EntryType enum. Currently, only FILESET enum value is allowed. All other entries created through Data Catalog must use userSpecifiedType. Possible values: ["FILESET"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#type DataCatalogEntry#type}
        :param user_specified_system: This field indicates the entry's source system that Data Catalog does not integrate with. userSpecifiedSystem strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#user_specified_system DataCatalogEntry#user_specified_system}
        :param user_specified_type: Entry type if it does not fit any of the input-allowed values listed in EntryType enum above. When creating an entry, users should check the enum values first, if nothing matches the entry to be created, then provide a custom value, for example "my_special_type". userSpecifiedType strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#user_specified_type DataCatalogEntry#user_specified_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(gcs_fileset_spec, dict):
            gcs_fileset_spec = DataCatalogEntryGcsFilesetSpec(**gcs_fileset_spec)
        if isinstance(timeouts, dict):
            timeouts = DataCatalogEntryTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7bc76a585eb903b6d199fde5e0622512ffd53dd7c3572fae29e785a9baee755)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument entry_group", value=entry_group, expected_type=type_hints["entry_group"])
            check_type(argname="argument entry_id", value=entry_id, expected_type=type_hints["entry_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gcs_fileset_spec", value=gcs_fileset_spec, expected_type=type_hints["gcs_fileset_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument linked_resource", value=linked_resource, expected_type=type_hints["linked_resource"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_specified_system", value=user_specified_system, expected_type=type_hints["user_specified_system"])
            check_type(argname="argument user_specified_type", value=user_specified_type, expected_type=type_hints["user_specified_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entry_group": entry_group,
            "entry_id": entry_id,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if gcs_fileset_spec is not None:
            self._values["gcs_fileset_spec"] = gcs_fileset_spec
        if id is not None:
            self._values["id"] = id
        if linked_resource is not None:
            self._values["linked_resource"] = linked_resource
        if schema is not None:
            self._values["schema"] = schema
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if user_specified_system is not None:
            self._values["user_specified_system"] = user_specified_system
        if user_specified_type is not None:
            self._values["user_specified_type"] = user_specified_type

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
    def entry_group(self) -> builtins.str:
        '''The name of the entry group this entry is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#entry_group DataCatalogEntry#entry_group}
        '''
        result = self._values.get("entry_group")
        assert result is not None, "Required property 'entry_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entry_id(self) -> builtins.str:
        '''The id of the entry to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#entry_id DataCatalogEntry#entry_id}
        '''
        result = self._values.get("entry_id")
        assert result is not None, "Required property 'entry_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Entry description, which can consist of several sentences or paragraphs that describe entry contents.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#description DataCatalogEntry#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display information such as title and description.

        A short name to identify the entry,
        for example, "Analytics Data - Jan 2011".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#display_name DataCatalogEntry#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_fileset_spec(self) -> typing.Optional["DataCatalogEntryGcsFilesetSpec"]:
        '''gcs_fileset_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#gcs_fileset_spec DataCatalogEntry#gcs_fileset_spec}
        '''
        result = self._values.get("gcs_fileset_spec")
        return typing.cast(typing.Optional["DataCatalogEntryGcsFilesetSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#id DataCatalogEntry#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def linked_resource(self) -> typing.Optional[builtins.str]:
        '''The resource this metadata entry refers to.

        For Google Cloud Platform resources, linkedResource is the full name of the resource.
        For example, the linkedResource for a table resource from BigQuery is:
        //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId
        Output only when Entry is of type in the EntryType enum. For entries with userSpecifiedType,
        this field is optional and defaults to an empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#linked_resource DataCatalogEntry#linked_resource}
        '''
        result = self._values.get("linked_resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Schema of the entry (e.g. BigQuery, GoogleSQL, Avro schema), as a json string. An entry might not have any schema attached to it. See https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.entryGroups.entries#schema for what fields this schema can contain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#schema DataCatalogEntry#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataCatalogEntryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#timeouts DataCatalogEntry#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataCatalogEntryTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the entry.

        Only used for Entries with types in the EntryType enum.
        Currently, only FILESET enum value is allowed. All other entries created through Data Catalog must use userSpecifiedType. Possible values: ["FILESET"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#type DataCatalogEntry#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_specified_system(self) -> typing.Optional[builtins.str]:
        '''This field indicates the entry's source system that Data Catalog does not integrate with.

        userSpecifiedSystem strings must begin with a letter or underscore and can only contain letters, numbers,
        and underscores; are case insensitive; must be at least 1 character and at most 64 characters long.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#user_specified_system DataCatalogEntry#user_specified_system}
        '''
        result = self._values.get("user_specified_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_specified_type(self) -> typing.Optional[builtins.str]:
        '''Entry type if it does not fit any of the input-allowed values listed in EntryType enum above.

        When creating an entry, users should check the enum values first, if nothing matches the entry
        to be created, then provide a custom value, for example "my_special_type".
        userSpecifiedType strings must begin with a letter or underscore and can only contain letters,
        numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#user_specified_type DataCatalogEntry#user_specified_type}
        '''
        result = self._values.get("user_specified_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryGcsFilesetSpec",
    jsii_struct_bases=[],
    name_mapping={"file_patterns": "filePatterns"},
)
class DataCatalogEntryGcsFilesetSpec:
    def __init__(self, *, file_patterns: typing.Sequence[builtins.str]) -> None:
        '''
        :param file_patterns: Patterns to identify a set of files in Google Cloud Storage. See `Cloud Storage documentation <https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames>`_ for more information. Note that bucket wildcards are currently not supported. Examples of valid filePatterns: - gs://bucket_name/dir/*: matches all files within bucket_name/dir directory. - gs://bucket_name/dir/**: matches all files in bucket_name/dir spanning all subdirectories. - gs://bucket_name/file*: matches files prefixed by file in bucket_name - gs://bucket_name/??.txt: matches files with two characters followed by .txt in bucket_name - gs://bucket_name/[aeiou].txt: matches files that contain a single vowel character followed by .txt in bucket_name - gs://bucket_name/[a-m].txt: matches files that contain a, b, ... or m followed by .txt in bucket_name - gs://bucket_name/a/* /b: matches all files in bucket_name that match a/* /b pattern, such as a/c/b, a/d/b - gs://another_bucket/a.txt: matches gs://another_bucket/a.txt Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#file_patterns DataCatalogEntry#file_patterns} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd8159bcb8b812efaf4ddb3f182188b479e12df040e67a90eaf60519081d4ce)
            check_type(argname="argument file_patterns", value=file_patterns, expected_type=type_hints["file_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_patterns": file_patterns,
        }

    @builtins.property
    def file_patterns(self) -> typing.List[builtins.str]:
        '''Patterns to identify a set of files in Google Cloud Storage.

        See `Cloud Storage documentation <https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames>`_
        for more information. Note that bucket wildcards are currently not supported. Examples of valid filePatterns:

        - gs://bucket_name/dir/*: matches all files within bucket_name/dir directory.
        - gs://bucket_name/dir/**: matches all files in bucket_name/dir spanning all subdirectories.
        - gs://bucket_name/file*: matches files prefixed by file in bucket_name
        - gs://bucket_name/??.txt: matches files with two characters followed by .txt in bucket_name
        - gs://bucket_name/[aeiou].txt: matches files that contain a single vowel character followed by .txt in bucket_name
        - gs://bucket_name/[a-m].txt: matches files that contain a, b, ... or m followed by .txt in bucket_name
        - gs://bucket_name/a/* /b: matches all files in bucket_name that match a/* /b pattern, such as a/c/b, a/d/b
        - gs://another_bucket/a.txt: matches gs://another_bucket/a.txt

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#file_patterns DataCatalogEntry#file_patterns}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("file_patterns")
        assert result is not None, "Required property 'file_patterns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryGcsFilesetSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogEntryGcsFilesetSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryGcsFilesetSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e376866d7b2eb35cb98984a23a7553730c617b8ba23710784051850b651987d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sampleGcsFileSpecs")
    def sample_gcs_file_specs(
        self,
    ) -> "DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList":
        return typing.cast("DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList", jsii.get(self, "sampleGcsFileSpecs"))

    @builtins.property
    @jsii.member(jsii_name="filePatternsInput")
    def file_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "filePatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="filePatterns")
    def file_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "filePatterns"))

    @file_patterns.setter
    def file_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8cbc9cc51fbdae17ffc65afecdf678198c43cf1c7471284a29f76c557bbba33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCatalogEntryGcsFilesetSpec]:
        return typing.cast(typing.Optional[DataCatalogEntryGcsFilesetSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogEntryGcsFilesetSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b09ffdbbc85526f7f6ccf929ed2db642a12736e0bb52a7240e5cd1396e8113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4cc0e4fc29eb6a88233fa7521b3361d24903a710e0acfeb9006876f925f7d13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393f46cc1d586e860a91bf040c640bc4d111cc8049e45dacc1e2756ffe9a0fd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb329d526adffeecb3ad5322904ebd05f7adc223cd3dfe92b557f129fc6d2bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d33fd5c80b067cf3490b7b83bf5926b74f4b056a5dea6974f2680067e2b3cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dfaf4cdd2472d3e2c0b87868d1600dcdd424042063ca4a7d4817731eb123065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c404cf8e0bfb0cfc9631b04089bd33aa0db1eaa38ab8ec9520a239f70c929b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @builtins.property
    @jsii.member(jsii_name="sizeBytes")
    def size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs]:
        return typing.cast(typing.Optional[DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248d90ae4bce0c5f66002634a1f5692660af1f51cbc96d6c9eab97153f2a3c4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataCatalogEntryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#create DataCatalogEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#delete DataCatalogEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#update DataCatalogEntry#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99766ede2ca89bb63bfd71635da9d4501e4a3c74d87a3b0c6ef6c195d7c632a1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#create DataCatalogEntry#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#delete DataCatalogEntry#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_entry#update DataCatalogEntry#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogEntryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogEntryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogEntry.DataCatalogEntryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46d0d0d96d1de8c4d74eb988513e5fca812aaf70765df72ab5b5314b0241d7a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8d1fa684165c0287e407f5b2f48561e77a683a95283e816f2c312218d6a7a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e20ec8e4d52fb040348291c621ee46106b371efc7df992d0c8a43c012f4354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea670fe964c27cf96993caf1b73abd7932ccca3dfbf7e5a27a719f93662d3504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogEntryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogEntryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogEntryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba23ceb936f0014402d1d7391b4a06f3493327873afec1e10c34eafcc75b5882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataCatalogEntry",
    "DataCatalogEntryBigqueryDateShardedSpec",
    "DataCatalogEntryBigqueryDateShardedSpecList",
    "DataCatalogEntryBigqueryDateShardedSpecOutputReference",
    "DataCatalogEntryBigqueryTableSpec",
    "DataCatalogEntryBigqueryTableSpecList",
    "DataCatalogEntryBigqueryTableSpecOutputReference",
    "DataCatalogEntryBigqueryTableSpecTableSpec",
    "DataCatalogEntryBigqueryTableSpecTableSpecList",
    "DataCatalogEntryBigqueryTableSpecTableSpecOutputReference",
    "DataCatalogEntryBigqueryTableSpecViewSpec",
    "DataCatalogEntryBigqueryTableSpecViewSpecList",
    "DataCatalogEntryBigqueryTableSpecViewSpecOutputReference",
    "DataCatalogEntryConfig",
    "DataCatalogEntryGcsFilesetSpec",
    "DataCatalogEntryGcsFilesetSpecOutputReference",
    "DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs",
    "DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList",
    "DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference",
    "DataCatalogEntryTimeouts",
    "DataCatalogEntryTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b5e2aee51c91c9218fe51c1a97af3308c2679403d32bfead0c4defc5a0fbe165(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    entry_group: builtins.str,
    entry_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    gcs_fileset_spec: typing.Optional[typing.Union[DataCatalogEntryGcsFilesetSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    linked_resource: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataCatalogEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    user_specified_system: typing.Optional[builtins.str] = None,
    user_specified_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bb881c8c899075e4d242b5f96e68b8e6d38bbefdd4c9766a55b1fe056f732288(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c1757aa701d330efa5c3151dc4849dbbd4f0177fae32e1d5519e4d1a7ed389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87e13288db8010296f79725624e2c76057986f9b6d81be17c35c67423bce0e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d446d4189efbe737e61ac367ea5ad3096d23a746213c5de963e668d695a143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9269ae65a4c11ea49aac8b0ab33989a61658b737a360d74bc43090e05c330f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7006ecb9a1dc1d460c102e589a982e2ec54ba6674f53b75effe637902975d8ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f885bd7624d8fb9bdaff05a646e740db3ab6cac68877dae8580cb00bc4893d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83605fcd8cab7bccf4d268312a8cd8b87f1ac628a9cae0562533065cde0cca7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6398a2ad7120a92745dbebc6bc55a8c0f80b9ae901ad509656a484666e5a252a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05254197602660acb99dd01f18f2c819ba40847d633c5c25cc3e76648b7b323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a9ebd40e78717f0e2bcdca3fb14853c503016742a4f12bb86741fe77ccd085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b1f5f1fcacf00386f9d372d864e335856686ebe8c217a1115cf40b74847d0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4598208dfae8c0defb6bb0ae93f6bb637c727eedba4fc3c19efbc696965f6ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797dbe9862238be5dc43a2f5a04af40dd9cc90f266dd53cc49bceb2c16481455(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b3492581fd33079c2c2d4460bb4df72e35a37ec6b50587a7570c05f4756a4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d00c73f1c941895475a6a1fe43c64a4694b39e07dcd6ac56c64bdba27d1fb8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132f7efdea3caedbf2a3327ec6f228f099131023ee3fe1a141edecb4d958d255(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1820b15e7347d20e1566cd6846511c062edb565f01da934cd47b20c73c196045(
    value: typing.Optional[DataCatalogEntryBigqueryDateShardedSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f504547451e2a913bef824891c9ccc49464e5417fea1869eb231ee1affeb4c4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfccdb7aff95bb41526cf6338ba153bb84029a7201556aabfd01bf5596889d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15efa690b0fd68f2c469f894fcee26aaedffc6bb4455b8b36fb8e88e55473b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a74f136cfb1b67b2e0d0e93e01d3507293970a1c7fad9f335bca93f94bc06ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791d20181a586aabb20af161daebad473773b98702108f9f754cf5dfc40bfafd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e559107467b0a7b8c6e9958b3fd2b1131e143dd5e9af7c42eae60e908ee7e96b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8a8f9a9bb318a5903e975acff4dbe814e9951e620640b4ef78b963debbc4d9(
    value: typing.Optional[DataCatalogEntryBigqueryTableSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae139a1c048a3d3cd2cd92f5ca097ab9735a309ebf04281be5d0a75337f936d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa33e6e73330dea815086cf3399dad0f99bd327720cf09ce84ff7a767b2f13e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174e923ca221c9444a5871738b99c5b393d90755fc5d9058d7109d8e63f7e1fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058214646cd3bfa6c4a8a377f495a57e6e90dbbc78e95fa5e36d002aa152548a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5838c2343563a59981f29a14bc4eee2333dcc28239e5afa42fdcea1ba8a22318(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ebf8a236145e7798679498fac2699855cf48d983324d9892695995a670ef90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e750a4816328790bd3ac9fcb123e0843a2f854b3da910eeed753f93072f7c4(
    value: typing.Optional[DataCatalogEntryBigqueryTableSpecTableSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1309c96d4845e979c7cc8b9c6e7402b489f2cce0d8f6cef66ec605ed7b6dd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff536d72efeb22052d74d7a7c20939b199c725e8d0d557f6050c5aa1690c10bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1a96b17e8614541eca2859ae9e43662444b3fa279a789ad7e3dca8a71458ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002eb552ca29bd0cb1973a4b8b47a097fe3f5c625c8496f1f3cecd5c56740568(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a56225355436cba5f498d594731cdf84336e631360299f59cf12885b115056(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4c2513d322d14014ea6c2c9412cc807e68b1b846f57a882086238b2ac6636d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac28a76ecbeda6f48189e9d1c6daf4164de91c2e8b6323f0c784b1d4c2338513(
    value: typing.Optional[DataCatalogEntryBigqueryTableSpecViewSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bc76a585eb903b6d199fde5e0622512ffd53dd7c3572fae29e785a9baee755(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entry_group: builtins.str,
    entry_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    gcs_fileset_spec: typing.Optional[typing.Union[DataCatalogEntryGcsFilesetSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    linked_resource: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataCatalogEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    user_specified_system: typing.Optional[builtins.str] = None,
    user_specified_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd8159bcb8b812efaf4ddb3f182188b479e12df040e67a90eaf60519081d4ce(
    *,
    file_patterns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e376866d7b2eb35cb98984a23a7553730c617b8ba23710784051850b651987d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cbc9cc51fbdae17ffc65afecdf678198c43cf1c7471284a29f76c557bbba33(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b09ffdbbc85526f7f6ccf929ed2db642a12736e0bb52a7240e5cd1396e8113(
    value: typing.Optional[DataCatalogEntryGcsFilesetSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cc0e4fc29eb6a88233fa7521b3361d24903a710e0acfeb9006876f925f7d13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393f46cc1d586e860a91bf040c640bc4d111cc8049e45dacc1e2756ffe9a0fd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb329d526adffeecb3ad5322904ebd05f7adc223cd3dfe92b557f129fc6d2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d33fd5c80b067cf3490b7b83bf5926b74f4b056a5dea6974f2680067e2b3cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfaf4cdd2472d3e2c0b87868d1600dcdd424042063ca4a7d4817731eb123065(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c404cf8e0bfb0cfc9631b04089bd33aa0db1eaa38ab8ec9520a239f70c929b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248d90ae4bce0c5f66002634a1f5692660af1f51cbc96d6c9eab97153f2a3c4c(
    value: typing.Optional[DataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99766ede2ca89bb63bfd71635da9d4501e4a3c74d87a3b0c6ef6c195d7c632a1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d0d0d96d1de8c4d74eb988513e5fca812aaf70765df72ab5b5314b0241d7a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d1fa684165c0287e407f5b2f48561e77a683a95283e816f2c312218d6a7a5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e20ec8e4d52fb040348291c621ee46106b371efc7df992d0c8a43c012f4354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea670fe964c27cf96993caf1b73abd7932ccca3dfbf7e5a27a719f93662d3504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba23ceb936f0014402d1d7391b4a06f3493327873afec1e10c34eafcc75b5882(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogEntryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
