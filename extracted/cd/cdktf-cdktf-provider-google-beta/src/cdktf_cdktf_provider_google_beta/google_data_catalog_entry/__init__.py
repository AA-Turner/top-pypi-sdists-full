r'''
# `google_data_catalog_entry`

Refer to the Terraform Registry for docs: [`google_data_catalog_entry`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry).
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


class GoogleDataCatalogEntry(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntry",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry google_data_catalog_entry}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        entry_group: builtins.str,
        entry_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        gcs_fileset_spec: typing.Optional[typing.Union["GoogleDataCatalogEntryGcsFilesetSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        linked_resource: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataCatalogEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry google_data_catalog_entry} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param entry_group: The name of the entry group this entry is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#entry_group GoogleDataCatalogEntry#entry_group}
        :param entry_id: The id of the entry to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#entry_id GoogleDataCatalogEntry#entry_id}
        :param description: Entry description, which can consist of several sentences or paragraphs that describe entry contents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#description GoogleDataCatalogEntry#description}
        :param display_name: Display information such as title and description. A short name to identify the entry, for example, "Analytics Data - Jan 2011". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#display_name GoogleDataCatalogEntry#display_name}
        :param gcs_fileset_spec: gcs_fileset_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#gcs_fileset_spec GoogleDataCatalogEntry#gcs_fileset_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#id GoogleDataCatalogEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param linked_resource: The resource this metadata entry refers to. For Google Cloud Platform resources, linkedResource is the full name of the resource. For example, the linkedResource for a table resource from BigQuery is: //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId Output only when Entry is of type in the EntryType enum. For entries with userSpecifiedType, this field is optional and defaults to an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#linked_resource GoogleDataCatalogEntry#linked_resource}
        :param schema: Schema of the entry (e.g. BigQuery, GoogleSQL, Avro schema), as a json string. An entry might not have any schema attached to it. See https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.entryGroups.entries#schema for what fields this schema can contain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#schema GoogleDataCatalogEntry#schema}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#timeouts GoogleDataCatalogEntry#timeouts}
        :param type: The type of the entry. Only used for Entries with types in the EntryType enum. Currently, only FILESET enum value is allowed. All other entries created through Data Catalog must use userSpecifiedType. Possible values: ["FILESET"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#type GoogleDataCatalogEntry#type}
        :param user_specified_system: This field indicates the entry's source system that Data Catalog does not integrate with. userSpecifiedSystem strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#user_specified_system GoogleDataCatalogEntry#user_specified_system}
        :param user_specified_type: Entry type if it does not fit any of the input-allowed values listed in EntryType enum above. When creating an entry, users should check the enum values first, if nothing matches the entry to be created, then provide a custom value, for example "my_special_type". userSpecifiedType strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#user_specified_type GoogleDataCatalogEntry#user_specified_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789e6860d61d8fcc956bbd0633891f0f51324093d6b42200b64e37a82bc89026)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataCatalogEntryConfig(
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
        '''Generates CDKTF code for importing a GoogleDataCatalogEntry resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataCatalogEntry to import.
        :param import_from_id: The id of the existing GoogleDataCatalogEntry that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataCatalogEntry to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4509acf846661ecb6e07beefc13b9e031ae034d078726d218e6403696f0f948)
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
        :param file_patterns: Patterns to identify a set of files in Google Cloud Storage. See `Cloud Storage documentation <https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames>`_ for more information. Note that bucket wildcards are currently not supported. Examples of valid filePatterns: - gs://bucket_name/dir/*: matches all files within bucket_name/dir directory. - gs://bucket_name/dir/**: matches all files in bucket_name/dir spanning all subdirectories. - gs://bucket_name/file*: matches files prefixed by file in bucket_name - gs://bucket_name/??.txt: matches files with two characters followed by .txt in bucket_name - gs://bucket_name/[aeiou].txt: matches files that contain a single vowel character followed by .txt in bucket_name - gs://bucket_name/[a-m].txt: matches files that contain a, b, ... or m followed by .txt in bucket_name - gs://bucket_name/a/* /b: matches all files in bucket_name that match a/* /b pattern, such as a/c/b, a/d/b - gs://another_bucket/a.txt: matches gs://another_bucket/a.txt Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#file_patterns GoogleDataCatalogEntry#file_patterns} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDataCatalogEntryGcsFilesetSpec(file_patterns=file_patterns)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#create GoogleDataCatalogEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#delete GoogleDataCatalogEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#update GoogleDataCatalogEntry#update}.
        '''
        value = GoogleDataCatalogEntryTimeouts(
            create=create, delete=delete, update=update
        )

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
    ) -> "GoogleDataCatalogEntryBigqueryDateShardedSpecList":
        return typing.cast("GoogleDataCatalogEntryBigqueryDateShardedSpecList", jsii.get(self, "bigqueryDateShardedSpec"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryTableSpec")
    def bigquery_table_spec(self) -> "GoogleDataCatalogEntryBigqueryTableSpecList":
        return typing.cast("GoogleDataCatalogEntryBigqueryTableSpecList", jsii.get(self, "bigqueryTableSpec"))

    @builtins.property
    @jsii.member(jsii_name="gcsFilesetSpec")
    def gcs_fileset_spec(self) -> "GoogleDataCatalogEntryGcsFilesetSpecOutputReference":
        return typing.cast("GoogleDataCatalogEntryGcsFilesetSpecOutputReference", jsii.get(self, "gcsFilesetSpec"))

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
    def timeouts(self) -> "GoogleDataCatalogEntryTimeoutsOutputReference":
        return typing.cast("GoogleDataCatalogEntryTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleDataCatalogEntryGcsFilesetSpec"]:
        return typing.cast(typing.Optional["GoogleDataCatalogEntryGcsFilesetSpec"], jsii.get(self, "gcsFilesetSpecInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataCatalogEntryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataCatalogEntryTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0ef022638b96722c42a93b7b080adb558ee0cc27f13c2e02f27c698e2093472c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cedf5e5672622dbf99bd3b1848931b6bba7d0c6770bae9535157ffa818b5e179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryGroup")
    def entry_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryGroup"))

    @entry_group.setter
    def entry_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc1d3995a9213d666693c1a4d7d359bb6b906282784fc9b57cd7f5a3a046988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryId")
    def entry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryId"))

    @entry_id.setter
    def entry_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309c2761e4d8b9149d01ccf2eb5f7a6784be60675040bf526f40b33dc6f3cbd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee843418db8ef142e32117ad79c44b33b3f6181b25e7cb88577260353eb45b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedResource")
    def linked_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedResource"))

    @linked_resource.setter
    def linked_resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b38868b27e190579f96723c257d62aac3f8b3758a42b56d851ea5b4e62113f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16bf8cbe000f8cf1e9e4452431bb79ddc35d2f31893d2c8eff048043e9d8d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1425189ee4feff1e719d90d7c48cb3be0fab742e247688d23a02f66be6badb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userSpecifiedSystem")
    def user_specified_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userSpecifiedSystem"))

    @user_specified_system.setter
    def user_specified_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91aec37b293e010a86e8201fd1ed2431ddb2db3ed7590485ae5f927e2e0f160f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSpecifiedSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userSpecifiedType")
    def user_specified_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userSpecifiedType"))

    @user_specified_type.setter
    def user_specified_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edfa7c55e96b2a6177c6625410ce52912e22b2ee0e7c67c08eccea07cda34dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSpecifiedType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryDateShardedSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataCatalogEntryBigqueryDateShardedSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataCatalogEntryBigqueryDateShardedSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataCatalogEntryBigqueryDateShardedSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryDateShardedSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b0a277b13a5282e27cc82fa6c958e1c1f5614e683f500d577fb0f89f139e7d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataCatalogEntryBigqueryDateShardedSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c81721e6037f63649a0465b4b38860a9c36c1015fb1bcb91e26d186ec5c127)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataCatalogEntryBigqueryDateShardedSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22bea8f2342b9e5617a8ec321d2fe4782fd67b9aa78c022cf3d7f5f9101c03b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e534923345e2e25477687fe3826fedd9fed96166485903876fae65218f69cc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a024439381d5ebf1bd436095fa89a79092de112ffd64f2776d46ed407aed53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataCatalogEntryBigqueryDateShardedSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryDateShardedSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c0c731cd89b978f2b60e3b802c0b7dc1a7e13142b20905149cc002c3a4fda07)
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
    ) -> typing.Optional[GoogleDataCatalogEntryBigqueryDateShardedSpec]:
        return typing.cast(typing.Optional[GoogleDataCatalogEntryBigqueryDateShardedSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataCatalogEntryBigqueryDateShardedSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e2e1bcb8e20ee411d1bae46a7d0041e8ab2baa8ca0501203ad4efe38c35f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataCatalogEntryBigqueryTableSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataCatalogEntryBigqueryTableSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataCatalogEntryBigqueryTableSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b92a00c0ee72644e31c18a684aa053e6b05f6fbeac329c2b7ed62b4e87ef082d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataCatalogEntryBigqueryTableSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450eceda6d1c6b16ae3136be6bd2f8c0eee02ea0c1047fa9992932923678026f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataCatalogEntryBigqueryTableSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb06be12a898d22ba7baa50d091dbacab7b3dd8edfbfdde7b0beab6dc7d4ff8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d1b2715b708e005db9286e180d83badb97bff80569bcb9b9e8ad0db96f0b32e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9a133d105ba6594cf99ab8764e92b1dc8555e2c392dbf491ae5f3151e70413a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataCatalogEntryBigqueryTableSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c1913a2102f620a8955707a6b81a233b2da8542434029010bbeef08092f482)
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
    def table_spec(self) -> "GoogleDataCatalogEntryBigqueryTableSpecTableSpecList":
        return typing.cast("GoogleDataCatalogEntryBigqueryTableSpecTableSpecList", jsii.get(self, "tableSpec"))

    @builtins.property
    @jsii.member(jsii_name="viewSpec")
    def view_spec(self) -> "GoogleDataCatalogEntryBigqueryTableSpecViewSpecList":
        return typing.cast("GoogleDataCatalogEntryBigqueryTableSpecViewSpecList", jsii.get(self, "viewSpec"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataCatalogEntryBigqueryTableSpec]:
        return typing.cast(typing.Optional[GoogleDataCatalogEntryBigqueryTableSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataCatalogEntryBigqueryTableSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e62e4adf1579d3e6697f7cdfb1df999b2c54b296870fb9425f16fbb1a2175f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecTableSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataCatalogEntryBigqueryTableSpecTableSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataCatalogEntryBigqueryTableSpecTableSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataCatalogEntryBigqueryTableSpecTableSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecTableSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2eb66c76567ff62c2584c7ef7fdd94c1d798a64971b274cba9e6e20a4b5bb65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataCatalogEntryBigqueryTableSpecTableSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a200d84cb5276bd2f7407c2dd99e69e052b0d46dac9d8a585b733d2133b6ab17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataCatalogEntryBigqueryTableSpecTableSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2821fda32ce76fc74eda680602eda50ae08a12db4f0f5a4fb56f8ede053a0c5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c94f5f9562b70390acb8b9ee6046e7b89d2bbc802c75b2c2a3adb108fc040a72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c89d7b81f1a17e7d656f0ca7101df915360110c45528d6e2ab6e26e3783666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataCatalogEntryBigqueryTableSpecTableSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecTableSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__beb8875ac39c3c760a8dd7f2fbe679c40b8db7da8b1315da31916ddc4503e32b)
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
    ) -> typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecTableSpec]:
        return typing.cast(typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecTableSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecTableSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21501c170034974d8276ec37f6995361fa6452e3a0321167ca1260c61f42c78c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecViewSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataCatalogEntryBigqueryTableSpecViewSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataCatalogEntryBigqueryTableSpecViewSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataCatalogEntryBigqueryTableSpecViewSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecViewSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7dafc2c86ac6042eda3891299438e4bdda2918015440c4e58447a5dbf0e0e53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataCatalogEntryBigqueryTableSpecViewSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd759ec853ffeff748d819753476561c7ccc691c618fef13ec399ec1174dcc4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataCatalogEntryBigqueryTableSpecViewSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ece27d733231d01127b6bad5491468ed114b3ead0a3f932f2998d60338408fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__696663ea6fe964ff29d01e4e306680c95a44bc29a7b53e87c3d5d0c14b654add)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8c9c5463a86edc2f5061ef505c4fe4276fe8ac5224cd4ad8b19fb16d01c75b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataCatalogEntryBigqueryTableSpecViewSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryBigqueryTableSpecViewSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d011ab91b20de629885468a93a878d1e817f312dd9035dd7c73822529b8c9c35)
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
    ) -> typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecViewSpec]:
        return typing.cast(typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecViewSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecViewSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82955c986dfeba695337ae45b6b8047986e2c090a120bba8c1de47f4d66ad243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryConfig",
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
class GoogleDataCatalogEntryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gcs_fileset_spec: typing.Optional[typing.Union["GoogleDataCatalogEntryGcsFilesetSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        linked_resource: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataCatalogEntryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param entry_group: The name of the entry group this entry is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#entry_group GoogleDataCatalogEntry#entry_group}
        :param entry_id: The id of the entry to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#entry_id GoogleDataCatalogEntry#entry_id}
        :param description: Entry description, which can consist of several sentences or paragraphs that describe entry contents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#description GoogleDataCatalogEntry#description}
        :param display_name: Display information such as title and description. A short name to identify the entry, for example, "Analytics Data - Jan 2011". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#display_name GoogleDataCatalogEntry#display_name}
        :param gcs_fileset_spec: gcs_fileset_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#gcs_fileset_spec GoogleDataCatalogEntry#gcs_fileset_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#id GoogleDataCatalogEntry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param linked_resource: The resource this metadata entry refers to. For Google Cloud Platform resources, linkedResource is the full name of the resource. For example, the linkedResource for a table resource from BigQuery is: //bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId Output only when Entry is of type in the EntryType enum. For entries with userSpecifiedType, this field is optional and defaults to an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#linked_resource GoogleDataCatalogEntry#linked_resource}
        :param schema: Schema of the entry (e.g. BigQuery, GoogleSQL, Avro schema), as a json string. An entry might not have any schema attached to it. See https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.entryGroups.entries#schema for what fields this schema can contain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#schema GoogleDataCatalogEntry#schema}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#timeouts GoogleDataCatalogEntry#timeouts}
        :param type: The type of the entry. Only used for Entries with types in the EntryType enum. Currently, only FILESET enum value is allowed. All other entries created through Data Catalog must use userSpecifiedType. Possible values: ["FILESET"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#type GoogleDataCatalogEntry#type}
        :param user_specified_system: This field indicates the entry's source system that Data Catalog does not integrate with. userSpecifiedSystem strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#user_specified_system GoogleDataCatalogEntry#user_specified_system}
        :param user_specified_type: Entry type if it does not fit any of the input-allowed values listed in EntryType enum above. When creating an entry, users should check the enum values first, if nothing matches the entry to be created, then provide a custom value, for example "my_special_type". userSpecifiedType strings must begin with a letter or underscore and can only contain letters, numbers, and underscores; are case insensitive; must be at least 1 character and at most 64 characters long. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#user_specified_type GoogleDataCatalogEntry#user_specified_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(gcs_fileset_spec, dict):
            gcs_fileset_spec = GoogleDataCatalogEntryGcsFilesetSpec(**gcs_fileset_spec)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataCatalogEntryTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec307687f9530e2d6839667f414b8380a100235957f4b2fe012f4c31a882256)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#entry_group GoogleDataCatalogEntry#entry_group}
        '''
        result = self._values.get("entry_group")
        assert result is not None, "Required property 'entry_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entry_id(self) -> builtins.str:
        '''The id of the entry to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#entry_id GoogleDataCatalogEntry#entry_id}
        '''
        result = self._values.get("entry_id")
        assert result is not None, "Required property 'entry_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Entry description, which can consist of several sentences or paragraphs that describe entry contents.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#description GoogleDataCatalogEntry#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display information such as title and description.

        A short name to identify the entry,
        for example, "Analytics Data - Jan 2011".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#display_name GoogleDataCatalogEntry#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_fileset_spec(
        self,
    ) -> typing.Optional["GoogleDataCatalogEntryGcsFilesetSpec"]:
        '''gcs_fileset_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#gcs_fileset_spec GoogleDataCatalogEntry#gcs_fileset_spec}
        '''
        result = self._values.get("gcs_fileset_spec")
        return typing.cast(typing.Optional["GoogleDataCatalogEntryGcsFilesetSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#id GoogleDataCatalogEntry#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#linked_resource GoogleDataCatalogEntry#linked_resource}
        '''
        result = self._values.get("linked_resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Schema of the entry (e.g. BigQuery, GoogleSQL, Avro schema), as a json string. An entry might not have any schema attached to it. See https://cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.entryGroups.entries#schema for what fields this schema can contain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#schema GoogleDataCatalogEntry#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataCatalogEntryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#timeouts GoogleDataCatalogEntry#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataCatalogEntryTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the entry.

        Only used for Entries with types in the EntryType enum.
        Currently, only FILESET enum value is allowed. All other entries created through Data Catalog must use userSpecifiedType. Possible values: ["FILESET"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#type GoogleDataCatalogEntry#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_specified_system(self) -> typing.Optional[builtins.str]:
        '''This field indicates the entry's source system that Data Catalog does not integrate with.

        userSpecifiedSystem strings must begin with a letter or underscore and can only contain letters, numbers,
        and underscores; are case insensitive; must be at least 1 character and at most 64 characters long.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#user_specified_system GoogleDataCatalogEntry#user_specified_system}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#user_specified_type GoogleDataCatalogEntry#user_specified_type}
        '''
        result = self._values.get("user_specified_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataCatalogEntryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryGcsFilesetSpec",
    jsii_struct_bases=[],
    name_mapping={"file_patterns": "filePatterns"},
)
class GoogleDataCatalogEntryGcsFilesetSpec:
    def __init__(self, *, file_patterns: typing.Sequence[builtins.str]) -> None:
        '''
        :param file_patterns: Patterns to identify a set of files in Google Cloud Storage. See `Cloud Storage documentation <https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames>`_ for more information. Note that bucket wildcards are currently not supported. Examples of valid filePatterns: - gs://bucket_name/dir/*: matches all files within bucket_name/dir directory. - gs://bucket_name/dir/**: matches all files in bucket_name/dir spanning all subdirectories. - gs://bucket_name/file*: matches files prefixed by file in bucket_name - gs://bucket_name/??.txt: matches files with two characters followed by .txt in bucket_name - gs://bucket_name/[aeiou].txt: matches files that contain a single vowel character followed by .txt in bucket_name - gs://bucket_name/[a-m].txt: matches files that contain a, b, ... or m followed by .txt in bucket_name - gs://bucket_name/a/* /b: matches all files in bucket_name that match a/* /b pattern, such as a/c/b, a/d/b - gs://another_bucket/a.txt: matches gs://another_bucket/a.txt Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#file_patterns GoogleDataCatalogEntry#file_patterns} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d06b0c7925dbc5eca056b48eb3726d036ef5327fb6d3d7d2609dd3521de10f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#file_patterns GoogleDataCatalogEntry#file_patterns}

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
        return "GoogleDataCatalogEntryGcsFilesetSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataCatalogEntryGcsFilesetSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryGcsFilesetSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28f22cad7b281eedd9b0f8a189e38d007a38b411c6ade2160ec893ac86a826da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sampleGcsFileSpecs")
    def sample_gcs_file_specs(
        self,
    ) -> "GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList":
        return typing.cast("GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList", jsii.get(self, "sampleGcsFileSpecs"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e83171cb8c068bbc377911970293a125da77186512af0ccc0a2fdae4a0ec66b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataCatalogEntryGcsFilesetSpec]:
        return typing.cast(typing.Optional[GoogleDataCatalogEntryGcsFilesetSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataCatalogEntryGcsFilesetSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91863c3bfc17c7a7ad99004077409abfa4cf6aa3944c5348b62c50fe42ef32e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__809bc4849eaa1d1ec6f2ab33ccaf8af1428dda26dc7380e1f7b40959040e2198)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd1e697b2cf47a1b5f6ed0d372cfb41b3b4db96867c81e325bc9ba2417954af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc13eaac8d808dc39b0263e7fc784a7fd54df8ac3d6bf8ad83fee621384109cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d35c4f8ae203ff1fc545b03932d94940ca5a06be229a6099c0680a27e33627c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6657fc3f93731fc2d8f0a143aaa3d1ce1909785035193c4a21c338a93bb6ed92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c7bc206d8eae685334cbfc5370787a7e09abadc73f0f1cc50a30a6a0b3174bd)
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
    ) -> typing.Optional[GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs]:
        return typing.cast(typing.Optional[GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6337a57d1f891fe9b85dfcb15fecc7d1bf224c5c678b536093fef6089f6f4965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataCatalogEntryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#create GoogleDataCatalogEntry#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#delete GoogleDataCatalogEntry#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#update GoogleDataCatalogEntry#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae4ffd97f6912ce43fda939d5ec9eeab1303f646687bf10c00442b36ab2fafa)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#create GoogleDataCatalogEntry#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#delete GoogleDataCatalogEntry#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_catalog_entry#update GoogleDataCatalogEntry#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataCatalogEntryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataCatalogEntryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataCatalogEntry.GoogleDataCatalogEntryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e5b48eac08243cb264c3b650f1c6c8b2a4dfe9f4fea04e783210aa09fd0de07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd0e4fbbb33b1d38463e063b5e196f3204f3c6c0de10a193193d57db56789544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cef196ae13accff3a122ffde2a5da31bc218a756a3e9ff3344cb92367c5b442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db99a49149358a59412417ffc94b037123144e02f3d9c8667b626dbbb3e47899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataCatalogEntryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataCatalogEntryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataCatalogEntryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0284aa0ff57ca441b3a0b524258006d9d3ec257b44cc1bb8fd0c0552e1e7f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataCatalogEntry",
    "GoogleDataCatalogEntryBigqueryDateShardedSpec",
    "GoogleDataCatalogEntryBigqueryDateShardedSpecList",
    "GoogleDataCatalogEntryBigqueryDateShardedSpecOutputReference",
    "GoogleDataCatalogEntryBigqueryTableSpec",
    "GoogleDataCatalogEntryBigqueryTableSpecList",
    "GoogleDataCatalogEntryBigqueryTableSpecOutputReference",
    "GoogleDataCatalogEntryBigqueryTableSpecTableSpec",
    "GoogleDataCatalogEntryBigqueryTableSpecTableSpecList",
    "GoogleDataCatalogEntryBigqueryTableSpecTableSpecOutputReference",
    "GoogleDataCatalogEntryBigqueryTableSpecViewSpec",
    "GoogleDataCatalogEntryBigqueryTableSpecViewSpecList",
    "GoogleDataCatalogEntryBigqueryTableSpecViewSpecOutputReference",
    "GoogleDataCatalogEntryConfig",
    "GoogleDataCatalogEntryGcsFilesetSpec",
    "GoogleDataCatalogEntryGcsFilesetSpecOutputReference",
    "GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs",
    "GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsList",
    "GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecsOutputReference",
    "GoogleDataCatalogEntryTimeouts",
    "GoogleDataCatalogEntryTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__789e6860d61d8fcc956bbd0633891f0f51324093d6b42200b64e37a82bc89026(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    entry_group: builtins.str,
    entry_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    gcs_fileset_spec: typing.Optional[typing.Union[GoogleDataCatalogEntryGcsFilesetSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    linked_resource: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataCatalogEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d4509acf846661ecb6e07beefc13b9e031ae034d078726d218e6403696f0f948(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef022638b96722c42a93b7b080adb558ee0cc27f13c2e02f27c698e2093472c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedf5e5672622dbf99bd3b1848931b6bba7d0c6770bae9535157ffa818b5e179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc1d3995a9213d666693c1a4d7d359bb6b906282784fc9b57cd7f5a3a046988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309c2761e4d8b9149d01ccf2eb5f7a6784be60675040bf526f40b33dc6f3cbd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee843418db8ef142e32117ad79c44b33b3f6181b25e7cb88577260353eb45b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b38868b27e190579f96723c257d62aac3f8b3758a42b56d851ea5b4e62113f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16bf8cbe000f8cf1e9e4452431bb79ddc35d2f31893d2c8eff048043e9d8d37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1425189ee4feff1e719d90d7c48cb3be0fab742e247688d23a02f66be6badb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91aec37b293e010a86e8201fd1ed2431ddb2db3ed7590485ae5f927e2e0f160f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edfa7c55e96b2a6177c6625410ce52912e22b2ee0e7c67c08eccea07cda34dd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0a277b13a5282e27cc82fa6c958e1c1f5614e683f500d577fb0f89f139e7d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c81721e6037f63649a0465b4b38860a9c36c1015fb1bcb91e26d186ec5c127(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22bea8f2342b9e5617a8ec321d2fe4782fd67b9aa78c022cf3d7f5f9101c03b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e534923345e2e25477687fe3826fedd9fed96166485903876fae65218f69cc2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a024439381d5ebf1bd436095fa89a79092de112ffd64f2776d46ed407aed53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0c731cd89b978f2b60e3b802c0b7dc1a7e13142b20905149cc002c3a4fda07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e2e1bcb8e20ee411d1bae46a7d0041e8ab2baa8ca0501203ad4efe38c35f58(
    value: typing.Optional[GoogleDataCatalogEntryBigqueryDateShardedSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92a00c0ee72644e31c18a684aa053e6b05f6fbeac329c2b7ed62b4e87ef082d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450eceda6d1c6b16ae3136be6bd2f8c0eee02ea0c1047fa9992932923678026f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb06be12a898d22ba7baa50d091dbacab7b3dd8edfbfdde7b0beab6dc7d4ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1b2715b708e005db9286e180d83badb97bff80569bcb9b9e8ad0db96f0b32e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a133d105ba6594cf99ab8764e92b1dc8555e2c392dbf491ae5f3151e70413a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c1913a2102f620a8955707a6b81a233b2da8542434029010bbeef08092f482(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e62e4adf1579d3e6697f7cdfb1df999b2c54b296870fb9425f16fbb1a2175f2(
    value: typing.Optional[GoogleDataCatalogEntryBigqueryTableSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2eb66c76567ff62c2584c7ef7fdd94c1d798a64971b274cba9e6e20a4b5bb65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a200d84cb5276bd2f7407c2dd99e69e052b0d46dac9d8a585b733d2133b6ab17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2821fda32ce76fc74eda680602eda50ae08a12db4f0f5a4fb56f8ede053a0c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94f5f9562b70390acb8b9ee6046e7b89d2bbc802c75b2c2a3adb108fc040a72(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c89d7b81f1a17e7d656f0ca7101df915360110c45528d6e2ab6e26e3783666(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb8875ac39c3c760a8dd7f2fbe679c40b8db7da8b1315da31916ddc4503e32b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21501c170034974d8276ec37f6995361fa6452e3a0321167ca1260c61f42c78c(
    value: typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecTableSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dafc2c86ac6042eda3891299438e4bdda2918015440c4e58447a5dbf0e0e53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd759ec853ffeff748d819753476561c7ccc691c618fef13ec399ec1174dcc4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ece27d733231d01127b6bad5491468ed114b3ead0a3f932f2998d60338408fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696663ea6fe964ff29d01e4e306680c95a44bc29a7b53e87c3d5d0c14b654add(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c9c5463a86edc2f5061ef505c4fe4276fe8ac5224cd4ad8b19fb16d01c75b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d011ab91b20de629885468a93a878d1e817f312dd9035dd7c73822529b8c9c35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82955c986dfeba695337ae45b6b8047986e2c090a120bba8c1de47f4d66ad243(
    value: typing.Optional[GoogleDataCatalogEntryBigqueryTableSpecViewSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec307687f9530e2d6839667f414b8380a100235957f4b2fe012f4c31a882256(
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
    gcs_fileset_spec: typing.Optional[typing.Union[GoogleDataCatalogEntryGcsFilesetSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    linked_resource: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataCatalogEntryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    user_specified_system: typing.Optional[builtins.str] = None,
    user_specified_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d06b0c7925dbc5eca056b48eb3726d036ef5327fb6d3d7d2609dd3521de10f(
    *,
    file_patterns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f22cad7b281eedd9b0f8a189e38d007a38b411c6ade2160ec893ac86a826da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83171cb8c068bbc377911970293a125da77186512af0ccc0a2fdae4a0ec66b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91863c3bfc17c7a7ad99004077409abfa4cf6aa3944c5348b62c50fe42ef32e4(
    value: typing.Optional[GoogleDataCatalogEntryGcsFilesetSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809bc4849eaa1d1ec6f2ab33ccaf8af1428dda26dc7380e1f7b40959040e2198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd1e697b2cf47a1b5f6ed0d372cfb41b3b4db96867c81e325bc9ba2417954af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc13eaac8d808dc39b0263e7fc784a7fd54df8ac3d6bf8ad83fee621384109cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35c4f8ae203ff1fc545b03932d94940ca5a06be229a6099c0680a27e33627c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6657fc3f93731fc2d8f0a143aaa3d1ce1909785035193c4a21c338a93bb6ed92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7bc206d8eae685334cbfc5370787a7e09abadc73f0f1cc50a30a6a0b3174bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6337a57d1f891fe9b85dfcb15fecc7d1bf224c5c678b536093fef6089f6f4965(
    value: typing.Optional[GoogleDataCatalogEntryGcsFilesetSpecSampleGcsFileSpecs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae4ffd97f6912ce43fda939d5ec9eeab1303f646687bf10c00442b36ab2fafa(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5b48eac08243cb264c3b650f1c6c8b2a4dfe9f4fea04e783210aa09fd0de07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0e4fbbb33b1d38463e063b5e196f3204f3c6c0de10a193193d57db56789544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cef196ae13accff3a122ffde2a5da31bc218a756a3e9ff3344cb92367c5b442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db99a49149358a59412417ffc94b037123144e02f3d9c8667b626dbbb3e47899(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0284aa0ff57ca441b3a0b524258006d9d3ec257b44cc1bb8fd0c0552e1e7f6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataCatalogEntryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
