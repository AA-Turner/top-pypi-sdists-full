r'''
# `google_bigquery_table`

Refer to the Terraform Registry for docs: [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table).
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


class BigqueryTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTable",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table google_bigquery_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_id: builtins.str,
        table_id: builtins.str,
        biglake_configuration: typing.Optional[typing.Union["BigqueryTableBiglakeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["BigqueryTableEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        expiration_time: typing.Optional[jsii.Number] = None,
        external_catalog_table_options: typing.Optional[typing.Union["BigqueryTableExternalCatalogTableOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        external_data_configuration: typing.Optional[typing.Union["BigqueryTableExternalDataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_auto_generated_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_schema_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        materialized_view: typing.Optional[typing.Union["BigqueryTableMaterializedView", typing.Dict[builtins.str, typing.Any]]] = None,
        max_staleness: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        range_partitioning: typing.Optional[typing.Union["BigqueryTableRangePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        schema: typing.Optional[builtins.str] = None,
        schema_foreign_type_info: typing.Optional[typing.Union["BigqueryTableSchemaForeignTypeInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        table_constraints: typing.Optional[typing.Union["BigqueryTableTableConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        table_metadata_view: typing.Optional[builtins.str] = None,
        table_replication_info: typing.Optional[typing.Union["BigqueryTableTableReplicationInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        time_partitioning: typing.Optional[typing.Union["BigqueryTableTimePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        view: typing.Optional[typing.Union["BigqueryTableView", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table google_bigquery_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_id: The dataset ID to create the table in. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#dataset_id BigqueryTable#dataset_id}
        :param table_id: A unique ID for the resource. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_id BigqueryTable#table_id}
        :param biglake_configuration: biglake_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#biglake_configuration BigqueryTable#biglake_configuration}
        :param clustering: Specifies column names to use for data clustering. Up to four top-level columns are allowed, and should be specified in descending priority order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#clustering BigqueryTable#clustering}
        :param deletion_protection: Whether Terraform will be prevented from destroying the instance. When the field is set to true or unset in Terraform state, a terraform apply or terraform destroy that would delete the table will fail. When the field is set to false, deleting the table is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#deletion_protection BigqueryTable#deletion_protection}
        :param description: The field description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#description BigqueryTable#description}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encryption_configuration BigqueryTable#encryption_configuration}
        :param expiration_time: The time when this table expires, in milliseconds since the epoch. If not present, the table will persist indefinitely. Expired tables will be deleted and their storage reclaimed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#expiration_time BigqueryTable#expiration_time}
        :param external_catalog_table_options: external_catalog_table_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#external_catalog_table_options BigqueryTable#external_catalog_table_options}
        :param external_data_configuration: external_data_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#external_data_configuration BigqueryTable#external_data_configuration}
        :param friendly_name: A descriptive name for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#friendly_name BigqueryTable#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#id BigqueryTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_auto_generated_schema: Whether Terraform will prevent implicitly added columns in schema from showing diff. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_auto_generated_schema BigqueryTable#ignore_auto_generated_schema}
        :param ignore_schema_changes: Mention which fields in schema are to be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_schema_changes BigqueryTable#ignore_schema_changes}
        :param labels: A mapping of labels to assign to the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#labels BigqueryTable#labels}
        :param materialized_view: materialized_view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#materialized_view BigqueryTable#materialized_view}
        :param max_staleness: The maximum staleness of data that could be returned when the table (or stale MV) is queried. Staleness encoded as a string encoding of `SQL IntervalValue type <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#interval_type>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#max_staleness BigqueryTable#max_staleness}
        :param project: The ID of the project in which the resource belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#project BigqueryTable#project}
        :param range_partitioning: range_partitioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range_partitioning BigqueryTable#range_partitioning}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        :param resource_tags: The tags attached to this table. Tag keys are globally unique. Tag key is expected to be in the namespaced format, for example "123456789012/environment" where 123456789012 is the ID of the parent organization or project resource for this tag key. Tag value is expected to be the short name, for example "Production". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#resource_tags BigqueryTable#resource_tags}
        :param schema: A JSON schema for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema BigqueryTable#schema}
        :param schema_foreign_type_info: schema_foreign_type_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema_foreign_type_info BigqueryTable#schema_foreign_type_info}
        :param table_constraints: table_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_constraints BigqueryTable#table_constraints}
        :param table_metadata_view: View sets the optional parameter "view": Specifies the view that determines which table information is returned. By default, basic table information and storage statistics (STORAGE_STATS) are returned. Possible values: TABLE_METADATA_VIEW_UNSPECIFIED, BASIC, STORAGE_STATS, FULL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_metadata_view BigqueryTable#table_metadata_view}
        :param table_replication_info: table_replication_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_replication_info BigqueryTable#table_replication_info}
        :param time_partitioning: time_partitioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#time_partitioning BigqueryTable#time_partitioning}
        :param view: view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#view BigqueryTable#view}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b097032883d450d5b0dd2683567f8b829165b537d5a8be476cbb660ce43d5747)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryTableConfig(
            dataset_id=dataset_id,
            table_id=table_id,
            biglake_configuration=biglake_configuration,
            clustering=clustering,
            deletion_protection=deletion_protection,
            description=description,
            encryption_configuration=encryption_configuration,
            expiration_time=expiration_time,
            external_catalog_table_options=external_catalog_table_options,
            external_data_configuration=external_data_configuration,
            friendly_name=friendly_name,
            id=id,
            ignore_auto_generated_schema=ignore_auto_generated_schema,
            ignore_schema_changes=ignore_schema_changes,
            labels=labels,
            materialized_view=materialized_view,
            max_staleness=max_staleness,
            project=project,
            range_partitioning=range_partitioning,
            require_partition_filter=require_partition_filter,
            resource_tags=resource_tags,
            schema=schema,
            schema_foreign_type_info=schema_foreign_type_info,
            table_constraints=table_constraints,
            table_metadata_view=table_metadata_view,
            table_replication_info=table_replication_info,
            time_partitioning=time_partitioning,
            view=view,
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
        '''Generates CDKTF code for importing a BigqueryTable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryTable to import.
        :param import_from_id: The id of the existing BigqueryTable that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryTable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c63bb4b9fd744406390cf66f7b1566dc5801d712accd67b66fb9c4fca46ac4f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBiglakeConfiguration")
    def put_biglake_configuration(
        self,
        *,
        connection_id: builtins.str,
        file_format: builtins.str,
        storage_uri: builtins.str,
        table_format: builtins.str,
    ) -> None:
        '''
        :param connection_id: The connection specifying the credentials to be used to read and write to external storage, such as Cloud Storage. The connection_id can have the form "<project_id>.<location_id>.<connection_id>" or "projects/<project_id>/locations/<location_id>/connections/<connection_id>". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        :param file_format: The file format the data is stored in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#file_format BigqueryTable#file_format}
        :param storage_uri: The fully qualified location prefix of the external folder where table data is stored. The '*' wildcard character is not allowed. The URI should be in the format "gs://bucket/path_to_table/" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#storage_uri BigqueryTable#storage_uri}
        :param table_format: The table format the metadata only snapshots are stored in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_format BigqueryTable#table_format}
        '''
        value = BigqueryTableBiglakeConfiguration(
            connection_id=connection_id,
            file_format=file_format,
            storage_uri=storage_uri,
            table_format=table_format,
        )

        return typing.cast(None, jsii.invoke(self, "putBiglakeConfiguration", [value]))

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The self link or full name of a key which should be used to encrypt this table. Note that the default bigquery service account will need to have encrypt/decrypt permissions on this key - you may want to see the google_bigquery_default_service_account datasource and the google_kms_crypto_key_iam_binding resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#kms_key_name BigqueryTable#kms_key_name}
        '''
        value = BigqueryTableEncryptionConfiguration(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putExternalCatalogTableOptions")
    def put_external_catalog_table_options(
        self,
        *,
        connection_id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_descriptor: typing.Optional[typing.Union["BigqueryTableExternalCatalogTableOptionsStorageDescriptor", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection_id: The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3. The connection is needed to read the open source table from BigQuery Engine. The connection_id can have the form <project_id>.<location_id>.<connection_id> or projects/<project_id>/locations/<location_id>/connections/<connection_id>. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        :param parameters: A map of key value pairs defining the parameters and properties of the open source table. Corresponds with hive meta store table parameters. Maximum size of 4Mib. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parameters BigqueryTable#parameters}
        :param storage_descriptor: storage_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#storage_descriptor BigqueryTable#storage_descriptor}
        '''
        value = BigqueryTableExternalCatalogTableOptions(
            connection_id=connection_id,
            parameters=parameters,
            storage_descriptor=storage_descriptor,
        )

        return typing.cast(None, jsii.invoke(self, "putExternalCatalogTableOptions", [value]))

    @jsii.member(jsii_name="putExternalDataConfiguration")
    def put_external_data_configuration(
        self,
        *,
        autodetect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        source_uris: typing.Sequence[builtins.str],
        avro_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationAvroOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        bigtable_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationBigtableOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression: typing.Optional[builtins.str] = None,
        connection_id: typing.Optional[builtins.str] = None,
        csv_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        file_set_spec_type: typing.Optional[builtins.str] = None,
        google_sheets_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationGoogleSheetsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_partitioning_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationHivePartitioningOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_extension: typing.Optional[builtins.str] = None,
        json_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        max_bad_records: typing.Optional[jsii.Number] = None,
        metadata_cache_mode: typing.Optional[builtins.str] = None,
        object_metadata: typing.Optional[builtins.str] = None,
        parquet_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        reference_file_schema_uri: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autodetect: Let BigQuery try to autodetect the schema and format of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#autodetect BigqueryTable#autodetect}
        :param source_uris: A list of the fully-qualified URIs that point to your data in Google Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_uris BigqueryTable#source_uris}
        :param avro_options: avro_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#avro_options BigqueryTable#avro_options}
        :param bigtable_options: bigtable_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#bigtable_options BigqueryTable#bigtable_options}
        :param compression: The compression type of the data source. Valid values are "NONE" or "GZIP". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#compression BigqueryTable#compression}
        :param connection_id: The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3. The connectionId can have the form "..<connection_id>" or "projects//locations//connections/<connection_id>". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#csv_options BigqueryTable#csv_options}
        :param file_set_spec_type: Specifies how source URIs are interpreted for constructing the file set to load. By default source URIs are expanded against the underlying storage. Other options include specifying manifest files. Only applicable to object storage systems. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#file_set_spec_type BigqueryTable#file_set_spec_type}
        :param google_sheets_options: google_sheets_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#google_sheets_options BigqueryTable#google_sheets_options}
        :param hive_partitioning_options: hive_partitioning_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#hive_partitioning_options BigqueryTable#hive_partitioning_options}
        :param ignore_unknown_values: Indicates if BigQuery should allow extra values that are not represented in the table schema. If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_unknown_values BigqueryTable#ignore_unknown_values}
        :param json_extension: Load option to be used together with sourceFormat newline-delimited JSON to indicate that a variant of JSON is being loaded. To load newline-delimited GeoJSON, specify GEOJSON (and sourceFormat must be set to NEWLINE_DELIMITED_JSON). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#json_extension BigqueryTable#json_extension}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#json_options BigqueryTable#json_options}
        :param max_bad_records: The maximum number of bad records that BigQuery can ignore when reading data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#max_bad_records BigqueryTable#max_bad_records}
        :param metadata_cache_mode: Metadata Cache Mode for the table. Set this to enable caching of metadata from external data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#metadata_cache_mode BigqueryTable#metadata_cache_mode}
        :param object_metadata: Object Metadata is used to create Object Tables. Object Tables contain a listing of objects (with their metadata) found at the sourceUris. If ObjectMetadata is set, sourceFormat should be omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#object_metadata BigqueryTable#object_metadata}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parquet_options BigqueryTable#parquet_options}
        :param reference_file_schema_uri: When creating an external table, the user can provide a reference file with the table schema. This is enabled for the following formats: AVRO, PARQUET, ORC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#reference_file_schema_uri BigqueryTable#reference_file_schema_uri}
        :param schema: A JSON schema for the external table. Schema is required for CSV and JSON formats and is disallowed for Google Cloud Bigtable, Cloud Datastore backups, and Avro formats when using external tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema BigqueryTable#schema}
        :param source_format: Please see sourceFormat under ExternalDataConfiguration in Bigquery's public API documentation (https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externaldataconfiguration) for supported formats. To use "GOOGLE_SHEETS" the scopes must include "googleapis.com/auth/drive.readonly". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_format BigqueryTable#source_format}
        '''
        value = BigqueryTableExternalDataConfiguration(
            autodetect=autodetect,
            source_uris=source_uris,
            avro_options=avro_options,
            bigtable_options=bigtable_options,
            compression=compression,
            connection_id=connection_id,
            csv_options=csv_options,
            file_set_spec_type=file_set_spec_type,
            google_sheets_options=google_sheets_options,
            hive_partitioning_options=hive_partitioning_options,
            ignore_unknown_values=ignore_unknown_values,
            json_extension=json_extension,
            json_options=json_options,
            max_bad_records=max_bad_records,
            metadata_cache_mode=metadata_cache_mode,
            object_metadata=object_metadata,
            parquet_options=parquet_options,
            reference_file_schema_uri=reference_file_schema_uri,
            schema=schema,
            source_format=source_format,
        )

        return typing.cast(None, jsii.invoke(self, "putExternalDataConfiguration", [value]))

    @jsii.member(jsii_name="putMaterializedView")
    def put_materialized_view(
        self,
        *,
        query: builtins.str,
        allow_non_incremental_definition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        refresh_interval_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: A query whose result is persisted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#query BigqueryTable#query}
        :param allow_non_incremental_definition: Allow non incremental materialized view definition. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_non_incremental_definition BigqueryTable#allow_non_incremental_definition}
        :param enable_refresh: Specifies if BigQuery should automatically refresh materialized view when the base table is updated. The default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enable_refresh BigqueryTable#enable_refresh}
        :param refresh_interval_ms: Specifies maximum frequency at which this materialized view will be refreshed. The default is 1800000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#refresh_interval_ms BigqueryTable#refresh_interval_ms}
        '''
        value = BigqueryTableMaterializedView(
            query=query,
            allow_non_incremental_definition=allow_non_incremental_definition,
            enable_refresh=enable_refresh,
            refresh_interval_ms=refresh_interval_ms,
        )

        return typing.cast(None, jsii.invoke(self, "putMaterializedView", [value]))

    @jsii.member(jsii_name="putRangePartitioning")
    def put_range_partitioning(
        self,
        *,
        field: builtins.str,
        range: typing.Union["BigqueryTableRangePartitioningRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: The field used to determine how to create a range-based partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field BigqueryTable#field}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range BigqueryTable#range}
        '''
        value = BigqueryTableRangePartitioning(field=field, range=range)

        return typing.cast(None, jsii.invoke(self, "putRangePartitioning", [value]))

    @jsii.member(jsii_name="putSchemaForeignTypeInfo")
    def put_schema_foreign_type_info(self, *, type_system: builtins.str) -> None:
        '''
        :param type_system: Specifies the system which defines the foreign data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type_system BigqueryTable#type_system}
        '''
        value = BigqueryTableSchemaForeignTypeInfo(type_system=type_system)

        return typing.cast(None, jsii.invoke(self, "putSchemaForeignTypeInfo", [value]))

    @jsii.member(jsii_name="putTableConstraints")
    def put_table_constraints(
        self,
        *,
        foreign_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryTableTableConstraintsForeignKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        primary_key: typing.Optional[typing.Union["BigqueryTableTableConstraintsPrimaryKey", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param foreign_keys: foreign_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#foreign_keys BigqueryTable#foreign_keys}
        :param primary_key: primary_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#primary_key BigqueryTable#primary_key}
        '''
        value = BigqueryTableTableConstraints(
            foreign_keys=foreign_keys, primary_key=primary_key
        )

        return typing.cast(None, jsii.invoke(self, "putTableConstraints", [value]))

    @jsii.member(jsii_name="putTableReplicationInfo")
    def put_table_replication_info(
        self,
        *,
        source_dataset_id: builtins.str,
        source_project_id: builtins.str,
        source_table_id: builtins.str,
        replication_interval_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_dataset_id: The ID of the source dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_dataset_id BigqueryTable#source_dataset_id}
        :param source_project_id: The ID of the source project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_project_id BigqueryTable#source_project_id}
        :param source_table_id: The ID of the source materialized view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_table_id BigqueryTable#source_table_id}
        :param replication_interval_ms: The interval at which the source materialized view is polled for updates. The default is 300000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#replication_interval_ms BigqueryTable#replication_interval_ms}
        '''
        value = BigqueryTableTableReplicationInfo(
            source_dataset_id=source_dataset_id,
            source_project_id=source_project_id,
            source_table_id=source_table_id,
            replication_interval_ms=replication_interval_ms,
        )

        return typing.cast(None, jsii.invoke(self, "putTableReplicationInfo", [value]))

    @jsii.member(jsii_name="putTimePartitioning")
    def put_time_partitioning(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[jsii.Number] = None,
        field: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: The supported types are DAY, HOUR, MONTH, and YEAR, which will generate one partition per day, hour, month, and year, respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type BigqueryTable#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#expiration_ms BigqueryTable#expiration_ms}
        :param field: The field used to determine how to create a time-based partition. If time-based partitioning is enabled without this value, the table is partitioned based on the load time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field BigqueryTable#field}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        value = BigqueryTableTimePartitioning(
            type=type,
            expiration_ms=expiration_ms,
            field=field,
            require_partition_filter=require_partition_filter,
        )

        return typing.cast(None, jsii.invoke(self, "putTimePartitioning", [value]))

    @jsii.member(jsii_name="putView")
    def put_view(
        self,
        *,
        query: builtins.str,
        use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query: A query that BigQuery executes when the view is referenced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#query BigqueryTable#query}
        :param use_legacy_sql: Specifies whether to use BigQuery's legacy SQL for this view. The default value is true. If set to false, the view will use BigQuery's standard SQL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#use_legacy_sql BigqueryTable#use_legacy_sql}
        '''
        value = BigqueryTableView(query=query, use_legacy_sql=use_legacy_sql)

        return typing.cast(None, jsii.invoke(self, "putView", [value]))

    @jsii.member(jsii_name="resetBiglakeConfiguration")
    def reset_biglake_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBiglakeConfiguration", []))

    @jsii.member(jsii_name="resetClustering")
    def reset_clustering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClustering", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetExpirationTime")
    def reset_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationTime", []))

    @jsii.member(jsii_name="resetExternalCatalogTableOptions")
    def reset_external_catalog_table_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalCatalogTableOptions", []))

    @jsii.member(jsii_name="resetExternalDataConfiguration")
    def reset_external_data_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalDataConfiguration", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreAutoGeneratedSchema")
    def reset_ignore_auto_generated_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreAutoGeneratedSchema", []))

    @jsii.member(jsii_name="resetIgnoreSchemaChanges")
    def reset_ignore_schema_changes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreSchemaChanges", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaterializedView")
    def reset_materialized_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaterializedView", []))

    @jsii.member(jsii_name="resetMaxStaleness")
    def reset_max_staleness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxStaleness", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRangePartitioning")
    def reset_range_partitioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangePartitioning", []))

    @jsii.member(jsii_name="resetRequirePartitionFilter")
    def reset_require_partition_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirePartitionFilter", []))

    @jsii.member(jsii_name="resetResourceTags")
    def reset_resource_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTags", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetSchemaForeignTypeInfo")
    def reset_schema_foreign_type_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaForeignTypeInfo", []))

    @jsii.member(jsii_name="resetTableConstraints")
    def reset_table_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableConstraints", []))

    @jsii.member(jsii_name="resetTableMetadataView")
    def reset_table_metadata_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableMetadataView", []))

    @jsii.member(jsii_name="resetTableReplicationInfo")
    def reset_table_replication_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableReplicationInfo", []))

    @jsii.member(jsii_name="resetTimePartitioning")
    def reset_time_partitioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimePartitioning", []))

    @jsii.member(jsii_name="resetView")
    def reset_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetView", []))

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
    @jsii.member(jsii_name="biglakeConfiguration")
    def biglake_configuration(
        self,
    ) -> "BigqueryTableBiglakeConfigurationOutputReference":
        return typing.cast("BigqueryTableBiglakeConfigurationOutputReference", jsii.get(self, "biglakeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> "BigqueryTableEncryptionConfigurationOutputReference":
        return typing.cast("BigqueryTableEncryptionConfigurationOutputReference", jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="externalCatalogTableOptions")
    def external_catalog_table_options(
        self,
    ) -> "BigqueryTableExternalCatalogTableOptionsOutputReference":
        return typing.cast("BigqueryTableExternalCatalogTableOptionsOutputReference", jsii.get(self, "externalCatalogTableOptions"))

    @builtins.property
    @jsii.member(jsii_name="externalDataConfiguration")
    def external_data_configuration(
        self,
    ) -> "BigqueryTableExternalDataConfigurationOutputReference":
        return typing.cast("BigqueryTableExternalDataConfigurationOutputReference", jsii.get(self, "externalDataConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="materializedView")
    def materialized_view(self) -> "BigqueryTableMaterializedViewOutputReference":
        return typing.cast("BigqueryTableMaterializedViewOutputReference", jsii.get(self, "materializedView"))

    @builtins.property
    @jsii.member(jsii_name="numBytes")
    def num_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numBytes"))

    @builtins.property
    @jsii.member(jsii_name="numLongTermBytes")
    def num_long_term_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLongTermBytes"))

    @builtins.property
    @jsii.member(jsii_name="numRows")
    def num_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numRows"))

    @builtins.property
    @jsii.member(jsii_name="rangePartitioning")
    def range_partitioning(self) -> "BigqueryTableRangePartitioningOutputReference":
        return typing.cast("BigqueryTableRangePartitioningOutputReference", jsii.get(self, "rangePartitioning"))

    @builtins.property
    @jsii.member(jsii_name="schemaForeignTypeInfo")
    def schema_foreign_type_info(
        self,
    ) -> "BigqueryTableSchemaForeignTypeInfoOutputReference":
        return typing.cast("BigqueryTableSchemaForeignTypeInfoOutputReference", jsii.get(self, "schemaForeignTypeInfo"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="tableConstraints")
    def table_constraints(self) -> "BigqueryTableTableConstraintsOutputReference":
        return typing.cast("BigqueryTableTableConstraintsOutputReference", jsii.get(self, "tableConstraints"))

    @builtins.property
    @jsii.member(jsii_name="tableReplicationInfo")
    def table_replication_info(
        self,
    ) -> "BigqueryTableTableReplicationInfoOutputReference":
        return typing.cast("BigqueryTableTableReplicationInfoOutputReference", jsii.get(self, "tableReplicationInfo"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timePartitioning")
    def time_partitioning(self) -> "BigqueryTableTimePartitioningOutputReference":
        return typing.cast("BigqueryTableTimePartitioningOutputReference", jsii.get(self, "timePartitioning"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="view")
    def view(self) -> "BigqueryTableViewOutputReference":
        return typing.cast("BigqueryTableViewOutputReference", jsii.get(self, "view"))

    @builtins.property
    @jsii.member(jsii_name="biglakeConfigurationInput")
    def biglake_configuration_input(
        self,
    ) -> typing.Optional["BigqueryTableBiglakeConfiguration"]:
        return typing.cast(typing.Optional["BigqueryTableBiglakeConfiguration"], jsii.get(self, "biglakeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="clusteringInput")
    def clustering_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusteringInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional["BigqueryTableEncryptionConfiguration"]:
        return typing.cast(typing.Optional["BigqueryTableEncryptionConfiguration"], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTimeInput")
    def expiration_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalCatalogTableOptionsInput")
    def external_catalog_table_options_input(
        self,
    ) -> typing.Optional["BigqueryTableExternalCatalogTableOptions"]:
        return typing.cast(typing.Optional["BigqueryTableExternalCatalogTableOptions"], jsii.get(self, "externalCatalogTableOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="externalDataConfigurationInput")
    def external_data_configuration_input(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfiguration"]:
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfiguration"], jsii.get(self, "externalDataConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreAutoGeneratedSchemaInput")
    def ignore_auto_generated_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreAutoGeneratedSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreSchemaChangesInput")
    def ignore_schema_changes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignoreSchemaChangesInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="materializedViewInput")
    def materialized_view_input(
        self,
    ) -> typing.Optional["BigqueryTableMaterializedView"]:
        return typing.cast(typing.Optional["BigqueryTableMaterializedView"], jsii.get(self, "materializedViewInput"))

    @builtins.property
    @jsii.member(jsii_name="maxStalenessInput")
    def max_staleness_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxStalenessInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rangePartitioningInput")
    def range_partitioning_input(
        self,
    ) -> typing.Optional["BigqueryTableRangePartitioning"]:
        return typing.cast(typing.Optional["BigqueryTableRangePartitioning"], jsii.get(self, "rangePartitioningInput"))

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilterInput")
    def require_partition_filter_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requirePartitionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagsInput")
    def resource_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaForeignTypeInfoInput")
    def schema_foreign_type_info_input(
        self,
    ) -> typing.Optional["BigqueryTableSchemaForeignTypeInfo"]:
        return typing.cast(typing.Optional["BigqueryTableSchemaForeignTypeInfo"], jsii.get(self, "schemaForeignTypeInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tableConstraintsInput")
    def table_constraints_input(
        self,
    ) -> typing.Optional["BigqueryTableTableConstraints"]:
        return typing.cast(typing.Optional["BigqueryTableTableConstraints"], jsii.get(self, "tableConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableMetadataViewInput")
    def table_metadata_view_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableMetadataViewInput"))

    @builtins.property
    @jsii.member(jsii_name="tableReplicationInfoInput")
    def table_replication_info_input(
        self,
    ) -> typing.Optional["BigqueryTableTableReplicationInfo"]:
        return typing.cast(typing.Optional["BigqueryTableTableReplicationInfo"], jsii.get(self, "tableReplicationInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="timePartitioningInput")
    def time_partitioning_input(
        self,
    ) -> typing.Optional["BigqueryTableTimePartitioning"]:
        return typing.cast(typing.Optional["BigqueryTableTimePartitioning"], jsii.get(self, "timePartitioningInput"))

    @builtins.property
    @jsii.member(jsii_name="viewInput")
    def view_input(self) -> typing.Optional["BigqueryTableView"]:
        return typing.cast(typing.Optional["BigqueryTableView"], jsii.get(self, "viewInput"))

    @builtins.property
    @jsii.member(jsii_name="clustering")
    def clustering(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clustering"))

    @clustering.setter
    def clustering(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36a827767218e30e15ed46c620f1d6ac1649ac81e9a1f8fbf50b44994a8de7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clustering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ba56c49b068bbf8763ea0042060807cbf89b0406ef980ed1fc45513c07dca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62578b34b021403200b1036268e3acd655157cb771a72f5d129bf260f4c27cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c0bfe985825d9a80acd8f5aefedd8901d464dacf94af409b2a81efccfc3fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5413b10f3ec29a1d03f7c2f42f492fee9e3d71fa450c28d4bd6f46ef3ef51e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b95bd39489b26bd16347f815db6f92fba878214004df53fa734ec6f798849ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af66ed510248d931e4bb1f43b218cca02cd6069e76f18cdb7150e9530186201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreAutoGeneratedSchema")
    def ignore_auto_generated_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreAutoGeneratedSchema"))

    @ignore_auto_generated_schema.setter
    def ignore_auto_generated_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d9c292ece217d3549642355546610c9c921d03644d0036d53e2f4b01de2916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreAutoGeneratedSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreSchemaChanges")
    def ignore_schema_changes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ignoreSchemaChanges"))

    @ignore_schema_changes.setter
    def ignore_schema_changes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3299834edde10412dba8507dd9bbb1103c12e86905ca5fd8dbc00415deaf5058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreSchemaChanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c74889bf00ce24f484abd1bc28bf3cf7d61665b2ab8f55381086fce8f1291c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxStaleness")
    def max_staleness(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxStaleness"))

    @max_staleness.setter
    def max_staleness(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc79c2fa24fcd8108b4d32f5f2411cc78630355878d937c6df66e6330c75711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxStaleness", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1a6d53539cb352313127bc88400bfb27109837e44e77e3c2445bb3a3ceaa22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilter")
    def require_partition_filter(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requirePartitionFilter"))

    @require_partition_filter.setter
    def require_partition_filter(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baca9cd111dd2c321ea33796f0042eb16fce60720708bc62959bbce16e17e6e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirePartitionFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8578b4a8db03882361789b6dcd1c8943a41c5e0b12027987a63f64f259b86762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570adc90f3ed8491972bb571ec80eb5f0b0fdf5931d71a249e93fd1f993d7b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ff67f97457c05dfe2bdc38c7d1b6d4d3ab19d3aed9a3b6ab5e87619edf6da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableMetadataView")
    def table_metadata_view(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableMetadataView"))

    @table_metadata_view.setter
    def table_metadata_view(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3b81c8674496306bcc75d720b6c39b4af02782c243df31969f5495909ac5b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableMetadataView", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableBiglakeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "connection_id": "connectionId",
        "file_format": "fileFormat",
        "storage_uri": "storageUri",
        "table_format": "tableFormat",
    },
)
class BigqueryTableBiglakeConfiguration:
    def __init__(
        self,
        *,
        connection_id: builtins.str,
        file_format: builtins.str,
        storage_uri: builtins.str,
        table_format: builtins.str,
    ) -> None:
        '''
        :param connection_id: The connection specifying the credentials to be used to read and write to external storage, such as Cloud Storage. The connection_id can have the form "<project_id>.<location_id>.<connection_id>" or "projects/<project_id>/locations/<location_id>/connections/<connection_id>". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        :param file_format: The file format the data is stored in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#file_format BigqueryTable#file_format}
        :param storage_uri: The fully qualified location prefix of the external folder where table data is stored. The '*' wildcard character is not allowed. The URI should be in the format "gs://bucket/path_to_table/" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#storage_uri BigqueryTable#storage_uri}
        :param table_format: The table format the metadata only snapshots are stored in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_format BigqueryTable#table_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dccd07ead4367a3bc4cd191ef4729bd296220175d0b8991db980fd2af262039)
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument storage_uri", value=storage_uri, expected_type=type_hints["storage_uri"])
            check_type(argname="argument table_format", value=table_format, expected_type=type_hints["table_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_id": connection_id,
            "file_format": file_format,
            "storage_uri": storage_uri,
            "table_format": table_format,
        }

    @builtins.property
    def connection_id(self) -> builtins.str:
        '''The connection specifying the credentials to be used to read and write to external storage, such as Cloud Storage.

        The connection_id can have the form "<project_id>.<location_id>.<connection_id>" or "projects/<project_id>/locations/<location_id>/connections/<connection_id>".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        '''
        result = self._values.get("connection_id")
        assert result is not None, "Required property 'connection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_format(self) -> builtins.str:
        '''The file format the data is stored in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#file_format BigqueryTable#file_format}
        '''
        result = self._values.get("file_format")
        assert result is not None, "Required property 'file_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_uri(self) -> builtins.str:
        '''The fully qualified location prefix of the external folder where table data is stored.

        The '*' wildcard character is not allowed. The URI should be in the format "gs://bucket/path_to_table/"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#storage_uri BigqueryTable#storage_uri}
        '''
        result = self._values.get("storage_uri")
        assert result is not None, "Required property 'storage_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_format(self) -> builtins.str:
        '''The table format the metadata only snapshots are stored in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_format BigqueryTable#table_format}
        '''
        result = self._values.get("table_format")
        assert result is not None, "Required property 'table_format' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableBiglakeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableBiglakeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableBiglakeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a509fe31b2c6b19f7ecf2c52c8c10d233620b2b0723b2cc93a464c36d4863ffe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="fileFormatInput")
    def file_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUriInput")
    def storage_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="tableFormatInput")
    def table_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500bfdde294f601a4372c18ff5821627c35f3ca1684395e3b29a63c109af86bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileFormat")
    def file_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileFormat"))

    @file_format.setter
    def file_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ce961f3aef0437fc73f474e2fa2710c4ba6c077e27fb379976f4d48156b777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageUri")
    def storage_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageUri"))

    @storage_uri.setter
    def storage_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64cf859df62ab61eb1f8f4f07a9b43fdd93cc8e623b853f57d4cfb39b69eb913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableFormat")
    def table_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableFormat"))

    @table_format.setter
    def table_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2743cf8f9612f2920af6ed5f715f0dbfc1b4f095010aac0dd76e4f87cf22b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableBiglakeConfiguration]:
        return typing.cast(typing.Optional[BigqueryTableBiglakeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableBiglakeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a1e361e20f5b31aff949115dab66215002a3b8936dcb653eace5de1dc5234e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset_id": "datasetId",
        "table_id": "tableId",
        "biglake_configuration": "biglakeConfiguration",
        "clustering": "clustering",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "encryption_configuration": "encryptionConfiguration",
        "expiration_time": "expirationTime",
        "external_catalog_table_options": "externalCatalogTableOptions",
        "external_data_configuration": "externalDataConfiguration",
        "friendly_name": "friendlyName",
        "id": "id",
        "ignore_auto_generated_schema": "ignoreAutoGeneratedSchema",
        "ignore_schema_changes": "ignoreSchemaChanges",
        "labels": "labels",
        "materialized_view": "materializedView",
        "max_staleness": "maxStaleness",
        "project": "project",
        "range_partitioning": "rangePartitioning",
        "require_partition_filter": "requirePartitionFilter",
        "resource_tags": "resourceTags",
        "schema": "schema",
        "schema_foreign_type_info": "schemaForeignTypeInfo",
        "table_constraints": "tableConstraints",
        "table_metadata_view": "tableMetadataView",
        "table_replication_info": "tableReplicationInfo",
        "time_partitioning": "timePartitioning",
        "view": "view",
    },
)
class BigqueryTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset_id: builtins.str,
        table_id: builtins.str,
        biglake_configuration: typing.Optional[typing.Union[BigqueryTableBiglakeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["BigqueryTableEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        expiration_time: typing.Optional[jsii.Number] = None,
        external_catalog_table_options: typing.Optional[typing.Union["BigqueryTableExternalCatalogTableOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        external_data_configuration: typing.Optional[typing.Union["BigqueryTableExternalDataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_auto_generated_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_schema_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        materialized_view: typing.Optional[typing.Union["BigqueryTableMaterializedView", typing.Dict[builtins.str, typing.Any]]] = None,
        max_staleness: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        range_partitioning: typing.Optional[typing.Union["BigqueryTableRangePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        schema: typing.Optional[builtins.str] = None,
        schema_foreign_type_info: typing.Optional[typing.Union["BigqueryTableSchemaForeignTypeInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        table_constraints: typing.Optional[typing.Union["BigqueryTableTableConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        table_metadata_view: typing.Optional[builtins.str] = None,
        table_replication_info: typing.Optional[typing.Union["BigqueryTableTableReplicationInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        time_partitioning: typing.Optional[typing.Union["BigqueryTableTimePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        view: typing.Optional[typing.Union["BigqueryTableView", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_id: The dataset ID to create the table in. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#dataset_id BigqueryTable#dataset_id}
        :param table_id: A unique ID for the resource. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_id BigqueryTable#table_id}
        :param biglake_configuration: biglake_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#biglake_configuration BigqueryTable#biglake_configuration}
        :param clustering: Specifies column names to use for data clustering. Up to four top-level columns are allowed, and should be specified in descending priority order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#clustering BigqueryTable#clustering}
        :param deletion_protection: Whether Terraform will be prevented from destroying the instance. When the field is set to true or unset in Terraform state, a terraform apply or terraform destroy that would delete the table will fail. When the field is set to false, deleting the table is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#deletion_protection BigqueryTable#deletion_protection}
        :param description: The field description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#description BigqueryTable#description}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encryption_configuration BigqueryTable#encryption_configuration}
        :param expiration_time: The time when this table expires, in milliseconds since the epoch. If not present, the table will persist indefinitely. Expired tables will be deleted and their storage reclaimed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#expiration_time BigqueryTable#expiration_time}
        :param external_catalog_table_options: external_catalog_table_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#external_catalog_table_options BigqueryTable#external_catalog_table_options}
        :param external_data_configuration: external_data_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#external_data_configuration BigqueryTable#external_data_configuration}
        :param friendly_name: A descriptive name for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#friendly_name BigqueryTable#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#id BigqueryTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_auto_generated_schema: Whether Terraform will prevent implicitly added columns in schema from showing diff. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_auto_generated_schema BigqueryTable#ignore_auto_generated_schema}
        :param ignore_schema_changes: Mention which fields in schema are to be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_schema_changes BigqueryTable#ignore_schema_changes}
        :param labels: A mapping of labels to assign to the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#labels BigqueryTable#labels}
        :param materialized_view: materialized_view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#materialized_view BigqueryTable#materialized_view}
        :param max_staleness: The maximum staleness of data that could be returned when the table (or stale MV) is queried. Staleness encoded as a string encoding of `SQL IntervalValue type <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#interval_type>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#max_staleness BigqueryTable#max_staleness}
        :param project: The ID of the project in which the resource belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#project BigqueryTable#project}
        :param range_partitioning: range_partitioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range_partitioning BigqueryTable#range_partitioning}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        :param resource_tags: The tags attached to this table. Tag keys are globally unique. Tag key is expected to be in the namespaced format, for example "123456789012/environment" where 123456789012 is the ID of the parent organization or project resource for this tag key. Tag value is expected to be the short name, for example "Production". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#resource_tags BigqueryTable#resource_tags}
        :param schema: A JSON schema for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema BigqueryTable#schema}
        :param schema_foreign_type_info: schema_foreign_type_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema_foreign_type_info BigqueryTable#schema_foreign_type_info}
        :param table_constraints: table_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_constraints BigqueryTable#table_constraints}
        :param table_metadata_view: View sets the optional parameter "view": Specifies the view that determines which table information is returned. By default, basic table information and storage statistics (STORAGE_STATS) are returned. Possible values: TABLE_METADATA_VIEW_UNSPECIFIED, BASIC, STORAGE_STATS, FULL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_metadata_view BigqueryTable#table_metadata_view}
        :param table_replication_info: table_replication_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_replication_info BigqueryTable#table_replication_info}
        :param time_partitioning: time_partitioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#time_partitioning BigqueryTable#time_partitioning}
        :param view: view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#view BigqueryTable#view}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(biglake_configuration, dict):
            biglake_configuration = BigqueryTableBiglakeConfiguration(**biglake_configuration)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = BigqueryTableEncryptionConfiguration(**encryption_configuration)
        if isinstance(external_catalog_table_options, dict):
            external_catalog_table_options = BigqueryTableExternalCatalogTableOptions(**external_catalog_table_options)
        if isinstance(external_data_configuration, dict):
            external_data_configuration = BigqueryTableExternalDataConfiguration(**external_data_configuration)
        if isinstance(materialized_view, dict):
            materialized_view = BigqueryTableMaterializedView(**materialized_view)
        if isinstance(range_partitioning, dict):
            range_partitioning = BigqueryTableRangePartitioning(**range_partitioning)
        if isinstance(schema_foreign_type_info, dict):
            schema_foreign_type_info = BigqueryTableSchemaForeignTypeInfo(**schema_foreign_type_info)
        if isinstance(table_constraints, dict):
            table_constraints = BigqueryTableTableConstraints(**table_constraints)
        if isinstance(table_replication_info, dict):
            table_replication_info = BigqueryTableTableReplicationInfo(**table_replication_info)
        if isinstance(time_partitioning, dict):
            time_partitioning = BigqueryTableTimePartitioning(**time_partitioning)
        if isinstance(view, dict):
            view = BigqueryTableView(**view)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a75785b12d60945a47678d02ebd6a12a808d31eb6207fa82349d07fd479f943)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument biglake_configuration", value=biglake_configuration, expected_type=type_hints["biglake_configuration"])
            check_type(argname="argument clustering", value=clustering, expected_type=type_hints["clustering"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument expiration_time", value=expiration_time, expected_type=type_hints["expiration_time"])
            check_type(argname="argument external_catalog_table_options", value=external_catalog_table_options, expected_type=type_hints["external_catalog_table_options"])
            check_type(argname="argument external_data_configuration", value=external_data_configuration, expected_type=type_hints["external_data_configuration"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_auto_generated_schema", value=ignore_auto_generated_schema, expected_type=type_hints["ignore_auto_generated_schema"])
            check_type(argname="argument ignore_schema_changes", value=ignore_schema_changes, expected_type=type_hints["ignore_schema_changes"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument materialized_view", value=materialized_view, expected_type=type_hints["materialized_view"])
            check_type(argname="argument max_staleness", value=max_staleness, expected_type=type_hints["max_staleness"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument range_partitioning", value=range_partitioning, expected_type=type_hints["range_partitioning"])
            check_type(argname="argument require_partition_filter", value=require_partition_filter, expected_type=type_hints["require_partition_filter"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument schema_foreign_type_info", value=schema_foreign_type_info, expected_type=type_hints["schema_foreign_type_info"])
            check_type(argname="argument table_constraints", value=table_constraints, expected_type=type_hints["table_constraints"])
            check_type(argname="argument table_metadata_view", value=table_metadata_view, expected_type=type_hints["table_metadata_view"])
            check_type(argname="argument table_replication_info", value=table_replication_info, expected_type=type_hints["table_replication_info"])
            check_type(argname="argument time_partitioning", value=time_partitioning, expected_type=type_hints["time_partitioning"])
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "table_id": table_id,
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
        if biglake_configuration is not None:
            self._values["biglake_configuration"] = biglake_configuration
        if clustering is not None:
            self._values["clustering"] = clustering
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if expiration_time is not None:
            self._values["expiration_time"] = expiration_time
        if external_catalog_table_options is not None:
            self._values["external_catalog_table_options"] = external_catalog_table_options
        if external_data_configuration is not None:
            self._values["external_data_configuration"] = external_data_configuration
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if id is not None:
            self._values["id"] = id
        if ignore_auto_generated_schema is not None:
            self._values["ignore_auto_generated_schema"] = ignore_auto_generated_schema
        if ignore_schema_changes is not None:
            self._values["ignore_schema_changes"] = ignore_schema_changes
        if labels is not None:
            self._values["labels"] = labels
        if materialized_view is not None:
            self._values["materialized_view"] = materialized_view
        if max_staleness is not None:
            self._values["max_staleness"] = max_staleness
        if project is not None:
            self._values["project"] = project
        if range_partitioning is not None:
            self._values["range_partitioning"] = range_partitioning
        if require_partition_filter is not None:
            self._values["require_partition_filter"] = require_partition_filter
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if schema is not None:
            self._values["schema"] = schema
        if schema_foreign_type_info is not None:
            self._values["schema_foreign_type_info"] = schema_foreign_type_info
        if table_constraints is not None:
            self._values["table_constraints"] = table_constraints
        if table_metadata_view is not None:
            self._values["table_metadata_view"] = table_metadata_view
        if table_replication_info is not None:
            self._values["table_replication_info"] = table_replication_info
        if time_partitioning is not None:
            self._values["time_partitioning"] = time_partitioning
        if view is not None:
            self._values["view"] = view

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
    def dataset_id(self) -> builtins.str:
        '''The dataset ID to create the table in. Changing this forces a new resource to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#dataset_id BigqueryTable#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''A unique ID for the resource. Changing this forces a new resource to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_id BigqueryTable#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def biglake_configuration(
        self,
    ) -> typing.Optional[BigqueryTableBiglakeConfiguration]:
        '''biglake_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#biglake_configuration BigqueryTable#biglake_configuration}
        '''
        result = self._values.get("biglake_configuration")
        return typing.cast(typing.Optional[BigqueryTableBiglakeConfiguration], result)

    @builtins.property
    def clustering(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies column names to use for data clustering.

        Up to four top-level columns are allowed, and should be specified in descending priority order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#clustering BigqueryTable#clustering}
        '''
        result = self._values.get("clustering")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the instance.

        When the field is set to true or unset in Terraform state, a terraform apply or terraform destroy that would delete the table will fail. When the field is set to false, deleting the table is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#deletion_protection BigqueryTable#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The field description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#description BigqueryTable#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["BigqueryTableEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encryption_configuration BigqueryTable#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["BigqueryTableEncryptionConfiguration"], result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[jsii.Number]:
        '''The time when this table expires, in milliseconds since the epoch.

        If not present, the table will persist indefinitely. Expired tables will be deleted and their storage reclaimed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#expiration_time BigqueryTable#expiration_time}
        '''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_catalog_table_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalCatalogTableOptions"]:
        '''external_catalog_table_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#external_catalog_table_options BigqueryTable#external_catalog_table_options}
        '''
        result = self._values.get("external_catalog_table_options")
        return typing.cast(typing.Optional["BigqueryTableExternalCatalogTableOptions"], result)

    @builtins.property
    def external_data_configuration(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfiguration"]:
        '''external_data_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#external_data_configuration BigqueryTable#external_data_configuration}
        '''
        result = self._values.get("external_data_configuration")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfiguration"], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''A descriptive name for the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#friendly_name BigqueryTable#friendly_name}
        '''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#id BigqueryTable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_auto_generated_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will prevent implicitly added columns in schema from showing diff.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_auto_generated_schema BigqueryTable#ignore_auto_generated_schema}
        '''
        result = self._values.get("ignore_auto_generated_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_schema_changes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Mention which fields in schema are to be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_schema_changes BigqueryTable#ignore_schema_changes}
        '''
        result = self._values.get("ignore_schema_changes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of labels to assign to the resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#labels BigqueryTable#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def materialized_view(self) -> typing.Optional["BigqueryTableMaterializedView"]:
        '''materialized_view block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#materialized_view BigqueryTable#materialized_view}
        '''
        result = self._values.get("materialized_view")
        return typing.cast(typing.Optional["BigqueryTableMaterializedView"], result)

    @builtins.property
    def max_staleness(self) -> typing.Optional[builtins.str]:
        '''The maximum staleness of data that could be returned when the table (or stale MV) is queried.

        Staleness encoded as a string encoding of `SQL IntervalValue type <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#interval_type>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#max_staleness BigqueryTable#max_staleness}
        '''
        result = self._values.get("max_staleness")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#project BigqueryTable#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_partitioning(self) -> typing.Optional["BigqueryTableRangePartitioning"]:
        '''range_partitioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range_partitioning BigqueryTable#range_partitioning}
        '''
        result = self._values.get("range_partitioning")
        return typing.cast(typing.Optional["BigqueryTableRangePartitioning"], result)

    @builtins.property
    def require_partition_filter(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        result = self._values.get("require_partition_filter")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags attached to this table.

        Tag keys are globally unique. Tag key is expected to be in the namespaced format, for example "123456789012/environment" where 123456789012 is the ID of the parent organization or project resource for this tag key. Tag value is expected to be the short name, for example "Production".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#resource_tags BigqueryTable#resource_tags}
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema BigqueryTable#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_foreign_type_info(
        self,
    ) -> typing.Optional["BigqueryTableSchemaForeignTypeInfo"]:
        '''schema_foreign_type_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema_foreign_type_info BigqueryTable#schema_foreign_type_info}
        '''
        result = self._values.get("schema_foreign_type_info")
        return typing.cast(typing.Optional["BigqueryTableSchemaForeignTypeInfo"], result)

    @builtins.property
    def table_constraints(self) -> typing.Optional["BigqueryTableTableConstraints"]:
        '''table_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_constraints BigqueryTable#table_constraints}
        '''
        result = self._values.get("table_constraints")
        return typing.cast(typing.Optional["BigqueryTableTableConstraints"], result)

    @builtins.property
    def table_metadata_view(self) -> typing.Optional[builtins.str]:
        '''View sets the optional parameter "view": Specifies the view that determines which table information is returned.

        By default, basic table information and storage statistics (STORAGE_STATS) are returned. Possible values: TABLE_METADATA_VIEW_UNSPECIFIED, BASIC, STORAGE_STATS, FULL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_metadata_view BigqueryTable#table_metadata_view}
        '''
        result = self._values.get("table_metadata_view")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_replication_info(
        self,
    ) -> typing.Optional["BigqueryTableTableReplicationInfo"]:
        '''table_replication_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_replication_info BigqueryTable#table_replication_info}
        '''
        result = self._values.get("table_replication_info")
        return typing.cast(typing.Optional["BigqueryTableTableReplicationInfo"], result)

    @builtins.property
    def time_partitioning(self) -> typing.Optional["BigqueryTableTimePartitioning"]:
        '''time_partitioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#time_partitioning BigqueryTable#time_partitioning}
        '''
        result = self._values.get("time_partitioning")
        return typing.cast(typing.Optional["BigqueryTableTimePartitioning"], result)

    @builtins.property
    def view(self) -> typing.Optional["BigqueryTableView"]:
        '''view block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#view BigqueryTable#view}
        '''
        result = self._values.get("view")
        return typing.cast(typing.Optional["BigqueryTableView"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class BigqueryTableEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The self link or full name of a key which should be used to encrypt this table. Note that the default bigquery service account will need to have encrypt/decrypt permissions on this key - you may want to see the google_bigquery_default_service_account datasource and the google_kms_crypto_key_iam_binding resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#kms_key_name BigqueryTable#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b602152e3492b2b9cf562d37b34e16cd46fcdd5aebb8344fde8383837c318d)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The self link or full name of a key which should be used to encrypt this table.

        Note that the default bigquery service account will need to have encrypt/decrypt permissions on this key - you may want to see the google_bigquery_default_service_account datasource and the google_kms_crypto_key_iam_binding resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#kms_key_name BigqueryTable#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af10cc39b5f5ba6eded054f31ffbd4706d4231d04b57aedc127bf4e576f255b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyVersion")
    def kms_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyVersion"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159555baf2bda86fb2b1cb4f203eb8889cd2ec3395162f7d34f6b3bf4bdb405a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableEncryptionConfiguration]:
        return typing.cast(typing.Optional[BigqueryTableEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fca302717ac54bb59f5552189434c71d9bec42d7b2a28bf6430bf5e7c4f8c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalCatalogTableOptions",
    jsii_struct_bases=[],
    name_mapping={
        "connection_id": "connectionId",
        "parameters": "parameters",
        "storage_descriptor": "storageDescriptor",
    },
)
class BigqueryTableExternalCatalogTableOptions:
    def __init__(
        self,
        *,
        connection_id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_descriptor: typing.Optional[typing.Union["BigqueryTableExternalCatalogTableOptionsStorageDescriptor", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection_id: The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3. The connection is needed to read the open source table from BigQuery Engine. The connection_id can have the form <project_id>.<location_id>.<connection_id> or projects/<project_id>/locations/<location_id>/connections/<connection_id>. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        :param parameters: A map of key value pairs defining the parameters and properties of the open source table. Corresponds with hive meta store table parameters. Maximum size of 4Mib. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parameters BigqueryTable#parameters}
        :param storage_descriptor: storage_descriptor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#storage_descriptor BigqueryTable#storage_descriptor}
        '''
        if isinstance(storage_descriptor, dict):
            storage_descriptor = BigqueryTableExternalCatalogTableOptionsStorageDescriptor(**storage_descriptor)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b0e3afe094e8b99db0d67fb8396e0f1b4b708c334fc80353487a3c8d980b11)
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument storage_descriptor", value=storage_descriptor, expected_type=type_hints["storage_descriptor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if parameters is not None:
            self._values["parameters"] = parameters
        if storage_descriptor is not None:
            self._values["storage_descriptor"] = storage_descriptor

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3.

        The connection is needed to read the open source table from BigQuery Engine. The connection_id can have the form <project_id>.<location_id>.<connection_id> or projects/<project_id>/locations/<location_id>/connections/<connection_id>.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key value pairs defining the parameters and properties of the open source table.

        Corresponds with hive meta store table parameters. Maximum size of 4Mib.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parameters BigqueryTable#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def storage_descriptor(
        self,
    ) -> typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptor"]:
        '''storage_descriptor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#storage_descriptor BigqueryTable#storage_descriptor}
        '''
        result = self._values.get("storage_descriptor")
        return typing.cast(typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptor"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalCatalogTableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalCatalogTableOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalCatalogTableOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aff7d282da9c093166083df1ab1763a234a96fbb4b6847a5747c6a741e74cb6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStorageDescriptor")
    def put_storage_descriptor(
        self,
        *,
        input_format: typing.Optional[builtins.str] = None,
        location_uri: typing.Optional[builtins.str] = None,
        output_format: typing.Optional[builtins.str] = None,
        serde_info: typing.Optional[typing.Union["BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param input_format: Specifies the fully qualified class name of the InputFormat (e.g. "org.apache.hadoop.hive.ql.io.orc.OrcInputFormat"). The maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#input_format BigqueryTable#input_format}
        :param location_uri: The physical location of the table (e.g. 'gs://spark-dataproc-data/pangea-data/case_sensitive/' or 'gs://spark-dataproc-data/pangea-data/*'). The maximum length is 2056 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#location_uri BigqueryTable#location_uri}
        :param output_format: Specifies the fully qualified class name of the OutputFormat (e.g. "org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat"). The maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#output_format BigqueryTable#output_format}
        :param serde_info: serde_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#serde_info BigqueryTable#serde_info}
        '''
        value = BigqueryTableExternalCatalogTableOptionsStorageDescriptor(
            input_format=input_format,
            location_uri=location_uri,
            output_format=output_format,
            serde_info=serde_info,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageDescriptor", [value]))

    @jsii.member(jsii_name="resetConnectionId")
    def reset_connection_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionId", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetStorageDescriptor")
    def reset_storage_descriptor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageDescriptor", []))

    @builtins.property
    @jsii.member(jsii_name="storageDescriptor")
    def storage_descriptor(
        self,
    ) -> "BigqueryTableExternalCatalogTableOptionsStorageDescriptorOutputReference":
        return typing.cast("BigqueryTableExternalCatalogTableOptionsStorageDescriptorOutputReference", jsii.get(self, "storageDescriptor"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="storageDescriptorInput")
    def storage_descriptor_input(
        self,
    ) -> typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptor"]:
        return typing.cast(typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptor"], jsii.get(self, "storageDescriptorInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afac7e00b4f26e85d005cc14449a8c185ddc1b092cb275fc68b95cd6fd63dd7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4911693fc40ac447b03a5fe76a98dfff32fb98a28671e9b2464e86be482652c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalCatalogTableOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalCatalogTableOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalCatalogTableOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e3215e90124bb7b0e2fe9e387bccb6b1c48f83d8d4e752676433a3cb9a118a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalCatalogTableOptionsStorageDescriptor",
    jsii_struct_bases=[],
    name_mapping={
        "input_format": "inputFormat",
        "location_uri": "locationUri",
        "output_format": "outputFormat",
        "serde_info": "serdeInfo",
    },
)
class BigqueryTableExternalCatalogTableOptionsStorageDescriptor:
    def __init__(
        self,
        *,
        input_format: typing.Optional[builtins.str] = None,
        location_uri: typing.Optional[builtins.str] = None,
        output_format: typing.Optional[builtins.str] = None,
        serde_info: typing.Optional[typing.Union["BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param input_format: Specifies the fully qualified class name of the InputFormat (e.g. "org.apache.hadoop.hive.ql.io.orc.OrcInputFormat"). The maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#input_format BigqueryTable#input_format}
        :param location_uri: The physical location of the table (e.g. 'gs://spark-dataproc-data/pangea-data/case_sensitive/' or 'gs://spark-dataproc-data/pangea-data/*'). The maximum length is 2056 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#location_uri BigqueryTable#location_uri}
        :param output_format: Specifies the fully qualified class name of the OutputFormat (e.g. "org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat"). The maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#output_format BigqueryTable#output_format}
        :param serde_info: serde_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#serde_info BigqueryTable#serde_info}
        '''
        if isinstance(serde_info, dict):
            serde_info = BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo(**serde_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920b87282493d65c1c922bb25140bfa1bb7dc93a2b901231d76e1256d1d18228)
            check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
            check_type(argname="argument location_uri", value=location_uri, expected_type=type_hints["location_uri"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument serde_info", value=serde_info, expected_type=type_hints["serde_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_format is not None:
            self._values["input_format"] = input_format
        if location_uri is not None:
            self._values["location_uri"] = location_uri
        if output_format is not None:
            self._values["output_format"] = output_format
        if serde_info is not None:
            self._values["serde_info"] = serde_info

    @builtins.property
    def input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the fully qualified class name of the InputFormat (e.g. "org.apache.hadoop.hive.ql.io.orc.OrcInputFormat"). The maximum length is 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#input_format BigqueryTable#input_format}
        '''
        result = self._values.get("input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_uri(self) -> typing.Optional[builtins.str]:
        '''The physical location of the table (e.g. 'gs://spark-dataproc-data/pangea-data/case_sensitive/' or 'gs://spark-dataproc-data/pangea-data/*'). The maximum length is 2056 bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#location_uri BigqueryTable#location_uri}
        '''
        result = self._values.get("location_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the fully qualified class name of the OutputFormat (e.g. "org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat"). The maximum length is 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#output_format BigqueryTable#output_format}
        '''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serde_info(
        self,
    ) -> typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo"]:
        '''serde_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#serde_info BigqueryTable#serde_info}
        '''
        result = self._values.get("serde_info")
        return typing.cast(typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalCatalogTableOptionsStorageDescriptor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalCatalogTableOptionsStorageDescriptorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalCatalogTableOptionsStorageDescriptorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ee992d881595b02d854c0be415c3e2f869b1519856351129a2bfa4355ea92c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSerdeInfo")
    def put_serde_info(
        self,
        *,
        serialization_library: builtins.str,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param serialization_library: Specifies a fully-qualified class name of the serialization library that is responsible for the translation of data between table representation and the underlying low-level input and output format structures. The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#serialization_library BigqueryTable#serialization_library}
        :param name: Name of the SerDe. The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#name BigqueryTable#name}
        :param parameters: Key-value pairs that define the initialization parameters for the serialization library. Maximum size 10 Kib. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parameters BigqueryTable#parameters}
        '''
        value = BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo(
            serialization_library=serialization_library,
            name=name,
            parameters=parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putSerdeInfo", [value]))

    @jsii.member(jsii_name="resetInputFormat")
    def reset_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputFormat", []))

    @jsii.member(jsii_name="resetLocationUri")
    def reset_location_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationUri", []))

    @jsii.member(jsii_name="resetOutputFormat")
    def reset_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFormat", []))

    @jsii.member(jsii_name="resetSerdeInfo")
    def reset_serde_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerdeInfo", []))

    @builtins.property
    @jsii.member(jsii_name="serdeInfo")
    def serde_info(
        self,
    ) -> "BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfoOutputReference":
        return typing.cast("BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfoOutputReference", jsii.get(self, "serdeInfo"))

    @builtins.property
    @jsii.member(jsii_name="inputFormatInput")
    def input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="locationUriInput")
    def location_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationUriInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFormatInput")
    def output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="serdeInfoInput")
    def serde_info_input(
        self,
    ) -> typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo"]:
        return typing.cast(typing.Optional["BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo"], jsii.get(self, "serdeInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="inputFormat")
    def input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputFormat"))

    @input_format.setter
    def input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ad8698af7da0e26a568ae6c52ae4f6303a00bebf61e90a4f8d4045b2e90d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationUri"))

    @location_uri.setter
    def location_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2237726f998dbb574c43b22493f4c4fec065db28ff403fce6ef7fb421dea7d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93964b4c2276115b4fd364d73d8e84b87cb959fe5adb8758bf5900ebd04aaa5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptor]:
        return typing.cast(typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134a34a850a6cec544046568009519f9508f1f6d14ad6b39b6c9706ee20448c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo",
    jsii_struct_bases=[],
    name_mapping={
        "serialization_library": "serializationLibrary",
        "name": "name",
        "parameters": "parameters",
    },
)
class BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo:
    def __init__(
        self,
        *,
        serialization_library: builtins.str,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param serialization_library: Specifies a fully-qualified class name of the serialization library that is responsible for the translation of data between table representation and the underlying low-level input and output format structures. The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#serialization_library BigqueryTable#serialization_library}
        :param name: Name of the SerDe. The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#name BigqueryTable#name}
        :param parameters: Key-value pairs that define the initialization parameters for the serialization library. Maximum size 10 Kib. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parameters BigqueryTable#parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4886efe8b4a4296e9c7e29778779a2593d55d95f6f98ac90dbc48ccb7c10443e)
            check_type(argname="argument serialization_library", value=serialization_library, expected_type=type_hints["serialization_library"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "serialization_library": serialization_library,
        }
        if name is not None:
            self._values["name"] = name
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def serialization_library(self) -> builtins.str:
        '''Specifies a fully-qualified class name of the serialization library that is responsible for the translation of data between table representation and the underlying low-level input and output format structures.

        The maximum length is 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#serialization_library BigqueryTable#serialization_library}
        '''
        result = self._values.get("serialization_library")
        assert result is not None, "Required property 'serialization_library' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the SerDe. The maximum length is 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#name BigqueryTable#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs that define the initialization parameters for the serialization library. Maximum size 10 Kib.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parameters BigqueryTable#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1931f62454ceb27c66621bd9d2b6f42011781cd36fe19c5c1b6c597b6772050)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="serializationLibraryInput")
    def serialization_library_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serializationLibraryInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2976fd59ea71494a4c0b092a9c55986498d7c421a9d55b859ba768138eacc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2424fe3f5e0e6aef2d07dbc581c92457f2c2a44da8d22d2ae929817b757104c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serializationLibrary")
    def serialization_library(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serializationLibrary"))

    @serialization_library.setter
    def serialization_library(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d65a3b21682b815457483059f3fde4b4c9434deef165adb0faf88be5c521ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serializationLibrary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo]:
        return typing.cast(typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90e677f5d706ef832e2cad3ba694971fc877415fc30730861bac752b80dc693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "autodetect": "autodetect",
        "source_uris": "sourceUris",
        "avro_options": "avroOptions",
        "bigtable_options": "bigtableOptions",
        "compression": "compression",
        "connection_id": "connectionId",
        "csv_options": "csvOptions",
        "file_set_spec_type": "fileSetSpecType",
        "google_sheets_options": "googleSheetsOptions",
        "hive_partitioning_options": "hivePartitioningOptions",
        "ignore_unknown_values": "ignoreUnknownValues",
        "json_extension": "jsonExtension",
        "json_options": "jsonOptions",
        "max_bad_records": "maxBadRecords",
        "metadata_cache_mode": "metadataCacheMode",
        "object_metadata": "objectMetadata",
        "parquet_options": "parquetOptions",
        "reference_file_schema_uri": "referenceFileSchemaUri",
        "schema": "schema",
        "source_format": "sourceFormat",
    },
)
class BigqueryTableExternalDataConfiguration:
    def __init__(
        self,
        *,
        autodetect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        source_uris: typing.Sequence[builtins.str],
        avro_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationAvroOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        bigtable_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationBigtableOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression: typing.Optional[builtins.str] = None,
        connection_id: typing.Optional[builtins.str] = None,
        csv_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        file_set_spec_type: typing.Optional[builtins.str] = None,
        google_sheets_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationGoogleSheetsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_partitioning_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationHivePartitioningOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_extension: typing.Optional[builtins.str] = None,
        json_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        max_bad_records: typing.Optional[jsii.Number] = None,
        metadata_cache_mode: typing.Optional[builtins.str] = None,
        object_metadata: typing.Optional[builtins.str] = None,
        parquet_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        reference_file_schema_uri: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autodetect: Let BigQuery try to autodetect the schema and format of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#autodetect BigqueryTable#autodetect}
        :param source_uris: A list of the fully-qualified URIs that point to your data in Google Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_uris BigqueryTable#source_uris}
        :param avro_options: avro_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#avro_options BigqueryTable#avro_options}
        :param bigtable_options: bigtable_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#bigtable_options BigqueryTable#bigtable_options}
        :param compression: The compression type of the data source. Valid values are "NONE" or "GZIP". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#compression BigqueryTable#compression}
        :param connection_id: The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3. The connectionId can have the form "..<connection_id>" or "projects//locations//connections/<connection_id>". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#csv_options BigqueryTable#csv_options}
        :param file_set_spec_type: Specifies how source URIs are interpreted for constructing the file set to load. By default source URIs are expanded against the underlying storage. Other options include specifying manifest files. Only applicable to object storage systems. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#file_set_spec_type BigqueryTable#file_set_spec_type}
        :param google_sheets_options: google_sheets_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#google_sheets_options BigqueryTable#google_sheets_options}
        :param hive_partitioning_options: hive_partitioning_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#hive_partitioning_options BigqueryTable#hive_partitioning_options}
        :param ignore_unknown_values: Indicates if BigQuery should allow extra values that are not represented in the table schema. If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_unknown_values BigqueryTable#ignore_unknown_values}
        :param json_extension: Load option to be used together with sourceFormat newline-delimited JSON to indicate that a variant of JSON is being loaded. To load newline-delimited GeoJSON, specify GEOJSON (and sourceFormat must be set to NEWLINE_DELIMITED_JSON). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#json_extension BigqueryTable#json_extension}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#json_options BigqueryTable#json_options}
        :param max_bad_records: The maximum number of bad records that BigQuery can ignore when reading data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#max_bad_records BigqueryTable#max_bad_records}
        :param metadata_cache_mode: Metadata Cache Mode for the table. Set this to enable caching of metadata from external data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#metadata_cache_mode BigqueryTable#metadata_cache_mode}
        :param object_metadata: Object Metadata is used to create Object Tables. Object Tables contain a listing of objects (with their metadata) found at the sourceUris. If ObjectMetadata is set, sourceFormat should be omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#object_metadata BigqueryTable#object_metadata}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parquet_options BigqueryTable#parquet_options}
        :param reference_file_schema_uri: When creating an external table, the user can provide a reference file with the table schema. This is enabled for the following formats: AVRO, PARQUET, ORC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#reference_file_schema_uri BigqueryTable#reference_file_schema_uri}
        :param schema: A JSON schema for the external table. Schema is required for CSV and JSON formats and is disallowed for Google Cloud Bigtable, Cloud Datastore backups, and Avro formats when using external tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema BigqueryTable#schema}
        :param source_format: Please see sourceFormat under ExternalDataConfiguration in Bigquery's public API documentation (https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externaldataconfiguration) for supported formats. To use "GOOGLE_SHEETS" the scopes must include "googleapis.com/auth/drive.readonly". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_format BigqueryTable#source_format}
        '''
        if isinstance(avro_options, dict):
            avro_options = BigqueryTableExternalDataConfigurationAvroOptions(**avro_options)
        if isinstance(bigtable_options, dict):
            bigtable_options = BigqueryTableExternalDataConfigurationBigtableOptions(**bigtable_options)
        if isinstance(csv_options, dict):
            csv_options = BigqueryTableExternalDataConfigurationCsvOptions(**csv_options)
        if isinstance(google_sheets_options, dict):
            google_sheets_options = BigqueryTableExternalDataConfigurationGoogleSheetsOptions(**google_sheets_options)
        if isinstance(hive_partitioning_options, dict):
            hive_partitioning_options = BigqueryTableExternalDataConfigurationHivePartitioningOptions(**hive_partitioning_options)
        if isinstance(json_options, dict):
            json_options = BigqueryTableExternalDataConfigurationJsonOptions(**json_options)
        if isinstance(parquet_options, dict):
            parquet_options = BigqueryTableExternalDataConfigurationParquetOptions(**parquet_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c60ab8fdd68e02c385fb19a744285eb35baeda52e37f6cea6837e2b0f015c1)
            check_type(argname="argument autodetect", value=autodetect, expected_type=type_hints["autodetect"])
            check_type(argname="argument source_uris", value=source_uris, expected_type=type_hints["source_uris"])
            check_type(argname="argument avro_options", value=avro_options, expected_type=type_hints["avro_options"])
            check_type(argname="argument bigtable_options", value=bigtable_options, expected_type=type_hints["bigtable_options"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument csv_options", value=csv_options, expected_type=type_hints["csv_options"])
            check_type(argname="argument file_set_spec_type", value=file_set_spec_type, expected_type=type_hints["file_set_spec_type"])
            check_type(argname="argument google_sheets_options", value=google_sheets_options, expected_type=type_hints["google_sheets_options"])
            check_type(argname="argument hive_partitioning_options", value=hive_partitioning_options, expected_type=type_hints["hive_partitioning_options"])
            check_type(argname="argument ignore_unknown_values", value=ignore_unknown_values, expected_type=type_hints["ignore_unknown_values"])
            check_type(argname="argument json_extension", value=json_extension, expected_type=type_hints["json_extension"])
            check_type(argname="argument json_options", value=json_options, expected_type=type_hints["json_options"])
            check_type(argname="argument max_bad_records", value=max_bad_records, expected_type=type_hints["max_bad_records"])
            check_type(argname="argument metadata_cache_mode", value=metadata_cache_mode, expected_type=type_hints["metadata_cache_mode"])
            check_type(argname="argument object_metadata", value=object_metadata, expected_type=type_hints["object_metadata"])
            check_type(argname="argument parquet_options", value=parquet_options, expected_type=type_hints["parquet_options"])
            check_type(argname="argument reference_file_schema_uri", value=reference_file_schema_uri, expected_type=type_hints["reference_file_schema_uri"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autodetect": autodetect,
            "source_uris": source_uris,
        }
        if avro_options is not None:
            self._values["avro_options"] = avro_options
        if bigtable_options is not None:
            self._values["bigtable_options"] = bigtable_options
        if compression is not None:
            self._values["compression"] = compression
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if csv_options is not None:
            self._values["csv_options"] = csv_options
        if file_set_spec_type is not None:
            self._values["file_set_spec_type"] = file_set_spec_type
        if google_sheets_options is not None:
            self._values["google_sheets_options"] = google_sheets_options
        if hive_partitioning_options is not None:
            self._values["hive_partitioning_options"] = hive_partitioning_options
        if ignore_unknown_values is not None:
            self._values["ignore_unknown_values"] = ignore_unknown_values
        if json_extension is not None:
            self._values["json_extension"] = json_extension
        if json_options is not None:
            self._values["json_options"] = json_options
        if max_bad_records is not None:
            self._values["max_bad_records"] = max_bad_records
        if metadata_cache_mode is not None:
            self._values["metadata_cache_mode"] = metadata_cache_mode
        if object_metadata is not None:
            self._values["object_metadata"] = object_metadata
        if parquet_options is not None:
            self._values["parquet_options"] = parquet_options
        if reference_file_schema_uri is not None:
            self._values["reference_file_schema_uri"] = reference_file_schema_uri
        if schema is not None:
            self._values["schema"] = schema
        if source_format is not None:
            self._values["source_format"] = source_format

    @builtins.property
    def autodetect(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Let BigQuery try to autodetect the schema and format of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#autodetect BigqueryTable#autodetect}
        '''
        result = self._values.get("autodetect")
        assert result is not None, "Required property 'autodetect' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def source_uris(self) -> typing.List[builtins.str]:
        '''A list of the fully-qualified URIs that point to your data in Google Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_uris BigqueryTable#source_uris}
        '''
        result = self._values.get("source_uris")
        assert result is not None, "Required property 'source_uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def avro_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationAvroOptions"]:
        '''avro_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#avro_options BigqueryTable#avro_options}
        '''
        result = self._values.get("avro_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationAvroOptions"], result)

    @builtins.property
    def bigtable_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationBigtableOptions"]:
        '''bigtable_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#bigtable_options BigqueryTable#bigtable_options}
        '''
        result = self._values.get("bigtable_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationBigtableOptions"], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''The compression type of the data source. Valid values are "NONE" or "GZIP".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#compression BigqueryTable#compression}
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3.

        The connectionId can have the form "..<connection_id>" or "projects//locations//connections/<connection_id>".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#connection_id BigqueryTable#connection_id}
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationCsvOptions"]:
        '''csv_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#csv_options BigqueryTable#csv_options}
        '''
        result = self._values.get("csv_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationCsvOptions"], result)

    @builtins.property
    def file_set_spec_type(self) -> typing.Optional[builtins.str]:
        '''Specifies how source URIs are interpreted for constructing the file set to load.

        By default source URIs are expanded against the underlying storage.  Other options include specifying manifest files. Only applicable to object storage systems.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#file_set_spec_type BigqueryTable#file_set_spec_type}
        '''
        result = self._values.get("file_set_spec_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def google_sheets_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationGoogleSheetsOptions"]:
        '''google_sheets_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#google_sheets_options BigqueryTable#google_sheets_options}
        '''
        result = self._values.get("google_sheets_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationGoogleSheetsOptions"], result)

    @builtins.property
    def hive_partitioning_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationHivePartitioningOptions"]:
        '''hive_partitioning_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#hive_partitioning_options BigqueryTable#hive_partitioning_options}
        '''
        result = self._values.get("hive_partitioning_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationHivePartitioningOptions"], result)

    @builtins.property
    def ignore_unknown_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should allow extra values that are not represented in the table schema.

        If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_unknown_values BigqueryTable#ignore_unknown_values}
        '''
        result = self._values.get("ignore_unknown_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def json_extension(self) -> typing.Optional[builtins.str]:
        '''Load option to be used together with sourceFormat newline-delimited JSON to indicate that a variant of JSON is being loaded.

        To load newline-delimited GeoJSON, specify GEOJSON (and sourceFormat must be set to NEWLINE_DELIMITED_JSON).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#json_extension BigqueryTable#json_extension}
        '''
        result = self._values.get("json_extension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def json_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationJsonOptions"]:
        '''json_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#json_options BigqueryTable#json_options}
        '''
        result = self._values.get("json_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationJsonOptions"], result)

    @builtins.property
    def max_bad_records(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of bad records that BigQuery can ignore when reading data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#max_bad_records BigqueryTable#max_bad_records}
        '''
        result = self._values.get("max_bad_records")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata_cache_mode(self) -> typing.Optional[builtins.str]:
        '''Metadata Cache Mode for the table. Set this to enable caching of metadata from external data source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#metadata_cache_mode BigqueryTable#metadata_cache_mode}
        '''
        result = self._values.get("metadata_cache_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_metadata(self) -> typing.Optional[builtins.str]:
        '''Object Metadata is used to create Object Tables.

        Object Tables contain a listing of objects (with their metadata) found at the sourceUris. If ObjectMetadata is set, sourceFormat should be omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#object_metadata BigqueryTable#object_metadata}
        '''
        result = self._values.get("object_metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parquet_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationParquetOptions"]:
        '''parquet_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#parquet_options BigqueryTable#parquet_options}
        '''
        result = self._values.get("parquet_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationParquetOptions"], result)

    @builtins.property
    def reference_file_schema_uri(self) -> typing.Optional[builtins.str]:
        '''When creating an external table, the user can provide a reference file with the table schema.

        This is enabled for the following formats: AVRO, PARQUET, ORC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#reference_file_schema_uri BigqueryTable#reference_file_schema_uri}
        '''
        result = self._values.get("reference_file_schema_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the external table.

        Schema is required for CSV and JSON formats and is disallowed for Google Cloud Bigtable, Cloud Datastore backups, and Avro formats when using external tables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#schema BigqueryTable#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''Please see sourceFormat under ExternalDataConfiguration in Bigquery's public API documentation (https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externaldataconfiguration) for supported formats. To use "GOOGLE_SHEETS" the scopes must include "googleapis.com/auth/drive.readonly".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_format BigqueryTable#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationAvroOptions",
    jsii_struct_bases=[],
    name_mapping={"use_avro_logical_types": "useAvroLogicalTypes"},
)
class BigqueryTableExternalDataConfigurationAvroOptions:
    def __init__(
        self,
        *,
        use_avro_logical_types: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param use_avro_logical_types: If sourceFormat is set to "AVRO", indicates whether to interpret logical types as the corresponding BigQuery data type (for example, TIMESTAMP), instead of using the raw type (for example, INTEGER). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#use_avro_logical_types BigqueryTable#use_avro_logical_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020a0a10768b90ca49555c5e7a89b9faabb072bc6d5bf986be581e51358bb59e)
            check_type(argname="argument use_avro_logical_types", value=use_avro_logical_types, expected_type=type_hints["use_avro_logical_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "use_avro_logical_types": use_avro_logical_types,
        }

    @builtins.property
    def use_avro_logical_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If sourceFormat is set to "AVRO", indicates whether to interpret logical types as the corresponding BigQuery data type (for example, TIMESTAMP), instead of using the raw type (for example, INTEGER).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#use_avro_logical_types BigqueryTable#use_avro_logical_types}
        '''
        result = self._values.get("use_avro_logical_types")
        assert result is not None, "Required property 'use_avro_logical_types' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationAvroOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationAvroOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationAvroOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9fd5bb8fb0dfbc052fe96da13cf662d0ad0a733594bb360e47c8249fcf45082)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="useAvroLogicalTypesInput")
    def use_avro_logical_types_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useAvroLogicalTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="useAvroLogicalTypes")
    def use_avro_logical_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useAvroLogicalTypes"))

    @use_avro_logical_types.setter
    def use_avro_logical_types(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be785777b38b52889c2672086fa4df78e5b5176f5807463eaa63b17717b5921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAvroLogicalTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fcc8f040d82e48ec6840d2bc03598108e4065f5975b2f5eee455518f4ece75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptions",
    jsii_struct_bases=[],
    name_mapping={
        "column_family": "columnFamily",
        "ignore_unspecified_column_families": "ignoreUnspecifiedColumnFamilies",
        "output_column_families_as_json": "outputColumnFamiliesAsJson",
        "read_rowkey_as_string": "readRowkeyAsString",
    },
)
class BigqueryTableExternalDataConfigurationBigtableOptions:
    def __init__(
        self,
        *,
        column_family: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ignore_unspecified_column_families: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_column_families_as_json: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_rowkey_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param column_family: column_family block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#column_family BigqueryTable#column_family}
        :param ignore_unspecified_column_families: If field is true, then the column families that are not specified in columnFamilies list are not exposed in the table schema. Otherwise, they are read with BYTES type values. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_unspecified_column_families BigqueryTable#ignore_unspecified_column_families}
        :param output_column_families_as_json: If field is true, then each column family will be read as a single JSON column. Otherwise they are read as a repeated cell structure containing timestamp/value tuples. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#output_column_families_as_json BigqueryTable#output_column_families_as_json}
        :param read_rowkey_as_string: If field is true, then the rowkey column families will be read and converted to string. Otherwise they are read with BYTES type values and users need to manually cast them with CAST if necessary. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#read_rowkey_as_string BigqueryTable#read_rowkey_as_string}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7334e17337fa62ad6afad6315e2f65b99f922fdfacc1ee639d8141db00027780)
            check_type(argname="argument column_family", value=column_family, expected_type=type_hints["column_family"])
            check_type(argname="argument ignore_unspecified_column_families", value=ignore_unspecified_column_families, expected_type=type_hints["ignore_unspecified_column_families"])
            check_type(argname="argument output_column_families_as_json", value=output_column_families_as_json, expected_type=type_hints["output_column_families_as_json"])
            check_type(argname="argument read_rowkey_as_string", value=read_rowkey_as_string, expected_type=type_hints["read_rowkey_as_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column_family is not None:
            self._values["column_family"] = column_family
        if ignore_unspecified_column_families is not None:
            self._values["ignore_unspecified_column_families"] = ignore_unspecified_column_families
        if output_column_families_as_json is not None:
            self._values["output_column_families_as_json"] = output_column_families_as_json
        if read_rowkey_as_string is not None:
            self._values["read_rowkey_as_string"] = read_rowkey_as_string

    @builtins.property
    def column_family(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily"]]]:
        '''column_family block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#column_family BigqueryTable#column_family}
        '''
        result = self._values.get("column_family")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily"]]], result)

    @builtins.property
    def ignore_unspecified_column_families(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If field is true, then the column families that are not specified in columnFamilies list are not exposed in the table schema.

        Otherwise, they are read with BYTES type values. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_unspecified_column_families BigqueryTable#ignore_unspecified_column_families}
        '''
        result = self._values.get("ignore_unspecified_column_families")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def output_column_families_as_json(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If field is true, then each column family will be read as a single JSON column.

        Otherwise they are read as a repeated cell structure containing timestamp/value tuples. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#output_column_families_as_json BigqueryTable#output_column_families_as_json}
        '''
        result = self._values.get("output_column_families_as_json")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def read_rowkey_as_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If field is true, then the rowkey column families will be read and converted to string.

        Otherwise they are read with BYTES type values and users need to manually cast them with CAST if necessary. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#read_rowkey_as_string BigqueryTable#read_rowkey_as_string}
        '''
        result = self._values.get("read_rowkey_as_string")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationBigtableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "encoding": "encoding",
        "family_id": "familyId",
        "only_read_latest": "onlyReadLatest",
        "type": "type",
    },
)
class BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily:
    def __init__(
        self,
        *,
        column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encoding: typing.Optional[builtins.str] = None,
        family_id: typing.Optional[builtins.str] = None,
        only_read_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#column BigqueryTable#column}
        :param encoding: The encoding of the values when the type is not STRING. Acceptable encoding values are: TEXT - indicates values are alphanumeric text strings. BINARY - indicates values are encoded using HBase Bytes.toBytes family of functions. This can be overridden for a specific column by listing that column in 'columns' and specifying an encoding for it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        :param family_id: Identifier of the column family. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#family_id BigqueryTable#family_id}
        :param only_read_latest: If this is set only the latest version of value are exposed for all columns in this column family. This can be overridden for a specific column by listing that column in 'columns' and specifying a different setting for that column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#only_read_latest BigqueryTable#only_read_latest}
        :param type: The type to convert the value in cells of this column family. The values are expected to be encoded using HBase Bytes.toBytes function when using the BINARY encoding value. Following BigQuery types are allowed (case-sensitive): "BYTES", "STRING", "INTEGER", "FLOAT", "BOOLEAN", "JSON". Default type is BYTES. This can be overridden for a specific column by listing that column in 'columns' and specifying a type for it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type BigqueryTable#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611f92f3c0b7a1b44ab7bf6517ffd7f5738de788ec8d6bfda2ee0a63e975a78c)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument family_id", value=family_id, expected_type=type_hints["family_id"])
            check_type(argname="argument only_read_latest", value=only_read_latest, expected_type=type_hints["only_read_latest"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column is not None:
            self._values["column"] = column
        if encoding is not None:
            self._values["encoding"] = encoding
        if family_id is not None:
            self._values["family_id"] = family_id
        if only_read_latest is not None:
            self._values["only_read_latest"] = only_read_latest
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def column(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn"]]]:
        '''column block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#column BigqueryTable#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn"]]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The encoding of the values when the type is not STRING.

        Acceptable encoding values are: TEXT - indicates values are alphanumeric text strings. BINARY - indicates values are encoded using HBase Bytes.toBytes family of functions. This can be overridden for a specific column by listing that column in 'columns' and specifying an encoding for it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def family_id(self) -> typing.Optional[builtins.str]:
        '''Identifier of the column family.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#family_id BigqueryTable#family_id}
        '''
        result = self._values.get("family_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def only_read_latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this is set only the latest version of value are exposed for all columns in this column family.

        This can be overridden for a specific column by listing that column in 'columns' and specifying a different setting for that column.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#only_read_latest BigqueryTable#only_read_latest}
        '''
        result = self._values.get("only_read_latest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type to convert the value in cells of this column family.

        The values are expected to be encoded using HBase Bytes.toBytes function when using the BINARY encoding value. Following BigQuery types are allowed (case-sensitive): "BYTES", "STRING", "INTEGER", "FLOAT", "BOOLEAN", "JSON". Default type is BYTES. This can be overridden for a specific column by listing that column in 'columns' and specifying a type for it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type BigqueryTable#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn",
    jsii_struct_bases=[],
    name_mapping={
        "encoding": "encoding",
        "field_name": "fieldName",
        "only_read_latest": "onlyReadLatest",
        "qualifier_encoded": "qualifierEncoded",
        "qualifier_string": "qualifierString",
        "type": "type",
    },
)
class BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn:
    def __init__(
        self,
        *,
        encoding: typing.Optional[builtins.str] = None,
        field_name: typing.Optional[builtins.str] = None,
        only_read_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        qualifier_encoded: typing.Optional[builtins.str] = None,
        qualifier_string: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encoding: The encoding of the values when the type is not STRING. Acceptable encoding values are: TEXT - indicates values are alphanumeric text strings. BINARY - indicates values are encoded using HBase Bytes.toBytes family of functions. 'encoding' can also be set at the column family level. However, the setting at this level takes precedence if 'encoding' is set at both levels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        :param field_name: If the qualifier is not a valid BigQuery field identifier i.e. does not match [a-zA-Z][a-zA-Z0-9_]*, a valid identifier must be provided as the column field name and is used as field name in queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field_name BigqueryTable#field_name}
        :param only_read_latest: If this is set, only the latest version of value in this column are exposed. 'onlyReadLatest' can also be set at the column family level. However, the setting at this level takes precedence if 'onlyReadLatest' is set at both levels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#only_read_latest BigqueryTable#only_read_latest}
        :param qualifier_encoded: Qualifier of the column. Columns in the parent column family that has this exact qualifier are exposed as . field. If the qualifier is valid UTF-8 string, it can be specified in the qualifierString field. Otherwise, a base-64 encoded value must be set to qualifierEncoded. The column field name is the same as the column qualifier. However, if the qualifier is not a valid BigQuery field identifier i.e. does not match [a-zA-Z][a-zA-Z0-9_]*, a valid identifier must be provided as fieldName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#qualifier_encoded BigqueryTable#qualifier_encoded}
        :param qualifier_string: Qualifier string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#qualifier_string BigqueryTable#qualifier_string}
        :param type: The type to convert the value in cells of this column. The values are expected to be encoded using HBase Bytes.toBytes function when using the BINARY encoding value. Following BigQuery types are allowed (case-sensitive): "BYTES", "STRING", "INTEGER", "FLOAT", "BOOLEAN", "JSON", Default type is "BYTES". 'type' can also be set at the column family level. However, the setting at this level takes precedence if 'type' is set at both levels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type BigqueryTable#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4b0982793fc5bb5ca68003758c0c10b36daba98208b4e87dedd3e52966db19)
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument only_read_latest", value=only_read_latest, expected_type=type_hints["only_read_latest"])
            check_type(argname="argument qualifier_encoded", value=qualifier_encoded, expected_type=type_hints["qualifier_encoded"])
            check_type(argname="argument qualifier_string", value=qualifier_string, expected_type=type_hints["qualifier_string"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encoding is not None:
            self._values["encoding"] = encoding
        if field_name is not None:
            self._values["field_name"] = field_name
        if only_read_latest is not None:
            self._values["only_read_latest"] = only_read_latest
        if qualifier_encoded is not None:
            self._values["qualifier_encoded"] = qualifier_encoded
        if qualifier_string is not None:
            self._values["qualifier_string"] = qualifier_string
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The encoding of the values when the type is not STRING.

        Acceptable encoding values are: TEXT - indicates values are alphanumeric text strings. BINARY - indicates values are encoded using HBase Bytes.toBytes family of functions. 'encoding' can also be set at the column family level. However, the setting at this level takes precedence if 'encoding' is set at both levels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_name(self) -> typing.Optional[builtins.str]:
        '''If the qualifier is not a valid BigQuery field identifier i.e. does not match [a-zA-Z][a-zA-Z0-9_]*, a valid identifier must be provided as the column field name and is used as field name in queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field_name BigqueryTable#field_name}
        '''
        result = self._values.get("field_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def only_read_latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this is set, only the latest version of value in this column are exposed.

        'onlyReadLatest' can also be set at the column family level. However, the setting at this level takes precedence if 'onlyReadLatest' is set at both levels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#only_read_latest BigqueryTable#only_read_latest}
        '''
        result = self._values.get("only_read_latest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def qualifier_encoded(self) -> typing.Optional[builtins.str]:
        '''Qualifier of the column.

        Columns in the parent column family that has this exact qualifier are exposed as . field. If the qualifier is valid UTF-8 string, it can be specified in the qualifierString field. Otherwise, a base-64 encoded value must be set to qualifierEncoded. The column field name is the same as the column qualifier. However, if the qualifier is not a valid BigQuery field identifier i.e. does not match [a-zA-Z][a-zA-Z0-9_]*, a valid identifier must be provided as fieldName.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#qualifier_encoded BigqueryTable#qualifier_encoded}
        '''
        result = self._values.get("qualifier_encoded")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qualifier_string(self) -> typing.Optional[builtins.str]:
        '''Qualifier string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#qualifier_string BigqueryTable#qualifier_string}
        '''
        result = self._values.get("qualifier_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type to convert the value in cells of this column.

        The values are expected to be encoded using HBase Bytes.toBytes function when using the BINARY encoding value. Following BigQuery types are allowed (case-sensitive): "BYTES", "STRING", "INTEGER", "FLOAT", "BOOLEAN", "JSON", Default type is "BYTES". 'type' can also be set at the column family level. However, the setting at this level takes precedence if 'type' is set at both levels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type BigqueryTable#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd4b3a7e80bf6653d05927e73e9db1706f3be3446bd09fee767de34a0cd95226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ceb23f7a9470e888c75c3b849c88acddc0ae33ca65604de0ce33ab62b5fd466)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9fa499b4fcbe5af9c8819f2535dc369e350419afca8bcbcb4a7e65cd9a47c05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab220eb0cdd216790a4e703dc5366bfa7e8af60fba8f7a26410270756e908861)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26de8a0b9c0bd866fd2674ed89ec532a9b76782f607ff21d1b5bbccbde2fe0e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109e0d5fe26759686fa7daf46093a8ca495afceb15589675f52d6e4056b84124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99d352f57c76b71511cfae9b9f7b17ae2677b6ea95583c7e863c4291cabf23cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetFieldName")
    def reset_field_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldName", []))

    @jsii.member(jsii_name="resetOnlyReadLatest")
    def reset_only_read_latest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyReadLatest", []))

    @jsii.member(jsii_name="resetQualifierEncoded")
    def reset_qualifier_encoded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQualifierEncoded", []))

    @jsii.member(jsii_name="resetQualifierString")
    def reset_qualifier_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQualifierString", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldNameInput")
    def field_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldNameInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyReadLatestInput")
    def only_read_latest_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyReadLatestInput"))

    @builtins.property
    @jsii.member(jsii_name="qualifierEncodedInput")
    def qualifier_encoded_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qualifierEncodedInput"))

    @builtins.property
    @jsii.member(jsii_name="qualifierStringInput")
    def qualifier_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qualifierStringInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368d216c6c5f35275232d6eef3e140338c6bfa3ff85ea6c8fce8c6a790117f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldName")
    def field_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldName"))

    @field_name.setter
    def field_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56ffdeb3280bd7156512b88cffecddac88731db092ae20dc7c2f2b70aec0211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyReadLatest")
    def only_read_latest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyReadLatest"))

    @only_read_latest.setter
    def only_read_latest(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399efea2fd63f12a0c8db58e974f99318b6bfc82c8721de96caef42135e34e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyReadLatest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qualifierEncoded")
    def qualifier_encoded(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qualifierEncoded"))

    @qualifier_encoded.setter
    def qualifier_encoded(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8f4ad5a87da983318fdafe4f7467adcbf602e0dc7dd01aff356ea2cdd71699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifierEncoded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qualifierString")
    def qualifier_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qualifierString"))

    @qualifier_string.setter
    def qualifier_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa7e6c4d58c7d1b39d275abea6ba64c4ce1453d18f648f9b5aeb55862c375d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifierString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431cd7b910e92659ceb3f80da9fe185d674d5ef12895e9778e7a3c787b7e2d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f84994a813138d1b8733925d81904b8c13eb1712f67d11a302ba7bfb473be3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb3cb703d3d685cd5e426341638ee3328420a1450f01ebf3c49ad8270c2871d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfe62a10624576c07c310e2b36b5fc8c3870cbd927348514fc90efbd2453bd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7110c41b66bb6e3f0385ab2bf13f55e729985f3dc5232b63c639fef6e291a86a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5848d4798f2d8ae4b99fe368ea27d0166d9d95cf638513c0d18c4b9c3755fbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e8e5f895b1d36628333cb2cf9b3925a393671a6c76d10a27e5165f0a5b1ccdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a175f1a9edc4f7fa90883e85d1f60bb9044d6a3708ecdb982bb92c40b1c6be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4402f369b45b17dbe24f5ef95c786d3716c80abe37168d84e5557dc34ec30067)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putColumn")
    def put_column(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca9c9b7e8603068c5ffaa8b0440eb396dc499a28263089df035beb1214af2db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumn", [value]))

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetFamilyId")
    def reset_family_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFamilyId", []))

    @jsii.member(jsii_name="resetOnlyReadLatest")
    def reset_only_read_latest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyReadLatest", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(
        self,
    ) -> BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnList:
        return typing.cast(BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnList, jsii.get(self, "column"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]]], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="familyIdInput")
    def family_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "familyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyReadLatestInput")
    def only_read_latest_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyReadLatestInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81144d7a754f069044508cc760ef844929ad769bdbdc9425dfbb3b390813d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="familyId")
    def family_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "familyId"))

    @family_id.setter
    def family_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce804c611c2d79dcb397ddad3870fbf4d438afccafd8dfdf24c24a581c06a510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "familyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyReadLatest")
    def only_read_latest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyReadLatest"))

    @only_read_latest.setter
    def only_read_latest(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1881b1771792f5afa7e07e18416bd32cad8d0a9c846e3390ac23926f27974f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyReadLatest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826a3155e4b15f225642e1a79c934a13ff9fa94b0ab6abd9c10c27ce59ae50b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac8abfca4365b5b9fbe395d433ef66f10130069c4261da3570bad256dabfe98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableExternalDataConfigurationBigtableOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationBigtableOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9d80810fce706dc5193a2da41a70396b30325588e504ff5c5d1eb52ea7f4dbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putColumnFamily")
    def put_column_family(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2de31968af73c7f388ebf3e27b0a0516fca03a3c61b63b92e41e7728eb2c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumnFamily", [value]))

    @jsii.member(jsii_name="resetColumnFamily")
    def reset_column_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnFamily", []))

    @jsii.member(jsii_name="resetIgnoreUnspecifiedColumnFamilies")
    def reset_ignore_unspecified_column_families(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreUnspecifiedColumnFamilies", []))

    @jsii.member(jsii_name="resetOutputColumnFamiliesAsJson")
    def reset_output_column_families_as_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputColumnFamiliesAsJson", []))

    @jsii.member(jsii_name="resetReadRowkeyAsString")
    def reset_read_rowkey_as_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadRowkeyAsString", []))

    @builtins.property
    @jsii.member(jsii_name="columnFamily")
    def column_family(
        self,
    ) -> BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyList:
        return typing.cast(BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyList, jsii.get(self, "columnFamily"))

    @builtins.property
    @jsii.member(jsii_name="columnFamilyInput")
    def column_family_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]]], jsii.get(self, "columnFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreUnspecifiedColumnFamiliesInput")
    def ignore_unspecified_column_families_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreUnspecifiedColumnFamiliesInput"))

    @builtins.property
    @jsii.member(jsii_name="outputColumnFamiliesAsJsonInput")
    def output_column_families_as_json_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outputColumnFamiliesAsJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="readRowkeyAsStringInput")
    def read_rowkey_as_string_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readRowkeyAsStringInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreUnspecifiedColumnFamilies")
    def ignore_unspecified_column_families(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreUnspecifiedColumnFamilies"))

    @ignore_unspecified_column_families.setter
    def ignore_unspecified_column_families(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece32edd05a4ce36393d56d4103415342e558e089d9e1197d55ac0fe00684c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreUnspecifiedColumnFamilies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputColumnFamiliesAsJson")
    def output_column_families_as_json(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outputColumnFamiliesAsJson"))

    @output_column_families_as_json.setter
    def output_column_families_as_json(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8ecf85f96d55bb2504496cf85a8cc7ec5a0e4cdf4e7b843b5db043bd7c2656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputColumnFamiliesAsJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readRowkeyAsString")
    def read_rowkey_as_string(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readRowkeyAsString"))

    @read_rowkey_as_string.setter
    def read_rowkey_as_string(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f7e132e662c0231d0d91659efb772067d08f86365a36ce35370659adb580e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readRowkeyAsString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationBigtableOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationBigtableOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationBigtableOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bb6b496e771c1a1cf6fed701ec0c2e4780a8a7d887a8a3386ba9bfb8ac37b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationCsvOptions",
    jsii_struct_bases=[],
    name_mapping={
        "quote": "quote",
        "allow_jagged_rows": "allowJaggedRows",
        "allow_quoted_newlines": "allowQuotedNewlines",
        "encoding": "encoding",
        "field_delimiter": "fieldDelimiter",
        "skip_leading_rows": "skipLeadingRows",
    },
)
class BigqueryTableExternalDataConfigurationCsvOptions:
    def __init__(
        self,
        *,
        quote: builtins.str,
        allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param quote: The value that is used to quote data sections in a CSV file. If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allow_quoted_newlines property to true. The API-side default is ", specified in Terraform escaped as ". Due to limitations with Terraform default values, this value is required to be explicitly set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#quote BigqueryTable#quote}
        :param allow_jagged_rows: Indicates if BigQuery should accept rows that are missing trailing optional columns. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_jagged_rows BigqueryTable#allow_jagged_rows}
        :param allow_quoted_newlines: Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_quoted_newlines BigqueryTable#allow_quoted_newlines}
        :param encoding: The character encoding of the data. The supported values are UTF-8 or ISO-8859-1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        :param field_delimiter: The separator for fields in a CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field_delimiter BigqueryTable#field_delimiter}
        :param skip_leading_rows: The number of rows at the top of a CSV file that BigQuery will skip when reading the data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbe70f4df9985ff876e0f2ae8cd3f32cc7a5d0424dcd4f97052fc74b0e00937)
            check_type(argname="argument quote", value=quote, expected_type=type_hints["quote"])
            check_type(argname="argument allow_jagged_rows", value=allow_jagged_rows, expected_type=type_hints["allow_jagged_rows"])
            check_type(argname="argument allow_quoted_newlines", value=allow_quoted_newlines, expected_type=type_hints["allow_quoted_newlines"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument skip_leading_rows", value=skip_leading_rows, expected_type=type_hints["skip_leading_rows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "quote": quote,
        }
        if allow_jagged_rows is not None:
            self._values["allow_jagged_rows"] = allow_jagged_rows
        if allow_quoted_newlines is not None:
            self._values["allow_quoted_newlines"] = allow_quoted_newlines
        if encoding is not None:
            self._values["encoding"] = encoding
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if skip_leading_rows is not None:
            self._values["skip_leading_rows"] = skip_leading_rows

    @builtins.property
    def quote(self) -> builtins.str:
        '''The value that is used to quote data sections in a CSV file.

        If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allow_quoted_newlines property to true. The API-side default is ", specified in Terraform escaped as ". Due to limitations with Terraform default values, this value is required to be explicitly set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#quote BigqueryTable#quote}
        '''
        result = self._values.get("quote")
        assert result is not None, "Required property 'quote' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_jagged_rows(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should accept rows that are missing trailing optional columns.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_jagged_rows BigqueryTable#allow_jagged_rows}
        '''
        result = self._values.get("allow_jagged_rows")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_quoted_newlines(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file.

        The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_quoted_newlines BigqueryTable#allow_quoted_newlines}
        '''
        result = self._values.get("allow_quoted_newlines")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The character encoding of the data. The supported values are UTF-8 or ISO-8859-1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''The separator for fields in a CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field_delimiter BigqueryTable#field_delimiter}
        '''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_leading_rows(self) -> typing.Optional[jsii.Number]:
        '''The number of rows at the top of a CSV file that BigQuery will skip when reading the data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        result = self._values.get("skip_leading_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationCsvOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationCsvOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationCsvOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60af4fc24e71e637c6fa900482563f246e261e062f3062c295a2bad98420962)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowJaggedRows")
    def reset_allow_jagged_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowJaggedRows", []))

    @jsii.member(jsii_name="resetAllowQuotedNewlines")
    def reset_allow_quoted_newlines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowQuotedNewlines", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetFieldDelimiter")
    def reset_field_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldDelimiter", []))

    @jsii.member(jsii_name="resetSkipLeadingRows")
    def reset_skip_leading_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipLeadingRows", []))

    @builtins.property
    @jsii.member(jsii_name="allowJaggedRowsInput")
    def allow_jagged_rows_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowJaggedRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowQuotedNewlinesInput")
    def allow_quoted_newlines_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowQuotedNewlinesInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiterInput")
    def field_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteInput")
    def quote_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteInput"))

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRowsInput")
    def skip_leading_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "skipLeadingRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowJaggedRows")
    def allow_jagged_rows(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowJaggedRows"))

    @allow_jagged_rows.setter
    def allow_jagged_rows(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e73d09915846f7821d69bbaafe21042ed21254594e34719c29494cb50b3a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowJaggedRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowQuotedNewlines")
    def allow_quoted_newlines(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowQuotedNewlines"))

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e69d30776a200962cdf1ae7dbfec1ed9bc8dd3a8bbc993e020ff52eee4a4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowQuotedNewlines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97b74c86bec5163696d29826bf6274501cc5d15f5a8981eecd353bafe0ad6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldDelimiter"))

    @field_delimiter.setter
    def field_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4ef4f6ceb6adf5f5e4f857fe2a3abfa9551e8515e1c01b43f46ad903e65a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quote")
    def quote(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quote"))

    @quote.setter
    def quote(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c97c66ebe5dd4be082754498f497e0dd3a039989089797867763631092e415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRows")
    def skip_leading_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "skipLeadingRows"))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750a54e77026baaefd7596886e1ff0599ce1f18278039fa40bd4ab7b0e00e47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipLeadingRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49253d1d598fd8a759e5fb7260bd43f838344fc041171c17e9fdb960f0bca7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationGoogleSheetsOptions",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "skip_leading_rows": "skipLeadingRows"},
)
class BigqueryTableExternalDataConfigurationGoogleSheetsOptions:
    def __init__(
        self,
        *,
        range: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param range: Range of a sheet to query from. Only used when non-empty. At least one of range or skip_leading_rows must be set. Typical format: "sheet_name!top_left_cell_id:bottom_right_cell_id" For example: "sheet1!A1:B20 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range BigqueryTable#range}
        :param skip_leading_rows: The number of rows at the top of the sheet that BigQuery will skip when reading the data. At least one of range or skip_leading_rows must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d038f67db09f696cd8f12f3dd998ac5d9aaa643c029b6323a5865470d5e1bb13)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument skip_leading_rows", value=skip_leading_rows, expected_type=type_hints["skip_leading_rows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if range is not None:
            self._values["range"] = range
        if skip_leading_rows is not None:
            self._values["skip_leading_rows"] = skip_leading_rows

    @builtins.property
    def range(self) -> typing.Optional[builtins.str]:
        '''Range of a sheet to query from.

        Only used when non-empty. At least one of range or skip_leading_rows must be set. Typical format: "sheet_name!top_left_cell_id:bottom_right_cell_id" For example: "sheet1!A1:B20

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range BigqueryTable#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_leading_rows(self) -> typing.Optional[jsii.Number]:
        '''The number of rows at the top of the sheet that BigQuery will skip when reading the data.

        At least one of range or skip_leading_rows must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        result = self._values.get("skip_leading_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationGoogleSheetsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdc19019d32a22a60c6a9ca6c1e9a76258e4553f4456f2df92bef8f673d7390c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @jsii.member(jsii_name="resetSkipLeadingRows")
    def reset_skip_leading_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipLeadingRows", []))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRowsInput")
    def skip_leading_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "skipLeadingRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "range"))

    @range.setter
    def range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37f5f39bd5216808ff0bfd8dfaf4e99a1f1c79731e27bae75778a2d3136bea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "range", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRows")
    def skip_leading_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "skipLeadingRows"))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52592b7fc99331f5d59d8b9949f4a4ec26a81695186d39a91dc86b408c9263e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipLeadingRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74e3e17939cb2af1a1dda80388692345f22ee6e9ebbbc005cef5c75e631246d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationHivePartitioningOptions",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "require_partition_filter": "requirePartitionFilter",
        "source_uri_prefix": "sourceUriPrefix",
    },
)
class BigqueryTableExternalDataConfigurationHivePartitioningOptions:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_uri_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: When set, what mode of hive partitioning to use when reading data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#mode BigqueryTable#mode}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        :param source_uri_prefix: When hive partition detection is requested, a common for all source uris must be required. The prefix must end immediately before the partition key encoding begins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_uri_prefix BigqueryTable#source_uri_prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810784a6342c4175b64b73278d9e89558c903464868b3a31434d1454105155a7)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument require_partition_filter", value=require_partition_filter, expected_type=type_hints["require_partition_filter"])
            check_type(argname="argument source_uri_prefix", value=source_uri_prefix, expected_type=type_hints["source_uri_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if require_partition_filter is not None:
            self._values["require_partition_filter"] = require_partition_filter
        if source_uri_prefix is not None:
            self._values["source_uri_prefix"] = source_uri_prefix

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''When set, what mode of hive partitioning to use when reading data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#mode BigqueryTable#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_partition_filter(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        result = self._values.get("require_partition_filter")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_uri_prefix(self) -> typing.Optional[builtins.str]:
        '''When hive partition detection is requested, a common for all source uris must be required.

        The prefix must end immediately before the partition key encoding begins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_uri_prefix BigqueryTable#source_uri_prefix}
        '''
        result = self._values.get("source_uri_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationHivePartitioningOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__427d241048413617b3bd3a828418f1d0ac690b71dfe0d2e2068199e9bddd2441)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetRequirePartitionFilter")
    def reset_require_partition_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirePartitionFilter", []))

    @jsii.member(jsii_name="resetSourceUriPrefix")
    def reset_source_uri_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceUriPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilterInput")
    def require_partition_filter_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requirePartitionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUriPrefixInput")
    def source_uri_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceUriPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01a839fea9d2d522ebdb2c7d2a742aa9480bdbd7bb8032c9a1cb98fb08540e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilter")
    def require_partition_filter(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requirePartitionFilter"))

    @require_partition_filter.setter
    def require_partition_filter(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a766f84b3d43b2709c94c8f8521d26c341493a08ed89bef1a658cffcf736efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirePartitionFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUriPrefix")
    def source_uri_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUriPrefix"))

    @source_uri_prefix.setter
    def source_uri_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece8fc4dc9da2b45528b8120676c44420820ae71ca2379a6b811788655de2ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUriPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ea00c1a595be450f340f82ebd3b57198a01adae42a7d6bd7aa2a43f9bfbeb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationJsonOptions",
    jsii_struct_bases=[],
    name_mapping={"encoding": "encoding"},
)
class BigqueryTableExternalDataConfigurationJsonOptions:
    def __init__(self, *, encoding: typing.Optional[builtins.str] = None) -> None:
        '''
        :param encoding: The character encoding of the data. The supported values are UTF-8, UTF-16BE, UTF-16LE, UTF-32BE, and UTF-32LE. The default value is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dec8149763ea2d60862524cfc78a30bfdb3e3f445909cc7308899dbbe3dad3e)
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encoding is not None:
            self._values["encoding"] = encoding

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The character encoding of the data.

        The supported values are UTF-8, UTF-16BE, UTF-16LE, UTF-32BE, and UTF-32LE. The default value is UTF-8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationJsonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationJsonOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationJsonOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55435ebdfa949ad7443de43d41be8a51657e616280bfb76550dcac29a67c7fdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a08b652d0dfd1f677d39a18d6a228377996d531901dfdfec197db54e29d408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationJsonOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationJsonOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationJsonOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f3bc4705cf0a542c770a4ba7a430740c271f1e1e32cc0f8b25f7fa4bb6935d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableExternalDataConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aedd3ec19da32a66f5345c97d51ab2ec0daa172ece609031aadaa848060186d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvroOptions")
    def put_avro_options(
        self,
        *,
        use_avro_logical_types: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param use_avro_logical_types: If sourceFormat is set to "AVRO", indicates whether to interpret logical types as the corresponding BigQuery data type (for example, TIMESTAMP), instead of using the raw type (for example, INTEGER). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#use_avro_logical_types BigqueryTable#use_avro_logical_types}
        '''
        value = BigqueryTableExternalDataConfigurationAvroOptions(
            use_avro_logical_types=use_avro_logical_types
        )

        return typing.cast(None, jsii.invoke(self, "putAvroOptions", [value]))

    @jsii.member(jsii_name="putBigtableOptions")
    def put_bigtable_options(
        self,
        *,
        column_family: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily, typing.Dict[builtins.str, typing.Any]]]]] = None,
        ignore_unspecified_column_families: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_column_families_as_json: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_rowkey_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param column_family: column_family block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#column_family BigqueryTable#column_family}
        :param ignore_unspecified_column_families: If field is true, then the column families that are not specified in columnFamilies list are not exposed in the table schema. Otherwise, they are read with BYTES type values. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#ignore_unspecified_column_families BigqueryTable#ignore_unspecified_column_families}
        :param output_column_families_as_json: If field is true, then each column family will be read as a single JSON column. Otherwise they are read as a repeated cell structure containing timestamp/value tuples. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#output_column_families_as_json BigqueryTable#output_column_families_as_json}
        :param read_rowkey_as_string: If field is true, then the rowkey column families will be read and converted to string. Otherwise they are read with BYTES type values and users need to manually cast them with CAST if necessary. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#read_rowkey_as_string BigqueryTable#read_rowkey_as_string}
        '''
        value = BigqueryTableExternalDataConfigurationBigtableOptions(
            column_family=column_family,
            ignore_unspecified_column_families=ignore_unspecified_column_families,
            output_column_families_as_json=output_column_families_as_json,
            read_rowkey_as_string=read_rowkey_as_string,
        )

        return typing.cast(None, jsii.invoke(self, "putBigtableOptions", [value]))

    @jsii.member(jsii_name="putCsvOptions")
    def put_csv_options(
        self,
        *,
        quote: builtins.str,
        allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param quote: The value that is used to quote data sections in a CSV file. If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allow_quoted_newlines property to true. The API-side default is ", specified in Terraform escaped as ". Due to limitations with Terraform default values, this value is required to be explicitly set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#quote BigqueryTable#quote}
        :param allow_jagged_rows: Indicates if BigQuery should accept rows that are missing trailing optional columns. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_jagged_rows BigqueryTable#allow_jagged_rows}
        :param allow_quoted_newlines: Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_quoted_newlines BigqueryTable#allow_quoted_newlines}
        :param encoding: The character encoding of the data. The supported values are UTF-8 or ISO-8859-1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        :param field_delimiter: The separator for fields in a CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field_delimiter BigqueryTable#field_delimiter}
        :param skip_leading_rows: The number of rows at the top of a CSV file that BigQuery will skip when reading the data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        value = BigqueryTableExternalDataConfigurationCsvOptions(
            quote=quote,
            allow_jagged_rows=allow_jagged_rows,
            allow_quoted_newlines=allow_quoted_newlines,
            encoding=encoding,
            field_delimiter=field_delimiter,
            skip_leading_rows=skip_leading_rows,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvOptions", [value]))

    @jsii.member(jsii_name="putGoogleSheetsOptions")
    def put_google_sheets_options(
        self,
        *,
        range: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param range: Range of a sheet to query from. Only used when non-empty. At least one of range or skip_leading_rows must be set. Typical format: "sheet_name!top_left_cell_id:bottom_right_cell_id" For example: "sheet1!A1:B20 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range BigqueryTable#range}
        :param skip_leading_rows: The number of rows at the top of the sheet that BigQuery will skip when reading the data. At least one of range or skip_leading_rows must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        value = BigqueryTableExternalDataConfigurationGoogleSheetsOptions(
            range=range, skip_leading_rows=skip_leading_rows
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleSheetsOptions", [value]))

    @jsii.member(jsii_name="putHivePartitioningOptions")
    def put_hive_partitioning_options(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_uri_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: When set, what mode of hive partitioning to use when reading data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#mode BigqueryTable#mode}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        :param source_uri_prefix: When hive partition detection is requested, a common for all source uris must be required. The prefix must end immediately before the partition key encoding begins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_uri_prefix BigqueryTable#source_uri_prefix}
        '''
        value = BigqueryTableExternalDataConfigurationHivePartitioningOptions(
            mode=mode,
            require_partition_filter=require_partition_filter,
            source_uri_prefix=source_uri_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putHivePartitioningOptions", [value]))

    @jsii.member(jsii_name="putJsonOptions")
    def put_json_options(
        self,
        *,
        encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encoding: The character encoding of the data. The supported values are UTF-8, UTF-16BE, UTF-16LE, UTF-32BE, and UTF-32LE. The default value is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#encoding BigqueryTable#encoding}
        '''
        value = BigqueryTableExternalDataConfigurationJsonOptions(encoding=encoding)

        return typing.cast(None, jsii.invoke(self, "putJsonOptions", [value]))

    @jsii.member(jsii_name="putParquetOptions")
    def put_parquet_options(
        self,
        *,
        enable_list_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enum_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_list_inference: Indicates whether to use schema inference specifically for Parquet LIST logical type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enable_list_inference BigqueryTable#enable_list_inference}
        :param enum_as_string: Indicates whether to infer Parquet ENUM logical type as STRING instead of BYTES by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enum_as_string BigqueryTable#enum_as_string}
        '''
        value = BigqueryTableExternalDataConfigurationParquetOptions(
            enable_list_inference=enable_list_inference, enum_as_string=enum_as_string
        )

        return typing.cast(None, jsii.invoke(self, "putParquetOptions", [value]))

    @jsii.member(jsii_name="resetAvroOptions")
    def reset_avro_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvroOptions", []))

    @jsii.member(jsii_name="resetBigtableOptions")
    def reset_bigtable_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigtableOptions", []))

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetConnectionId")
    def reset_connection_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionId", []))

    @jsii.member(jsii_name="resetCsvOptions")
    def reset_csv_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvOptions", []))

    @jsii.member(jsii_name="resetFileSetSpecType")
    def reset_file_set_spec_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSetSpecType", []))

    @jsii.member(jsii_name="resetGoogleSheetsOptions")
    def reset_google_sheets_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleSheetsOptions", []))

    @jsii.member(jsii_name="resetHivePartitioningOptions")
    def reset_hive_partitioning_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHivePartitioningOptions", []))

    @jsii.member(jsii_name="resetIgnoreUnknownValues")
    def reset_ignore_unknown_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreUnknownValues", []))

    @jsii.member(jsii_name="resetJsonExtension")
    def reset_json_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonExtension", []))

    @jsii.member(jsii_name="resetJsonOptions")
    def reset_json_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonOptions", []))

    @jsii.member(jsii_name="resetMaxBadRecords")
    def reset_max_bad_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBadRecords", []))

    @jsii.member(jsii_name="resetMetadataCacheMode")
    def reset_metadata_cache_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataCacheMode", []))

    @jsii.member(jsii_name="resetObjectMetadata")
    def reset_object_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectMetadata", []))

    @jsii.member(jsii_name="resetParquetOptions")
    def reset_parquet_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParquetOptions", []))

    @jsii.member(jsii_name="resetReferenceFileSchemaUri")
    def reset_reference_file_schema_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceFileSchemaUri", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetSourceFormat")
    def reset_source_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFormat", []))

    @builtins.property
    @jsii.member(jsii_name="avroOptions")
    def avro_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationAvroOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationAvroOptionsOutputReference, jsii.get(self, "avroOptions"))

    @builtins.property
    @jsii.member(jsii_name="bigtableOptions")
    def bigtable_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationBigtableOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationBigtableOptionsOutputReference, jsii.get(self, "bigtableOptions"))

    @builtins.property
    @jsii.member(jsii_name="csvOptions")
    def csv_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationCsvOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationCsvOptionsOutputReference, jsii.get(self, "csvOptions"))

    @builtins.property
    @jsii.member(jsii_name="googleSheetsOptions")
    def google_sheets_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference, jsii.get(self, "googleSheetsOptions"))

    @builtins.property
    @jsii.member(jsii_name="hivePartitioningOptions")
    def hive_partitioning_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference, jsii.get(self, "hivePartitioningOptions"))

    @builtins.property
    @jsii.member(jsii_name="jsonOptions")
    def json_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationJsonOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationJsonOptionsOutputReference, jsii.get(self, "jsonOptions"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptions")
    def parquet_options(
        self,
    ) -> "BigqueryTableExternalDataConfigurationParquetOptionsOutputReference":
        return typing.cast("BigqueryTableExternalDataConfigurationParquetOptionsOutputReference", jsii.get(self, "parquetOptions"))

    @builtins.property
    @jsii.member(jsii_name="autodetectInput")
    def autodetect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autodetectInput"))

    @builtins.property
    @jsii.member(jsii_name="avroOptionsInput")
    def avro_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions], jsii.get(self, "avroOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="bigtableOptionsInput")
    def bigtable_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationBigtableOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationBigtableOptions], jsii.get(self, "bigtableOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="csvOptionsInput")
    def csv_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions], jsii.get(self, "csvOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSetSpecTypeInput")
    def file_set_spec_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSetSpecTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="googleSheetsOptionsInput")
    def google_sheets_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions], jsii.get(self, "googleSheetsOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="hivePartitioningOptionsInput")
    def hive_partitioning_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions], jsii.get(self, "hivePartitioningOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreUnknownValuesInput")
    def ignore_unknown_values_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreUnknownValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonExtensionInput")
    def json_extension_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonExtensionInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonOptionsInput")
    def json_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationJsonOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationJsonOptions], jsii.get(self, "jsonOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBadRecordsInput")
    def max_bad_records_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBadRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataCacheModeInput")
    def metadata_cache_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataCacheModeInput"))

    @builtins.property
    @jsii.member(jsii_name="objectMetadataInput")
    def object_metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptionsInput")
    def parquet_options_input(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationParquetOptions"]:
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationParquetOptions"], jsii.get(self, "parquetOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceFileSchemaUriInput")
    def reference_file_schema_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referenceFileSchemaUriInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFormatInput")
    def source_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrisInput")
    def source_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="autodetect")
    def autodetect(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autodetect"))

    @autodetect.setter
    def autodetect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa92013cd8c6f4654573bca59cada4acf1ab4fa24e0c33e4d4183250eea524a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autodetect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171e466428ef05f4c723a94ae4be4749554bd2eea5cd174382809e39dc1531e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b513971418e35e0889daa1af0c24cd9d68fe2c0c11f24a4107c11bdd933e16b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileSetSpecType")
    def file_set_spec_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSetSpecType"))

    @file_set_spec_type.setter
    def file_set_spec_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec15ce63e9c828984a5d7f41096c3695022e6115b14821a07a91f3e4bbd5448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSetSpecType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreUnknownValues")
    def ignore_unknown_values(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreUnknownValues"))

    @ignore_unknown_values.setter
    def ignore_unknown_values(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a59007098ead2bf4df9dc5cfcdcf21549a84089fbee66a5e258d3fd9a97d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreUnknownValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonExtension")
    def json_extension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonExtension"))

    @json_extension.setter
    def json_extension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26036ad0a935ab122cb8292288b221d29c5c83df4c9ef6a251f72defd50f6a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonExtension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBadRecords")
    def max_bad_records(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBadRecords"))

    @max_bad_records.setter
    def max_bad_records(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d69f7654bb9a49339cdf5f1425dadb79c83dad7cad0ee4c0b95ee260bcf1b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBadRecords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataCacheMode")
    def metadata_cache_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataCacheMode"))

    @metadata_cache_mode.setter
    def metadata_cache_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb09cd9d1c318de492a7c2211d2e38e5ef97cc409f9e3ca3680609b1ed487a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataCacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectMetadata")
    def object_metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectMetadata"))

    @object_metadata.setter
    def object_metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299af1e3e836561fcb503c63c0716231093c196a6ddfad2175cfd1fe62e17814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referenceFileSchemaUri")
    def reference_file_schema_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceFileSchemaUri"))

    @reference_file_schema_uri.setter
    def reference_file_schema_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213c2a36ef7a804e14ba80c930b6fd7a3688ffe9e23f248712dce815b05a86f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceFileSchemaUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0884b65b0bdd6567b088bb09c59a013f1c64f0c864984a8075b6a4e371875e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a03112d506997097f3ea5d211e0cd0d133f64fde4a35c3bc1ceafc857b28a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUris")
    def source_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceUris"))

    @source_uris.setter
    def source_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2411a1cf8a70ffbcaa7d39b40a4d65c9ac8a09f10bddc890f5e9f3dfa59fd1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableExternalDataConfiguration]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a895f0de550b51ae084bc84300b10c9de0fb66c609b0968fc28545ce0c6a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationParquetOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enable_list_inference": "enableListInference",
        "enum_as_string": "enumAsString",
    },
)
class BigqueryTableExternalDataConfigurationParquetOptions:
    def __init__(
        self,
        *,
        enable_list_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enum_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_list_inference: Indicates whether to use schema inference specifically for Parquet LIST logical type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enable_list_inference BigqueryTable#enable_list_inference}
        :param enum_as_string: Indicates whether to infer Parquet ENUM logical type as STRING instead of BYTES by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enum_as_string BigqueryTable#enum_as_string}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e580c4d966a2cc25478344c0e79c9c6342f4aee2890c85d19c972100dab08977)
            check_type(argname="argument enable_list_inference", value=enable_list_inference, expected_type=type_hints["enable_list_inference"])
            check_type(argname="argument enum_as_string", value=enum_as_string, expected_type=type_hints["enum_as_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_list_inference is not None:
            self._values["enable_list_inference"] = enable_list_inference
        if enum_as_string is not None:
            self._values["enum_as_string"] = enum_as_string

    @builtins.property
    def enable_list_inference(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether to use schema inference specifically for Parquet LIST logical type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enable_list_inference BigqueryTable#enable_list_inference}
        '''
        result = self._values.get("enable_list_inference")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enum_as_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether to infer Parquet ENUM logical type as STRING instead of BYTES by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enum_as_string BigqueryTable#enum_as_string}
        '''
        result = self._values.get("enum_as_string")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationParquetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationParquetOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationParquetOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c21531b9bf1753605c506d734d31f8c05da55a2e18787c846ba0f11523e334)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableListInference")
    def reset_enable_list_inference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableListInference", []))

    @jsii.member(jsii_name="resetEnumAsString")
    def reset_enum_as_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnumAsString", []))

    @builtins.property
    @jsii.member(jsii_name="enableListInferenceInput")
    def enable_list_inference_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableListInferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="enumAsStringInput")
    def enum_as_string_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enumAsStringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableListInference")
    def enable_list_inference(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableListInference"))

    @enable_list_inference.setter
    def enable_list_inference(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5908d98cdfb96a6db3cf813b2c415271f41e5255d612906ebf4a29558cab5bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableListInference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enumAsString")
    def enum_as_string(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enumAsString"))

    @enum_as_string.setter
    def enum_as_string(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bac64ebafef3ca5bea0ec86252a289d94c58f429837110b52e4febffd0ad127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enumAsString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationParquetOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationParquetOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationParquetOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690db45b00cc068b07c9eef643410cc67f91cc6b39bd826b690fa3bac49b737d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableMaterializedView",
    jsii_struct_bases=[],
    name_mapping={
        "query": "query",
        "allow_non_incremental_definition": "allowNonIncrementalDefinition",
        "enable_refresh": "enableRefresh",
        "refresh_interval_ms": "refreshIntervalMs",
    },
)
class BigqueryTableMaterializedView:
    def __init__(
        self,
        *,
        query: builtins.str,
        allow_non_incremental_definition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        refresh_interval_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: A query whose result is persisted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#query BigqueryTable#query}
        :param allow_non_incremental_definition: Allow non incremental materialized view definition. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_non_incremental_definition BigqueryTable#allow_non_incremental_definition}
        :param enable_refresh: Specifies if BigQuery should automatically refresh materialized view when the base table is updated. The default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enable_refresh BigqueryTable#enable_refresh}
        :param refresh_interval_ms: Specifies maximum frequency at which this materialized view will be refreshed. The default is 1800000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#refresh_interval_ms BigqueryTable#refresh_interval_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bfac7ffc7a9089b8ef1d3b22082c499bb74076ee32063e98bfc14ba774af19)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument allow_non_incremental_definition", value=allow_non_incremental_definition, expected_type=type_hints["allow_non_incremental_definition"])
            check_type(argname="argument enable_refresh", value=enable_refresh, expected_type=type_hints["enable_refresh"])
            check_type(argname="argument refresh_interval_ms", value=refresh_interval_ms, expected_type=type_hints["refresh_interval_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if allow_non_incremental_definition is not None:
            self._values["allow_non_incremental_definition"] = allow_non_incremental_definition
        if enable_refresh is not None:
            self._values["enable_refresh"] = enable_refresh
        if refresh_interval_ms is not None:
            self._values["refresh_interval_ms"] = refresh_interval_ms

    @builtins.property
    def query(self) -> builtins.str:
        '''A query whose result is persisted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#query BigqueryTable#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_non_incremental_definition(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow non incremental materialized view definition. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#allow_non_incremental_definition BigqueryTable#allow_non_incremental_definition}
        '''
        result = self._values.get("allow_non_incremental_definition")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_refresh(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if BigQuery should automatically refresh materialized view when the base table is updated. The default is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#enable_refresh BigqueryTable#enable_refresh}
        '''
        result = self._values.get("enable_refresh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def refresh_interval_ms(self) -> typing.Optional[jsii.Number]:
        '''Specifies maximum frequency at which this materialized view will be refreshed. The default is 1800000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#refresh_interval_ms BigqueryTable#refresh_interval_ms}
        '''
        result = self._values.get("refresh_interval_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableMaterializedView(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableMaterializedViewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableMaterializedViewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a06199473432610a340d54e912a27a45d9838f276f5ddefb8ea5ed442551b84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowNonIncrementalDefinition")
    def reset_allow_non_incremental_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowNonIncrementalDefinition", []))

    @jsii.member(jsii_name="resetEnableRefresh")
    def reset_enable_refresh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRefresh", []))

    @jsii.member(jsii_name="resetRefreshIntervalMs")
    def reset_refresh_interval_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshIntervalMs", []))

    @builtins.property
    @jsii.member(jsii_name="allowNonIncrementalDefinitionInput")
    def allow_non_incremental_definition_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowNonIncrementalDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRefreshInput")
    def enable_refresh_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshIntervalMsInput")
    def refresh_interval_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "refreshIntervalMsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowNonIncrementalDefinition")
    def allow_non_incremental_definition(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowNonIncrementalDefinition"))

    @allow_non_incremental_definition.setter
    def allow_non_incremental_definition(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57984ff9f86a6b8017c67bd873d16cb38383fa841cb1c329b4e6cc1039c2919b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNonIncrementalDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableRefresh")
    def enable_refresh(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRefresh"))

    @enable_refresh.setter
    def enable_refresh(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95c47f7821838b81eb06f48bf5b0c5aed91c07011b4d48d8073fce2186f17bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRefresh", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9fea0c74fd4684d8ad56faaf0179f2f5bb721644dff852d3e6979f302106755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshIntervalMs")
    def refresh_interval_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "refreshIntervalMs"))

    @refresh_interval_ms.setter
    def refresh_interval_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9657a3990dc569b85efe467953e2b35134c6d571e8a9003d13db7d882c11d771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshIntervalMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableMaterializedView]:
        return typing.cast(typing.Optional[BigqueryTableMaterializedView], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableMaterializedView],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35804a2287301e8b044546610ce9f0fb372c6b235f2ade6d86c3105305e0f8c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioning",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "range": "range"},
)
class BigqueryTableRangePartitioning:
    def __init__(
        self,
        *,
        field: builtins.str,
        range: typing.Union["BigqueryTableRangePartitioningRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: The field used to determine how to create a range-based partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field BigqueryTable#field}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range BigqueryTable#range}
        '''
        if isinstance(range, dict):
            range = BigqueryTableRangePartitioningRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdcc485551cdda9350f0ec3b6f635fb181dfeb360e8a64dc8017a129edb17bf)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field": field,
            "range": range,
        }

    @builtins.property
    def field(self) -> builtins.str:
        '''The field used to determine how to create a range-based partition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field BigqueryTable#field}
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(self) -> "BigqueryTableRangePartitioningRange":
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#range BigqueryTable#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("BigqueryTableRangePartitioningRange", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableRangePartitioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableRangePartitioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5846667bda1a92cfa7b2128c33f2548d65ee779e39fcfee01fc1ed16c3071bdc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        *,
        end: jsii.Number,
        interval: jsii.Number,
        start: jsii.Number,
    ) -> None:
        '''
        :param end: End of the range partitioning, exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#end BigqueryTable#end}
        :param interval: The width of each range within the partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#interval BigqueryTable#interval}
        :param start: Start of the range partitioning, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#start BigqueryTable#start}
        '''
        value = BigqueryTableRangePartitioningRange(
            end=end, interval=interval, start=start
        )

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "BigqueryTableRangePartitioningRangeOutputReference":
        return typing.cast("BigqueryTableRangePartitioningRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional["BigqueryTableRangePartitioningRange"]:
        return typing.cast(typing.Optional["BigqueryTableRangePartitioningRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395c6f6f36489faff4acf790a2a2cc1c21f8f9966c5ef9a170a50199315505e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableRangePartitioning]:
        return typing.cast(typing.Optional[BigqueryTableRangePartitioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableRangePartitioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ed36eb55e507419b8535e2c7cafa45c85bff6123571a8edb4886a44bacae48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioningRange",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "interval": "interval", "start": "start"},
)
class BigqueryTableRangePartitioningRange:
    def __init__(
        self,
        *,
        end: jsii.Number,
        interval: jsii.Number,
        start: jsii.Number,
    ) -> None:
        '''
        :param end: End of the range partitioning, exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#end BigqueryTable#end}
        :param interval: The width of each range within the partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#interval BigqueryTable#interval}
        :param start: Start of the range partitioning, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#start BigqueryTable#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69572fe55635746c6c943f6472627f9914d257e914d14e8158134965b8a38fb4)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "interval": interval,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''End of the range partitioning, exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#end BigqueryTable#end}
        '''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval(self) -> jsii.Number:
        '''The width of each range within the partition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#interval BigqueryTable#interval}
        '''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Start of the range partitioning, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#start BigqueryTable#start}
        '''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableRangePartitioningRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableRangePartitioningRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioningRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e346b07c1bf2602c604ad14a57886686548a1aa4a51a38351b11b562dc21085)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2b695fdea4b4df8ca95b67883601572c7925871a37b6a6422ddb8f986cab0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3633200eb7491ca91f5312d0e52d612aafd64c3a611f85726166d54ad0765116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f689dce76260a1d7c60657cf8bca91a3d9a497d6f1788949e150195b1c9820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableRangePartitioningRange]:
        return typing.cast(typing.Optional[BigqueryTableRangePartitioningRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableRangePartitioningRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19729f38363279736c21ff6e0255ab435dae55bb7e61e454e836a44d18820d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableSchemaForeignTypeInfo",
    jsii_struct_bases=[],
    name_mapping={"type_system": "typeSystem"},
)
class BigqueryTableSchemaForeignTypeInfo:
    def __init__(self, *, type_system: builtins.str) -> None:
        '''
        :param type_system: Specifies the system which defines the foreign data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type_system BigqueryTable#type_system}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7420a9b9b94a9461f6490dac852736f6e4ed9faeabd266e2342653d72f53a32)
            check_type(argname="argument type_system", value=type_system, expected_type=type_hints["type_system"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type_system": type_system,
        }

    @builtins.property
    def type_system(self) -> builtins.str:
        '''Specifies the system which defines the foreign data type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type_system BigqueryTable#type_system}
        '''
        result = self._values.get("type_system")
        assert result is not None, "Required property 'type_system' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableSchemaForeignTypeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableSchemaForeignTypeInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableSchemaForeignTypeInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f81ad197e874f23809ef138d38b926f76d492b315b2d28aa38aa88c841dc852)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeSystemInput")
    def type_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="typeSystem")
    def type_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeSystem"))

    @type_system.setter
    def type_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f483fcd6c0328f2ab60823f093560799024bea885887802d187b9d34343da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableSchemaForeignTypeInfo]:
        return typing.cast(typing.Optional[BigqueryTableSchemaForeignTypeInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableSchemaForeignTypeInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f2484934af76611be99a81a47064a10bbbb595d376abed94ac499ad99ff49a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraints",
    jsii_struct_bases=[],
    name_mapping={"foreign_keys": "foreignKeys", "primary_key": "primaryKey"},
)
class BigqueryTableTableConstraints:
    def __init__(
        self,
        *,
        foreign_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryTableTableConstraintsForeignKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        primary_key: typing.Optional[typing.Union["BigqueryTableTableConstraintsPrimaryKey", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param foreign_keys: foreign_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#foreign_keys BigqueryTable#foreign_keys}
        :param primary_key: primary_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#primary_key BigqueryTable#primary_key}
        '''
        if isinstance(primary_key, dict):
            primary_key = BigqueryTableTableConstraintsPrimaryKey(**primary_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66412678e0af26f8b78798f0102a6b1ea68db9f05edf807a3cd7fa94d235c56)
            check_type(argname="argument foreign_keys", value=foreign_keys, expected_type=type_hints["foreign_keys"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if foreign_keys is not None:
            self._values["foreign_keys"] = foreign_keys
        if primary_key is not None:
            self._values["primary_key"] = primary_key

    @builtins.property
    def foreign_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryTableTableConstraintsForeignKeys"]]]:
        '''foreign_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#foreign_keys BigqueryTable#foreign_keys}
        '''
        result = self._values.get("foreign_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryTableTableConstraintsForeignKeys"]]], result)

    @builtins.property
    def primary_key(self) -> typing.Optional["BigqueryTableTableConstraintsPrimaryKey"]:
        '''primary_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#primary_key BigqueryTable#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional["BigqueryTableTableConstraintsPrimaryKey"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTableConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsForeignKeys",
    jsii_struct_bases=[],
    name_mapping={
        "column_references": "columnReferences",
        "referenced_table": "referencedTable",
        "name": "name",
    },
)
class BigqueryTableTableConstraintsForeignKeys:
    def __init__(
        self,
        *,
        column_references: typing.Union["BigqueryTableTableConstraintsForeignKeysColumnReferences", typing.Dict[builtins.str, typing.Any]],
        referenced_table: typing.Union["BigqueryTableTableConstraintsForeignKeysReferencedTable", typing.Dict[builtins.str, typing.Any]],
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_references: column_references block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#column_references BigqueryTable#column_references}
        :param referenced_table: referenced_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referenced_table BigqueryTable#referenced_table}
        :param name: Set only if the foreign key constraint is named. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#name BigqueryTable#name}
        '''
        if isinstance(column_references, dict):
            column_references = BigqueryTableTableConstraintsForeignKeysColumnReferences(**column_references)
        if isinstance(referenced_table, dict):
            referenced_table = BigqueryTableTableConstraintsForeignKeysReferencedTable(**referenced_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f61370d43968c22f52ef6734d2e77d1a8a96dd965a869b48860662ee6a21722)
            check_type(argname="argument column_references", value=column_references, expected_type=type_hints["column_references"])
            check_type(argname="argument referenced_table", value=referenced_table, expected_type=type_hints["referenced_table"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_references": column_references,
            "referenced_table": referenced_table,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def column_references(
        self,
    ) -> "BigqueryTableTableConstraintsForeignKeysColumnReferences":
        '''column_references block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#column_references BigqueryTable#column_references}
        '''
        result = self._values.get("column_references")
        assert result is not None, "Required property 'column_references' is missing"
        return typing.cast("BigqueryTableTableConstraintsForeignKeysColumnReferences", result)

    @builtins.property
    def referenced_table(
        self,
    ) -> "BigqueryTableTableConstraintsForeignKeysReferencedTable":
        '''referenced_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referenced_table BigqueryTable#referenced_table}
        '''
        result = self._values.get("referenced_table")
        assert result is not None, "Required property 'referenced_table' is missing"
        return typing.cast("BigqueryTableTableConstraintsForeignKeysReferencedTable", result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Set only if the foreign key constraint is named.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#name BigqueryTable#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTableConstraintsForeignKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsForeignKeysColumnReferences",
    jsii_struct_bases=[],
    name_mapping={
        "referenced_column": "referencedColumn",
        "referencing_column": "referencingColumn",
    },
)
class BigqueryTableTableConstraintsForeignKeysColumnReferences:
    def __init__(
        self,
        *,
        referenced_column: builtins.str,
        referencing_column: builtins.str,
    ) -> None:
        '''
        :param referenced_column: The column in the primary key that are referenced by the referencingColumn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referenced_column BigqueryTable#referenced_column}
        :param referencing_column: The column that composes the foreign key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referencing_column BigqueryTable#referencing_column}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124b9358eb11410c5cc7b746109df639f5aeb5a0187a99866457543232b33213)
            check_type(argname="argument referenced_column", value=referenced_column, expected_type=type_hints["referenced_column"])
            check_type(argname="argument referencing_column", value=referencing_column, expected_type=type_hints["referencing_column"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "referenced_column": referenced_column,
            "referencing_column": referencing_column,
        }

    @builtins.property
    def referenced_column(self) -> builtins.str:
        '''The column in the primary key that are referenced by the referencingColumn.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referenced_column BigqueryTable#referenced_column}
        '''
        result = self._values.get("referenced_column")
        assert result is not None, "Required property 'referenced_column' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def referencing_column(self) -> builtins.str:
        '''The column that composes the foreign key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referencing_column BigqueryTable#referencing_column}
        '''
        result = self._values.get("referencing_column")
        assert result is not None, "Required property 'referencing_column' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTableConstraintsForeignKeysColumnReferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableTableConstraintsForeignKeysColumnReferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsForeignKeysColumnReferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fef1fba74406c995d56a4dab9e0db702753afab608a07cdb9b37c2fd9bd1e60d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="referencedColumnInput")
    def referenced_column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referencedColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="referencingColumnInput")
    def referencing_column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referencingColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="referencedColumn")
    def referenced_column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referencedColumn"))

    @referenced_column.setter
    def referenced_column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc52fea06ba2300d376003a0cb48490bfd95c1077e6abd6471cbf81e6eef15ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referencedColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referencingColumn")
    def referencing_column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referencingColumn"))

    @referencing_column.setter
    def referencing_column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4735a4c0b6173bbc5687e6c13dca78d807c63288f93813f4738e4769cead18b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referencingColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableTableConstraintsForeignKeysColumnReferences]:
        return typing.cast(typing.Optional[BigqueryTableTableConstraintsForeignKeysColumnReferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableTableConstraintsForeignKeysColumnReferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05b700cf16429be44e70ac0074b1d8eece74f899cc760c21cd1721ac11b7da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableTableConstraintsForeignKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsForeignKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c756f29f1215ccd7ac0060b571d65fafdb1947164c0ed08b9881fec8ce62d52d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BigqueryTableTableConstraintsForeignKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8c7f5a9ff56b07445407b65df99256ece2c9e6ca1efd4af3506bf73b929ac0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigqueryTableTableConstraintsForeignKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ece3323761b1d97ecedb617f03c06d4173c9ceddaf5a5e504220c1f63f29b62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__711588ff5bfdfee301a7e68c1274a6b573c182fb9bb80281639b9b0534cdf4ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9989e18a083944a74bf1085e3d10de10062cac2034298754dae460c44b878497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableTableConstraintsForeignKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableTableConstraintsForeignKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableTableConstraintsForeignKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a03f2179150028ae4d02dde02a6a8eb1758c6fa5acc045485b3f2c92d910ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableTableConstraintsForeignKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsForeignKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e1deacd089d448db4567dc11360f6f185222d7bd24cb840e9955ee2e68a5d9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putColumnReferences")
    def put_column_references(
        self,
        *,
        referenced_column: builtins.str,
        referencing_column: builtins.str,
    ) -> None:
        '''
        :param referenced_column: The column in the primary key that are referenced by the referencingColumn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referenced_column BigqueryTable#referenced_column}
        :param referencing_column: The column that composes the foreign key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#referencing_column BigqueryTable#referencing_column}
        '''
        value = BigqueryTableTableConstraintsForeignKeysColumnReferences(
            referenced_column=referenced_column, referencing_column=referencing_column
        )

        return typing.cast(None, jsii.invoke(self, "putColumnReferences", [value]))

    @jsii.member(jsii_name="putReferencedTable")
    def put_referenced_table(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#dataset_id BigqueryTable#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#project_id BigqueryTable#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Certain operations allow suffixing of the table ID with a partition decorator, such as sample_table$20190123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_id BigqueryTable#table_id}
        '''
        value = BigqueryTableTableConstraintsForeignKeysReferencedTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putReferencedTable", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="columnReferences")
    def column_references(
        self,
    ) -> BigqueryTableTableConstraintsForeignKeysColumnReferencesOutputReference:
        return typing.cast(BigqueryTableTableConstraintsForeignKeysColumnReferencesOutputReference, jsii.get(self, "columnReferences"))

    @builtins.property
    @jsii.member(jsii_name="referencedTable")
    def referenced_table(
        self,
    ) -> "BigqueryTableTableConstraintsForeignKeysReferencedTableOutputReference":
        return typing.cast("BigqueryTableTableConstraintsForeignKeysReferencedTableOutputReference", jsii.get(self, "referencedTable"))

    @builtins.property
    @jsii.member(jsii_name="columnReferencesInput")
    def column_references_input(
        self,
    ) -> typing.Optional[BigqueryTableTableConstraintsForeignKeysColumnReferences]:
        return typing.cast(typing.Optional[BigqueryTableTableConstraintsForeignKeysColumnReferences], jsii.get(self, "columnReferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="referencedTableInput")
    def referenced_table_input(
        self,
    ) -> typing.Optional["BigqueryTableTableConstraintsForeignKeysReferencedTable"]:
        return typing.cast(typing.Optional["BigqueryTableTableConstraintsForeignKeysReferencedTable"], jsii.get(self, "referencedTableInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75675d4550bcb2658a5fcd41dc689470826bc3798f62fec465792a3c952801b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableTableConstraintsForeignKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableTableConstraintsForeignKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableTableConstraintsForeignKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e519e26935bf6c9b9f013b8e96dbd65d24c5e4801ffe5cbeb66d734b0637b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsForeignKeysReferencedTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class BigqueryTableTableConstraintsForeignKeysReferencedTable:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#dataset_id BigqueryTable#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#project_id BigqueryTable#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Certain operations allow suffixing of the table ID with a partition decorator, such as sample_table$20190123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_id BigqueryTable#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0498de677b1f2b6280675020b860ec4bbe3cf7017633a54fb6d1a9aaf678fe77)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
            "table_id": table_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#dataset_id BigqueryTable#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#project_id BigqueryTable#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The ID of the table.

        The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Certain operations allow suffixing of the table ID with a partition decorator, such as sample_table$20190123.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#table_id BigqueryTable#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTableConstraintsForeignKeysReferencedTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableTableConstraintsForeignKeysReferencedTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsForeignKeysReferencedTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b19e413299c8ff3c038626de3edd7b16c37479424a7883a567c1db834e92a676)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e8749a7fc2226e4735f38a0d13738328082c24fd83cfd96da6c8214f20116e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e035db842824dbfd776d33e11e45d49d32a3732280d2353a9f8c89b8d587ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78170eb408811e1d4ef6457e62b4fbd840e3332ac2716a92d3663aa18119676a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableTableConstraintsForeignKeysReferencedTable]:
        return typing.cast(typing.Optional[BigqueryTableTableConstraintsForeignKeysReferencedTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableTableConstraintsForeignKeysReferencedTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e985db9c3fa037cb23dc1967830b2fd34b517ca60101f63491f069cdd34dab48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryTableTableConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d673047801d7fb42c6396f4f80447d2b507e3b4dd2dc050cd75ffabe062659)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putForeignKeys")
    def put_foreign_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableTableConstraintsForeignKeys, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d58cba0938837919b6dcd2ac1a969dce87c59a5e303ec534be1327490141c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putForeignKeys", [value]))

    @jsii.member(jsii_name="putPrimaryKey")
    def put_primary_key(self, *, columns: typing.Sequence[builtins.str]) -> None:
        '''
        :param columns: The columns that are composed of the primary key constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#columns BigqueryTable#columns}
        '''
        value = BigqueryTableTableConstraintsPrimaryKey(columns=columns)

        return typing.cast(None, jsii.invoke(self, "putPrimaryKey", [value]))

    @jsii.member(jsii_name="resetForeignKeys")
    def reset_foreign_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForeignKeys", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @builtins.property
    @jsii.member(jsii_name="foreignKeys")
    def foreign_keys(self) -> BigqueryTableTableConstraintsForeignKeysList:
        return typing.cast(BigqueryTableTableConstraintsForeignKeysList, jsii.get(self, "foreignKeys"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> "BigqueryTableTableConstraintsPrimaryKeyOutputReference":
        return typing.cast("BigqueryTableTableConstraintsPrimaryKeyOutputReference", jsii.get(self, "primaryKey"))

    @builtins.property
    @jsii.member(jsii_name="foreignKeysInput")
    def foreign_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableTableConstraintsForeignKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableTableConstraintsForeignKeys]]], jsii.get(self, "foreignKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(
        self,
    ) -> typing.Optional["BigqueryTableTableConstraintsPrimaryKey"]:
        return typing.cast(typing.Optional["BigqueryTableTableConstraintsPrimaryKey"], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableTableConstraints]:
        return typing.cast(typing.Optional[BigqueryTableTableConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableTableConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3959b03c3f97b42b2cd251bf03069a3c966436bfda7e3055b2d42db5a69680d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsPrimaryKey",
    jsii_struct_bases=[],
    name_mapping={"columns": "columns"},
)
class BigqueryTableTableConstraintsPrimaryKey:
    def __init__(self, *, columns: typing.Sequence[builtins.str]) -> None:
        '''
        :param columns: The columns that are composed of the primary key constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#columns BigqueryTable#columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7c48c97ad365b615185ea236f534b48101a1019d24cb3f7928bfecdaaec9e1)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
        }

    @builtins.property
    def columns(self) -> typing.List[builtins.str]:
        '''The columns that are composed of the primary key constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#columns BigqueryTable#columns}
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTableConstraintsPrimaryKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableTableConstraintsPrimaryKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableConstraintsPrimaryKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2391852a0c62909fe0eadc8bb4fdc54cbfc6398b2a0f23506d71d1b90e800b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e322b715fc8d22347e8aaf8006a76d5bbc9ffb9217a9ae6dc25915b0e96107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableTableConstraintsPrimaryKey]:
        return typing.cast(typing.Optional[BigqueryTableTableConstraintsPrimaryKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableTableConstraintsPrimaryKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b82bfc98420341ac9aa3379df25d954f44556f460e27bdf49cd5a181190ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableReplicationInfo",
    jsii_struct_bases=[],
    name_mapping={
        "source_dataset_id": "sourceDatasetId",
        "source_project_id": "sourceProjectId",
        "source_table_id": "sourceTableId",
        "replication_interval_ms": "replicationIntervalMs",
    },
)
class BigqueryTableTableReplicationInfo:
    def __init__(
        self,
        *,
        source_dataset_id: builtins.str,
        source_project_id: builtins.str,
        source_table_id: builtins.str,
        replication_interval_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_dataset_id: The ID of the source dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_dataset_id BigqueryTable#source_dataset_id}
        :param source_project_id: The ID of the source project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_project_id BigqueryTable#source_project_id}
        :param source_table_id: The ID of the source materialized view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_table_id BigqueryTable#source_table_id}
        :param replication_interval_ms: The interval at which the source materialized view is polled for updates. The default is 300000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#replication_interval_ms BigqueryTable#replication_interval_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9dbea1d377c74b24f3288e0105d6a57a108694b1874b635b77bc913ed33c92)
            check_type(argname="argument source_dataset_id", value=source_dataset_id, expected_type=type_hints["source_dataset_id"])
            check_type(argname="argument source_project_id", value=source_project_id, expected_type=type_hints["source_project_id"])
            check_type(argname="argument source_table_id", value=source_table_id, expected_type=type_hints["source_table_id"])
            check_type(argname="argument replication_interval_ms", value=replication_interval_ms, expected_type=type_hints["replication_interval_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_dataset_id": source_dataset_id,
            "source_project_id": source_project_id,
            "source_table_id": source_table_id,
        }
        if replication_interval_ms is not None:
            self._values["replication_interval_ms"] = replication_interval_ms

    @builtins.property
    def source_dataset_id(self) -> builtins.str:
        '''The ID of the source dataset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_dataset_id BigqueryTable#source_dataset_id}
        '''
        result = self._values.get("source_dataset_id")
        assert result is not None, "Required property 'source_dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_project_id(self) -> builtins.str:
        '''The ID of the source project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_project_id BigqueryTable#source_project_id}
        '''
        result = self._values.get("source_project_id")
        assert result is not None, "Required property 'source_project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_table_id(self) -> builtins.str:
        '''The ID of the source materialized view.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#source_table_id BigqueryTable#source_table_id}
        '''
        result = self._values.get("source_table_id")
        assert result is not None, "Required property 'source_table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_interval_ms(self) -> typing.Optional[jsii.Number]:
        '''The interval at which the source materialized view is polled for updates. The default is 300000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#replication_interval_ms BigqueryTable#replication_interval_ms}
        '''
        result = self._values.get("replication_interval_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTableReplicationInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableTableReplicationInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTableReplicationInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__783bd33a6f915df8936c5ab4f7ed3587298deb49c51ec9f165eacaffd39aa945)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReplicationIntervalMs")
    def reset_replication_interval_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationIntervalMs", []))

    @builtins.property
    @jsii.member(jsii_name="replicationIntervalMsInput")
    def replication_interval_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicationIntervalMsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDatasetIdInput")
    def source_dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDatasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceProjectIdInput")
    def source_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTableIdInput")
    def source_table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationIntervalMs")
    def replication_interval_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicationIntervalMs"))

    @replication_interval_ms.setter
    def replication_interval_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472472dabe3fb80463be2a4f6d56b26f57e7095046beb190cde2cceb45b494f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationIntervalMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceDatasetId")
    def source_dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDatasetId"))

    @source_dataset_id.setter
    def source_dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2c23e3ba499d975d7753639a5b7111b622abf136d484360b68934cee2f569d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDatasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceProjectId")
    def source_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceProjectId"))

    @source_project_id.setter
    def source_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0bc5ed403c4601e10cbfabeb77c50c7f8bd1d21c45f69cc1fad79ffe0244a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceTableId")
    def source_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceTableId"))

    @source_table_id.setter
    def source_table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b211cbee92d92c7f58eb7647eccd8f4a685528648422907a2a1eef1d21523da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceTableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableTableReplicationInfo]:
        return typing.cast(typing.Optional[BigqueryTableTableReplicationInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableTableReplicationInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c396f71ec5a38ba59408905d921258f52f058da78cf10bdf57d44068138b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTimePartitioning",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "expiration_ms": "expirationMs",
        "field": "field",
        "require_partition_filter": "requirePartitionFilter",
    },
)
class BigqueryTableTimePartitioning:
    def __init__(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[jsii.Number] = None,
        field: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: The supported types are DAY, HOUR, MONTH, and YEAR, which will generate one partition per day, hour, month, and year, respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type BigqueryTable#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#expiration_ms BigqueryTable#expiration_ms}
        :param field: The field used to determine how to create a time-based partition. If time-based partitioning is enabled without this value, the table is partitioned based on the load time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field BigqueryTable#field}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb89c8f47dc2aa75c98d1b70fe727492265de34a7f04fcc70fb2ac919a4b609)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument expiration_ms", value=expiration_ms, expected_type=type_hints["expiration_ms"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument require_partition_filter", value=require_partition_filter, expected_type=type_hints["require_partition_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if expiration_ms is not None:
            self._values["expiration_ms"] = expiration_ms
        if field is not None:
            self._values["field"] = field
        if require_partition_filter is not None:
            self._values["require_partition_filter"] = require_partition_filter

    @builtins.property
    def type(self) -> builtins.str:
        '''The supported types are DAY, HOUR, MONTH, and YEAR, which will generate one partition per day, hour, month, and year, respectively.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#type BigqueryTable#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_ms(self) -> typing.Optional[jsii.Number]:
        '''Number of milliseconds for which to keep the storage for a partition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#expiration_ms BigqueryTable#expiration_ms}
        '''
        result = self._values.get("expiration_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''The field used to determine how to create a time-based partition.

        If time-based partitioning is enabled without this value, the table is partitioned based on the load time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#field BigqueryTable#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_partition_filter(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        result = self._values.get("require_partition_filter")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTimePartitioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableTimePartitioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTimePartitioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb1012c6f07e275e2c7ac99db9bd6af2dbbbe5b56308e74d8073d34cf791a6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpirationMs")
    def reset_expiration_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationMs", []))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @jsii.member(jsii_name="resetRequirePartitionFilter")
    def reset_require_partition_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirePartitionFilter", []))

    @builtins.property
    @jsii.member(jsii_name="expirationMsInput")
    def expiration_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationMsInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilterInput")
    def require_partition_filter_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requirePartitionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationMs")
    def expiration_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expirationMs"))

    @expiration_ms.setter
    def expiration_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463cb583811d7bce632cdacc04ef7a813a9464f2fd0935bdb317acbdf50877af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9f1f7e339594c721b212be7ee4b6441e2e4cfba1f61b12bb2bf75f78fa8edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilter")
    def require_partition_filter(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requirePartitionFilter"))

    @require_partition_filter.setter
    def require_partition_filter(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d848604fbd9c70477cd62b8b91073abca4ee3d39caf376d82ad8cb379f3295c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirePartitionFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e229f2df185e40b0ee1aec2c292b2f480e52700cd9e7d4e30c50fd2871166f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableTimePartitioning]:
        return typing.cast(typing.Optional[BigqueryTableTimePartitioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableTimePartitioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57aa79d96b36de527ea884cebcfcccaa556f71725930521bec3778b8be50e098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableView",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "use_legacy_sql": "useLegacySql"},
)
class BigqueryTableView:
    def __init__(
        self,
        *,
        query: builtins.str,
        use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query: A query that BigQuery executes when the view is referenced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#query BigqueryTable#query}
        :param use_legacy_sql: Specifies whether to use BigQuery's legacy SQL for this view. The default value is true. If set to false, the view will use BigQuery's standard SQL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#use_legacy_sql BigqueryTable#use_legacy_sql}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a3916e2251c4ce938996c4d3230e60885f992563fbccd7813ffeeaec1eeada)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument use_legacy_sql", value=use_legacy_sql, expected_type=type_hints["use_legacy_sql"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if use_legacy_sql is not None:
            self._values["use_legacy_sql"] = use_legacy_sql

    @builtins.property
    def query(self) -> builtins.str:
        '''A query that BigQuery executes when the view is referenced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#query BigqueryTable#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_legacy_sql(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to use BigQuery's legacy SQL for this view.

        The default value is true. If set to false, the view will use BigQuery's standard SQL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_table#use_legacy_sql BigqueryTable#use_legacy_sql}
        '''
        result = self._values.get("use_legacy_sql")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableView(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableViewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableViewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5d3a89bee4916b9695c0ff59eb7dadc6367caaf6a57673b503046edf0dcc9bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUseLegacySql")
    def reset_use_legacy_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseLegacySql", []))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="useLegacySqlInput")
    def use_legacy_sql_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useLegacySqlInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722fbc23443a9a33d97f796a37943d92c33e8b32289d7ca8d1190dbf88ecbdea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useLegacySql")
    def use_legacy_sql(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useLegacySql"))

    @use_legacy_sql.setter
    def use_legacy_sql(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7d9b7655097a8ae61f21e1a58fea8369d86360dab40227def1947e1e1193ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLegacySql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableView]:
        return typing.cast(typing.Optional[BigqueryTableView], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BigqueryTableView]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7686a49feb74dbf2c8805b0999264b2707d637196b1090f8df1405c64fa0fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryTable",
    "BigqueryTableBiglakeConfiguration",
    "BigqueryTableBiglakeConfigurationOutputReference",
    "BigqueryTableConfig",
    "BigqueryTableEncryptionConfiguration",
    "BigqueryTableEncryptionConfigurationOutputReference",
    "BigqueryTableExternalCatalogTableOptions",
    "BigqueryTableExternalCatalogTableOptionsOutputReference",
    "BigqueryTableExternalCatalogTableOptionsStorageDescriptor",
    "BigqueryTableExternalCatalogTableOptionsStorageDescriptorOutputReference",
    "BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo",
    "BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfoOutputReference",
    "BigqueryTableExternalDataConfiguration",
    "BigqueryTableExternalDataConfigurationAvroOptions",
    "BigqueryTableExternalDataConfigurationAvroOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationBigtableOptions",
    "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily",
    "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn",
    "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnList",
    "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumnOutputReference",
    "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyList",
    "BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyOutputReference",
    "BigqueryTableExternalDataConfigurationBigtableOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationCsvOptions",
    "BigqueryTableExternalDataConfigurationCsvOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationGoogleSheetsOptions",
    "BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationHivePartitioningOptions",
    "BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationJsonOptions",
    "BigqueryTableExternalDataConfigurationJsonOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationOutputReference",
    "BigqueryTableExternalDataConfigurationParquetOptions",
    "BigqueryTableExternalDataConfigurationParquetOptionsOutputReference",
    "BigqueryTableMaterializedView",
    "BigqueryTableMaterializedViewOutputReference",
    "BigqueryTableRangePartitioning",
    "BigqueryTableRangePartitioningOutputReference",
    "BigqueryTableRangePartitioningRange",
    "BigqueryTableRangePartitioningRangeOutputReference",
    "BigqueryTableSchemaForeignTypeInfo",
    "BigqueryTableSchemaForeignTypeInfoOutputReference",
    "BigqueryTableTableConstraints",
    "BigqueryTableTableConstraintsForeignKeys",
    "BigqueryTableTableConstraintsForeignKeysColumnReferences",
    "BigqueryTableTableConstraintsForeignKeysColumnReferencesOutputReference",
    "BigqueryTableTableConstraintsForeignKeysList",
    "BigqueryTableTableConstraintsForeignKeysOutputReference",
    "BigqueryTableTableConstraintsForeignKeysReferencedTable",
    "BigqueryTableTableConstraintsForeignKeysReferencedTableOutputReference",
    "BigqueryTableTableConstraintsOutputReference",
    "BigqueryTableTableConstraintsPrimaryKey",
    "BigqueryTableTableConstraintsPrimaryKeyOutputReference",
    "BigqueryTableTableReplicationInfo",
    "BigqueryTableTableReplicationInfoOutputReference",
    "BigqueryTableTimePartitioning",
    "BigqueryTableTimePartitioningOutputReference",
    "BigqueryTableView",
    "BigqueryTableViewOutputReference",
]

publication.publish()

def _typecheckingstub__b097032883d450d5b0dd2683567f8b829165b537d5a8be476cbb660ce43d5747(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_id: builtins.str,
    table_id: builtins.str,
    biglake_configuration: typing.Optional[typing.Union[BigqueryTableBiglakeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[BigqueryTableEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    expiration_time: typing.Optional[jsii.Number] = None,
    external_catalog_table_options: typing.Optional[typing.Union[BigqueryTableExternalCatalogTableOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    external_data_configuration: typing.Optional[typing.Union[BigqueryTableExternalDataConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_auto_generated_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_schema_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    materialized_view: typing.Optional[typing.Union[BigqueryTableMaterializedView, typing.Dict[builtins.str, typing.Any]]] = None,
    max_staleness: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    range_partitioning: typing.Optional[typing.Union[BigqueryTableRangePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    schema: typing.Optional[builtins.str] = None,
    schema_foreign_type_info: typing.Optional[typing.Union[BigqueryTableSchemaForeignTypeInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    table_constraints: typing.Optional[typing.Union[BigqueryTableTableConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    table_metadata_view: typing.Optional[builtins.str] = None,
    table_replication_info: typing.Optional[typing.Union[BigqueryTableTableReplicationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    time_partitioning: typing.Optional[typing.Union[BigqueryTableTimePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    view: typing.Optional[typing.Union[BigqueryTableView, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6c63bb4b9fd744406390cf66f7b1566dc5801d712accd67b66fb9c4fca46ac4f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36a827767218e30e15ed46c620f1d6ac1649ac81e9a1f8fbf50b44994a8de7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ba56c49b068bbf8763ea0042060807cbf89b0406ef980ed1fc45513c07dca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62578b34b021403200b1036268e3acd655157cb771a72f5d129bf260f4c27cf2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c0bfe985825d9a80acd8f5aefedd8901d464dacf94af409b2a81efccfc3fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5413b10f3ec29a1d03f7c2f42f492fee9e3d71fa450c28d4bd6f46ef3ef51e77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b95bd39489b26bd16347f815db6f92fba878214004df53fa734ec6f798849ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af66ed510248d931e4bb1f43b218cca02cd6069e76f18cdb7150e9530186201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d9c292ece217d3549642355546610c9c921d03644d0036d53e2f4b01de2916(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3299834edde10412dba8507dd9bbb1103c12e86905ca5fd8dbc00415deaf5058(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c74889bf00ce24f484abd1bc28bf3cf7d61665b2ab8f55381086fce8f1291c4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc79c2fa24fcd8108b4d32f5f2411cc78630355878d937c6df66e6330c75711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1a6d53539cb352313127bc88400bfb27109837e44e77e3c2445bb3a3ceaa22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baca9cd111dd2c321ea33796f0042eb16fce60720708bc62959bbce16e17e6e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8578b4a8db03882361789b6dcd1c8943a41c5e0b12027987a63f64f259b86762(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570adc90f3ed8491972bb571ec80eb5f0b0fdf5931d71a249e93fd1f993d7b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ff67f97457c05dfe2bdc38c7d1b6d4d3ab19d3aed9a3b6ab5e87619edf6da4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3b81c8674496306bcc75d720b6c39b4af02782c243df31969f5495909ac5b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dccd07ead4367a3bc4cd191ef4729bd296220175d0b8991db980fd2af262039(
    *,
    connection_id: builtins.str,
    file_format: builtins.str,
    storage_uri: builtins.str,
    table_format: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a509fe31b2c6b19f7ecf2c52c8c10d233620b2b0723b2cc93a464c36d4863ffe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500bfdde294f601a4372c18ff5821627c35f3ca1684395e3b29a63c109af86bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ce961f3aef0437fc73f474e2fa2710c4ba6c077e27fb379976f4d48156b777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cf859df62ab61eb1f8f4f07a9b43fdd93cc8e623b853f57d4cfb39b69eb913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2743cf8f9612f2920af6ed5f715f0dbfc1b4f095010aac0dd76e4f87cf22b15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a1e361e20f5b31aff949115dab66215002a3b8936dcb653eace5de1dc5234e(
    value: typing.Optional[BigqueryTableBiglakeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a75785b12d60945a47678d02ebd6a12a808d31eb6207fa82349d07fd479f943(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_id: builtins.str,
    table_id: builtins.str,
    biglake_configuration: typing.Optional[typing.Union[BigqueryTableBiglakeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[BigqueryTableEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    expiration_time: typing.Optional[jsii.Number] = None,
    external_catalog_table_options: typing.Optional[typing.Union[BigqueryTableExternalCatalogTableOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    external_data_configuration: typing.Optional[typing.Union[BigqueryTableExternalDataConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_auto_generated_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_schema_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    materialized_view: typing.Optional[typing.Union[BigqueryTableMaterializedView, typing.Dict[builtins.str, typing.Any]]] = None,
    max_staleness: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    range_partitioning: typing.Optional[typing.Union[BigqueryTableRangePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    schema: typing.Optional[builtins.str] = None,
    schema_foreign_type_info: typing.Optional[typing.Union[BigqueryTableSchemaForeignTypeInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    table_constraints: typing.Optional[typing.Union[BigqueryTableTableConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    table_metadata_view: typing.Optional[builtins.str] = None,
    table_replication_info: typing.Optional[typing.Union[BigqueryTableTableReplicationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    time_partitioning: typing.Optional[typing.Union[BigqueryTableTimePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    view: typing.Optional[typing.Union[BigqueryTableView, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b602152e3492b2b9cf562d37b34e16cd46fcdd5aebb8344fde8383837c318d(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af10cc39b5f5ba6eded054f31ffbd4706d4231d04b57aedc127bf4e576f255b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159555baf2bda86fb2b1cb4f203eb8889cd2ec3395162f7d34f6b3bf4bdb405a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fca302717ac54bb59f5552189434c71d9bec42d7b2a28bf6430bf5e7c4f8c84(
    value: typing.Optional[BigqueryTableEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b0e3afe094e8b99db0d67fb8396e0f1b4b708c334fc80353487a3c8d980b11(
    *,
    connection_id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    storage_descriptor: typing.Optional[typing.Union[BigqueryTableExternalCatalogTableOptionsStorageDescriptor, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff7d282da9c093166083df1ab1763a234a96fbb4b6847a5747c6a741e74cb6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afac7e00b4f26e85d005cc14449a8c185ddc1b092cb275fc68b95cd6fd63dd7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4911693fc40ac447b03a5fe76a98dfff32fb98a28671e9b2464e86be482652c9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e3215e90124bb7b0e2fe9e387bccb6b1c48f83d8d4e752676433a3cb9a118a(
    value: typing.Optional[BigqueryTableExternalCatalogTableOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920b87282493d65c1c922bb25140bfa1bb7dc93a2b901231d76e1256d1d18228(
    *,
    input_format: typing.Optional[builtins.str] = None,
    location_uri: typing.Optional[builtins.str] = None,
    output_format: typing.Optional[builtins.str] = None,
    serde_info: typing.Optional[typing.Union[BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee992d881595b02d854c0be415c3e2f869b1519856351129a2bfa4355ea92c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ad8698af7da0e26a568ae6c52ae4f6303a00bebf61e90a4f8d4045b2e90d74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2237726f998dbb574c43b22493f4c4fec065db28ff403fce6ef7fb421dea7d2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93964b4c2276115b4fd364d73d8e84b87cb959fe5adb8758bf5900ebd04aaa5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134a34a850a6cec544046568009519f9508f1f6d14ad6b39b6c9706ee20448c0(
    value: typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4886efe8b4a4296e9c7e29778779a2593d55d95f6f98ac90dbc48ccb7c10443e(
    *,
    serialization_library: builtins.str,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1931f62454ceb27c66621bd9d2b6f42011781cd36fe19c5c1b6c597b6772050(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2976fd59ea71494a4c0b092a9c55986498d7c421a9d55b859ba768138eacc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2424fe3f5e0e6aef2d07dbc581c92457f2c2a44da8d22d2ae929817b757104c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d65a3b21682b815457483059f3fde4b4c9434deef165adb0faf88be5c521ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90e677f5d706ef832e2cad3ba694971fc877415fc30730861bac752b80dc693(
    value: typing.Optional[BigqueryTableExternalCatalogTableOptionsStorageDescriptorSerdeInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c60ab8fdd68e02c385fb19a744285eb35baeda52e37f6cea6837e2b0f015c1(
    *,
    autodetect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    source_uris: typing.Sequence[builtins.str],
    avro_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationAvroOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    bigtable_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compression: typing.Optional[builtins.str] = None,
    connection_id: typing.Optional[builtins.str] = None,
    csv_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    file_set_spec_type: typing.Optional[builtins.str] = None,
    google_sheets_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationGoogleSheetsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_partitioning_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationHivePartitioningOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_extension: typing.Optional[builtins.str] = None,
    json_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    max_bad_records: typing.Optional[jsii.Number] = None,
    metadata_cache_mode: typing.Optional[builtins.str] = None,
    object_metadata: typing.Optional[builtins.str] = None,
    parquet_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationParquetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    reference_file_schema_uri: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
    source_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020a0a10768b90ca49555c5e7a89b9faabb072bc6d5bf986be581e51358bb59e(
    *,
    use_avro_logical_types: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fd5bb8fb0dfbc052fe96da13cf662d0ad0a733594bb360e47c8249fcf45082(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be785777b38b52889c2672086fa4df78e5b5176f5807463eaa63b17717b5921(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fcc8f040d82e48ec6840d2bc03598108e4065f5975b2f5eee455518f4ece75(
    value: typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7334e17337fa62ad6afad6315e2f65b99f922fdfacc1ee639d8141db00027780(
    *,
    column_family: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ignore_unspecified_column_families: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_column_families_as_json: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_rowkey_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611f92f3c0b7a1b44ab7bf6517ffd7f5738de788ec8d6bfda2ee0a63e975a78c(
    *,
    column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encoding: typing.Optional[builtins.str] = None,
    family_id: typing.Optional[builtins.str] = None,
    only_read_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4b0982793fc5bb5ca68003758c0c10b36daba98208b4e87dedd3e52966db19(
    *,
    encoding: typing.Optional[builtins.str] = None,
    field_name: typing.Optional[builtins.str] = None,
    only_read_latest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    qualifier_encoded: typing.Optional[builtins.str] = None,
    qualifier_string: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4b3a7e80bf6653d05927e73e9db1706f3be3446bd09fee767de34a0cd95226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ceb23f7a9470e888c75c3b849c88acddc0ae33ca65604de0ce33ab62b5fd466(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fa499b4fcbe5af9c8819f2535dc369e350419afca8bcbcb4a7e65cd9a47c05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab220eb0cdd216790a4e703dc5366bfa7e8af60fba8f7a26410270756e908861(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26de8a0b9c0bd866fd2674ed89ec532a9b76782f607ff21d1b5bbccbde2fe0e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109e0d5fe26759686fa7daf46093a8ca495afceb15589675f52d6e4056b84124(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d352f57c76b71511cfae9b9f7b17ae2677b6ea95583c7e863c4291cabf23cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368d216c6c5f35275232d6eef3e140338c6bfa3ff85ea6c8fce8c6a790117f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56ffdeb3280bd7156512b88cffecddac88731db092ae20dc7c2f2b70aec0211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399efea2fd63f12a0c8db58e974f99318b6bfc82c8721de96caef42135e34e48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8f4ad5a87da983318fdafe4f7467adcbf602e0dc7dd01aff356ea2cdd71699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa7e6c4d58c7d1b39d275abea6ba64c4ce1453d18f648f9b5aeb55862c375d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431cd7b910e92659ceb3f80da9fe185d674d5ef12895e9778e7a3c787b7e2d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f84994a813138d1b8733925d81904b8c13eb1712f67d11a302ba7bfb473be3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3cb703d3d685cd5e426341638ee3328420a1450f01ebf3c49ad8270c2871d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfe62a10624576c07c310e2b36b5fc8c3870cbd927348514fc90efbd2453bd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7110c41b66bb6e3f0385ab2bf13f55e729985f3dc5232b63c639fef6e291a86a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5848d4798f2d8ae4b99fe368ea27d0166d9d95cf638513c0d18c4b9c3755fbe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8e5f895b1d36628333cb2cf9b3925a393671a6c76d10a27e5165f0a5b1ccdf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a175f1a9edc4f7fa90883e85d1f60bb9044d6a3708ecdb982bb92c40b1c6be5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4402f369b45b17dbe24f5ef95c786d3716c80abe37168d84e5557dc34ec30067(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca9c9b7e8603068c5ffaa8b0440eb396dc499a28263089df035beb1214af2db(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamilyColumn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81144d7a754f069044508cc760ef844929ad769bdbdc9425dfbb3b390813d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce804c611c2d79dcb397ddad3870fbf4d438afccafd8dfdf24c24a581c06a510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1881b1771792f5afa7e07e18416bd32cad8d0a9c846e3390ac23926f27974f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826a3155e4b15f225642e1a79c934a13ff9fa94b0ab6abd9c10c27ce59ae50b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac8abfca4365b5b9fbe395d433ef66f10130069c4261da3570bad256dabfe98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d80810fce706dc5193a2da41a70396b30325588e504ff5c5d1eb52ea7f4dbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2de31968af73c7f388ebf3e27b0a0516fca03a3c61b63b92e41e7728eb2c49(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableExternalDataConfigurationBigtableOptionsColumnFamily, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece32edd05a4ce36393d56d4103415342e558e089d9e1197d55ac0fe00684c85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8ecf85f96d55bb2504496cf85a8cc7ec5a0e4cdf4e7b843b5db043bd7c2656(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f7e132e662c0231d0d91659efb772067d08f86365a36ce35370659adb580e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bb6b496e771c1a1cf6fed701ec0c2e4780a8a7d887a8a3386ba9bfb8ac37b1(
    value: typing.Optional[BigqueryTableExternalDataConfigurationBigtableOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbe70f4df9985ff876e0f2ae8cd3f32cc7a5d0424dcd4f97052fc74b0e00937(
    *,
    quote: builtins.str,
    allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    skip_leading_rows: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60af4fc24e71e637c6fa900482563f246e261e062f3062c295a2bad98420962(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e73d09915846f7821d69bbaafe21042ed21254594e34719c29494cb50b3a92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e69d30776a200962cdf1ae7dbfec1ed9bc8dd3a8bbc993e020ff52eee4a4e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97b74c86bec5163696d29826bf6274501cc5d15f5a8981eecd353bafe0ad6d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4ef4f6ceb6adf5f5e4f857fe2a3abfa9551e8515e1c01b43f46ad903e65a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c97c66ebe5dd4be082754498f497e0dd3a039989089797867763631092e415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750a54e77026baaefd7596886e1ff0599ce1f18278039fa40bd4ab7b0e00e47a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49253d1d598fd8a759e5fb7260bd43f838344fc041171c17e9fdb960f0bca7ac(
    value: typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d038f67db09f696cd8f12f3dd998ac5d9aaa643c029b6323a5865470d5e1bb13(
    *,
    range: typing.Optional[builtins.str] = None,
    skip_leading_rows: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc19019d32a22a60c6a9ca6c1e9a76258e4553f4456f2df92bef8f673d7390c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37f5f39bd5216808ff0bfd8dfaf4e99a1f1c79731e27bae75778a2d3136bea5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52592b7fc99331f5d59d8b9949f4a4ec26a81695186d39a91dc86b408c9263e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74e3e17939cb2af1a1dda80388692345f22ee6e9ebbbc005cef5c75e631246d(
    value: typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810784a6342c4175b64b73278d9e89558c903464868b3a31434d1454105155a7(
    *,
    mode: typing.Optional[builtins.str] = None,
    require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_uri_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427d241048413617b3bd3a828418f1d0ac690b71dfe0d2e2068199e9bddd2441(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01a839fea9d2d522ebdb2c7d2a742aa9480bdbd7bb8032c9a1cb98fb08540e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a766f84b3d43b2709c94c8f8521d26c341493a08ed89bef1a658cffcf736efc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece8fc4dc9da2b45528b8120676c44420820ae71ca2379a6b811788655de2ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ea00c1a595be450f340f82ebd3b57198a01adae42a7d6bd7aa2a43f9bfbeb3(
    value: typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dec8149763ea2d60862524cfc78a30bfdb3e3f445909cc7308899dbbe3dad3e(
    *,
    encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55435ebdfa949ad7443de43d41be8a51657e616280bfb76550dcac29a67c7fdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a08b652d0dfd1f677d39a18d6a228377996d531901dfdfec197db54e29d408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f3bc4705cf0a542c770a4ba7a430740c271f1e1e32cc0f8b25f7fa4bb6935d(
    value: typing.Optional[BigqueryTableExternalDataConfigurationJsonOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aedd3ec19da32a66f5345c97d51ab2ec0daa172ece609031aadaa848060186d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa92013cd8c6f4654573bca59cada4acf1ab4fa24e0c33e4d4183250eea524a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171e466428ef05f4c723a94ae4be4749554bd2eea5cd174382809e39dc1531e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b513971418e35e0889daa1af0c24cd9d68fe2c0c11f24a4107c11bdd933e16b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec15ce63e9c828984a5d7f41096c3695022e6115b14821a07a91f3e4bbd5448(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a59007098ead2bf4df9dc5cfcdcf21549a84089fbee66a5e258d3fd9a97d35(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26036ad0a935ab122cb8292288b221d29c5c83df4c9ef6a251f72defd50f6a0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d69f7654bb9a49339cdf5f1425dadb79c83dad7cad0ee4c0b95ee260bcf1b1b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb09cd9d1c318de492a7c2211d2e38e5ef97cc409f9e3ca3680609b1ed487a05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299af1e3e836561fcb503c63c0716231093c196a6ddfad2175cfd1fe62e17814(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213c2a36ef7a804e14ba80c930b6fd7a3688ffe9e23f248712dce815b05a86f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0884b65b0bdd6567b088bb09c59a013f1c64f0c864984a8075b6a4e371875e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a03112d506997097f3ea5d211e0cd0d133f64fde4a35c3bc1ceafc857b28a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2411a1cf8a70ffbcaa7d39b40a4d65c9ac8a09f10bddc890f5e9f3dfa59fd1c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a895f0de550b51ae084bc84300b10c9de0fb66c609b0968fc28545ce0c6a53(
    value: typing.Optional[BigqueryTableExternalDataConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e580c4d966a2cc25478344c0e79c9c6342f4aee2890c85d19c972100dab08977(
    *,
    enable_list_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enum_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c21531b9bf1753605c506d734d31f8c05da55a2e18787c846ba0f11523e334(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5908d98cdfb96a6db3cf813b2c415271f41e5255d612906ebf4a29558cab5bbb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bac64ebafef3ca5bea0ec86252a289d94c58f429837110b52e4febffd0ad127(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690db45b00cc068b07c9eef643410cc67f91cc6b39bd826b690fa3bac49b737d(
    value: typing.Optional[BigqueryTableExternalDataConfigurationParquetOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bfac7ffc7a9089b8ef1d3b22082c499bb74076ee32063e98bfc14ba774af19(
    *,
    query: builtins.str,
    allow_non_incremental_definition: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    refresh_interval_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a06199473432610a340d54e912a27a45d9838f276f5ddefb8ea5ed442551b84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57984ff9f86a6b8017c67bd873d16cb38383fa841cb1c329b4e6cc1039c2919b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95c47f7821838b81eb06f48bf5b0c5aed91c07011b4d48d8073fce2186f17bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fea0c74fd4684d8ad56faaf0179f2f5bb721644dff852d3e6979f302106755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9657a3990dc569b85efe467953e2b35134c6d571e8a9003d13db7d882c11d771(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35804a2287301e8b044546610ce9f0fb372c6b235f2ade6d86c3105305e0f8c0(
    value: typing.Optional[BigqueryTableMaterializedView],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdcc485551cdda9350f0ec3b6f635fb181dfeb360e8a64dc8017a129edb17bf(
    *,
    field: builtins.str,
    range: typing.Union[BigqueryTableRangePartitioningRange, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5846667bda1a92cfa7b2128c33f2548d65ee779e39fcfee01fc1ed16c3071bdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395c6f6f36489faff4acf790a2a2cc1c21f8f9966c5ef9a170a50199315505e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ed36eb55e507419b8535e2c7cafa45c85bff6123571a8edb4886a44bacae48(
    value: typing.Optional[BigqueryTableRangePartitioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69572fe55635746c6c943f6472627f9914d257e914d14e8158134965b8a38fb4(
    *,
    end: jsii.Number,
    interval: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e346b07c1bf2602c604ad14a57886686548a1aa4a51a38351b11b562dc21085(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2b695fdea4b4df8ca95b67883601572c7925871a37b6a6422ddb8f986cab0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3633200eb7491ca91f5312d0e52d612aafd64c3a611f85726166d54ad0765116(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f689dce76260a1d7c60657cf8bca91a3d9a497d6f1788949e150195b1c9820(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19729f38363279736c21ff6e0255ab435dae55bb7e61e454e836a44d18820d73(
    value: typing.Optional[BigqueryTableRangePartitioningRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7420a9b9b94a9461f6490dac852736f6e4ed9faeabd266e2342653d72f53a32(
    *,
    type_system: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f81ad197e874f23809ef138d38b926f76d492b315b2d28aa38aa88c841dc852(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f483fcd6c0328f2ab60823f093560799024bea885887802d187b9d34343da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f2484934af76611be99a81a47064a10bbbb595d376abed94ac499ad99ff49a(
    value: typing.Optional[BigqueryTableSchemaForeignTypeInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66412678e0af26f8b78798f0102a6b1ea68db9f05edf807a3cd7fa94d235c56(
    *,
    foreign_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableTableConstraintsForeignKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    primary_key: typing.Optional[typing.Union[BigqueryTableTableConstraintsPrimaryKey, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f61370d43968c22f52ef6734d2e77d1a8a96dd965a869b48860662ee6a21722(
    *,
    column_references: typing.Union[BigqueryTableTableConstraintsForeignKeysColumnReferences, typing.Dict[builtins.str, typing.Any]],
    referenced_table: typing.Union[BigqueryTableTableConstraintsForeignKeysReferencedTable, typing.Dict[builtins.str, typing.Any]],
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124b9358eb11410c5cc7b746109df639f5aeb5a0187a99866457543232b33213(
    *,
    referenced_column: builtins.str,
    referencing_column: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef1fba74406c995d56a4dab9e0db702753afab608a07cdb9b37c2fd9bd1e60d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc52fea06ba2300d376003a0cb48490bfd95c1077e6abd6471cbf81e6eef15ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4735a4c0b6173bbc5687e6c13dca78d807c63288f93813f4738e4769cead18b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05b700cf16429be44e70ac0074b1d8eece74f899cc760c21cd1721ac11b7da1(
    value: typing.Optional[BigqueryTableTableConstraintsForeignKeysColumnReferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c756f29f1215ccd7ac0060b571d65fafdb1947164c0ed08b9881fec8ce62d52d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8c7f5a9ff56b07445407b65df99256ece2c9e6ca1efd4af3506bf73b929ac0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ece3323761b1d97ecedb617f03c06d4173c9ceddaf5a5e504220c1f63f29b62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711588ff5bfdfee301a7e68c1274a6b573c182fb9bb80281639b9b0534cdf4ce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9989e18a083944a74bf1085e3d10de10062cac2034298754dae460c44b878497(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a03f2179150028ae4d02dde02a6a8eb1758c6fa5acc045485b3f2c92d910ae0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryTableTableConstraintsForeignKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1deacd089d448db4567dc11360f6f185222d7bd24cb840e9955ee2e68a5d9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75675d4550bcb2658a5fcd41dc689470826bc3798f62fec465792a3c952801b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e519e26935bf6c9b9f013b8e96dbd65d24c5e4801ffe5cbeb66d734b0637b21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryTableTableConstraintsForeignKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0498de677b1f2b6280675020b860ec4bbe3cf7017633a54fb6d1a9aaf678fe77(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19e413299c8ff3c038626de3edd7b16c37479424a7883a567c1db834e92a676(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e8749a7fc2226e4735f38a0d13738328082c24fd83cfd96da6c8214f20116e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e035db842824dbfd776d33e11e45d49d32a3732280d2353a9f8c89b8d587ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78170eb408811e1d4ef6457e62b4fbd840e3332ac2716a92d3663aa18119676a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e985db9c3fa037cb23dc1967830b2fd34b517ca60101f63491f069cdd34dab48(
    value: typing.Optional[BigqueryTableTableConstraintsForeignKeysReferencedTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d673047801d7fb42c6396f4f80447d2b507e3b4dd2dc050cd75ffabe062659(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d58cba0938837919b6dcd2ac1a969dce87c59a5e303ec534be1327490141c25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryTableTableConstraintsForeignKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3959b03c3f97b42b2cd251bf03069a3c966436bfda7e3055b2d42db5a69680d(
    value: typing.Optional[BigqueryTableTableConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7c48c97ad365b615185ea236f534b48101a1019d24cb3f7928bfecdaaec9e1(
    *,
    columns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2391852a0c62909fe0eadc8bb4fdc54cbfc6398b2a0f23506d71d1b90e800b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e322b715fc8d22347e8aaf8006a76d5bbc9ffb9217a9ae6dc25915b0e96107(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b82bfc98420341ac9aa3379df25d954f44556f460e27bdf49cd5a181190ae0(
    value: typing.Optional[BigqueryTableTableConstraintsPrimaryKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9dbea1d377c74b24f3288e0105d6a57a108694b1874b635b77bc913ed33c92(
    *,
    source_dataset_id: builtins.str,
    source_project_id: builtins.str,
    source_table_id: builtins.str,
    replication_interval_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783bd33a6f915df8936c5ab4f7ed3587298deb49c51ec9f165eacaffd39aa945(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472472dabe3fb80463be2a4f6d56b26f57e7095046beb190cde2cceb45b494f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2c23e3ba499d975d7753639a5b7111b622abf136d484360b68934cee2f569d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0bc5ed403c4601e10cbfabeb77c50c7f8bd1d21c45f69cc1fad79ffe0244a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b211cbee92d92c7f58eb7647eccd8f4a685528648422907a2a1eef1d21523da2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c396f71ec5a38ba59408905d921258f52f058da78cf10bdf57d44068138b22(
    value: typing.Optional[BigqueryTableTableReplicationInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb89c8f47dc2aa75c98d1b70fe727492265de34a7f04fcc70fb2ac919a4b609(
    *,
    type: builtins.str,
    expiration_ms: typing.Optional[jsii.Number] = None,
    field: typing.Optional[builtins.str] = None,
    require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb1012c6f07e275e2c7ac99db9bd6af2dbbbe5b56308e74d8073d34cf791a6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463cb583811d7bce632cdacc04ef7a813a9464f2fd0935bdb317acbdf50877af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9f1f7e339594c721b212be7ee4b6441e2e4cfba1f61b12bb2bf75f78fa8edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d848604fbd9c70477cd62b8b91073abca4ee3d39caf376d82ad8cb379f3295c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e229f2df185e40b0ee1aec2c292b2f480e52700cd9e7d4e30c50fd2871166f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57aa79d96b36de527ea884cebcfcccaa556f71725930521bec3778b8be50e098(
    value: typing.Optional[BigqueryTableTimePartitioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a3916e2251c4ce938996c4d3230e60885f992563fbccd7813ffeeaec1eeada(
    *,
    query: builtins.str,
    use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d3a89bee4916b9695c0ff59eb7dadc6367caaf6a57673b503046edf0dcc9bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722fbc23443a9a33d97f796a37943d92c33e8b32289d7ca8d1190dbf88ecbdea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7d9b7655097a8ae61f21e1a58fea8369d86360dab40227def1947e1e1193ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7686a49feb74dbf2c8805b0999264b2707d637196b1090f8df1405c64fa0fc4(
    value: typing.Optional[BigqueryTableView],
) -> None:
    """Type checking stubs"""
    pass
