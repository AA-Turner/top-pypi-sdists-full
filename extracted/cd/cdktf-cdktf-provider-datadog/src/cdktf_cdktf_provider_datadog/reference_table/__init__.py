r'''
# `datadog_reference_table`

Refer to the Terraform Registry for docs: [`datadog_reference_table`](https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table).
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


class ReferenceTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTable",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table datadog_reference_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source: builtins.str,
        table_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        file_metadata: typing.Optional[typing.Union["ReferenceTableFileMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        schema: typing.Optional[typing.Union["ReferenceTableSchema", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table datadog_reference_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param source: The source type for the reference table. Valid values are ``S3``, ``GCS``, ``AZURE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#source ReferenceTable#source}
        :param table_name: The name of the reference table. This must be unique within your organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#table_name ReferenceTable#table_name}
        :param description: The description of the reference table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#description ReferenceTable#description}
        :param file_metadata: file_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_metadata ReferenceTable#file_metadata}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#schema ReferenceTable#schema}
        :param tags: A list of tags to associate with the reference table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#tags ReferenceTable#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3fddb49813a88da3cdae85be2c1504ec735df762a43cb213ce5a79685b88ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ReferenceTableConfig(
            source=source,
            table_name=table_name,
            description=description,
            file_metadata=file_metadata,
            schema=schema,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ReferenceTable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ReferenceTable to import.
        :param import_from_id: The id of the existing ReferenceTable that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ReferenceTable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73e0008504923bc037ee7e6f077e83eead2542df9d811914420039afc991900)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFileMetadata")
    def put_file_metadata(
        self,
        *,
        sync_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_details: typing.Optional[typing.Union["ReferenceTableFileMetadataAccessDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sync_enabled: Whether this table should automatically sync with the cloud storage source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#sync_enabled ReferenceTable#sync_enabled}
        :param access_details: access_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#access_details ReferenceTable#access_details}
        '''
        value = ReferenceTableFileMetadata(
            sync_enabled=sync_enabled, access_details=access_details
        )

        return typing.cast(None, jsii.invoke(self, "putFileMetadata", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(
        self,
        *,
        fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReferenceTableSchemaFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        primary_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param fields: fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#fields ReferenceTable#fields}
        :param primary_keys: List of field names that serve as primary keys for the table. Currently only one primary key is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#primary_keys ReferenceTable#primary_keys}
        '''
        value = ReferenceTableSchema(fields=fields, primary_keys=primary_keys)

        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFileMetadata")
    def reset_file_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileMetadata", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="fileMetadata")
    def file_metadata(self) -> "ReferenceTableFileMetadataOutputReference":
        return typing.cast("ReferenceTableFileMetadataOutputReference", jsii.get(self, "fileMetadata"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedBy")
    def last_updated_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedBy"))

    @builtins.property
    @jsii.member(jsii_name="rowCount")
    def row_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowCount"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> "ReferenceTableSchemaOutputReference":
        return typing.cast("ReferenceTableSchemaOutputReference", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fileMetadataInput")
    def file_metadata_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReferenceTableFileMetadata"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReferenceTableFileMetadata"]], jsii.get(self, "fileMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReferenceTableSchema"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReferenceTableSchema"]], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c5badee9ba6134aaaa64de77d46261bcd6b8c2079858c4f813c41c26043d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc86cf83a419efea2e263bf040bc1fff8283dfc2485f694633eb9e6a25c155c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7e5a6ae598b5c4edbda1c050183e12c09e0fbce3dcec97e28f3e037d867322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1105af78a1f530b3032c4438e36f605e5a3e5bccc83637bcd4f8f2d1527747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "source": "source",
        "table_name": "tableName",
        "description": "description",
        "file_metadata": "fileMetadata",
        "schema": "schema",
        "tags": "tags",
    },
)
class ReferenceTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        source: builtins.str,
        table_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        file_metadata: typing.Optional[typing.Union["ReferenceTableFileMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        schema: typing.Optional[typing.Union["ReferenceTableSchema", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param source: The source type for the reference table. Valid values are ``S3``, ``GCS``, ``AZURE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#source ReferenceTable#source}
        :param table_name: The name of the reference table. This must be unique within your organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#table_name ReferenceTable#table_name}
        :param description: The description of the reference table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#description ReferenceTable#description}
        :param file_metadata: file_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_metadata ReferenceTable#file_metadata}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#schema ReferenceTable#schema}
        :param tags: A list of tags to associate with the reference table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#tags ReferenceTable#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(file_metadata, dict):
            file_metadata = ReferenceTableFileMetadata(**file_metadata)
        if isinstance(schema, dict):
            schema = ReferenceTableSchema(**schema)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdecf4216c1785b5bed1a8f6e0ab591271c31ffcbcbecdca89946518dc22fdc3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument file_metadata", value=file_metadata, expected_type=type_hints["file_metadata"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "table_name": table_name,
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
        if file_metadata is not None:
            self._values["file_metadata"] = file_metadata
        if schema is not None:
            self._values["schema"] = schema
        if tags is not None:
            self._values["tags"] = tags

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
    def source(self) -> builtins.str:
        '''The source type for the reference table. Valid values are ``S3``, ``GCS``, ``AZURE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#source ReferenceTable#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''The name of the reference table. This must be unique within your organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#table_name ReferenceTable#table_name}
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the reference table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#description ReferenceTable#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_metadata(self) -> typing.Optional["ReferenceTableFileMetadata"]:
        '''file_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_metadata ReferenceTable#file_metadata}
        '''
        result = self._values.get("file_metadata")
        return typing.cast(typing.Optional["ReferenceTableFileMetadata"], result)

    @builtins.property
    def schema(self) -> typing.Optional["ReferenceTableSchema"]:
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#schema ReferenceTable#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional["ReferenceTableSchema"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tags to associate with the reference table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#tags ReferenceTable#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadata",
    jsii_struct_bases=[],
    name_mapping={"sync_enabled": "syncEnabled", "access_details": "accessDetails"},
)
class ReferenceTableFileMetadata:
    def __init__(
        self,
        *,
        sync_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_details: typing.Optional[typing.Union["ReferenceTableFileMetadataAccessDetails", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sync_enabled: Whether this table should automatically sync with the cloud storage source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#sync_enabled ReferenceTable#sync_enabled}
        :param access_details: access_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#access_details ReferenceTable#access_details}
        '''
        if isinstance(access_details, dict):
            access_details = ReferenceTableFileMetadataAccessDetails(**access_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95e41681968b240f954f6c77f5a64689d72f308e2f3c16b9b3818ba24bce146)
            check_type(argname="argument sync_enabled", value=sync_enabled, expected_type=type_hints["sync_enabled"])
            check_type(argname="argument access_details", value=access_details, expected_type=type_hints["access_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sync_enabled": sync_enabled,
        }
        if access_details is not None:
            self._values["access_details"] = access_details

    @builtins.property
    def sync_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether this table should automatically sync with the cloud storage source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#sync_enabled ReferenceTable#sync_enabled}
        '''
        result = self._values.get("sync_enabled")
        assert result is not None, "Required property 'sync_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def access_details(
        self,
    ) -> typing.Optional["ReferenceTableFileMetadataAccessDetails"]:
        '''access_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#access_details ReferenceTable#access_details}
        '''
        result = self._values.get("access_details")
        return typing.cast(typing.Optional["ReferenceTableFileMetadataAccessDetails"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableFileMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetails",
    jsii_struct_bases=[],
    name_mapping={
        "aws_detail": "awsDetail",
        "azure_detail": "azureDetail",
        "gcp_detail": "gcpDetail",
    },
)
class ReferenceTableFileMetadataAccessDetails:
    def __init__(
        self,
        *,
        aws_detail: typing.Optional[typing.Union["ReferenceTableFileMetadataAccessDetailsAwsDetail", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_detail: typing.Optional[typing.Union["ReferenceTableFileMetadataAccessDetailsAzureDetail", typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_detail: typing.Optional[typing.Union["ReferenceTableFileMetadataAccessDetailsGcpDetail", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_detail: aws_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_detail ReferenceTable#aws_detail}
        :param azure_detail: azure_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_detail ReferenceTable#azure_detail}
        :param gcp_detail: gcp_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_detail ReferenceTable#gcp_detail}
        '''
        if isinstance(aws_detail, dict):
            aws_detail = ReferenceTableFileMetadataAccessDetailsAwsDetail(**aws_detail)
        if isinstance(azure_detail, dict):
            azure_detail = ReferenceTableFileMetadataAccessDetailsAzureDetail(**azure_detail)
        if isinstance(gcp_detail, dict):
            gcp_detail = ReferenceTableFileMetadataAccessDetailsGcpDetail(**gcp_detail)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f91d706feda8e153fc2f6daf497b46a3d461e7d5b21103799e61f0b89d26b36)
            check_type(argname="argument aws_detail", value=aws_detail, expected_type=type_hints["aws_detail"])
            check_type(argname="argument azure_detail", value=azure_detail, expected_type=type_hints["azure_detail"])
            check_type(argname="argument gcp_detail", value=gcp_detail, expected_type=type_hints["gcp_detail"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_detail is not None:
            self._values["aws_detail"] = aws_detail
        if azure_detail is not None:
            self._values["azure_detail"] = azure_detail
        if gcp_detail is not None:
            self._values["gcp_detail"] = gcp_detail

    @builtins.property
    def aws_detail(
        self,
    ) -> typing.Optional["ReferenceTableFileMetadataAccessDetailsAwsDetail"]:
        '''aws_detail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_detail ReferenceTable#aws_detail}
        '''
        result = self._values.get("aws_detail")
        return typing.cast(typing.Optional["ReferenceTableFileMetadataAccessDetailsAwsDetail"], result)

    @builtins.property
    def azure_detail(
        self,
    ) -> typing.Optional["ReferenceTableFileMetadataAccessDetailsAzureDetail"]:
        '''azure_detail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_detail ReferenceTable#azure_detail}
        '''
        result = self._values.get("azure_detail")
        return typing.cast(typing.Optional["ReferenceTableFileMetadataAccessDetailsAzureDetail"], result)

    @builtins.property
    def gcp_detail(
        self,
    ) -> typing.Optional["ReferenceTableFileMetadataAccessDetailsGcpDetail"]:
        '''gcp_detail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_detail ReferenceTable#gcp_detail}
        '''
        result = self._values.get("gcp_detail")
        return typing.cast(typing.Optional["ReferenceTableFileMetadataAccessDetailsGcpDetail"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableFileMetadataAccessDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetailsAwsDetail",
    jsii_struct_bases=[],
    name_mapping={
        "aws_account_id": "awsAccountId",
        "aws_bucket_name": "awsBucketName",
        "file_path": "filePath",
    },
)
class ReferenceTableFileMetadataAccessDetailsAwsDetail:
    def __init__(
        self,
        *,
        aws_account_id: typing.Optional[builtins.str] = None,
        aws_bucket_name: typing.Optional[builtins.str] = None,
        file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_account_id: The ID of the AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_account_id ReferenceTable#aws_account_id}
        :param aws_bucket_name: The name of the AWS S3 bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_bucket_name ReferenceTable#aws_bucket_name}
        :param file_path: The relative file path from the AWS S3 bucket root to the CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068f9ba7a55acf622e2e4984a0c782e76f44716e403db04566befac61edd5885)
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_bucket_name", value=aws_bucket_name, expected_type=type_hints["aws_bucket_name"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if aws_bucket_name is not None:
            self._values["aws_bucket_name"] = aws_bucket_name
        if file_path is not None:
            self._values["file_path"] = file_path

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_account_id ReferenceTable#aws_account_id}
        '''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AWS S3 bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_bucket_name ReferenceTable#aws_bucket_name}
        '''
        result = self._values.get("aws_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''The relative file path from the AWS S3 bucket root to the CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        '''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableFileMetadataAccessDetailsAwsDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReferenceTableFileMetadataAccessDetailsAwsDetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetailsAwsDetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be273cf7bdea0c6cadb3a59061d9aeecec54b12411d91164439860dfdf181a77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetAwsBucketName")
    def reset_aws_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsBucketName", []))

    @jsii.member(jsii_name="resetFilePath")
    def reset_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePath", []))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="awsBucketNameInput")
    def aws_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="filePathInput")
    def file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePathInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b1f1c1192571c045c3ec043536d264ad976509c480edcc31150257b4c0be56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsBucketName")
    def aws_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsBucketName"))

    @aws_bucket_name.setter
    def aws_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcda1b7b7ed172332890a5ede31aed393e2f042ca91f58a466d776de3b26675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @file_path.setter
    def file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__badf0f9289bd89e8bae254341ffaa38562f9352982978d0311d42fafa9dcaad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAwsDetail]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAwsDetail]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAwsDetail]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a8a6938bbade380458c3d851d667756d11396fbb839d07193794294bc539b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetailsAzureDetail",
    jsii_struct_bases=[],
    name_mapping={
        "azure_client_id": "azureClientId",
        "azure_container_name": "azureContainerName",
        "azure_storage_account_name": "azureStorageAccountName",
        "azure_tenant_id": "azureTenantId",
        "file_path": "filePath",
    },
)
class ReferenceTableFileMetadataAccessDetailsAzureDetail:
    def __init__(
        self,
        *,
        azure_client_id: typing.Optional[builtins.str] = None,
        azure_container_name: typing.Optional[builtins.str] = None,
        azure_storage_account_name: typing.Optional[builtins.str] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param azure_client_id: The Azure client ID (application ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_client_id ReferenceTable#azure_client_id}
        :param azure_container_name: The name of the Azure container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_container_name ReferenceTable#azure_container_name}
        :param azure_storage_account_name: The name of the Azure storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_storage_account_name ReferenceTable#azure_storage_account_name}
        :param azure_tenant_id: The ID of the Azure tenant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_tenant_id ReferenceTable#azure_tenant_id}
        :param file_path: The relative file path from the Azure container root to the CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06fcb0f96f1ce4076b50a02828a1fd9cb912b3930d57c5a1273b1869f06c149f)
            check_type(argname="argument azure_client_id", value=azure_client_id, expected_type=type_hints["azure_client_id"])
            check_type(argname="argument azure_container_name", value=azure_container_name, expected_type=type_hints["azure_container_name"])
            check_type(argname="argument azure_storage_account_name", value=azure_storage_account_name, expected_type=type_hints["azure_storage_account_name"])
            check_type(argname="argument azure_tenant_id", value=azure_tenant_id, expected_type=type_hints["azure_tenant_id"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if azure_client_id is not None:
            self._values["azure_client_id"] = azure_client_id
        if azure_container_name is not None:
            self._values["azure_container_name"] = azure_container_name
        if azure_storage_account_name is not None:
            self._values["azure_storage_account_name"] = azure_storage_account_name
        if azure_tenant_id is not None:
            self._values["azure_tenant_id"] = azure_tenant_id
        if file_path is not None:
            self._values["file_path"] = file_path

    @builtins.property
    def azure_client_id(self) -> typing.Optional[builtins.str]:
        '''The Azure client ID (application ID).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_client_id ReferenceTable#azure_client_id}
        '''
        result = self._values.get("azure_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_container_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Azure container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_container_name ReferenceTable#azure_container_name}
        '''
        result = self._values.get("azure_container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_storage_account_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Azure storage account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_storage_account_name ReferenceTable#azure_storage_account_name}
        '''
        result = self._values.get("azure_storage_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_tenant_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Azure tenant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_tenant_id ReferenceTable#azure_tenant_id}
        '''
        result = self._values.get("azure_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''The relative file path from the Azure container root to the CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        '''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableFileMetadataAccessDetailsAzureDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReferenceTableFileMetadataAccessDetailsAzureDetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetailsAzureDetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab03f799baa2ae392fe1df1110d97efa4924ea906d903964ec6ac7e53d53cf1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAzureClientId")
    def reset_azure_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureClientId", []))

    @jsii.member(jsii_name="resetAzureContainerName")
    def reset_azure_container_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureContainerName", []))

    @jsii.member(jsii_name="resetAzureStorageAccountName")
    def reset_azure_storage_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureStorageAccountName", []))

    @jsii.member(jsii_name="resetAzureTenantId")
    def reset_azure_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureTenantId", []))

    @jsii.member(jsii_name="resetFilePath")
    def reset_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePath", []))

    @builtins.property
    @jsii.member(jsii_name="azureClientIdInput")
    def azure_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="azureContainerNameInput")
    def azure_container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureContainerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="azureStorageAccountNameInput")
    def azure_storage_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureStorageAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="azureTenantIdInput")
    def azure_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="filePathInput")
    def file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePathInput"))

    @builtins.property
    @jsii.member(jsii_name="azureClientId")
    def azure_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureClientId"))

    @azure_client_id.setter
    def azure_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61cb9e874bbff0e1d3ea43234e308468ab78ea2f48354f830b4be10589bd5e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureContainerName")
    def azure_container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureContainerName"))

    @azure_container_name.setter
    def azure_container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c16eda69289d879d619c94631fe2a31a644aaea24bffe402194ec184e0d2159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureContainerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureStorageAccountName")
    def azure_storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureStorageAccountName"))

    @azure_storage_account_name.setter
    def azure_storage_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d771ec001fc4ccae3f315b24b6ca4443fcd6edc5ad8de5ba4fa5474a3291fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureStorageAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureTenantId")
    def azure_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureTenantId"))

    @azure_tenant_id.setter
    def azure_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b31d85c738b3786f8d8e96cb934a90928f638cd8c5812b49ffa2dfc61ca6477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @file_path.setter
    def file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35cd2fde4d237871ad09c4eb082b9fb2f4211a453f4ec5cbf663055c836de37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAzureDetail]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAzureDetail]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAzureDetail]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae86225ba0ea945f5ff9e2d67389e30acc88bbb002385298ead7cbc0200f3e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetailsGcpDetail",
    jsii_struct_bases=[],
    name_mapping={
        "file_path": "filePath",
        "gcp_bucket_name": "gcpBucketName",
        "gcp_project_id": "gcpProjectId",
        "gcp_service_account_email": "gcpServiceAccountEmail",
    },
)
class ReferenceTableFileMetadataAccessDetailsGcpDetail:
    def __init__(
        self,
        *,
        file_path: typing.Optional[builtins.str] = None,
        gcp_bucket_name: typing.Optional[builtins.str] = None,
        gcp_project_id: typing.Optional[builtins.str] = None,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_path: The relative file path from the GCS bucket root to the CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        :param gcp_bucket_name: The name of the GCP bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_bucket_name ReferenceTable#gcp_bucket_name}
        :param gcp_project_id: The ID of the GCP project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_project_id ReferenceTable#gcp_project_id}
        :param gcp_service_account_email: The email of the GCP service account used to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_service_account_email ReferenceTable#gcp_service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5b4f53e6ab0444d72e253e9ad5559f2c9a73ce70eb29d540d33ffd5250ea02)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
            check_type(argname="argument gcp_bucket_name", value=gcp_bucket_name, expected_type=type_hints["gcp_bucket_name"])
            check_type(argname="argument gcp_project_id", value=gcp_project_id, expected_type=type_hints["gcp_project_id"])
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_path is not None:
            self._values["file_path"] = file_path
        if gcp_bucket_name is not None:
            self._values["gcp_bucket_name"] = gcp_bucket_name
        if gcp_project_id is not None:
            self._values["gcp_project_id"] = gcp_project_id
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''The relative file path from the GCS bucket root to the CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        '''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the GCP bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_bucket_name ReferenceTable#gcp_bucket_name}
        '''
        result = self._values.get("gcp_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the GCP project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_project_id ReferenceTable#gcp_project_id}
        '''
        result = self._values.get("gcp_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The email of the GCP service account used to access the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_service_account_email ReferenceTable#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableFileMetadataAccessDetailsGcpDetail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReferenceTableFileMetadataAccessDetailsGcpDetailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetailsGcpDetailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd4e5f967545c5fb84d0da000f17ed060ad9153bbb7679ab711ac4d5de4d0ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilePath")
    def reset_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePath", []))

    @jsii.member(jsii_name="resetGcpBucketName")
    def reset_gcp_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpBucketName", []))

    @jsii.member(jsii_name="resetGcpProjectId")
    def reset_gcp_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpProjectId", []))

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @builtins.property
    @jsii.member(jsii_name="filePathInput")
    def file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePathInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpBucketNameInput")
    def gcp_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpProjectIdInput")
    def gcp_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmailInput")
    def gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @file_path.setter
    def file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603998a7cc8bd1b141061961492dab8a018bc85c069fe60d43671205029faa25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpBucketName")
    def gcp_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpBucketName"))

    @gcp_bucket_name.setter
    def gcp_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426dc3310480d99a9eba6fe3795ade817815cdf6f9c4019c9f6370205f20ff3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpProjectId")
    def gcp_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpProjectId"))

    @gcp_project_id.setter
    def gcp_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794a0ba04bd647d8a88ea55e391a64d968282417e8fd41fe6b2c3f48c720feca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48711a8cd4959de45af2abcc8ea5be539f286ff086a71612078a1e2533e87af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsGcpDetail]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsGcpDetail]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsGcpDetail]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1156f4ad96439a6ffa5e5668bcd613ce8edd77fc6fb1f1b617ee234b3f893f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReferenceTableFileMetadataAccessDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataAccessDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bc5557f88383f9fb9fb18f24115348ee4e716b9823eabb49dc48c15cc340c53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsDetail")
    def put_aws_detail(
        self,
        *,
        aws_account_id: typing.Optional[builtins.str] = None,
        aws_bucket_name: typing.Optional[builtins.str] = None,
        file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_account_id: The ID of the AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_account_id ReferenceTable#aws_account_id}
        :param aws_bucket_name: The name of the AWS S3 bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_bucket_name ReferenceTable#aws_bucket_name}
        :param file_path: The relative file path from the AWS S3 bucket root to the CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        '''
        value = ReferenceTableFileMetadataAccessDetailsAwsDetail(
            aws_account_id=aws_account_id,
            aws_bucket_name=aws_bucket_name,
            file_path=file_path,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsDetail", [value]))

    @jsii.member(jsii_name="putAzureDetail")
    def put_azure_detail(
        self,
        *,
        azure_client_id: typing.Optional[builtins.str] = None,
        azure_container_name: typing.Optional[builtins.str] = None,
        azure_storage_account_name: typing.Optional[builtins.str] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param azure_client_id: The Azure client ID (application ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_client_id ReferenceTable#azure_client_id}
        :param azure_container_name: The name of the Azure container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_container_name ReferenceTable#azure_container_name}
        :param azure_storage_account_name: The name of the Azure storage account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_storage_account_name ReferenceTable#azure_storage_account_name}
        :param azure_tenant_id: The ID of the Azure tenant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_tenant_id ReferenceTable#azure_tenant_id}
        :param file_path: The relative file path from the Azure container root to the CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        '''
        value = ReferenceTableFileMetadataAccessDetailsAzureDetail(
            azure_client_id=azure_client_id,
            azure_container_name=azure_container_name,
            azure_storage_account_name=azure_storage_account_name,
            azure_tenant_id=azure_tenant_id,
            file_path=file_path,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureDetail", [value]))

    @jsii.member(jsii_name="putGcpDetail")
    def put_gcp_detail(
        self,
        *,
        file_path: typing.Optional[builtins.str] = None,
        gcp_bucket_name: typing.Optional[builtins.str] = None,
        gcp_project_id: typing.Optional[builtins.str] = None,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_path: The relative file path from the GCS bucket root to the CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#file_path ReferenceTable#file_path}
        :param gcp_bucket_name: The name of the GCP bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_bucket_name ReferenceTable#gcp_bucket_name}
        :param gcp_project_id: The ID of the GCP project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_project_id ReferenceTable#gcp_project_id}
        :param gcp_service_account_email: The email of the GCP service account used to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_service_account_email ReferenceTable#gcp_service_account_email}
        '''
        value = ReferenceTableFileMetadataAccessDetailsGcpDetail(
            file_path=file_path,
            gcp_bucket_name=gcp_bucket_name,
            gcp_project_id=gcp_project_id,
            gcp_service_account_email=gcp_service_account_email,
        )

        return typing.cast(None, jsii.invoke(self, "putGcpDetail", [value]))

    @jsii.member(jsii_name="resetAwsDetail")
    def reset_aws_detail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsDetail", []))

    @jsii.member(jsii_name="resetAzureDetail")
    def reset_azure_detail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureDetail", []))

    @jsii.member(jsii_name="resetGcpDetail")
    def reset_gcp_detail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpDetail", []))

    @builtins.property
    @jsii.member(jsii_name="awsDetail")
    def aws_detail(
        self,
    ) -> ReferenceTableFileMetadataAccessDetailsAwsDetailOutputReference:
        return typing.cast(ReferenceTableFileMetadataAccessDetailsAwsDetailOutputReference, jsii.get(self, "awsDetail"))

    @builtins.property
    @jsii.member(jsii_name="azureDetail")
    def azure_detail(
        self,
    ) -> ReferenceTableFileMetadataAccessDetailsAzureDetailOutputReference:
        return typing.cast(ReferenceTableFileMetadataAccessDetailsAzureDetailOutputReference, jsii.get(self, "azureDetail"))

    @builtins.property
    @jsii.member(jsii_name="gcpDetail")
    def gcp_detail(
        self,
    ) -> ReferenceTableFileMetadataAccessDetailsGcpDetailOutputReference:
        return typing.cast(ReferenceTableFileMetadataAccessDetailsGcpDetailOutputReference, jsii.get(self, "gcpDetail"))

    @builtins.property
    @jsii.member(jsii_name="awsDetailInput")
    def aws_detail_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAwsDetail]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAwsDetail]], jsii.get(self, "awsDetailInput"))

    @builtins.property
    @jsii.member(jsii_name="azureDetailInput")
    def azure_detail_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAzureDetail]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAzureDetail]], jsii.get(self, "azureDetailInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpDetailInput")
    def gcp_detail_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsGcpDetail]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsGcpDetail]], jsii.get(self, "gcpDetailInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetails]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetails]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetails]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fac1e7ed8a366f871c6637cf8178408cccfb40e3d457aa267b7290eb2001f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReferenceTableFileMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableFileMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48abee503450cd578aacf45caa262e78917a3fc5e37e81bdff244fa0c83740da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessDetails")
    def put_access_details(
        self,
        *,
        aws_detail: typing.Optional[typing.Union[ReferenceTableFileMetadataAccessDetailsAwsDetail, typing.Dict[builtins.str, typing.Any]]] = None,
        azure_detail: typing.Optional[typing.Union[ReferenceTableFileMetadataAccessDetailsAzureDetail, typing.Dict[builtins.str, typing.Any]]] = None,
        gcp_detail: typing.Optional[typing.Union[ReferenceTableFileMetadataAccessDetailsGcpDetail, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_detail: aws_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#aws_detail ReferenceTable#aws_detail}
        :param azure_detail: azure_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#azure_detail ReferenceTable#azure_detail}
        :param gcp_detail: gcp_detail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#gcp_detail ReferenceTable#gcp_detail}
        '''
        value = ReferenceTableFileMetadataAccessDetails(
            aws_detail=aws_detail, azure_detail=azure_detail, gcp_detail=gcp_detail
        )

        return typing.cast(None, jsii.invoke(self, "putAccessDetails", [value]))

    @jsii.member(jsii_name="resetAccessDetails")
    def reset_access_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessDetails", []))

    @builtins.property
    @jsii.member(jsii_name="accessDetails")
    def access_details(self) -> ReferenceTableFileMetadataAccessDetailsOutputReference:
        return typing.cast(ReferenceTableFileMetadataAccessDetailsOutputReference, jsii.get(self, "accessDetails"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="errorRowCount")
    def error_row_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "errorRowCount"))

    @builtins.property
    @jsii.member(jsii_name="errorType")
    def error_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorType"))

    @builtins.property
    @jsii.member(jsii_name="accessDetailsInput")
    def access_details_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetails]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetails]], jsii.get(self, "accessDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="syncEnabledInput")
    def sync_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="syncEnabled")
    def sync_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncEnabled"))

    @sync_enabled.setter
    def sync_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa1806933a903490e8187b59225bc31bdc47f1ad0645e090afa9a3975b8ecdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadata]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadata]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadata]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446bc66f58a4472226878c98269a16b8849b4d7f7f918f991b06b0c252fa9755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableSchema",
    jsii_struct_bases=[],
    name_mapping={"fields": "fields", "primary_keys": "primaryKeys"},
)
class ReferenceTableSchema:
    def __init__(
        self,
        *,
        fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReferenceTableSchemaFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        primary_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param fields: fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#fields ReferenceTable#fields}
        :param primary_keys: List of field names that serve as primary keys for the table. Currently only one primary key is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#primary_keys ReferenceTable#primary_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747171eccef8e333093099105a663d2cdc798bd667a4128777dc5c26515eea4a)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument primary_keys", value=primary_keys, expected_type=type_hints["primary_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fields is not None:
            self._values["fields"] = fields
        if primary_keys is not None:
            self._values["primary_keys"] = primary_keys

    @builtins.property
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReferenceTableSchemaFields"]]]:
        '''fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#fields ReferenceTable#fields}
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReferenceTableSchemaFields"]]], result)

    @builtins.property
    def primary_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of field names that serve as primary keys for the table. Currently only one primary key is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#primary_keys ReferenceTable#primary_keys}
        '''
        result = self._values.get("primary_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableSchemaFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class ReferenceTableSchemaFields:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#name ReferenceTable#name}
        :param type: The data type of the field. Must be one of: STRING, INT32. Valid values are ``STRING``, ``INT32``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#type ReferenceTable#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1158e3ee55bf2317d860022e952f0d09f8f653ff76984d79ceb46abcefe1e965)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#name ReferenceTable#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The data type of the field. Must be one of: STRING, INT32. Valid values are ``STRING``, ``INT32``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/reference_table#type ReferenceTable#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReferenceTableSchemaFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReferenceTableSchemaFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableSchemaFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0121cc1009749b91a6dca53b173d1df33d52b43dcba33b66033179a225dec805)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ReferenceTableSchemaFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca9a49dcdb6f36b452a6d8911da2fc29b53988194a50d41732f3654691a05c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ReferenceTableSchemaFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a544f62bf430a128395a309c3fd3dacb0e2e430226d7545d4beba08d547beb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3edf400ce8901b07b10c1bcd3e893125a33b673ca1ea8ee3c3f8c9f3bd8c14a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a81b14215e70fbb5d3cf8887ad937bca0665e176283bda864cfc9b20a4c932eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReferenceTableSchemaFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReferenceTableSchemaFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReferenceTableSchemaFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410d153d62fda2d093bf3ea48bf077e0d753c7f15011f09f0689406d870cdb6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReferenceTableSchemaFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableSchemaFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5f7d136b3c4ab02af73f4e1606303748fe0ba246d3d86ab25362f8e3c74ef54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dce8b71ad633149f3c6a8e0eb5593f14893b14f337cdbf9ab76996237360cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ffd698a57af02df6dbab36272808a4f24f4a3964d92cd88db28ae1399c0331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchemaFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchemaFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchemaFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850e91ceb43f6acfd1cd59b428dd5f521d486116c545b08c2f4941a740be2c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReferenceTableSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.referenceTable.ReferenceTableSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a72871c4888a8b9b486858ec4fed19ad40725e945f29f5bee42ab2a31ccdcb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFields")
    def put_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReferenceTableSchemaFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61658105a844c1185de4862e817cbc4684eaccd149b42132d125b6f76bc5a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFields", [value]))

    @jsii.member(jsii_name="resetFields")
    def reset_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFields", []))

    @jsii.member(jsii_name="resetPrimaryKeys")
    def reset_primary_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKeys", []))

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> ReferenceTableSchemaFieldsList:
        return typing.cast(ReferenceTableSchemaFieldsList, jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="fieldsInput")
    def fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReferenceTableSchemaFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReferenceTableSchemaFields]]], jsii.get(self, "fieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeysInput")
    def primary_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "primaryKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeys")
    def primary_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "primaryKeys"))

    @primary_keys.setter
    def primary_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99702ad0088a79c0a244b78422035ebd2acdc64f0e9eff4102748d6ff8707a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchema]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchema]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchema]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc8d3ff04480c17c79e8c8097c6b75afe9c764bcfe60be52ce8cf5be0fb9d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ReferenceTable",
    "ReferenceTableConfig",
    "ReferenceTableFileMetadata",
    "ReferenceTableFileMetadataAccessDetails",
    "ReferenceTableFileMetadataAccessDetailsAwsDetail",
    "ReferenceTableFileMetadataAccessDetailsAwsDetailOutputReference",
    "ReferenceTableFileMetadataAccessDetailsAzureDetail",
    "ReferenceTableFileMetadataAccessDetailsAzureDetailOutputReference",
    "ReferenceTableFileMetadataAccessDetailsGcpDetail",
    "ReferenceTableFileMetadataAccessDetailsGcpDetailOutputReference",
    "ReferenceTableFileMetadataAccessDetailsOutputReference",
    "ReferenceTableFileMetadataOutputReference",
    "ReferenceTableSchema",
    "ReferenceTableSchemaFields",
    "ReferenceTableSchemaFieldsList",
    "ReferenceTableSchemaFieldsOutputReference",
    "ReferenceTableSchemaOutputReference",
]

publication.publish()

def _typecheckingstub__0b3fddb49813a88da3cdae85be2c1504ec735df762a43cb213ce5a79685b88ac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source: builtins.str,
    table_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    file_metadata: typing.Optional[typing.Union[ReferenceTableFileMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    schema: typing.Optional[typing.Union[ReferenceTableSchema, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__d73e0008504923bc037ee7e6f077e83eead2542df9d811914420039afc991900(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c5badee9ba6134aaaa64de77d46261bcd6b8c2079858c4f813c41c26043d8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc86cf83a419efea2e263bf040bc1fff8283dfc2485f694633eb9e6a25c155c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7e5a6ae598b5c4edbda1c050183e12c09e0fbce3dcec97e28f3e037d867322(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1105af78a1f530b3032c4438e36f605e5a3e5bccc83637bcd4f8f2d1527747(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdecf4216c1785b5bed1a8f6e0ab591271c31ffcbcbecdca89946518dc22fdc3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source: builtins.str,
    table_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    file_metadata: typing.Optional[typing.Union[ReferenceTableFileMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    schema: typing.Optional[typing.Union[ReferenceTableSchema, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95e41681968b240f954f6c77f5a64689d72f308e2f3c16b9b3818ba24bce146(
    *,
    sync_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    access_details: typing.Optional[typing.Union[ReferenceTableFileMetadataAccessDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f91d706feda8e153fc2f6daf497b46a3d461e7d5b21103799e61f0b89d26b36(
    *,
    aws_detail: typing.Optional[typing.Union[ReferenceTableFileMetadataAccessDetailsAwsDetail, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_detail: typing.Optional[typing.Union[ReferenceTableFileMetadataAccessDetailsAzureDetail, typing.Dict[builtins.str, typing.Any]]] = None,
    gcp_detail: typing.Optional[typing.Union[ReferenceTableFileMetadataAccessDetailsGcpDetail, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068f9ba7a55acf622e2e4984a0c782e76f44716e403db04566befac61edd5885(
    *,
    aws_account_id: typing.Optional[builtins.str] = None,
    aws_bucket_name: typing.Optional[builtins.str] = None,
    file_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be273cf7bdea0c6cadb3a59061d9aeecec54b12411d91164439860dfdf181a77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b1f1c1192571c045c3ec043536d264ad976509c480edcc31150257b4c0be56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcda1b7b7ed172332890a5ede31aed393e2f042ca91f58a466d776de3b26675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__badf0f9289bd89e8bae254341ffaa38562f9352982978d0311d42fafa9dcaad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a8a6938bbade380458c3d851d667756d11396fbb839d07193794294bc539b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAwsDetail]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fcb0f96f1ce4076b50a02828a1fd9cb912b3930d57c5a1273b1869f06c149f(
    *,
    azure_client_id: typing.Optional[builtins.str] = None,
    azure_container_name: typing.Optional[builtins.str] = None,
    azure_storage_account_name: typing.Optional[builtins.str] = None,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    file_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab03f799baa2ae392fe1df1110d97efa4924ea906d903964ec6ac7e53d53cf1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cb9e874bbff0e1d3ea43234e308468ab78ea2f48354f830b4be10589bd5e6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c16eda69289d879d619c94631fe2a31a644aaea24bffe402194ec184e0d2159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d771ec001fc4ccae3f315b24b6ca4443fcd6edc5ad8de5ba4fa5474a3291fe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b31d85c738b3786f8d8e96cb934a90928f638cd8c5812b49ffa2dfc61ca6477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35cd2fde4d237871ad09c4eb082b9fb2f4211a453f4ec5cbf663055c836de37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae86225ba0ea945f5ff9e2d67389e30acc88bbb002385298ead7cbc0200f3e82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsAzureDetail]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5b4f53e6ab0444d72e253e9ad5559f2c9a73ce70eb29d540d33ffd5250ea02(
    *,
    file_path: typing.Optional[builtins.str] = None,
    gcp_bucket_name: typing.Optional[builtins.str] = None,
    gcp_project_id: typing.Optional[builtins.str] = None,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd4e5f967545c5fb84d0da000f17ed060ad9153bbb7679ab711ac4d5de4d0ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603998a7cc8bd1b141061961492dab8a018bc85c069fe60d43671205029faa25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426dc3310480d99a9eba6fe3795ade817815cdf6f9c4019c9f6370205f20ff3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794a0ba04bd647d8a88ea55e391a64d968282417e8fd41fe6b2c3f48c720feca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48711a8cd4959de45af2abcc8ea5be539f286ff086a71612078a1e2533e87af1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1156f4ad96439a6ffa5e5668bcd613ce8edd77fc6fb1f1b617ee234b3f893f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetailsGcpDetail]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc5557f88383f9fb9fb18f24115348ee4e716b9823eabb49dc48c15cc340c53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fac1e7ed8a366f871c6637cf8178408cccfb40e3d457aa267b7290eb2001f94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadataAccessDetails]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48abee503450cd578aacf45caa262e78917a3fc5e37e81bdff244fa0c83740da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa1806933a903490e8187b59225bc31bdc47f1ad0645e090afa9a3975b8ecdd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446bc66f58a4472226878c98269a16b8849b4d7f7f918f991b06b0c252fa9755(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableFileMetadata]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747171eccef8e333093099105a663d2cdc798bd667a4128777dc5c26515eea4a(
    *,
    fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReferenceTableSchemaFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    primary_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1158e3ee55bf2317d860022e952f0d09f8f653ff76984d79ceb46abcefe1e965(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0121cc1009749b91a6dca53b173d1df33d52b43dcba33b66033179a225dec805(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca9a49dcdb6f36b452a6d8911da2fc29b53988194a50d41732f3654691a05c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a544f62bf430a128395a309c3fd3dacb0e2e430226d7545d4beba08d547beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3edf400ce8901b07b10c1bcd3e893125a33b673ca1ea8ee3c3f8c9f3bd8c14a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81b14215e70fbb5d3cf8887ad937bca0665e176283bda864cfc9b20a4c932eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410d153d62fda2d093bf3ea48bf077e0d753c7f15011f09f0689406d870cdb6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReferenceTableSchemaFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f7d136b3c4ab02af73f4e1606303748fe0ba246d3d86ab25362f8e3c74ef54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dce8b71ad633149f3c6a8e0eb5593f14893b14f337cdbf9ab76996237360cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ffd698a57af02df6dbab36272808a4f24f4a3964d92cd88db28ae1399c0331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850e91ceb43f6acfd1cd59b428dd5f521d486116c545b08c2f4941a740be2c6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchemaFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a72871c4888a8b9b486858ec4fed19ad40725e945f29f5bee42ab2a31ccdcb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61658105a844c1185de4862e817cbc4684eaccd149b42132d125b6f76bc5a4e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReferenceTableSchemaFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99702ad0088a79c0a244b78422035ebd2acdc64f0e9eff4102748d6ff8707a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc8d3ff04480c17c79e8c8097c6b75afe9c764bcfe60be52ce8cf5be0fb9d41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReferenceTableSchema]],
) -> None:
    """Type checking stubs"""
    pass
