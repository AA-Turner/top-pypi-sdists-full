r'''
# `google_bigquery_job`

Refer to the Terraform Registry for docs: [`google_bigquery_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job).
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


class GoogleBigqueryJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job google_bigquery_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        job_id: builtins.str,
        copy: typing.Optional[typing.Union["GoogleBigqueryJobCopy", typing.Dict[builtins.str, typing.Any]]] = None,
        extract: typing.Optional[typing.Union["GoogleBigqueryJobExtract", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        job_timeout_ms: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load: typing.Optional[typing.Union["GoogleBigqueryJobLoad", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Union["GoogleBigqueryJobQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job google_bigquery_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param job_id: The ID of the job. The ID must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#job_id GoogleBigqueryJob#job_id}
        :param copy: copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#copy GoogleBigqueryJob#copy}
        :param extract: extract block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#extract GoogleBigqueryJob#extract}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#id GoogleBigqueryJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_timeout_ms: Job timeout in milliseconds. If this time limit is exceeded, BigQuery may attempt to terminate the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#job_timeout_ms GoogleBigqueryJob#job_timeout_ms}
        :param labels: The labels associated with this job. You can use these to organize and group your jobs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#labels GoogleBigqueryJob#labels}
        :param load: load block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#load GoogleBigqueryJob#load}
        :param location: The geographic location of the job. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#location GoogleBigqueryJob#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project GoogleBigqueryJob#project}.
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#query GoogleBigqueryJob#query}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#timeouts GoogleBigqueryJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d016de9370127accbfc801d530d02bb263e20df82a9ceede54ac6b1b81ba2f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBigqueryJobConfig(
            job_id=job_id,
            copy=copy,
            extract=extract,
            id=id,
            job_timeout_ms=job_timeout_ms,
            labels=labels,
            load=load,
            location=location,
            project=project,
            query=query,
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
        '''Generates CDKTF code for importing a GoogleBigqueryJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBigqueryJob to import.
        :param import_from_id: The id of the existing GoogleBigqueryJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBigqueryJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c992fedf8d840ad912eadd0b45964382899a897197ef355ce1885f91122c82c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCopy")
    def put_copy(
        self,
        *,
        source_tables: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryJobCopySourceTables", typing.Dict[builtins.str, typing.Any]]]],
        create_disposition: typing.Optional[builtins.str] = None,
        destination_encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryJobCopyDestinationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_table: typing.Optional[typing.Union["GoogleBigqueryJobCopyDestinationTable", typing.Dict[builtins.str, typing.Any]]] = None,
        write_disposition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_tables: source_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_tables GoogleBigqueryJob#source_tables}
        :param create_disposition: Specifies whether the job is allowed to create new tables. The following values are supported: CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table. CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result. Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        :param destination_encryption_configuration: destination_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        :param destination_table: destination_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        :param write_disposition: Specifies the action that occurs if the destination table already exists. The following values are supported: WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result. WRITE_APPEND: If the table already exists, BigQuery appends the data to the table. WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        value = GoogleBigqueryJobCopy(
            source_tables=source_tables,
            create_disposition=create_disposition,
            destination_encryption_configuration=destination_encryption_configuration,
            destination_table=destination_table,
            write_disposition=write_disposition,
        )

        return typing.cast(None, jsii.invoke(self, "putCopy", [value]))

    @jsii.member(jsii_name="putExtract")
    def put_extract(
        self,
        *,
        destination_uris: typing.Sequence[builtins.str],
        compression: typing.Optional[builtins.str] = None,
        destination_format: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        print_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_model: typing.Optional[typing.Union["GoogleBigqueryJobExtractSourceModel", typing.Dict[builtins.str, typing.Any]]] = None,
        source_table: typing.Optional[typing.Union["GoogleBigqueryJobExtractSourceTable", typing.Dict[builtins.str, typing.Any]]] = None,
        use_avro_logical_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_uris: A list of fully-qualified Google Cloud Storage URIs where the extracted table should be written. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_uris GoogleBigqueryJob#destination_uris}
        :param compression: The compression type to use for exported files. Possible values include GZIP, DEFLATE, SNAPPY, and NONE. The default value is NONE. DEFLATE and SNAPPY are only supported for Avro. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#compression GoogleBigqueryJob#compression}
        :param destination_format: The exported file format. Possible values include CSV, NEWLINE_DELIMITED_JSON and AVRO for tables and SAVED_MODEL for models. The default value for tables is CSV. Tables with nested or repeated fields cannot be exported as CSV. The default value for models is SAVED_MODEL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_format GoogleBigqueryJob#destination_format}
        :param field_delimiter: When extracting data in CSV format, this defines the delimiter to use between fields in the exported data. Default is ',' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field_delimiter GoogleBigqueryJob#field_delimiter}
        :param print_header: Whether to print out a header row in the results. Default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#print_header GoogleBigqueryJob#print_header}
        :param source_model: source_model block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_model GoogleBigqueryJob#source_model}
        :param source_table: source_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_table GoogleBigqueryJob#source_table}
        :param use_avro_logical_types: Whether to use logical types when extracting to AVRO format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_avro_logical_types GoogleBigqueryJob#use_avro_logical_types}
        '''
        value = GoogleBigqueryJobExtract(
            destination_uris=destination_uris,
            compression=compression,
            destination_format=destination_format,
            field_delimiter=field_delimiter,
            print_header=print_header,
            source_model=source_model,
            source_table=source_table,
            use_avro_logical_types=use_avro_logical_types,
        )

        return typing.cast(None, jsii.invoke(self, "putExtract", [value]))

    @jsii.member(jsii_name="putLoad")
    def put_load(
        self,
        *,
        destination_table: typing.Union["GoogleBigqueryJobLoadDestinationTable", typing.Dict[builtins.str, typing.Any]],
        source_uris: typing.Sequence[builtins.str],
        allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autodetect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_disposition: typing.Optional[builtins.str] = None,
        destination_encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryJobLoadDestinationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_extension: typing.Optional[builtins.str] = None,
        max_bad_records: typing.Optional[jsii.Number] = None,
        null_marker: typing.Optional[builtins.str] = None,
        parquet_options: typing.Optional[typing.Union["GoogleBigqueryJobLoadParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projection_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        quote: typing.Optional[builtins.str] = None,
        schema_update_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
        source_format: typing.Optional[builtins.str] = None,
        time_partitioning: typing.Optional[typing.Union["GoogleBigqueryJobLoadTimePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        write_disposition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_table: destination_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        :param source_uris: The fully-qualified URIs that point to your data in Google Cloud. For Google Cloud Storage URIs: Each URI can contain one '*' wildcard character and it must come after the 'bucket' name. Size limits related to load jobs apply to external data sources. For Google Cloud Bigtable URIs: Exactly one URI can be specified and it has be a fully specified and valid HTTPS URL for a Google Cloud Bigtable table. For Google Cloud Datastore backups: Exactly one URI can be specified. Also, the '*' wildcard character is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_uris GoogleBigqueryJob#source_uris}
        :param allow_jagged_rows: Accept rows that are missing trailing optional columns. The missing values are treated as nulls. If false, records with missing trailing columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. Only applicable to CSV, ignored for other formats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_jagged_rows GoogleBigqueryJob#allow_jagged_rows}
        :param allow_quoted_newlines: Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_quoted_newlines GoogleBigqueryJob#allow_quoted_newlines}
        :param autodetect: Indicates if we should automatically infer the options and schema for CSV and JSON sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#autodetect GoogleBigqueryJob#autodetect}
        :param create_disposition: Specifies whether the job is allowed to create new tables. The following values are supported: CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table. CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result. Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        :param destination_encryption_configuration: destination_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        :param encoding: The character encoding of the data. The supported values are UTF-8 or ISO-8859-1. The default value is UTF-8. BigQuery decodes the data after the raw, binary data has been split using the values of the quote and fieldDelimiter properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#encoding GoogleBigqueryJob#encoding}
        :param field_delimiter: The separator for fields in a CSV file. The separator can be any ISO-8859-1 single-byte character. To use a character in the range 128-255, you must encode the character as UTF8. BigQuery converts the string to ISO-8859-1 encoding, and then uses the first byte of the encoded string to split the data in its raw, binary state. BigQuery also supports the escape sequence "\\t" to specify a tab separator. The default value is a comma (','). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field_delimiter GoogleBigqueryJob#field_delimiter}
        :param ignore_unknown_values: Indicates if BigQuery should allow extra values that are not represented in the table schema. If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. The sourceFormat property determines what BigQuery treats as an extra value: CSV: Trailing columns JSON: Named values that don't match any column names Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#ignore_unknown_values GoogleBigqueryJob#ignore_unknown_values}
        :param json_extension: If sourceFormat is set to newline-delimited JSON, indicates whether it should be processed as a JSON variant such as GeoJSON. For a sourceFormat other than JSON, omit this field. If the sourceFormat is newline-delimited JSON: - for newline-delimited GeoJSON: set to GEOJSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#json_extension GoogleBigqueryJob#json_extension}
        :param max_bad_records: The maximum number of bad records that BigQuery can ignore when running the job. If the number of bad records exceeds this value, an invalid error is returned in the job result. The default value is 0, which requires that all records are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#max_bad_records GoogleBigqueryJob#max_bad_records}
        :param null_marker: Specifies a string that represents a null value in a CSV file. For example, if you specify "\\N", BigQuery interprets "\\N" as a null value when loading a CSV file. The default value is the empty string. If you set this property to a custom value, BigQuery throws an error if an empty string is present for all data types except for STRING and BYTE. For STRING and BYTE columns, BigQuery interprets the empty string as an empty value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#null_marker GoogleBigqueryJob#null_marker}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#parquet_options GoogleBigqueryJob#parquet_options}
        :param projection_fields: If sourceFormat is set to "DATASTORE_BACKUP", indicates which entity properties to load into BigQuery from a Cloud Datastore backup. Property names are case sensitive and must be top-level properties. If no properties are specified, BigQuery loads all properties. If any named property isn't found in the Cloud Datastore backup, an invalid error is returned in the job result. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#projection_fields GoogleBigqueryJob#projection_fields}
        :param quote: The value that is used to quote data sections in a CSV file. BigQuery converts the string to ISO-8859-1 encoding, and then uses the first byte of the encoded string to split the data in its raw, binary state. The default value is a double-quote ('"'). If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allowQuotedNewlines property to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#quote GoogleBigqueryJob#quote}
        :param schema_update_options: Allows the schema of the destination table to be updated as a side effect of the load job if a schema is autodetected or supplied in the job configuration. Schema update options are supported in two cases: when writeDisposition is WRITE_APPEND; when writeDisposition is WRITE_TRUNCATE and the destination table is a partition of a table, specified by partition decorators. For normal tables, WRITE_TRUNCATE will always overwrite the schema. One or more of the following values are specified: ALLOW_FIELD_ADDITION: allow adding a nullable field to the schema. ALLOW_FIELD_RELAXATION: allow relaxing a required field in the original schema to nullable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#schema_update_options GoogleBigqueryJob#schema_update_options}
        :param skip_leading_rows: The number of rows at the top of a CSV file that BigQuery will skip when loading the data. The default value is 0. This property is useful if you have header rows in the file that should be skipped. When autodetect is on, the behavior is the following: skipLeadingRows unspecified - Autodetect tries to detect headers in the first row. If they are not detected, the row is read as data. Otherwise data is read starting from the second row. skipLeadingRows is 0 - Instructs autodetect that there are no headers and data should be read starting from the first row. skipLeadingRows = N > 0 - Autodetect skips N-1 rows and tries to detect headers in row N. If headers are not detected, row N is just skipped. Otherwise row N is used to extract column names for the detected schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#skip_leading_rows GoogleBigqueryJob#skip_leading_rows}
        :param source_format: The format of the data files. For CSV files, specify "CSV". For datastore backups, specify "DATASTORE_BACKUP". For newline-delimited JSON, specify "NEWLINE_DELIMITED_JSON". For Avro, specify "AVRO". For parquet, specify "PARQUET". For orc, specify "ORC". [Beta] For Bigtable, specify "BIGTABLE". The default value is CSV. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_format GoogleBigqueryJob#source_format}
        :param time_partitioning: time_partitioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#time_partitioning GoogleBigqueryJob#time_partitioning}
        :param write_disposition: Specifies the action that occurs if the destination table already exists. The following values are supported: WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result. WRITE_APPEND: If the table already exists, BigQuery appends the data to the table. WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        value = GoogleBigqueryJobLoad(
            destination_table=destination_table,
            source_uris=source_uris,
            allow_jagged_rows=allow_jagged_rows,
            allow_quoted_newlines=allow_quoted_newlines,
            autodetect=autodetect,
            create_disposition=create_disposition,
            destination_encryption_configuration=destination_encryption_configuration,
            encoding=encoding,
            field_delimiter=field_delimiter,
            ignore_unknown_values=ignore_unknown_values,
            json_extension=json_extension,
            max_bad_records=max_bad_records,
            null_marker=null_marker,
            parquet_options=parquet_options,
            projection_fields=projection_fields,
            quote=quote,
            schema_update_options=schema_update_options,
            skip_leading_rows=skip_leading_rows,
            source_format=source_format,
            time_partitioning=time_partitioning,
            write_disposition=write_disposition,
        )

        return typing.cast(None, jsii.invoke(self, "putLoad", [value]))

    @jsii.member(jsii_name="putQuery")
    def put_query(
        self,
        *,
        query: builtins.str,
        allow_large_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        continuous: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_disposition: typing.Optional[builtins.str] = None,
        default_dataset: typing.Optional[typing.Union["GoogleBigqueryJobQueryDefaultDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryJobQueryDestinationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_table: typing.Optional[typing.Union["GoogleBigqueryJobQueryDestinationTable", typing.Dict[builtins.str, typing.Any]]] = None,
        flatten_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maximum_billing_tier: typing.Optional[jsii.Number] = None,
        maximum_bytes_billed: typing.Optional[builtins.str] = None,
        parameter_mode: typing.Optional[builtins.str] = None,
        priority: typing.Optional[builtins.str] = None,
        schema_update_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_options: typing.Optional[typing.Union["GoogleBigqueryJobQueryScriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_query_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_defined_function_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryJobQueryUserDefinedFunctionResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        write_disposition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param query: SQL query text to execute. The useLegacySql field can be used to indicate whether the query uses legacy SQL or standard SQL. *NOTE*: queries containing `DML language <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language>`_ ('DELETE', 'UPDATE', 'MERGE', 'INSERT') must specify 'create_disposition = ""' and 'write_disposition = ""'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#query GoogleBigqueryJob#query}
        :param allow_large_results: If true and query uses legacy SQL dialect, allows the query to produce arbitrarily large result tables at a slight cost in performance. Requires destinationTable to be set. For standard SQL queries, this flag is ignored and large results are always allowed. However, you must still set destinationTable when result size exceeds the allowed maximum response size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_large_results GoogleBigqueryJob#allow_large_results}
        :param continuous: Whether to run the query as continuous or a regular query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#continuous GoogleBigqueryJob#continuous}
        :param create_disposition: Specifies whether the job is allowed to create new tables. The following values are supported: CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table. CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result. Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        :param default_dataset: default_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#default_dataset GoogleBigqueryJob#default_dataset}
        :param destination_encryption_configuration: destination_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        :param destination_table: destination_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        :param flatten_results: If true and query uses legacy SQL dialect, flattens all nested and repeated fields in the query results. allowLargeResults must be true if this is set to false. For standard SQL queries, this flag is ignored and results are never flattened. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#flatten_results GoogleBigqueryJob#flatten_results}
        :param maximum_billing_tier: Limits the billing tier for this job. Queries that have resource usage beyond this tier will fail (without incurring a charge). If unspecified, this will be set to your project default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#maximum_billing_tier GoogleBigqueryJob#maximum_billing_tier}
        :param maximum_bytes_billed: Limits the bytes billed for this job. Queries that will have bytes billed beyond this limit will fail (without incurring a charge). If unspecified, this will be set to your project default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#maximum_bytes_billed GoogleBigqueryJob#maximum_bytes_billed}
        :param parameter_mode: Standard SQL only. Set to POSITIONAL to use positional (?) query parameters or to NAMED to use named (@myparam) query parameters in this query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#parameter_mode GoogleBigqueryJob#parameter_mode}
        :param priority: Specifies a priority for the query. Default value: "INTERACTIVE" Possible values: ["INTERACTIVE", "BATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#priority GoogleBigqueryJob#priority}
        :param schema_update_options: Allows the schema of the destination table to be updated as a side effect of the query job. Schema update options are supported in two cases: when writeDisposition is WRITE_APPEND; when writeDisposition is WRITE_TRUNCATE and the destination table is a partition of a table, specified by partition decorators. For normal tables, WRITE_TRUNCATE will always overwrite the schema. One or more of the following values are specified: ALLOW_FIELD_ADDITION: allow adding a nullable field to the schema. ALLOW_FIELD_RELAXATION: allow relaxing a required field in the original schema to nullable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#schema_update_options GoogleBigqueryJob#schema_update_options}
        :param script_options: script_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#script_options GoogleBigqueryJob#script_options}
        :param use_legacy_sql: Specifies whether to use BigQuery's legacy SQL dialect for this query. The default value is true. If set to false, the query will use BigQuery's standard SQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_legacy_sql GoogleBigqueryJob#use_legacy_sql}
        :param use_query_cache: Whether to look for the result in the query cache. The query cache is a best-effort cache that will be flushed whenever tables in the query are modified. Moreover, the query cache is only available when a query does not have a destination table specified. The default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_query_cache GoogleBigqueryJob#use_query_cache}
        :param user_defined_function_resources: user_defined_function_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#user_defined_function_resources GoogleBigqueryJob#user_defined_function_resources}
        :param write_disposition: Specifies the action that occurs if the destination table already exists. The following values are supported: WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result. WRITE_APPEND: If the table already exists, BigQuery appends the data to the table. WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        value = GoogleBigqueryJobQuery(
            query=query,
            allow_large_results=allow_large_results,
            continuous=continuous,
            create_disposition=create_disposition,
            default_dataset=default_dataset,
            destination_encryption_configuration=destination_encryption_configuration,
            destination_table=destination_table,
            flatten_results=flatten_results,
            maximum_billing_tier=maximum_billing_tier,
            maximum_bytes_billed=maximum_bytes_billed,
            parameter_mode=parameter_mode,
            priority=priority,
            schema_update_options=schema_update_options,
            script_options=script_options,
            use_legacy_sql=use_legacy_sql,
            use_query_cache=use_query_cache,
            user_defined_function_resources=user_defined_function_resources,
            write_disposition=write_disposition,
        )

        return typing.cast(None, jsii.invoke(self, "putQuery", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create GoogleBigqueryJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#delete GoogleBigqueryJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#update GoogleBigqueryJob#update}.
        '''
        value = GoogleBigqueryJobTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCopy")
    def reset_copy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopy", []))

    @jsii.member(jsii_name="resetExtract")
    def reset_extract(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtract", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJobTimeoutMs")
    def reset_job_timeout_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobTimeoutMs", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLoad")
    def reset_load(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoad", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

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
    @jsii.member(jsii_name="copy")
    def copy(self) -> "GoogleBigqueryJobCopyOutputReference":
        return typing.cast("GoogleBigqueryJobCopyOutputReference", jsii.get(self, "copy"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="extract")
    def extract(self) -> "GoogleBigqueryJobExtractOutputReference":
        return typing.cast("GoogleBigqueryJobExtractOutputReference", jsii.get(self, "extract"))

    @builtins.property
    @jsii.member(jsii_name="jobType")
    def job_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobType"))

    @builtins.property
    @jsii.member(jsii_name="load")
    def load(self) -> "GoogleBigqueryJobLoadOutputReference":
        return typing.cast("GoogleBigqueryJobLoadOutputReference", jsii.get(self, "load"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> "GoogleBigqueryJobQueryOutputReference":
        return typing.cast("GoogleBigqueryJobQueryOutputReference", jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleBigqueryJobStatusList":
        return typing.cast("GoogleBigqueryJobStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBigqueryJobTimeoutsOutputReference":
        return typing.cast("GoogleBigqueryJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userEmail")
    def user_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userEmail"))

    @builtins.property
    @jsii.member(jsii_name="copyInput")
    def copy_input(self) -> typing.Optional["GoogleBigqueryJobCopy"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobCopy"], jsii.get(self, "copyInput"))

    @builtins.property
    @jsii.member(jsii_name="extractInput")
    def extract_input(self) -> typing.Optional["GoogleBigqueryJobExtract"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobExtract"], jsii.get(self, "extractInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobIdInput")
    def job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTimeoutMsInput")
    def job_timeout_ms_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobTimeoutMsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadInput")
    def load_input(self) -> typing.Optional["GoogleBigqueryJobLoad"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobLoad"], jsii.get(self, "loadInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional["GoogleBigqueryJobQuery"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobQuery"], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2bd79b60afb85e4978ad6c85f3192931bdd423abd0bb517f42c1b3e8d43984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @job_id.setter
    def job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20034d4695a355a01ca2738faa21ab4bdd6ee36d9cb3b6a93d01588f65694a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobTimeoutMs")
    def job_timeout_ms(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobTimeoutMs"))

    @job_timeout_ms.setter
    def job_timeout_ms(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5571d4b3576b06994b1c2e852c02a10958967fddd3c6aead60a2c75ecd01c9b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobTimeoutMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35f71566fe67311bc83bdad796a40a414834e750903b4a59daf986bdd93ee9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b18b6b61be1a88807d21cce1db7263c5381fc35c5bac15ba73eca6bc1833ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04693f430e4b5280be17ff83b158b94d5e8bd3f1fb423219d5c9ba410caa225b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "job_id": "jobId",
        "copy": "copy",
        "extract": "extract",
        "id": "id",
        "job_timeout_ms": "jobTimeoutMs",
        "labels": "labels",
        "load": "load",
        "location": "location",
        "project": "project",
        "query": "query",
        "timeouts": "timeouts",
    },
)
class GoogleBigqueryJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        job_id: builtins.str,
        copy: typing.Optional[typing.Union["GoogleBigqueryJobCopy", typing.Dict[builtins.str, typing.Any]]] = None,
        extract: typing.Optional[typing.Union["GoogleBigqueryJobExtract", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        job_timeout_ms: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load: typing.Optional[typing.Union["GoogleBigqueryJobLoad", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Union["GoogleBigqueryJobQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param job_id: The ID of the job. The ID must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#job_id GoogleBigqueryJob#job_id}
        :param copy: copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#copy GoogleBigqueryJob#copy}
        :param extract: extract block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#extract GoogleBigqueryJob#extract}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#id GoogleBigqueryJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_timeout_ms: Job timeout in milliseconds. If this time limit is exceeded, BigQuery may attempt to terminate the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#job_timeout_ms GoogleBigqueryJob#job_timeout_ms}
        :param labels: The labels associated with this job. You can use these to organize and group your jobs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#labels GoogleBigqueryJob#labels}
        :param load: load block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#load GoogleBigqueryJob#load}
        :param location: The geographic location of the job. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#location GoogleBigqueryJob#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project GoogleBigqueryJob#project}.
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#query GoogleBigqueryJob#query}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#timeouts GoogleBigqueryJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(copy, dict):
            copy = GoogleBigqueryJobCopy(**copy)
        if isinstance(extract, dict):
            extract = GoogleBigqueryJobExtract(**extract)
        if isinstance(load, dict):
            load = GoogleBigqueryJobLoad(**load)
        if isinstance(query, dict):
            query = GoogleBigqueryJobQuery(**query)
        if isinstance(timeouts, dict):
            timeouts = GoogleBigqueryJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422be9c12004b415a057025054cf812509a1b8a81c4c31f60e9a3ad38f62dd3b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
            check_type(argname="argument copy", value=copy, expected_type=type_hints["copy"])
            check_type(argname="argument extract", value=extract, expected_type=type_hints["extract"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_timeout_ms", value=job_timeout_ms, expected_type=type_hints["job_timeout_ms"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument load", value=load, expected_type=type_hints["load"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_id": job_id,
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
        if copy is not None:
            self._values["copy"] = copy
        if extract is not None:
            self._values["extract"] = extract
        if id is not None:
            self._values["id"] = id
        if job_timeout_ms is not None:
            self._values["job_timeout_ms"] = job_timeout_ms
        if labels is not None:
            self._values["labels"] = labels
        if load is not None:
            self._values["load"] = load
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if query is not None:
            self._values["query"] = query
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
    def job_id(self) -> builtins.str:
        '''The ID of the job.

        The ID must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). The maximum length is 1,024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#job_id GoogleBigqueryJob#job_id}
        '''
        result = self._values.get("job_id")
        assert result is not None, "Required property 'job_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def copy(self) -> typing.Optional["GoogleBigqueryJobCopy"]:
        '''copy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#copy GoogleBigqueryJob#copy}
        '''
        result = self._values.get("copy")
        return typing.cast(typing.Optional["GoogleBigqueryJobCopy"], result)

    @builtins.property
    def extract(self) -> typing.Optional["GoogleBigqueryJobExtract"]:
        '''extract block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#extract GoogleBigqueryJob#extract}
        '''
        result = self._values.get("extract")
        return typing.cast(typing.Optional["GoogleBigqueryJobExtract"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#id GoogleBigqueryJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_timeout_ms(self) -> typing.Optional[builtins.str]:
        '''Job timeout in milliseconds. If this time limit is exceeded, BigQuery may attempt to terminate the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#job_timeout_ms GoogleBigqueryJob#job_timeout_ms}
        '''
        result = self._values.get("job_timeout_ms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels associated with this job. You can use these to organize and group your jobs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#labels GoogleBigqueryJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def load(self) -> typing.Optional["GoogleBigqueryJobLoad"]:
        '''load block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#load GoogleBigqueryJob#load}
        '''
        result = self._values.get("load")
        return typing.cast(typing.Optional["GoogleBigqueryJobLoad"], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The geographic location of the job. The default value is US.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#location GoogleBigqueryJob#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project GoogleBigqueryJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional["GoogleBigqueryJobQuery"]:
        '''query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#query GoogleBigqueryJob#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional["GoogleBigqueryJobQuery"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBigqueryJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#timeouts GoogleBigqueryJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBigqueryJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopy",
    jsii_struct_bases=[],
    name_mapping={
        "source_tables": "sourceTables",
        "create_disposition": "createDisposition",
        "destination_encryption_configuration": "destinationEncryptionConfiguration",
        "destination_table": "destinationTable",
        "write_disposition": "writeDisposition",
    },
)
class GoogleBigqueryJobCopy:
    def __init__(
        self,
        *,
        source_tables: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryJobCopySourceTables", typing.Dict[builtins.str, typing.Any]]]],
        create_disposition: typing.Optional[builtins.str] = None,
        destination_encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryJobCopyDestinationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_table: typing.Optional[typing.Union["GoogleBigqueryJobCopyDestinationTable", typing.Dict[builtins.str, typing.Any]]] = None,
        write_disposition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_tables: source_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_tables GoogleBigqueryJob#source_tables}
        :param create_disposition: Specifies whether the job is allowed to create new tables. The following values are supported: CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table. CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result. Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        :param destination_encryption_configuration: destination_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        :param destination_table: destination_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        :param write_disposition: Specifies the action that occurs if the destination table already exists. The following values are supported: WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result. WRITE_APPEND: If the table already exists, BigQuery appends the data to the table. WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        if isinstance(destination_encryption_configuration, dict):
            destination_encryption_configuration = GoogleBigqueryJobCopyDestinationEncryptionConfiguration(**destination_encryption_configuration)
        if isinstance(destination_table, dict):
            destination_table = GoogleBigqueryJobCopyDestinationTable(**destination_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7287674d3b6ec771b37810e8c709b0fd45824b4961fa16273641289ed9a138a)
            check_type(argname="argument source_tables", value=source_tables, expected_type=type_hints["source_tables"])
            check_type(argname="argument create_disposition", value=create_disposition, expected_type=type_hints["create_disposition"])
            check_type(argname="argument destination_encryption_configuration", value=destination_encryption_configuration, expected_type=type_hints["destination_encryption_configuration"])
            check_type(argname="argument destination_table", value=destination_table, expected_type=type_hints["destination_table"])
            check_type(argname="argument write_disposition", value=write_disposition, expected_type=type_hints["write_disposition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_tables": source_tables,
        }
        if create_disposition is not None:
            self._values["create_disposition"] = create_disposition
        if destination_encryption_configuration is not None:
            self._values["destination_encryption_configuration"] = destination_encryption_configuration
        if destination_table is not None:
            self._values["destination_table"] = destination_table
        if write_disposition is not None:
            self._values["write_disposition"] = write_disposition

    @builtins.property
    def source_tables(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobCopySourceTables"]]:
        '''source_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_tables GoogleBigqueryJob#source_tables}
        '''
        result = self._values.get("source_tables")
        assert result is not None, "Required property 'source_tables' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobCopySourceTables"]], result)

    @builtins.property
    def create_disposition(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the job is allowed to create new tables.

        The following values are supported:
        CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table.
        CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result.
        Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        '''
        result = self._values.get("create_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_encryption_configuration(
        self,
    ) -> typing.Optional["GoogleBigqueryJobCopyDestinationEncryptionConfiguration"]:
        '''destination_encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        '''
        result = self._values.get("destination_encryption_configuration")
        return typing.cast(typing.Optional["GoogleBigqueryJobCopyDestinationEncryptionConfiguration"], result)

    @builtins.property
    def destination_table(
        self,
    ) -> typing.Optional["GoogleBigqueryJobCopyDestinationTable"]:
        '''destination_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        '''
        result = self._values.get("destination_table")
        return typing.cast(typing.Optional["GoogleBigqueryJobCopyDestinationTable"], result)

    @builtins.property
    def write_disposition(self) -> typing.Optional[builtins.str]:
        '''Specifies the action that occurs if the destination table already exists.

        The following values are supported:
        WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result.
        WRITE_APPEND: If the table already exists, BigQuery appends the data to the table.
        WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.
        Each action is atomic and only occurs if BigQuery is able to complete the job successfully.
        Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        result = self._values.get("write_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobCopy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopyDestinationEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleBigqueryJobCopyDestinationEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2b910f57b28de9cea0a17ac575a6b9d4fc3e9412d213d37121381185d7af94)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table.

        The BigQuery Service Account associated with your project requires access to this encryption key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobCopyDestinationEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobCopyDestinationEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopyDestinationEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61bb7fc567a168eda78d88391c372a16180ba20b2db1c7ec72d7b8b02228f0be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15cc9caa8cc9d87b638ade211e78a9a26039b8f613f789d9a772236a2e9b0279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryJobCopyDestinationEncryptionConfiguration]:
        return typing.cast(typing.Optional[GoogleBigqueryJobCopyDestinationEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobCopyDestinationEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453ab24ea25cf4ae3e19859f4db21ce1ffce823f603716c14de592233d7379e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopyDestinationTable",
    jsii_struct_bases=[],
    name_mapping={
        "table_id": "tableId",
        "dataset_id": "datasetId",
        "project_id": "projectId",
    },
)
class GoogleBigqueryJobCopyDestinationTable:
    def __init__(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7942fffd8225e0f837de7f4ec382d21e410f9a4153914a05ca69763b6dd9c2fb)
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_id": table_id,
        }
        if dataset_id is not None:
            self._values["dataset_id"] = dataset_id
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        '''
        result = self._values.get("dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobCopyDestinationTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobCopyDestinationTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopyDestinationTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e571fb8057b8c8a0ad3e7d7f656562bc7bd20d0451edb83f17035e816f6f47f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetId")
    def reset_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bedefb1c8972bef19fdd9d24424e7edcfd2d4e0b0c97d9278b1436afd188eb21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4c1d75baa8cf9f5139adea93ecc59c2ed9d77552b63c89cbb1bf1c9bd816af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb548f6b9a61576f7b6c8cf9aeed958ed71c049519cddb084bfe7371fde3fce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobCopyDestinationTable]:
        return typing.cast(typing.Optional[GoogleBigqueryJobCopyDestinationTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobCopyDestinationTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1509d6c5eff247e8ea7cee98a4d0903c1dfae7ad2ba8a49c7c4d3ab38cd23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobCopyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__631488c61265e5790e13379be726bfe6a2170a2ebc54bdfc426da88364d705fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinationEncryptionConfiguration")
    def put_destination_encryption_configuration(
        self,
        *,
        kms_key_name: builtins.str,
    ) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        value = GoogleBigqueryJobCopyDestinationEncryptionConfiguration(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putDestinationTable")
    def put_destination_table(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        value = GoogleBigqueryJobCopyDestinationTable(
            table_id=table_id, dataset_id=dataset_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationTable", [value]))

    @jsii.member(jsii_name="putSourceTables")
    def put_source_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryJobCopySourceTables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6b5b078901dd55295e89051ed4e6689c5cdbf1cc40dbbd27f0e00c66b0338a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceTables", [value]))

    @jsii.member(jsii_name="resetCreateDisposition")
    def reset_create_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateDisposition", []))

    @jsii.member(jsii_name="resetDestinationEncryptionConfiguration")
    def reset_destination_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetDestinationTable")
    def reset_destination_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationTable", []))

    @jsii.member(jsii_name="resetWriteDisposition")
    def reset_write_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteDisposition", []))

    @builtins.property
    @jsii.member(jsii_name="destinationEncryptionConfiguration")
    def destination_encryption_configuration(
        self,
    ) -> GoogleBigqueryJobCopyDestinationEncryptionConfigurationOutputReference:
        return typing.cast(GoogleBigqueryJobCopyDestinationEncryptionConfigurationOutputReference, jsii.get(self, "destinationEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="destinationTable")
    def destination_table(self) -> GoogleBigqueryJobCopyDestinationTableOutputReference:
        return typing.cast(GoogleBigqueryJobCopyDestinationTableOutputReference, jsii.get(self, "destinationTable"))

    @builtins.property
    @jsii.member(jsii_name="sourceTables")
    def source_tables(self) -> "GoogleBigqueryJobCopySourceTablesList":
        return typing.cast("GoogleBigqueryJobCopySourceTablesList", jsii.get(self, "sourceTables"))

    @builtins.property
    @jsii.member(jsii_name="createDispositionInput")
    def create_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationEncryptionConfigurationInput")
    def destination_encryption_configuration_input(
        self,
    ) -> typing.Optional[GoogleBigqueryJobCopyDestinationEncryptionConfiguration]:
        return typing.cast(typing.Optional[GoogleBigqueryJobCopyDestinationEncryptionConfiguration], jsii.get(self, "destinationEncryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTableInput")
    def destination_table_input(
        self,
    ) -> typing.Optional[GoogleBigqueryJobCopyDestinationTable]:
        return typing.cast(typing.Optional[GoogleBigqueryJobCopyDestinationTable], jsii.get(self, "destinationTableInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTablesInput")
    def source_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobCopySourceTables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobCopySourceTables"]]], jsii.get(self, "sourceTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="writeDispositionInput")
    def write_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="createDisposition")
    def create_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createDisposition"))

    @create_disposition.setter
    def create_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4e1e18c76693fdb1178e1953708ab7cbd3c631bb99a00c9cf530037106c300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeDisposition")
    def write_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeDisposition"))

    @write_disposition.setter
    def write_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b99339a6775944b08cfce94b3dc0f294865a81e75b4cc64c15953db964d6b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobCopy]:
        return typing.cast(typing.Optional[GoogleBigqueryJobCopy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleBigqueryJobCopy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf34ec45851cc8d36eb7b26951c919ce5d7dec4754995dc4535aad4050e46bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopySourceTables",
    jsii_struct_bases=[],
    name_mapping={
        "table_id": "tableId",
        "dataset_id": "datasetId",
        "project_id": "projectId",
    },
)
class GoogleBigqueryJobCopySourceTables:
    def __init__(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f398a8598a936143bec78bad8df5df250cdbe17e1b261dd8068bf2164f7219)
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_id": table_id,
        }
        if dataset_id is not None:
            self._values["dataset_id"] = dataset_id
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        '''
        result = self._values.get("dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobCopySourceTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobCopySourceTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopySourceTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82b911dc648a5a0e4afe4bf6be1fb8928d089d5e934a1d1731f7d7245bb7d140)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBigqueryJobCopySourceTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117b3ea5bb7db379e3d100bd3ff0d97ade74f6e2d5b7149525de86769f5c5765)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBigqueryJobCopySourceTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5675b05397e9836f8b6814ca03baa20c769deaa40126363e49c4da8cefb9c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7d0e9b9010cac8aae83a9d4581f79fb774a598fa086ecf2681d8ae7e900994b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac6e3192858f43fb1d14b582cdd3d43775cd5ee735063bd23a7b9a94a5d5cde2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobCopySourceTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobCopySourceTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobCopySourceTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f26748dda4e439c270949df7f9ee2fd29abb7f5772630865521298fee1ca1d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobCopySourceTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobCopySourceTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acfc53ddcdbff90420d62d3c492caf4f09b37b376c6095cdd2495e018e5298b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDatasetId")
    def reset_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__04333cf0648c4669e4950aca3b1fc3cd187262f4c1f1e4d4d24210c022c28f10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af666690ad05b81e4555c781d4e730c8d272d6835f73f9104083c9bb9138f76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f2b026e5cc5c9d96b99294fe8d257a777fb842055bf9a2ef8f34f03f580e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobCopySourceTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobCopySourceTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobCopySourceTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b774eec45e581d8110051a8ad065ee31f495de3bb7161d70601ff6a2dd834f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobExtract",
    jsii_struct_bases=[],
    name_mapping={
        "destination_uris": "destinationUris",
        "compression": "compression",
        "destination_format": "destinationFormat",
        "field_delimiter": "fieldDelimiter",
        "print_header": "printHeader",
        "source_model": "sourceModel",
        "source_table": "sourceTable",
        "use_avro_logical_types": "useAvroLogicalTypes",
    },
)
class GoogleBigqueryJobExtract:
    def __init__(
        self,
        *,
        destination_uris: typing.Sequence[builtins.str],
        compression: typing.Optional[builtins.str] = None,
        destination_format: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        print_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_model: typing.Optional[typing.Union["GoogleBigqueryJobExtractSourceModel", typing.Dict[builtins.str, typing.Any]]] = None,
        source_table: typing.Optional[typing.Union["GoogleBigqueryJobExtractSourceTable", typing.Dict[builtins.str, typing.Any]]] = None,
        use_avro_logical_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_uris: A list of fully-qualified Google Cloud Storage URIs where the extracted table should be written. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_uris GoogleBigqueryJob#destination_uris}
        :param compression: The compression type to use for exported files. Possible values include GZIP, DEFLATE, SNAPPY, and NONE. The default value is NONE. DEFLATE and SNAPPY are only supported for Avro. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#compression GoogleBigqueryJob#compression}
        :param destination_format: The exported file format. Possible values include CSV, NEWLINE_DELIMITED_JSON and AVRO for tables and SAVED_MODEL for models. The default value for tables is CSV. Tables with nested or repeated fields cannot be exported as CSV. The default value for models is SAVED_MODEL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_format GoogleBigqueryJob#destination_format}
        :param field_delimiter: When extracting data in CSV format, this defines the delimiter to use between fields in the exported data. Default is ',' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field_delimiter GoogleBigqueryJob#field_delimiter}
        :param print_header: Whether to print out a header row in the results. Default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#print_header GoogleBigqueryJob#print_header}
        :param source_model: source_model block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_model GoogleBigqueryJob#source_model}
        :param source_table: source_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_table GoogleBigqueryJob#source_table}
        :param use_avro_logical_types: Whether to use logical types when extracting to AVRO format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_avro_logical_types GoogleBigqueryJob#use_avro_logical_types}
        '''
        if isinstance(source_model, dict):
            source_model = GoogleBigqueryJobExtractSourceModel(**source_model)
        if isinstance(source_table, dict):
            source_table = GoogleBigqueryJobExtractSourceTable(**source_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00e8a8f9c8dc8ef988b5f0a5680fa482da4f46c63fd199ef4d4d373fc12a9ce)
            check_type(argname="argument destination_uris", value=destination_uris, expected_type=type_hints["destination_uris"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument destination_format", value=destination_format, expected_type=type_hints["destination_format"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument print_header", value=print_header, expected_type=type_hints["print_header"])
            check_type(argname="argument source_model", value=source_model, expected_type=type_hints["source_model"])
            check_type(argname="argument source_table", value=source_table, expected_type=type_hints["source_table"])
            check_type(argname="argument use_avro_logical_types", value=use_avro_logical_types, expected_type=type_hints["use_avro_logical_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_uris": destination_uris,
        }
        if compression is not None:
            self._values["compression"] = compression
        if destination_format is not None:
            self._values["destination_format"] = destination_format
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if print_header is not None:
            self._values["print_header"] = print_header
        if source_model is not None:
            self._values["source_model"] = source_model
        if source_table is not None:
            self._values["source_table"] = source_table
        if use_avro_logical_types is not None:
            self._values["use_avro_logical_types"] = use_avro_logical_types

    @builtins.property
    def destination_uris(self) -> typing.List[builtins.str]:
        '''A list of fully-qualified Google Cloud Storage URIs where the extracted table should be written.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_uris GoogleBigqueryJob#destination_uris}
        '''
        result = self._values.get("destination_uris")
        assert result is not None, "Required property 'destination_uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''The compression type to use for exported files.

        Possible values include GZIP, DEFLATE, SNAPPY, and NONE.
        The default value is NONE. DEFLATE and SNAPPY are only supported for Avro.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#compression GoogleBigqueryJob#compression}
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_format(self) -> typing.Optional[builtins.str]:
        '''The exported file format.

        Possible values include CSV, NEWLINE_DELIMITED_JSON and AVRO for tables and SAVED_MODEL for models.
        The default value for tables is CSV. Tables with nested or repeated fields cannot be exported as CSV.
        The default value for models is SAVED_MODEL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_format GoogleBigqueryJob#destination_format}
        '''
        result = self._values.get("destination_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''When extracting data in CSV format, this defines the delimiter to use between fields in the exported data.

        Default is ','

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field_delimiter GoogleBigqueryJob#field_delimiter}
        '''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def print_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to print out a header row in the results. Default is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#print_header GoogleBigqueryJob#print_header}
        '''
        result = self._values.get("print_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_model(self) -> typing.Optional["GoogleBigqueryJobExtractSourceModel"]:
        '''source_model block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_model GoogleBigqueryJob#source_model}
        '''
        result = self._values.get("source_model")
        return typing.cast(typing.Optional["GoogleBigqueryJobExtractSourceModel"], result)

    @builtins.property
    def source_table(self) -> typing.Optional["GoogleBigqueryJobExtractSourceTable"]:
        '''source_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_table GoogleBigqueryJob#source_table}
        '''
        result = self._values.get("source_table")
        return typing.cast(typing.Optional["GoogleBigqueryJobExtractSourceTable"], result)

    @builtins.property
    def use_avro_logical_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use logical types when extracting to AVRO format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_avro_logical_types GoogleBigqueryJob#use_avro_logical_types}
        '''
        result = self._values.get("use_avro_logical_types")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobExtract(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobExtractOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobExtractOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22a1c2b7b34a8f265ac7118e30d3bb341caf8542706ccc6d5a6b07d12ae8acd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSourceModel")
    def put_source_model(
        self,
        *,
        dataset_id: builtins.str,
        model_id: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param model_id: The ID of the model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#model_id GoogleBigqueryJob#model_id}
        :param project_id: The ID of the project containing this model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        value = GoogleBigqueryJobExtractSourceModel(
            dataset_id=dataset_id, model_id=model_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putSourceModel", [value]))

    @jsii.member(jsii_name="putSourceTable")
    def put_source_table(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        value = GoogleBigqueryJobExtractSourceTable(
            table_id=table_id, dataset_id=dataset_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putSourceTable", [value]))

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetDestinationFormat")
    def reset_destination_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFormat", []))

    @jsii.member(jsii_name="resetFieldDelimiter")
    def reset_field_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldDelimiter", []))

    @jsii.member(jsii_name="resetPrintHeader")
    def reset_print_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrintHeader", []))

    @jsii.member(jsii_name="resetSourceModel")
    def reset_source_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceModel", []))

    @jsii.member(jsii_name="resetSourceTable")
    def reset_source_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceTable", []))

    @jsii.member(jsii_name="resetUseAvroLogicalTypes")
    def reset_use_avro_logical_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseAvroLogicalTypes", []))

    @builtins.property
    @jsii.member(jsii_name="sourceModel")
    def source_model(self) -> "GoogleBigqueryJobExtractSourceModelOutputReference":
        return typing.cast("GoogleBigqueryJobExtractSourceModelOutputReference", jsii.get(self, "sourceModel"))

    @builtins.property
    @jsii.member(jsii_name="sourceTable")
    def source_table(self) -> "GoogleBigqueryJobExtractSourceTableOutputReference":
        return typing.cast("GoogleBigqueryJobExtractSourceTableOutputReference", jsii.get(self, "sourceTable"))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFormatInput")
    def destination_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationUrisInput")
    def destination_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiterInput")
    def field_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="printHeaderInput")
    def print_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "printHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceModelInput")
    def source_model_input(
        self,
    ) -> typing.Optional["GoogleBigqueryJobExtractSourceModel"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobExtractSourceModel"], jsii.get(self, "sourceModelInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTableInput")
    def source_table_input(
        self,
    ) -> typing.Optional["GoogleBigqueryJobExtractSourceTable"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobExtractSourceTable"], jsii.get(self, "sourceTableInput"))

    @builtins.property
    @jsii.member(jsii_name="useAvroLogicalTypesInput")
    def use_avro_logical_types_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useAvroLogicalTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eba62947dd5a12918f34a30020c2df9ce27c6df730f1045aaf6b7a4857573be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationFormat")
    def destination_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationFormat"))

    @destination_format.setter
    def destination_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75df51095267bfba371e5ded8ec79fab50e0f0126a3730c0bc3c8ce2b936ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationUris")
    def destination_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationUris"))

    @destination_uris.setter
    def destination_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c9787158debc32e5172bb5f63d934a14465cd0e8ae206dfc392246e172d58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldDelimiter"))

    @field_delimiter.setter
    def field_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8ed6d251abb4c038689d471839038fa93db29cecec60469fa02c29599c3b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="printHeader")
    def print_header(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "printHeader"))

    @print_header.setter
    def print_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caacbb8d1d6f38daa7857aa9ff5ff1c43a52d9151460c8ac24ef49f8e12e82de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "printHeader", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9f3085f0d8d2e0572f8b610a3127f85ee5a7a6e35e90ed024b2b93ded7dfd075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAvroLogicalTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobExtract]:
        return typing.cast(typing.Optional[GoogleBigqueryJobExtract], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleBigqueryJobExtract]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1937faa3ea70daad62b16971d15f338dcf103c933f0c068f4fb8b856d727f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobExtractSourceModel",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "model_id": "modelId",
        "project_id": "projectId",
    },
)
class GoogleBigqueryJobExtractSourceModel:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        model_id: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param model_id: The ID of the model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#model_id GoogleBigqueryJob#model_id}
        :param project_id: The ID of the project containing this model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953a33c1ad45eb37b1090a561bffcd44327027840767b0706d80d44d3269f0b9)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "model_id": model_id,
            "project_id": project_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_id(self) -> builtins.str:
        '''The ID of the model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#model_id GoogleBigqueryJob#model_id}
        '''
        result = self._values.get("model_id")
        assert result is not None, "Required property 'model_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobExtractSourceModel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobExtractSourceModelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobExtractSourceModelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7120f932732dfa38e6f98d38fa1f2de0e14b77e9225ebd42a115d2e476a65f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="modelIdInput")
    def model_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943e849008d18d961b5053d6f41143bde6dc9b8211704ab4b304a3b4b568c09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelId"))

    @model_id.setter
    def model_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6ae33b9bd9f7e66ebe170c39c0086e896c9a2e55abfad8d64c4721d58bfc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541d51b4ddc432d0913277623206222db26ad569f685868a2bbf05313be0ffe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobExtractSourceModel]:
        return typing.cast(typing.Optional[GoogleBigqueryJobExtractSourceModel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobExtractSourceModel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f79f27fd394ffe7c02b0e181cadd1b027667ed4ddc35a9aedd25247c6216a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobExtractSourceTable",
    jsii_struct_bases=[],
    name_mapping={
        "table_id": "tableId",
        "dataset_id": "datasetId",
        "project_id": "projectId",
    },
)
class GoogleBigqueryJobExtractSourceTable:
    def __init__(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ea5274027064d1b82e2dc12be903c3fa487f501ac44081c13905c1bbd3a79a)
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_id": table_id,
        }
        if dataset_id is not None:
            self._values["dataset_id"] = dataset_id
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        '''
        result = self._values.get("dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobExtractSourceTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobExtractSourceTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobExtractSourceTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef0ac9f97b668763c6bb130640ac20ced1daee46968891bc7c357172de1853c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetId")
    def reset_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__976611dd06e10c6d0ac269066a65306d074a93ae7074d3b0c65b6f9f6ed38622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e886643e1c43f9a395bd1f4f7bedfecd3022675d1e3eea2aa5f62f6d51cee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a73cdab3790b5d932c5983de917e239b3b352a947b1cf0d06f2f67737b4b5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobExtractSourceTable]:
        return typing.cast(typing.Optional[GoogleBigqueryJobExtractSourceTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobExtractSourceTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b627f9bd136a16466b9767327b2740d83ac97576c3d5db9a50af4844e9e142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoad",
    jsii_struct_bases=[],
    name_mapping={
        "destination_table": "destinationTable",
        "source_uris": "sourceUris",
        "allow_jagged_rows": "allowJaggedRows",
        "allow_quoted_newlines": "allowQuotedNewlines",
        "autodetect": "autodetect",
        "create_disposition": "createDisposition",
        "destination_encryption_configuration": "destinationEncryptionConfiguration",
        "encoding": "encoding",
        "field_delimiter": "fieldDelimiter",
        "ignore_unknown_values": "ignoreUnknownValues",
        "json_extension": "jsonExtension",
        "max_bad_records": "maxBadRecords",
        "null_marker": "nullMarker",
        "parquet_options": "parquetOptions",
        "projection_fields": "projectionFields",
        "quote": "quote",
        "schema_update_options": "schemaUpdateOptions",
        "skip_leading_rows": "skipLeadingRows",
        "source_format": "sourceFormat",
        "time_partitioning": "timePartitioning",
        "write_disposition": "writeDisposition",
    },
)
class GoogleBigqueryJobLoad:
    def __init__(
        self,
        *,
        destination_table: typing.Union["GoogleBigqueryJobLoadDestinationTable", typing.Dict[builtins.str, typing.Any]],
        source_uris: typing.Sequence[builtins.str],
        allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autodetect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_disposition: typing.Optional[builtins.str] = None,
        destination_encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryJobLoadDestinationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_extension: typing.Optional[builtins.str] = None,
        max_bad_records: typing.Optional[jsii.Number] = None,
        null_marker: typing.Optional[builtins.str] = None,
        parquet_options: typing.Optional[typing.Union["GoogleBigqueryJobLoadParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        projection_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        quote: typing.Optional[builtins.str] = None,
        schema_update_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
        source_format: typing.Optional[builtins.str] = None,
        time_partitioning: typing.Optional[typing.Union["GoogleBigqueryJobLoadTimePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        write_disposition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_table: destination_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        :param source_uris: The fully-qualified URIs that point to your data in Google Cloud. For Google Cloud Storage URIs: Each URI can contain one '*' wildcard character and it must come after the 'bucket' name. Size limits related to load jobs apply to external data sources. For Google Cloud Bigtable URIs: Exactly one URI can be specified and it has be a fully specified and valid HTTPS URL for a Google Cloud Bigtable table. For Google Cloud Datastore backups: Exactly one URI can be specified. Also, the '*' wildcard character is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_uris GoogleBigqueryJob#source_uris}
        :param allow_jagged_rows: Accept rows that are missing trailing optional columns. The missing values are treated as nulls. If false, records with missing trailing columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. Only applicable to CSV, ignored for other formats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_jagged_rows GoogleBigqueryJob#allow_jagged_rows}
        :param allow_quoted_newlines: Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_quoted_newlines GoogleBigqueryJob#allow_quoted_newlines}
        :param autodetect: Indicates if we should automatically infer the options and schema for CSV and JSON sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#autodetect GoogleBigqueryJob#autodetect}
        :param create_disposition: Specifies whether the job is allowed to create new tables. The following values are supported: CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table. CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result. Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        :param destination_encryption_configuration: destination_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        :param encoding: The character encoding of the data. The supported values are UTF-8 or ISO-8859-1. The default value is UTF-8. BigQuery decodes the data after the raw, binary data has been split using the values of the quote and fieldDelimiter properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#encoding GoogleBigqueryJob#encoding}
        :param field_delimiter: The separator for fields in a CSV file. The separator can be any ISO-8859-1 single-byte character. To use a character in the range 128-255, you must encode the character as UTF8. BigQuery converts the string to ISO-8859-1 encoding, and then uses the first byte of the encoded string to split the data in its raw, binary state. BigQuery also supports the escape sequence "\\t" to specify a tab separator. The default value is a comma (','). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field_delimiter GoogleBigqueryJob#field_delimiter}
        :param ignore_unknown_values: Indicates if BigQuery should allow extra values that are not represented in the table schema. If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. The sourceFormat property determines what BigQuery treats as an extra value: CSV: Trailing columns JSON: Named values that don't match any column names Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#ignore_unknown_values GoogleBigqueryJob#ignore_unknown_values}
        :param json_extension: If sourceFormat is set to newline-delimited JSON, indicates whether it should be processed as a JSON variant such as GeoJSON. For a sourceFormat other than JSON, omit this field. If the sourceFormat is newline-delimited JSON: - for newline-delimited GeoJSON: set to GEOJSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#json_extension GoogleBigqueryJob#json_extension}
        :param max_bad_records: The maximum number of bad records that BigQuery can ignore when running the job. If the number of bad records exceeds this value, an invalid error is returned in the job result. The default value is 0, which requires that all records are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#max_bad_records GoogleBigqueryJob#max_bad_records}
        :param null_marker: Specifies a string that represents a null value in a CSV file. For example, if you specify "\\N", BigQuery interprets "\\N" as a null value when loading a CSV file. The default value is the empty string. If you set this property to a custom value, BigQuery throws an error if an empty string is present for all data types except for STRING and BYTE. For STRING and BYTE columns, BigQuery interprets the empty string as an empty value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#null_marker GoogleBigqueryJob#null_marker}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#parquet_options GoogleBigqueryJob#parquet_options}
        :param projection_fields: If sourceFormat is set to "DATASTORE_BACKUP", indicates which entity properties to load into BigQuery from a Cloud Datastore backup. Property names are case sensitive and must be top-level properties. If no properties are specified, BigQuery loads all properties. If any named property isn't found in the Cloud Datastore backup, an invalid error is returned in the job result. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#projection_fields GoogleBigqueryJob#projection_fields}
        :param quote: The value that is used to quote data sections in a CSV file. BigQuery converts the string to ISO-8859-1 encoding, and then uses the first byte of the encoded string to split the data in its raw, binary state. The default value is a double-quote ('"'). If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allowQuotedNewlines property to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#quote GoogleBigqueryJob#quote}
        :param schema_update_options: Allows the schema of the destination table to be updated as a side effect of the load job if a schema is autodetected or supplied in the job configuration. Schema update options are supported in two cases: when writeDisposition is WRITE_APPEND; when writeDisposition is WRITE_TRUNCATE and the destination table is a partition of a table, specified by partition decorators. For normal tables, WRITE_TRUNCATE will always overwrite the schema. One or more of the following values are specified: ALLOW_FIELD_ADDITION: allow adding a nullable field to the schema. ALLOW_FIELD_RELAXATION: allow relaxing a required field in the original schema to nullable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#schema_update_options GoogleBigqueryJob#schema_update_options}
        :param skip_leading_rows: The number of rows at the top of a CSV file that BigQuery will skip when loading the data. The default value is 0. This property is useful if you have header rows in the file that should be skipped. When autodetect is on, the behavior is the following: skipLeadingRows unspecified - Autodetect tries to detect headers in the first row. If they are not detected, the row is read as data. Otherwise data is read starting from the second row. skipLeadingRows is 0 - Instructs autodetect that there are no headers and data should be read starting from the first row. skipLeadingRows = N > 0 - Autodetect skips N-1 rows and tries to detect headers in row N. If headers are not detected, row N is just skipped. Otherwise row N is used to extract column names for the detected schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#skip_leading_rows GoogleBigqueryJob#skip_leading_rows}
        :param source_format: The format of the data files. For CSV files, specify "CSV". For datastore backups, specify "DATASTORE_BACKUP". For newline-delimited JSON, specify "NEWLINE_DELIMITED_JSON". For Avro, specify "AVRO". For parquet, specify "PARQUET". For orc, specify "ORC". [Beta] For Bigtable, specify "BIGTABLE". The default value is CSV. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_format GoogleBigqueryJob#source_format}
        :param time_partitioning: time_partitioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#time_partitioning GoogleBigqueryJob#time_partitioning}
        :param write_disposition: Specifies the action that occurs if the destination table already exists. The following values are supported: WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result. WRITE_APPEND: If the table already exists, BigQuery appends the data to the table. WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        if isinstance(destination_table, dict):
            destination_table = GoogleBigqueryJobLoadDestinationTable(**destination_table)
        if isinstance(destination_encryption_configuration, dict):
            destination_encryption_configuration = GoogleBigqueryJobLoadDestinationEncryptionConfiguration(**destination_encryption_configuration)
        if isinstance(parquet_options, dict):
            parquet_options = GoogleBigqueryJobLoadParquetOptions(**parquet_options)
        if isinstance(time_partitioning, dict):
            time_partitioning = GoogleBigqueryJobLoadTimePartitioning(**time_partitioning)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327b4ac50c5058c33f8d9bdc8c24244a7fa32cfedc1080124b2356a18ac8f05d)
            check_type(argname="argument destination_table", value=destination_table, expected_type=type_hints["destination_table"])
            check_type(argname="argument source_uris", value=source_uris, expected_type=type_hints["source_uris"])
            check_type(argname="argument allow_jagged_rows", value=allow_jagged_rows, expected_type=type_hints["allow_jagged_rows"])
            check_type(argname="argument allow_quoted_newlines", value=allow_quoted_newlines, expected_type=type_hints["allow_quoted_newlines"])
            check_type(argname="argument autodetect", value=autodetect, expected_type=type_hints["autodetect"])
            check_type(argname="argument create_disposition", value=create_disposition, expected_type=type_hints["create_disposition"])
            check_type(argname="argument destination_encryption_configuration", value=destination_encryption_configuration, expected_type=type_hints["destination_encryption_configuration"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument ignore_unknown_values", value=ignore_unknown_values, expected_type=type_hints["ignore_unknown_values"])
            check_type(argname="argument json_extension", value=json_extension, expected_type=type_hints["json_extension"])
            check_type(argname="argument max_bad_records", value=max_bad_records, expected_type=type_hints["max_bad_records"])
            check_type(argname="argument null_marker", value=null_marker, expected_type=type_hints["null_marker"])
            check_type(argname="argument parquet_options", value=parquet_options, expected_type=type_hints["parquet_options"])
            check_type(argname="argument projection_fields", value=projection_fields, expected_type=type_hints["projection_fields"])
            check_type(argname="argument quote", value=quote, expected_type=type_hints["quote"])
            check_type(argname="argument schema_update_options", value=schema_update_options, expected_type=type_hints["schema_update_options"])
            check_type(argname="argument skip_leading_rows", value=skip_leading_rows, expected_type=type_hints["skip_leading_rows"])
            check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
            check_type(argname="argument time_partitioning", value=time_partitioning, expected_type=type_hints["time_partitioning"])
            check_type(argname="argument write_disposition", value=write_disposition, expected_type=type_hints["write_disposition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_table": destination_table,
            "source_uris": source_uris,
        }
        if allow_jagged_rows is not None:
            self._values["allow_jagged_rows"] = allow_jagged_rows
        if allow_quoted_newlines is not None:
            self._values["allow_quoted_newlines"] = allow_quoted_newlines
        if autodetect is not None:
            self._values["autodetect"] = autodetect
        if create_disposition is not None:
            self._values["create_disposition"] = create_disposition
        if destination_encryption_configuration is not None:
            self._values["destination_encryption_configuration"] = destination_encryption_configuration
        if encoding is not None:
            self._values["encoding"] = encoding
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if ignore_unknown_values is not None:
            self._values["ignore_unknown_values"] = ignore_unknown_values
        if json_extension is not None:
            self._values["json_extension"] = json_extension
        if max_bad_records is not None:
            self._values["max_bad_records"] = max_bad_records
        if null_marker is not None:
            self._values["null_marker"] = null_marker
        if parquet_options is not None:
            self._values["parquet_options"] = parquet_options
        if projection_fields is not None:
            self._values["projection_fields"] = projection_fields
        if quote is not None:
            self._values["quote"] = quote
        if schema_update_options is not None:
            self._values["schema_update_options"] = schema_update_options
        if skip_leading_rows is not None:
            self._values["skip_leading_rows"] = skip_leading_rows
        if source_format is not None:
            self._values["source_format"] = source_format
        if time_partitioning is not None:
            self._values["time_partitioning"] = time_partitioning
        if write_disposition is not None:
            self._values["write_disposition"] = write_disposition

    @builtins.property
    def destination_table(self) -> "GoogleBigqueryJobLoadDestinationTable":
        '''destination_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        '''
        result = self._values.get("destination_table")
        assert result is not None, "Required property 'destination_table' is missing"
        return typing.cast("GoogleBigqueryJobLoadDestinationTable", result)

    @builtins.property
    def source_uris(self) -> typing.List[builtins.str]:
        '''The fully-qualified URIs that point to your data in Google Cloud.

        For Google Cloud Storage URIs: Each URI can contain one '*' wildcard character
        and it must come after the 'bucket' name. Size limits related to load jobs apply
        to external data sources. For Google Cloud Bigtable URIs: Exactly one URI can be
        specified and it has be a fully specified and valid HTTPS URL for a Google Cloud Bigtable table.
        For Google Cloud Datastore backups: Exactly one URI can be specified. Also, the '*' wildcard character is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_uris GoogleBigqueryJob#source_uris}
        '''
        result = self._values.get("source_uris")
        assert result is not None, "Required property 'source_uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allow_jagged_rows(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Accept rows that are missing trailing optional columns.

        The missing values are treated as nulls.
        If false, records with missing trailing columns are treated as bad records, and if there are too many bad records,
        an invalid error is returned in the job result. The default value is false. Only applicable to CSV, ignored for other formats.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_jagged_rows GoogleBigqueryJob#allow_jagged_rows}
        '''
        result = self._values.get("allow_jagged_rows")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_quoted_newlines(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file.

        The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_quoted_newlines GoogleBigqueryJob#allow_quoted_newlines}
        '''
        result = self._values.get("allow_quoted_newlines")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def autodetect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if we should automatically infer the options and schema for CSV and JSON sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#autodetect GoogleBigqueryJob#autodetect}
        '''
        result = self._values.get("autodetect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_disposition(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the job is allowed to create new tables.

        The following values are supported:
        CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table.
        CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result.
        Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        '''
        result = self._values.get("create_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_encryption_configuration(
        self,
    ) -> typing.Optional["GoogleBigqueryJobLoadDestinationEncryptionConfiguration"]:
        '''destination_encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        '''
        result = self._values.get("destination_encryption_configuration")
        return typing.cast(typing.Optional["GoogleBigqueryJobLoadDestinationEncryptionConfiguration"], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The character encoding of the data.

        The supported values are UTF-8 or ISO-8859-1.
        The default value is UTF-8. BigQuery decodes the data after the raw, binary data
        has been split using the values of the quote and fieldDelimiter properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#encoding GoogleBigqueryJob#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''The separator for fields in a CSV file.

        The separator can be any ISO-8859-1 single-byte character.
        To use a character in the range 128-255, you must encode the character as UTF8. BigQuery converts
        the string to ISO-8859-1 encoding, and then uses the first byte of the encoded string to split the
        data in its raw, binary state. BigQuery also supports the escape sequence "\\t" to specify a tab separator.
        The default value is a comma (',').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field_delimiter GoogleBigqueryJob#field_delimiter}
        '''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_unknown_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should allow extra values that are not represented in the table schema.

        If true, the extra values are ignored. If false, records with extra columns are treated as bad records,
        and if there are too many bad records, an invalid error is returned in the job result.
        The default value is false. The sourceFormat property determines what BigQuery treats as an extra value:
        CSV: Trailing columns
        JSON: Named values that don't match any column names

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#ignore_unknown_values GoogleBigqueryJob#ignore_unknown_values}
        '''
        result = self._values.get("ignore_unknown_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def json_extension(self) -> typing.Optional[builtins.str]:
        '''If sourceFormat is set to newline-delimited JSON, indicates whether it should be processed as a JSON variant such as GeoJSON.

        For a sourceFormat other than JSON, omit this field. If the sourceFormat is newline-delimited JSON: - for newline-delimited
        GeoJSON: set to GEOJSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#json_extension GoogleBigqueryJob#json_extension}
        '''
        result = self._values.get("json_extension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_bad_records(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of bad records that BigQuery can ignore when running the job.

        If the number of bad records exceeds this value,
        an invalid error is returned in the job result. The default value is 0, which requires that all records are valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#max_bad_records GoogleBigqueryJob#max_bad_records}
        '''
        result = self._values.get("max_bad_records")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def null_marker(self) -> typing.Optional[builtins.str]:
        '''Specifies a string that represents a null value in a CSV file.

        For example, if you specify "\\N", BigQuery interprets "\\N" as a null value
        when loading a CSV file. The default value is the empty string. If you set this property to a custom value, BigQuery throws an error if an
        empty string is present for all data types except for STRING and BYTE. For STRING and BYTE columns, BigQuery interprets the empty string as
        an empty value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#null_marker GoogleBigqueryJob#null_marker}
        '''
        result = self._values.get("null_marker")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parquet_options(self) -> typing.Optional["GoogleBigqueryJobLoadParquetOptions"]:
        '''parquet_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#parquet_options GoogleBigqueryJob#parquet_options}
        '''
        result = self._values.get("parquet_options")
        return typing.cast(typing.Optional["GoogleBigqueryJobLoadParquetOptions"], result)

    @builtins.property
    def projection_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If sourceFormat is set to "DATASTORE_BACKUP", indicates which entity properties to load into BigQuery from a Cloud Datastore backup.

        Property names are case sensitive and must be top-level properties. If no properties are specified, BigQuery loads all properties.
        If any named property isn't found in the Cloud Datastore backup, an invalid error is returned in the job result.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#projection_fields GoogleBigqueryJob#projection_fields}
        '''
        result = self._values.get("projection_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def quote(self) -> typing.Optional[builtins.str]:
        '''The value that is used to quote data sections in a CSV file.

        BigQuery converts the string to ISO-8859-1 encoding,
        and then uses the first byte of the encoded string to split the data in its raw, binary state.
        The default value is a double-quote ('"'). If your data does not contain quoted sections, set the property value to an empty string.
        If your data contains quoted newline characters, you must also set the allowQuotedNewlines property to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#quote GoogleBigqueryJob#quote}
        '''
        result = self._values.get("quote")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_update_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allows the schema of the destination table to be updated as a side effect of the load job if a schema is autodetected or supplied in the job configuration.

        Schema update options are supported in two cases: when writeDisposition is WRITE_APPEND;
        when writeDisposition is WRITE_TRUNCATE and the destination table is a partition of a table, specified by partition decorators.
        For normal tables, WRITE_TRUNCATE will always overwrite the schema. One or more of the following values are specified:
        ALLOW_FIELD_ADDITION: allow adding a nullable field to the schema.
        ALLOW_FIELD_RELAXATION: allow relaxing a required field in the original schema to nullable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#schema_update_options GoogleBigqueryJob#schema_update_options}
        '''
        result = self._values.get("schema_update_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_leading_rows(self) -> typing.Optional[jsii.Number]:
        '''The number of rows at the top of a CSV file that BigQuery will skip when loading the data.

        The default value is 0. This property is useful if you have header rows in the file that should be skipped.
        When autodetect is on, the behavior is the following:
        skipLeadingRows unspecified - Autodetect tries to detect headers in the first row. If they are not detected,
        the row is read as data. Otherwise data is read starting from the second row.
        skipLeadingRows is 0 - Instructs autodetect that there are no headers and data should be read starting from the first row.
        skipLeadingRows = N > 0 - Autodetect skips N-1 rows and tries to detect headers in row N. If headers are not detected,
        row N is just skipped. Otherwise row N is used to extract column names for the detected schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#skip_leading_rows GoogleBigqueryJob#skip_leading_rows}
        '''
        result = self._values.get("skip_leading_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''The format of the data files.

        For CSV files, specify "CSV". For datastore backups, specify "DATASTORE_BACKUP".
        For newline-delimited JSON, specify "NEWLINE_DELIMITED_JSON". For Avro, specify "AVRO". For parquet, specify "PARQUET".
        For orc, specify "ORC". [Beta] For Bigtable, specify "BIGTABLE".
        The default value is CSV.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#source_format GoogleBigqueryJob#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_partitioning(
        self,
    ) -> typing.Optional["GoogleBigqueryJobLoadTimePartitioning"]:
        '''time_partitioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#time_partitioning GoogleBigqueryJob#time_partitioning}
        '''
        result = self._values.get("time_partitioning")
        return typing.cast(typing.Optional["GoogleBigqueryJobLoadTimePartitioning"], result)

    @builtins.property
    def write_disposition(self) -> typing.Optional[builtins.str]:
        '''Specifies the action that occurs if the destination table already exists.

        The following values are supported:
        WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result.
        WRITE_APPEND: If the table already exists, BigQuery appends the data to the table.
        WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.
        Each action is atomic and only occurs if BigQuery is able to complete the job successfully.
        Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        result = self._values.get("write_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobLoad(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadDestinationEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleBigqueryJobLoadDestinationEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970bd2c072850434de24403f52f86e1592244c053cf6eb010e586f310537a8df)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table.

        The BigQuery Service Account associated with your project requires access to this encryption key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobLoadDestinationEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobLoadDestinationEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadDestinationEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__697818b1e958df6322b47a5c9039ae964515876e2f48bff76b6802821c9ef4cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e92a363631cef595d0b690a81dc931d4f6359041fc79da24cb4940a1492c2cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryJobLoadDestinationEncryptionConfiguration]:
        return typing.cast(typing.Optional[GoogleBigqueryJobLoadDestinationEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobLoadDestinationEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0dfce41562442fd0699ce30aebbc6a5f3aae752d3b4c993c09a9a0e75711dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadDestinationTable",
    jsii_struct_bases=[],
    name_mapping={
        "table_id": "tableId",
        "dataset_id": "datasetId",
        "project_id": "projectId",
    },
)
class GoogleBigqueryJobLoadDestinationTable:
    def __init__(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea22afb464c998203a21c72ad410ddfb64dfec9600b70b96c9c650e25292c46b)
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_id": table_id,
        }
        if dataset_id is not None:
            self._values["dataset_id"] = dataset_id
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        '''
        result = self._values.get("dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobLoadDestinationTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobLoadDestinationTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadDestinationTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f10a6edb9759475b5af4a44e036cfc23943aa270a428b8302867b1af76d9513)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetId")
    def reset_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__61b49c09b00ea7eacbcfab5ffc72a7a04c24c7c024ccd74c48a7ff54cc00eb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9c9e133c7f8ba609f32c88814b8089c548355c60d91a86926ec1c801aa034b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e406572499febb4a31bffeb3fdbd203462ad38fb3fcdcc327b4311f40279c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobLoadDestinationTable]:
        return typing.cast(typing.Optional[GoogleBigqueryJobLoadDestinationTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobLoadDestinationTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0709b316912f08b3c23c50429db4ee7fe7f2b9c1e7eefe7eecd0227a0d8489b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobLoadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f130380e9a3cc3c050ffda867000f55ad39e65dfdb7e4e8e547405174da9ee4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinationEncryptionConfiguration")
    def put_destination_encryption_configuration(
        self,
        *,
        kms_key_name: builtins.str,
    ) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        value = GoogleBigqueryJobLoadDestinationEncryptionConfiguration(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putDestinationTable")
    def put_destination_table(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        value = GoogleBigqueryJobLoadDestinationTable(
            table_id=table_id, dataset_id=dataset_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationTable", [value]))

    @jsii.member(jsii_name="putParquetOptions")
    def put_parquet_options(
        self,
        *,
        enable_list_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enum_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_list_inference: If sourceFormat is set to PARQUET, indicates whether to use schema inference specifically for Parquet LIST logical type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#enable_list_inference GoogleBigqueryJob#enable_list_inference}
        :param enum_as_string: If sourceFormat is set to PARQUET, indicates whether to infer Parquet ENUM logical type as STRING instead of BYTES by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#enum_as_string GoogleBigqueryJob#enum_as_string}
        '''
        value = GoogleBigqueryJobLoadParquetOptions(
            enable_list_inference=enable_list_inference, enum_as_string=enum_as_string
        )

        return typing.cast(None, jsii.invoke(self, "putParquetOptions", [value]))

    @jsii.member(jsii_name="putTimePartitioning")
    def put_time_partitioning(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[builtins.str] = None,
        field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The only type supported is DAY, which will generate one partition per day. Providing an empty string used to cause an error, but in OnePlatform the field will be treated as unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#type GoogleBigqueryJob#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. A wrapper is used here because 0 is an invalid value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#expiration_ms GoogleBigqueryJob#expiration_ms}
        :param field: If not set, the table is partitioned by pseudo column '_PARTITIONTIME'; if set, the table is partitioned by this field. The field must be a top-level TIMESTAMP or DATE field. Its mode must be NULLABLE or REQUIRED. A wrapper is used here because an empty string is an invalid value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field GoogleBigqueryJob#field}
        '''
        value = GoogleBigqueryJobLoadTimePartitioning(
            type=type, expiration_ms=expiration_ms, field=field
        )

        return typing.cast(None, jsii.invoke(self, "putTimePartitioning", [value]))

    @jsii.member(jsii_name="resetAllowJaggedRows")
    def reset_allow_jagged_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowJaggedRows", []))

    @jsii.member(jsii_name="resetAllowQuotedNewlines")
    def reset_allow_quoted_newlines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowQuotedNewlines", []))

    @jsii.member(jsii_name="resetAutodetect")
    def reset_autodetect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutodetect", []))

    @jsii.member(jsii_name="resetCreateDisposition")
    def reset_create_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateDisposition", []))

    @jsii.member(jsii_name="resetDestinationEncryptionConfiguration")
    def reset_destination_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetFieldDelimiter")
    def reset_field_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldDelimiter", []))

    @jsii.member(jsii_name="resetIgnoreUnknownValues")
    def reset_ignore_unknown_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreUnknownValues", []))

    @jsii.member(jsii_name="resetJsonExtension")
    def reset_json_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonExtension", []))

    @jsii.member(jsii_name="resetMaxBadRecords")
    def reset_max_bad_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBadRecords", []))

    @jsii.member(jsii_name="resetNullMarker")
    def reset_null_marker(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullMarker", []))

    @jsii.member(jsii_name="resetParquetOptions")
    def reset_parquet_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParquetOptions", []))

    @jsii.member(jsii_name="resetProjectionFields")
    def reset_projection_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectionFields", []))

    @jsii.member(jsii_name="resetQuote")
    def reset_quote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuote", []))

    @jsii.member(jsii_name="resetSchemaUpdateOptions")
    def reset_schema_update_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaUpdateOptions", []))

    @jsii.member(jsii_name="resetSkipLeadingRows")
    def reset_skip_leading_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipLeadingRows", []))

    @jsii.member(jsii_name="resetSourceFormat")
    def reset_source_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFormat", []))

    @jsii.member(jsii_name="resetTimePartitioning")
    def reset_time_partitioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimePartitioning", []))

    @jsii.member(jsii_name="resetWriteDisposition")
    def reset_write_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteDisposition", []))

    @builtins.property
    @jsii.member(jsii_name="destinationEncryptionConfiguration")
    def destination_encryption_configuration(
        self,
    ) -> GoogleBigqueryJobLoadDestinationEncryptionConfigurationOutputReference:
        return typing.cast(GoogleBigqueryJobLoadDestinationEncryptionConfigurationOutputReference, jsii.get(self, "destinationEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="destinationTable")
    def destination_table(self) -> GoogleBigqueryJobLoadDestinationTableOutputReference:
        return typing.cast(GoogleBigqueryJobLoadDestinationTableOutputReference, jsii.get(self, "destinationTable"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptions")
    def parquet_options(self) -> "GoogleBigqueryJobLoadParquetOptionsOutputReference":
        return typing.cast("GoogleBigqueryJobLoadParquetOptionsOutputReference", jsii.get(self, "parquetOptions"))

    @builtins.property
    @jsii.member(jsii_name="timePartitioning")
    def time_partitioning(
        self,
    ) -> "GoogleBigqueryJobLoadTimePartitioningOutputReference":
        return typing.cast("GoogleBigqueryJobLoadTimePartitioningOutputReference", jsii.get(self, "timePartitioning"))

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
    @jsii.member(jsii_name="autodetectInput")
    def autodetect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autodetectInput"))

    @builtins.property
    @jsii.member(jsii_name="createDispositionInput")
    def create_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationEncryptionConfigurationInput")
    def destination_encryption_configuration_input(
        self,
    ) -> typing.Optional[GoogleBigqueryJobLoadDestinationEncryptionConfiguration]:
        return typing.cast(typing.Optional[GoogleBigqueryJobLoadDestinationEncryptionConfiguration], jsii.get(self, "destinationEncryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTableInput")
    def destination_table_input(
        self,
    ) -> typing.Optional[GoogleBigqueryJobLoadDestinationTable]:
        return typing.cast(typing.Optional[GoogleBigqueryJobLoadDestinationTable], jsii.get(self, "destinationTableInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiterInput")
    def field_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldDelimiterInput"))

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
    @jsii.member(jsii_name="maxBadRecordsInput")
    def max_bad_records_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBadRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="nullMarkerInput")
    def null_marker_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nullMarkerInput"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptionsInput")
    def parquet_options_input(
        self,
    ) -> typing.Optional["GoogleBigqueryJobLoadParquetOptions"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobLoadParquetOptions"], jsii.get(self, "parquetOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectionFieldsInput")
    def projection_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectionFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteInput")
    def quote_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaUpdateOptionsInput")
    def schema_update_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "schemaUpdateOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRowsInput")
    def skip_leading_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "skipLeadingRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFormatInput")
    def source_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrisInput")
    def source_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="timePartitioningInput")
    def time_partitioning_input(
        self,
    ) -> typing.Optional["GoogleBigqueryJobLoadTimePartitioning"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobLoadTimePartitioning"], jsii.get(self, "timePartitioningInput"))

    @builtins.property
    @jsii.member(jsii_name="writeDispositionInput")
    def write_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeDispositionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__22991294fe9a143a824a877086b413798c727eff557b1cc3fbb91442dce55acc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce621a8f2b6cfe0dcaabcbd966aff74c074ab9af4aebb4ef7f19f6960325ffd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowQuotedNewlines", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0ffdeee17ee55f3a18ea9689a13893903eea8d5f769cbeeffd8e0843d7c64683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autodetect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createDisposition")
    def create_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createDisposition"))

    @create_disposition.setter
    def create_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a258d5a90480fedfc639923c67792403ce3be0b2d41727c82acc458652116cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b267a2e407869e13333147e48524fbc8bc8664e5663f9a5cee3a09b79484cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldDelimiter"))

    @field_delimiter.setter
    def field_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f004be2fcc70f7c2251f8dd816b87ee18f3c4c969c7a392cf52c5d0c4311c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldDelimiter", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__f13ac6bf5c45da69fe6f342ae1c6b25f49329afa4014f4caa3630a2c544a7e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreUnknownValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonExtension")
    def json_extension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonExtension"))

    @json_extension.setter
    def json_extension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234cfbb07a9793faf006b0e0137b4559cc513dcdfaf795e64695a33fdb6fd6e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonExtension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBadRecords")
    def max_bad_records(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBadRecords"))

    @max_bad_records.setter
    def max_bad_records(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1068f48c6e309cddbd25beee2e29c774a63d6e161eddac88ddf4c286f9f9d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBadRecords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullMarker")
    def null_marker(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullMarker"))

    @null_marker.setter
    def null_marker(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1249235b2cb0b47afef5d0595a729b5af1abd99257c8700896b83a5839bc3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullMarker", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectionFields")
    def projection_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectionFields"))

    @projection_fields.setter
    def projection_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b493fa0a3f7e25f8f71fdd10030b7e95f11cdf3b23148a79e17a57d968d78aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectionFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quote")
    def quote(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quote"))

    @quote.setter
    def quote(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84375c81a10d8e770089f3065e20d217e54b3d432b32e1ccf7991a85ace717f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaUpdateOptions")
    def schema_update_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "schemaUpdateOptions"))

    @schema_update_options.setter
    def schema_update_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d83ad651d8b3ca6131ed4ba5c235703d19b433f8d80135d69b0d0e8eb5ead9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaUpdateOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRows")
    def skip_leading_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "skipLeadingRows"))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6e9eb75520d4238a66d5eeba023e5e5a7d66f8675714afdf753b0915a0176e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipLeadingRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a3c6acec268cf356f536ee974c2a55aec4fcc89ca1fcc1d3619d7ea04a0ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUris")
    def source_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceUris"))

    @source_uris.setter
    def source_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c60c801f245f54c14712014e95f813e1ca43f6db4f6364a87bafd061f8c156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeDisposition")
    def write_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeDisposition"))

    @write_disposition.setter
    def write_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f3d3d73e645045b2360f4141da2d9a133536fd962e7fe46909fcf7b24df26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobLoad]:
        return typing.cast(typing.Optional[GoogleBigqueryJobLoad], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleBigqueryJobLoad]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546f6bc1273827a90a73705da1c615c7ae5e0cda431c42db30140d9c6348f09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadParquetOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enable_list_inference": "enableListInference",
        "enum_as_string": "enumAsString",
    },
)
class GoogleBigqueryJobLoadParquetOptions:
    def __init__(
        self,
        *,
        enable_list_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enum_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_list_inference: If sourceFormat is set to PARQUET, indicates whether to use schema inference specifically for Parquet LIST logical type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#enable_list_inference GoogleBigqueryJob#enable_list_inference}
        :param enum_as_string: If sourceFormat is set to PARQUET, indicates whether to infer Parquet ENUM logical type as STRING instead of BYTES by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#enum_as_string GoogleBigqueryJob#enum_as_string}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495696a71e6a0e119da6de34dae3a153fd6b8b1ede85df734e00b4385cd266fb)
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
        '''If sourceFormat is set to PARQUET, indicates whether to use schema inference specifically for Parquet LIST logical type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#enable_list_inference GoogleBigqueryJob#enable_list_inference}
        '''
        result = self._values.get("enable_list_inference")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enum_as_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If sourceFormat is set to PARQUET, indicates whether to infer Parquet ENUM logical type as STRING instead of BYTES by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#enum_as_string GoogleBigqueryJob#enum_as_string}
        '''
        result = self._values.get("enum_as_string")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobLoadParquetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobLoadParquetOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadParquetOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a99f2d1d39a2be5e936fdc37c655a09cbca5cc86f0cc60dd837ef9b182b87573)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c38966446e68e4b9053b884926080e8b6678ab91ca4d1fa6bc8a94991220b75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9879c77040234bb63db92db08f083ff514f04e82b78e5ce464176d174907a4b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enumAsString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobLoadParquetOptions]:
        return typing.cast(typing.Optional[GoogleBigqueryJobLoadParquetOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobLoadParquetOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8ffeab1d526451a266f9fd027b2169d2937f2f6654786ee5d8716c59bee14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadTimePartitioning",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "expiration_ms": "expirationMs", "field": "field"},
)
class GoogleBigqueryJobLoadTimePartitioning:
    def __init__(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[builtins.str] = None,
        field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The only type supported is DAY, which will generate one partition per day. Providing an empty string used to cause an error, but in OnePlatform the field will be treated as unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#type GoogleBigqueryJob#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. A wrapper is used here because 0 is an invalid value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#expiration_ms GoogleBigqueryJob#expiration_ms}
        :param field: If not set, the table is partitioned by pseudo column '_PARTITIONTIME'; if set, the table is partitioned by this field. The field must be a top-level TIMESTAMP or DATE field. Its mode must be NULLABLE or REQUIRED. A wrapper is used here because an empty string is an invalid value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field GoogleBigqueryJob#field}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f763ab8fa69b9cf9b6e148e5d772cf8b07e6a12c8494eee584d6e728aae7c6d6)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument expiration_ms", value=expiration_ms, expected_type=type_hints["expiration_ms"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if expiration_ms is not None:
            self._values["expiration_ms"] = expiration_ms
        if field is not None:
            self._values["field"] = field

    @builtins.property
    def type(self) -> builtins.str:
        '''The only type supported is DAY, which will generate one partition per day.

        Providing an empty string used to cause an error,
        but in OnePlatform the field will be treated as unset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#type GoogleBigqueryJob#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_ms(self) -> typing.Optional[builtins.str]:
        '''Number of milliseconds for which to keep the storage for a partition.

        A wrapper is used here because 0 is an invalid value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#expiration_ms GoogleBigqueryJob#expiration_ms}
        '''
        result = self._values.get("expiration_ms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''If not set, the table is partitioned by pseudo column '_PARTITIONTIME';

        if set, the table is partitioned by this field.
        The field must be a top-level TIMESTAMP or DATE field. Its mode must be NULLABLE or REQUIRED.
        A wrapper is used here because an empty string is an invalid value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#field GoogleBigqueryJob#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobLoadTimePartitioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobLoadTimePartitioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobLoadTimePartitioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2104c536fba7bcdf6808ff105b777324f70bd3fd861c157548c2ac35cb7dae4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpirationMs")
    def reset_expiration_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationMs", []))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @builtins.property
    @jsii.member(jsii_name="expirationMsInput")
    def expiration_ms_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationMsInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationMs")
    def expiration_ms(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationMs"))

    @expiration_ms.setter
    def expiration_ms(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624ce0fc3b2524e743ac2213bcc927e62c4c3349b2f0e7f923cd81c8a3f3cf75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627fb5fdc8ee3b07ca007700d96dea119275ee32213f617e4fc2c5147dea65cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9c834cd92e9d2d3e1e3cf1b7819d51573a2aa4d092dec93a8f3a4b6b63a723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobLoadTimePartitioning]:
        return typing.cast(typing.Optional[GoogleBigqueryJobLoadTimePartitioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobLoadTimePartitioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe0903c8d22ce94d9ebdda5ff08413f54d7ab080a3ef657860eed0e8bd3a3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQuery",
    jsii_struct_bases=[],
    name_mapping={
        "query": "query",
        "allow_large_results": "allowLargeResults",
        "continuous": "continuous",
        "create_disposition": "createDisposition",
        "default_dataset": "defaultDataset",
        "destination_encryption_configuration": "destinationEncryptionConfiguration",
        "destination_table": "destinationTable",
        "flatten_results": "flattenResults",
        "maximum_billing_tier": "maximumBillingTier",
        "maximum_bytes_billed": "maximumBytesBilled",
        "parameter_mode": "parameterMode",
        "priority": "priority",
        "schema_update_options": "schemaUpdateOptions",
        "script_options": "scriptOptions",
        "use_legacy_sql": "useLegacySql",
        "use_query_cache": "useQueryCache",
        "user_defined_function_resources": "userDefinedFunctionResources",
        "write_disposition": "writeDisposition",
    },
)
class GoogleBigqueryJobQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        allow_large_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        continuous: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_disposition: typing.Optional[builtins.str] = None,
        default_dataset: typing.Optional[typing.Union["GoogleBigqueryJobQueryDefaultDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryJobQueryDestinationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_table: typing.Optional[typing.Union["GoogleBigqueryJobQueryDestinationTable", typing.Dict[builtins.str, typing.Any]]] = None,
        flatten_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maximum_billing_tier: typing.Optional[jsii.Number] = None,
        maximum_bytes_billed: typing.Optional[builtins.str] = None,
        parameter_mode: typing.Optional[builtins.str] = None,
        priority: typing.Optional[builtins.str] = None,
        schema_update_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_options: typing.Optional[typing.Union["GoogleBigqueryJobQueryScriptOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_query_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_defined_function_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryJobQueryUserDefinedFunctionResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        write_disposition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param query: SQL query text to execute. The useLegacySql field can be used to indicate whether the query uses legacy SQL or standard SQL. *NOTE*: queries containing `DML language <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language>`_ ('DELETE', 'UPDATE', 'MERGE', 'INSERT') must specify 'create_disposition = ""' and 'write_disposition = ""'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#query GoogleBigqueryJob#query}
        :param allow_large_results: If true and query uses legacy SQL dialect, allows the query to produce arbitrarily large result tables at a slight cost in performance. Requires destinationTable to be set. For standard SQL queries, this flag is ignored and large results are always allowed. However, you must still set destinationTable when result size exceeds the allowed maximum response size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_large_results GoogleBigqueryJob#allow_large_results}
        :param continuous: Whether to run the query as continuous or a regular query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#continuous GoogleBigqueryJob#continuous}
        :param create_disposition: Specifies whether the job is allowed to create new tables. The following values are supported: CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table. CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result. Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        :param default_dataset: default_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#default_dataset GoogleBigqueryJob#default_dataset}
        :param destination_encryption_configuration: destination_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        :param destination_table: destination_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        :param flatten_results: If true and query uses legacy SQL dialect, flattens all nested and repeated fields in the query results. allowLargeResults must be true if this is set to false. For standard SQL queries, this flag is ignored and results are never flattened. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#flatten_results GoogleBigqueryJob#flatten_results}
        :param maximum_billing_tier: Limits the billing tier for this job. Queries that have resource usage beyond this tier will fail (without incurring a charge). If unspecified, this will be set to your project default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#maximum_billing_tier GoogleBigqueryJob#maximum_billing_tier}
        :param maximum_bytes_billed: Limits the bytes billed for this job. Queries that will have bytes billed beyond this limit will fail (without incurring a charge). If unspecified, this will be set to your project default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#maximum_bytes_billed GoogleBigqueryJob#maximum_bytes_billed}
        :param parameter_mode: Standard SQL only. Set to POSITIONAL to use positional (?) query parameters or to NAMED to use named (@myparam) query parameters in this query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#parameter_mode GoogleBigqueryJob#parameter_mode}
        :param priority: Specifies a priority for the query. Default value: "INTERACTIVE" Possible values: ["INTERACTIVE", "BATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#priority GoogleBigqueryJob#priority}
        :param schema_update_options: Allows the schema of the destination table to be updated as a side effect of the query job. Schema update options are supported in two cases: when writeDisposition is WRITE_APPEND; when writeDisposition is WRITE_TRUNCATE and the destination table is a partition of a table, specified by partition decorators. For normal tables, WRITE_TRUNCATE will always overwrite the schema. One or more of the following values are specified: ALLOW_FIELD_ADDITION: allow adding a nullable field to the schema. ALLOW_FIELD_RELAXATION: allow relaxing a required field in the original schema to nullable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#schema_update_options GoogleBigqueryJob#schema_update_options}
        :param script_options: script_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#script_options GoogleBigqueryJob#script_options}
        :param use_legacy_sql: Specifies whether to use BigQuery's legacy SQL dialect for this query. The default value is true. If set to false, the query will use BigQuery's standard SQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_legacy_sql GoogleBigqueryJob#use_legacy_sql}
        :param use_query_cache: Whether to look for the result in the query cache. The query cache is a best-effort cache that will be flushed whenever tables in the query are modified. Moreover, the query cache is only available when a query does not have a destination table specified. The default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_query_cache GoogleBigqueryJob#use_query_cache}
        :param user_defined_function_resources: user_defined_function_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#user_defined_function_resources GoogleBigqueryJob#user_defined_function_resources}
        :param write_disposition: Specifies the action that occurs if the destination table already exists. The following values are supported: WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result. WRITE_APPEND: If the table already exists, BigQuery appends the data to the table. WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        if isinstance(default_dataset, dict):
            default_dataset = GoogleBigqueryJobQueryDefaultDataset(**default_dataset)
        if isinstance(destination_encryption_configuration, dict):
            destination_encryption_configuration = GoogleBigqueryJobQueryDestinationEncryptionConfiguration(**destination_encryption_configuration)
        if isinstance(destination_table, dict):
            destination_table = GoogleBigqueryJobQueryDestinationTable(**destination_table)
        if isinstance(script_options, dict):
            script_options = GoogleBigqueryJobQueryScriptOptions(**script_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d144d097002e6c8bcf69ccc2cec979440784c7c97d8cd761220ede60af74f209)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument allow_large_results", value=allow_large_results, expected_type=type_hints["allow_large_results"])
            check_type(argname="argument continuous", value=continuous, expected_type=type_hints["continuous"])
            check_type(argname="argument create_disposition", value=create_disposition, expected_type=type_hints["create_disposition"])
            check_type(argname="argument default_dataset", value=default_dataset, expected_type=type_hints["default_dataset"])
            check_type(argname="argument destination_encryption_configuration", value=destination_encryption_configuration, expected_type=type_hints["destination_encryption_configuration"])
            check_type(argname="argument destination_table", value=destination_table, expected_type=type_hints["destination_table"])
            check_type(argname="argument flatten_results", value=flatten_results, expected_type=type_hints["flatten_results"])
            check_type(argname="argument maximum_billing_tier", value=maximum_billing_tier, expected_type=type_hints["maximum_billing_tier"])
            check_type(argname="argument maximum_bytes_billed", value=maximum_bytes_billed, expected_type=type_hints["maximum_bytes_billed"])
            check_type(argname="argument parameter_mode", value=parameter_mode, expected_type=type_hints["parameter_mode"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument schema_update_options", value=schema_update_options, expected_type=type_hints["schema_update_options"])
            check_type(argname="argument script_options", value=script_options, expected_type=type_hints["script_options"])
            check_type(argname="argument use_legacy_sql", value=use_legacy_sql, expected_type=type_hints["use_legacy_sql"])
            check_type(argname="argument use_query_cache", value=use_query_cache, expected_type=type_hints["use_query_cache"])
            check_type(argname="argument user_defined_function_resources", value=user_defined_function_resources, expected_type=type_hints["user_defined_function_resources"])
            check_type(argname="argument write_disposition", value=write_disposition, expected_type=type_hints["write_disposition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if allow_large_results is not None:
            self._values["allow_large_results"] = allow_large_results
        if continuous is not None:
            self._values["continuous"] = continuous
        if create_disposition is not None:
            self._values["create_disposition"] = create_disposition
        if default_dataset is not None:
            self._values["default_dataset"] = default_dataset
        if destination_encryption_configuration is not None:
            self._values["destination_encryption_configuration"] = destination_encryption_configuration
        if destination_table is not None:
            self._values["destination_table"] = destination_table
        if flatten_results is not None:
            self._values["flatten_results"] = flatten_results
        if maximum_billing_tier is not None:
            self._values["maximum_billing_tier"] = maximum_billing_tier
        if maximum_bytes_billed is not None:
            self._values["maximum_bytes_billed"] = maximum_bytes_billed
        if parameter_mode is not None:
            self._values["parameter_mode"] = parameter_mode
        if priority is not None:
            self._values["priority"] = priority
        if schema_update_options is not None:
            self._values["schema_update_options"] = schema_update_options
        if script_options is not None:
            self._values["script_options"] = script_options
        if use_legacy_sql is not None:
            self._values["use_legacy_sql"] = use_legacy_sql
        if use_query_cache is not None:
            self._values["use_query_cache"] = use_query_cache
        if user_defined_function_resources is not None:
            self._values["user_defined_function_resources"] = user_defined_function_resources
        if write_disposition is not None:
            self._values["write_disposition"] = write_disposition

    @builtins.property
    def query(self) -> builtins.str:
        '''SQL query text to execute.

        The useLegacySql field can be used to indicate whether the query uses legacy SQL or standard SQL.
        *NOTE*: queries containing `DML language <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language>`_
        ('DELETE', 'UPDATE', 'MERGE', 'INSERT') must specify 'create_disposition = ""' and 'write_disposition = ""'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#query GoogleBigqueryJob#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_large_results(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true and query uses legacy SQL dialect, allows the query to produce arbitrarily large result tables at a slight cost in performance.

        Requires destinationTable to be set. For standard SQL queries, this flag is ignored and large results are always allowed.
        However, you must still set destinationTable when result size exceeds the allowed maximum response size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#allow_large_results GoogleBigqueryJob#allow_large_results}
        '''
        result = self._values.get("allow_large_results")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def continuous(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the query as continuous or a regular query.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#continuous GoogleBigqueryJob#continuous}
        '''
        result = self._values.get("continuous")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_disposition(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the job is allowed to create new tables.

        The following values are supported:
        CREATE_IF_NEEDED: If the table does not exist, BigQuery creates the table.
        CREATE_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result.
        Creation, truncation and append actions occur as one atomic update upon job completion Default value: "CREATE_IF_NEEDED" Possible values: ["CREATE_IF_NEEDED", "CREATE_NEVER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create_disposition GoogleBigqueryJob#create_disposition}
        '''
        result = self._values.get("create_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_dataset(
        self,
    ) -> typing.Optional["GoogleBigqueryJobQueryDefaultDataset"]:
        '''default_dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#default_dataset GoogleBigqueryJob#default_dataset}
        '''
        result = self._values.get("default_dataset")
        return typing.cast(typing.Optional["GoogleBigqueryJobQueryDefaultDataset"], result)

    @builtins.property
    def destination_encryption_configuration(
        self,
    ) -> typing.Optional["GoogleBigqueryJobQueryDestinationEncryptionConfiguration"]:
        '''destination_encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_encryption_configuration GoogleBigqueryJob#destination_encryption_configuration}
        '''
        result = self._values.get("destination_encryption_configuration")
        return typing.cast(typing.Optional["GoogleBigqueryJobQueryDestinationEncryptionConfiguration"], result)

    @builtins.property
    def destination_table(
        self,
    ) -> typing.Optional["GoogleBigqueryJobQueryDestinationTable"]:
        '''destination_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#destination_table GoogleBigqueryJob#destination_table}
        '''
        result = self._values.get("destination_table")
        return typing.cast(typing.Optional["GoogleBigqueryJobQueryDestinationTable"], result)

    @builtins.property
    def flatten_results(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true and query uses legacy SQL dialect, flattens all nested and repeated fields in the query results.

        allowLargeResults must be true if this is set to false. For standard SQL queries, this flag is ignored and results are never flattened.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#flatten_results GoogleBigqueryJob#flatten_results}
        '''
        result = self._values.get("flatten_results")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maximum_billing_tier(self) -> typing.Optional[jsii.Number]:
        '''Limits the billing tier for this job.

        Queries that have resource usage beyond this tier will fail (without incurring a charge).
        If unspecified, this will be set to your project default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#maximum_billing_tier GoogleBigqueryJob#maximum_billing_tier}
        '''
        result = self._values.get("maximum_billing_tier")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_bytes_billed(self) -> typing.Optional[builtins.str]:
        '''Limits the bytes billed for this job.

        Queries that will have bytes billed beyond this limit will fail (without incurring a charge).
        If unspecified, this will be set to your project default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#maximum_bytes_billed GoogleBigqueryJob#maximum_bytes_billed}
        '''
        result = self._values.get("maximum_bytes_billed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_mode(self) -> typing.Optional[builtins.str]:
        '''Standard SQL only.

        Set to POSITIONAL to use positional (?) query parameters or to NAMED to use named (@myparam) query parameters in this query.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#parameter_mode GoogleBigqueryJob#parameter_mode}
        '''
        result = self._values.get("parameter_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Specifies a priority for the query. Default value: "INTERACTIVE" Possible values: ["INTERACTIVE", "BATCH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#priority GoogleBigqueryJob#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_update_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allows the schema of the destination table to be updated as a side effect of the query job.

        Schema update options are supported in two cases: when writeDisposition is WRITE_APPEND;
        when writeDisposition is WRITE_TRUNCATE and the destination table is a partition of a table,
        specified by partition decorators. For normal tables, WRITE_TRUNCATE will always overwrite the schema.
        One or more of the following values are specified:
        ALLOW_FIELD_ADDITION: allow adding a nullable field to the schema.
        ALLOW_FIELD_RELAXATION: allow relaxing a required field in the original schema to nullable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#schema_update_options GoogleBigqueryJob#schema_update_options}
        '''
        result = self._values.get("schema_update_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def script_options(self) -> typing.Optional["GoogleBigqueryJobQueryScriptOptions"]:
        '''script_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#script_options GoogleBigqueryJob#script_options}
        '''
        result = self._values.get("script_options")
        return typing.cast(typing.Optional["GoogleBigqueryJobQueryScriptOptions"], result)

    @builtins.property
    def use_legacy_sql(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to use BigQuery's legacy SQL dialect for this query.

        The default value is true.
        If set to false, the query will use BigQuery's standard SQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_legacy_sql GoogleBigqueryJob#use_legacy_sql}
        '''
        result = self._values.get("use_legacy_sql")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_query_cache(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to look for the result in the query cache.

        The query cache is a best-effort cache that will be flushed whenever
        tables in the query are modified. Moreover, the query cache is only available when a query does not have a destination table specified.
        The default value is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#use_query_cache GoogleBigqueryJob#use_query_cache}
        '''
        result = self._values.get("use_query_cache")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_defined_function_resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobQueryUserDefinedFunctionResources"]]]:
        '''user_defined_function_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#user_defined_function_resources GoogleBigqueryJob#user_defined_function_resources}
        '''
        result = self._values.get("user_defined_function_resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobQueryUserDefinedFunctionResources"]]], result)

    @builtins.property
    def write_disposition(self) -> typing.Optional[builtins.str]:
        '''Specifies the action that occurs if the destination table already exists.

        The following values are supported:
        WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result.
        WRITE_APPEND: If the table already exists, BigQuery appends the data to the table.
        WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.
        Each action is atomic and only occurs if BigQuery is able to complete the job successfully.
        Creation, truncation and append actions occur as one atomic update upon job completion. Default value: "WRITE_EMPTY" Possible values: ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#write_disposition GoogleBigqueryJob#write_disposition}
        '''
        result = self._values.get("write_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryDefaultDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset_id": "datasetId", "project_id": "projectId"},
)
class GoogleBigqueryJobQueryDefaultDataset:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: The dataset. Can be specified '{{dataset_id}}' if 'project_id' is also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c8d81da5295ed1dded97b87b5bd4ee36ff23649f24dde8b906f707d89d75a6)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
        }
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The dataset. Can be specified '{{dataset_id}}' if 'project_id' is also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}' if not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobQueryDefaultDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobQueryDefaultDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryDefaultDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b3639fcbdedddb0126018397ca0431b3e954dc966badacefe1718c985ea03a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592aac5a22ab514852ac34cb2d743fb79ce0475b04d3018a391e228f8cb0ddcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c01550f15d1cb51c75ab61b6e82766b888cad83d2286bb647099f0b7bb173a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobQueryDefaultDataset]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQueryDefaultDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobQueryDefaultDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219444355624388ff105311f18bc93fc9c06d309576ffbb4600d1aa7bfe93852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryDestinationEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleBigqueryJobQueryDestinationEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3a5566ebb120a171d4c07ba883d8e1af67a9d6e5aaefcd5c0a44dbdebc3c41)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table.

        The BigQuery Service Account associated with your project requires access to this encryption key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobQueryDestinationEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobQueryDestinationEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryDestinationEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f0b1217bf1adf7ae3464a6684e51649f0eebc777bc578c3b0e676b72c9c47fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d5eef71a6e3f7ba4877099d5d2056857d88ee2e1b0ab16f0c06d0505c2d2c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryJobQueryDestinationEncryptionConfiguration]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQueryDestinationEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobQueryDestinationEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6e0832b1e361fdc8297f70ff30fc25a108d4818287044c4be3b3d4e67e9dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryDestinationTable",
    jsii_struct_bases=[],
    name_mapping={
        "table_id": "tableId",
        "dataset_id": "datasetId",
        "project_id": "projectId",
    },
)
class GoogleBigqueryJobQueryDestinationTable:
    def __init__(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9eb7550c451b0ff94ce57a19b0d16db80b71759e89c970836f80ce362a5024)
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_id": table_id,
        }
        if dataset_id is not None:
            self._values["dataset_id"] = dataset_id
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        '''
        result = self._values.get("dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobQueryDestinationTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobQueryDestinationTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryDestinationTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ff89cd2a322730cff310fca5ea3a6ce031857a96f677792c204bb9006b1b9b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetId")
    def reset_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5268836032f7d3a269d748659a31015f62ce1baf9279309b5391a87437662436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddff6864f83ea06c1e2fdb5dff4a584c7dbaacf0e441d9c81ba1a3108940f37b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dce7437266a43dae1e92314f7f5b4156efd0289768f4c759899df1f2a7cfd23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobQueryDestinationTable]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQueryDestinationTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobQueryDestinationTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e687b2cbc652428fc00f6ba545e4e0904b64afe7c46e0ffb147ff40f6b99b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__196f738efdaa8c13a19ec167245d22f409d1f4c2352efbc92e23194c7a677ebc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultDataset")
    def put_default_dataset(
        self,
        *,
        dataset_id: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: The dataset. Can be specified '{{dataset_id}}' if 'project_id' is also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        value = GoogleBigqueryJobQueryDefaultDataset(
            dataset_id=dataset_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultDataset", [value]))

    @jsii.member(jsii_name="putDestinationEncryptionConfiguration")
    def put_destination_encryption_configuration(
        self,
        *,
        kms_key_name: builtins.str,
    ) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#kms_key_name GoogleBigqueryJob#kms_key_name}
        '''
        value = GoogleBigqueryJobQueryDestinationEncryptionConfiguration(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putDestinationTable")
    def put_destination_table(
        self,
        *,
        table_id: builtins.str,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table_id: The table. Can be specified '{{table_id}}' if 'project_id' and 'dataset_id' are also set, or of the form 'projects/{{project}}/datasets/{{dataset_id}}/tables/{{table_id}}' if not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#table_id GoogleBigqueryJob#table_id}
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#dataset_id GoogleBigqueryJob#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#project_id GoogleBigqueryJob#project_id}
        '''
        value = GoogleBigqueryJobQueryDestinationTable(
            table_id=table_id, dataset_id=dataset_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationTable", [value]))

    @jsii.member(jsii_name="putScriptOptions")
    def put_script_options(
        self,
        *,
        key_result_statement: typing.Optional[builtins.str] = None,
        statement_byte_budget: typing.Optional[builtins.str] = None,
        statement_timeout_ms: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_result_statement: Determines which statement in the script represents the "key result", used to populate the schema and query results of the script job. Possible values: ["LAST", "FIRST_SELECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#key_result_statement GoogleBigqueryJob#key_result_statement}
        :param statement_byte_budget: Limit on the number of bytes billed per statement. Exceeding this budget results in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#statement_byte_budget GoogleBigqueryJob#statement_byte_budget}
        :param statement_timeout_ms: Timeout period for each statement in a script. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#statement_timeout_ms GoogleBigqueryJob#statement_timeout_ms}
        '''
        value = GoogleBigqueryJobQueryScriptOptions(
            key_result_statement=key_result_statement,
            statement_byte_budget=statement_byte_budget,
            statement_timeout_ms=statement_timeout_ms,
        )

        return typing.cast(None, jsii.invoke(self, "putScriptOptions", [value]))

    @jsii.member(jsii_name="putUserDefinedFunctionResources")
    def put_user_defined_function_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryJobQueryUserDefinedFunctionResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d0d47a3211910ee37b51d2449a69fe125b25fe485663a909786d20f91310ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserDefinedFunctionResources", [value]))

    @jsii.member(jsii_name="resetAllowLargeResults")
    def reset_allow_large_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowLargeResults", []))

    @jsii.member(jsii_name="resetContinuous")
    def reset_continuous(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinuous", []))

    @jsii.member(jsii_name="resetCreateDisposition")
    def reset_create_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateDisposition", []))

    @jsii.member(jsii_name="resetDefaultDataset")
    def reset_default_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDataset", []))

    @jsii.member(jsii_name="resetDestinationEncryptionConfiguration")
    def reset_destination_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetDestinationTable")
    def reset_destination_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationTable", []))

    @jsii.member(jsii_name="resetFlattenResults")
    def reset_flatten_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlattenResults", []))

    @jsii.member(jsii_name="resetMaximumBillingTier")
    def reset_maximum_billing_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBillingTier", []))

    @jsii.member(jsii_name="resetMaximumBytesBilled")
    def reset_maximum_bytes_billed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBytesBilled", []))

    @jsii.member(jsii_name="resetParameterMode")
    def reset_parameter_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameterMode", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetSchemaUpdateOptions")
    def reset_schema_update_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaUpdateOptions", []))

    @jsii.member(jsii_name="resetScriptOptions")
    def reset_script_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptOptions", []))

    @jsii.member(jsii_name="resetUseLegacySql")
    def reset_use_legacy_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseLegacySql", []))

    @jsii.member(jsii_name="resetUseQueryCache")
    def reset_use_query_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseQueryCache", []))

    @jsii.member(jsii_name="resetUserDefinedFunctionResources")
    def reset_user_defined_function_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedFunctionResources", []))

    @jsii.member(jsii_name="resetWriteDisposition")
    def reset_write_disposition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteDisposition", []))

    @builtins.property
    @jsii.member(jsii_name="defaultDataset")
    def default_dataset(self) -> GoogleBigqueryJobQueryDefaultDatasetOutputReference:
        return typing.cast(GoogleBigqueryJobQueryDefaultDatasetOutputReference, jsii.get(self, "defaultDataset"))

    @builtins.property
    @jsii.member(jsii_name="destinationEncryptionConfiguration")
    def destination_encryption_configuration(
        self,
    ) -> GoogleBigqueryJobQueryDestinationEncryptionConfigurationOutputReference:
        return typing.cast(GoogleBigqueryJobQueryDestinationEncryptionConfigurationOutputReference, jsii.get(self, "destinationEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="destinationTable")
    def destination_table(
        self,
    ) -> GoogleBigqueryJobQueryDestinationTableOutputReference:
        return typing.cast(GoogleBigqueryJobQueryDestinationTableOutputReference, jsii.get(self, "destinationTable"))

    @builtins.property
    @jsii.member(jsii_name="scriptOptions")
    def script_options(self) -> "GoogleBigqueryJobQueryScriptOptionsOutputReference":
        return typing.cast("GoogleBigqueryJobQueryScriptOptionsOutputReference", jsii.get(self, "scriptOptions"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFunctionResources")
    def user_defined_function_resources(
        self,
    ) -> "GoogleBigqueryJobQueryUserDefinedFunctionResourcesList":
        return typing.cast("GoogleBigqueryJobQueryUserDefinedFunctionResourcesList", jsii.get(self, "userDefinedFunctionResources"))

    @builtins.property
    @jsii.member(jsii_name="allowLargeResultsInput")
    def allow_large_results_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowLargeResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="continuousInput")
    def continuous_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continuousInput"))

    @builtins.property
    @jsii.member(jsii_name="createDispositionInput")
    def create_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDatasetInput")
    def default_dataset_input(
        self,
    ) -> typing.Optional[GoogleBigqueryJobQueryDefaultDataset]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQueryDefaultDataset], jsii.get(self, "defaultDatasetInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationEncryptionConfigurationInput")
    def destination_encryption_configuration_input(
        self,
    ) -> typing.Optional[GoogleBigqueryJobQueryDestinationEncryptionConfiguration]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQueryDestinationEncryptionConfiguration], jsii.get(self, "destinationEncryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTableInput")
    def destination_table_input(
        self,
    ) -> typing.Optional[GoogleBigqueryJobQueryDestinationTable]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQueryDestinationTable], jsii.get(self, "destinationTableInput"))

    @builtins.property
    @jsii.member(jsii_name="flattenResultsInput")
    def flatten_results_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "flattenResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBillingTierInput")
    def maximum_billing_tier_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBillingTierInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBytesBilledInput")
    def maximum_bytes_billed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumBytesBilledInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterModeInput")
    def parameter_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterModeInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaUpdateOptionsInput")
    def schema_update_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "schemaUpdateOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptOptionsInput")
    def script_options_input(
        self,
    ) -> typing.Optional["GoogleBigqueryJobQueryScriptOptions"]:
        return typing.cast(typing.Optional["GoogleBigqueryJobQueryScriptOptions"], jsii.get(self, "scriptOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="useLegacySqlInput")
    def use_legacy_sql_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useLegacySqlInput"))

    @builtins.property
    @jsii.member(jsii_name="useQueryCacheInput")
    def use_query_cache_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useQueryCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFunctionResourcesInput")
    def user_defined_function_resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobQueryUserDefinedFunctionResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryJobQueryUserDefinedFunctionResources"]]], jsii.get(self, "userDefinedFunctionResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="writeDispositionInput")
    def write_disposition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeDispositionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowLargeResults")
    def allow_large_results(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowLargeResults"))

    @allow_large_results.setter
    def allow_large_results(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f5f0ea82b4066eeacee162ac99aa30c9b8d7393ecab5b9a8c69c8d6bf6da7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowLargeResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="continuous")
    def continuous(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continuous"))

    @continuous.setter
    def continuous(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607d8d40e41b8e33f8ba6e7383e08a06454ff453430f9e2c8373083c10ccee67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continuous", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createDisposition")
    def create_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createDisposition"))

    @create_disposition.setter
    def create_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b86f33d2a175f2492aeff0bbf88eaee106b6d8bca758f2c2b64379c82750d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flattenResults")
    def flatten_results(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "flattenResults"))

    @flatten_results.setter
    def flatten_results(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64f5b924d91436c2a0d00673e242c331851968441b33c96c85c269a89a0df10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flattenResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBillingTier")
    def maximum_billing_tier(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBillingTier"))

    @maximum_billing_tier.setter
    def maximum_billing_tier(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94641c1e251335dd4c9d9dc05ad4648ad7b3574034eda08035c9a1607248805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBillingTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBytesBilled")
    def maximum_bytes_billed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumBytesBilled"))

    @maximum_bytes_billed.setter
    def maximum_bytes_billed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58436650a2b4c4d02831f05a1f4a916180029eff32835adfbab3ac70e3fc5565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBytesBilled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterMode")
    def parameter_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterMode"))

    @parameter_mode.setter
    def parameter_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b8da8426cbd0b4020005a8711826cd1f57ac7c872b49f6ae268714ec73de55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d2e02872b13e8558614dbbb2769cebda96056fef79c248dc259429727ad384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd1ce8f727832a365f2eac4f8d9066751bb18f287e88e7b8223c6be052b56a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaUpdateOptions")
    def schema_update_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "schemaUpdateOptions"))

    @schema_update_options.setter
    def schema_update_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66fd3b3768513861c911b1315f55091a674a75854a4ea6aa229792835133a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaUpdateOptions", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__5114f10e8ff6b57831190ea84c496afc7523efe1236669862bf93a56d01f6cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLegacySql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useQueryCache")
    def use_query_cache(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useQueryCache"))

    @use_query_cache.setter
    def use_query_cache(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280858e3b228c34c5e0cfcb1935fc20a63621bdec5a4fe5d17f4b77ee40a42b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useQueryCache", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeDisposition")
    def write_disposition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeDisposition"))

    @write_disposition.setter
    def write_disposition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa5186c35f697052a97e9e7a23e0bc5c6632fbdce6c0c86b9d53f3c7dad2111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeDisposition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobQuery]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleBigqueryJobQuery]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e6f40a78a34a231f1f29323ca008e49f52eec02204a2b1b2055558d42451d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryScriptOptions",
    jsii_struct_bases=[],
    name_mapping={
        "key_result_statement": "keyResultStatement",
        "statement_byte_budget": "statementByteBudget",
        "statement_timeout_ms": "statementTimeoutMs",
    },
)
class GoogleBigqueryJobQueryScriptOptions:
    def __init__(
        self,
        *,
        key_result_statement: typing.Optional[builtins.str] = None,
        statement_byte_budget: typing.Optional[builtins.str] = None,
        statement_timeout_ms: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_result_statement: Determines which statement in the script represents the "key result", used to populate the schema and query results of the script job. Possible values: ["LAST", "FIRST_SELECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#key_result_statement GoogleBigqueryJob#key_result_statement}
        :param statement_byte_budget: Limit on the number of bytes billed per statement. Exceeding this budget results in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#statement_byte_budget GoogleBigqueryJob#statement_byte_budget}
        :param statement_timeout_ms: Timeout period for each statement in a script. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#statement_timeout_ms GoogleBigqueryJob#statement_timeout_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c35638596eb7d8e5f0fc8ed71649a974d90ecea7f5fed257e78889e8aa737bb)
            check_type(argname="argument key_result_statement", value=key_result_statement, expected_type=type_hints["key_result_statement"])
            check_type(argname="argument statement_byte_budget", value=statement_byte_budget, expected_type=type_hints["statement_byte_budget"])
            check_type(argname="argument statement_timeout_ms", value=statement_timeout_ms, expected_type=type_hints["statement_timeout_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_result_statement is not None:
            self._values["key_result_statement"] = key_result_statement
        if statement_byte_budget is not None:
            self._values["statement_byte_budget"] = statement_byte_budget
        if statement_timeout_ms is not None:
            self._values["statement_timeout_ms"] = statement_timeout_ms

    @builtins.property
    def key_result_statement(self) -> typing.Optional[builtins.str]:
        '''Determines which statement in the script represents the "key result", used to populate the schema and query results of the script job.

        Possible values: ["LAST", "FIRST_SELECT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#key_result_statement GoogleBigqueryJob#key_result_statement}
        '''
        result = self._values.get("key_result_statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_byte_budget(self) -> typing.Optional[builtins.str]:
        '''Limit on the number of bytes billed per statement. Exceeding this budget results in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#statement_byte_budget GoogleBigqueryJob#statement_byte_budget}
        '''
        result = self._values.get("statement_byte_budget")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_timeout_ms(self) -> typing.Optional[builtins.str]:
        '''Timeout period for each statement in a script.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#statement_timeout_ms GoogleBigqueryJob#statement_timeout_ms}
        '''
        result = self._values.get("statement_timeout_ms")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobQueryScriptOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobQueryScriptOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryScriptOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27cb051d3f23467a13130c238ab6acba033db5b9429008cc419ecbb5d40ed2c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyResultStatement")
    def reset_key_result_statement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyResultStatement", []))

    @jsii.member(jsii_name="resetStatementByteBudget")
    def reset_statement_byte_budget(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementByteBudget", []))

    @jsii.member(jsii_name="resetStatementTimeoutMs")
    def reset_statement_timeout_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementTimeoutMs", []))

    @builtins.property
    @jsii.member(jsii_name="keyResultStatementInput")
    def key_result_statement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyResultStatementInput"))

    @builtins.property
    @jsii.member(jsii_name="statementByteBudgetInput")
    def statement_byte_budget_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementByteBudgetInput"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutMsInput")
    def statement_timeout_ms_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementTimeoutMsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyResultStatement")
    def key_result_statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyResultStatement"))

    @key_result_statement.setter
    def key_result_statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f68c6954bd15d3c69e93254415dc3cce5a304a918ebdae6216f27ec691aec06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyResultStatement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementByteBudget")
    def statement_byte_budget(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statementByteBudget"))

    @statement_byte_budget.setter
    def statement_byte_budget(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62862e13ee40ca21f9c411419cf87acde71e1d839acef82f1d9461919466949c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementByteBudget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutMs")
    def statement_timeout_ms(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statementTimeoutMs"))

    @statement_timeout_ms.setter
    def statement_timeout_ms(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a7880a5d16cfee3f6f4c9898af4b633c7c638289fdaa78889b659372e56bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementTimeoutMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobQueryScriptOptions]:
        return typing.cast(typing.Optional[GoogleBigqueryJobQueryScriptOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobQueryScriptOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8116558c78202f67e5e9702012dc5d2dff2535e8de66758c2f4de95747a1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryUserDefinedFunctionResources",
    jsii_struct_bases=[],
    name_mapping={"inline_code": "inlineCode", "resource_uri": "resourceUri"},
)
class GoogleBigqueryJobQueryUserDefinedFunctionResources:
    def __init__(
        self,
        *,
        inline_code: typing.Optional[builtins.str] = None,
        resource_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inline_code: An inline resource that contains code for a user-defined function (UDF). Providing a inline code resource is equivalent to providing a URI for a file containing the same code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#inline_code GoogleBigqueryJob#inline_code}
        :param resource_uri: A code resource to load from a Google Cloud Storage URI (gs://bucket/path). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#resource_uri GoogleBigqueryJob#resource_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485fd753924d252fd23c59db4c866dc15f7aeeaa34278b76f974124ee9f928b6)
            check_type(argname="argument inline_code", value=inline_code, expected_type=type_hints["inline_code"])
            check_type(argname="argument resource_uri", value=resource_uri, expected_type=type_hints["resource_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if resource_uri is not None:
            self._values["resource_uri"] = resource_uri

    @builtins.property
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''An inline resource that contains code for a user-defined function (UDF).

        Providing a inline code resource is equivalent to providing a URI for a file containing the same code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#inline_code GoogleBigqueryJob#inline_code}
        '''
        result = self._values.get("inline_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_uri(self) -> typing.Optional[builtins.str]:
        '''A code resource to load from a Google Cloud Storage URI (gs://bucket/path).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#resource_uri GoogleBigqueryJob#resource_uri}
        '''
        result = self._values.get("resource_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobQueryUserDefinedFunctionResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobQueryUserDefinedFunctionResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryUserDefinedFunctionResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4347bd6ec5ed8c432af8ae8e92e0bb906e01f745baa6bae207fd5b5e28e81629)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBigqueryJobQueryUserDefinedFunctionResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369843b0611fb2520e6b3dc8a9ab5084676f73dc04ee736fa093bf9cc7f37358)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBigqueryJobQueryUserDefinedFunctionResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fbdfe060499c59610f10dd0ceeb7295d6266a714d65a3a9e54c519392357a93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d917b51e3ba44d8c7f9240ad70b7cbb574b365cabceaf173cc28babc663b721)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b32d268b376ffd62d7a939f3efd5bcb3e9a602aa62b8071ca64b6969a2af39a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobQueryUserDefinedFunctionResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobQueryUserDefinedFunctionResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobQueryUserDefinedFunctionResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331f3ae9370c5f12f4472daf8279e841de96f78fdf4792c7cfbdcac3e3316d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobQueryUserDefinedFunctionResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobQueryUserDefinedFunctionResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32da890e7f9a423dbf44ce5c9e257212532c6592da9a53b142069815fed8fedd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInlineCode")
    def reset_inline_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineCode", []))

    @jsii.member(jsii_name="resetResourceUri")
    def reset_resource_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceUri", []))

    @builtins.property
    @jsii.member(jsii_name="inlineCodeInput")
    def inline_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceUriInput")
    def resource_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineCode")
    def inline_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inlineCode"))

    @inline_code.setter
    def inline_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179cef93e7558eeb6f30ec329647a8b74345ae0678d58b3f97d60a098b703442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inlineCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceUri")
    def resource_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceUri"))

    @resource_uri.setter
    def resource_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be2ad2d661be33f6bd59e6e4a82c6674d20f58476847ae4360e51424ec85e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobQueryUserDefinedFunctionResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobQueryUserDefinedFunctionResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobQueryUserDefinedFunctionResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58054c8d60e571a91e1445d88ba7eb59f88185af54dae4b72cb6f25062f5465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBigqueryJobStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusErrorResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBigqueryJobStatusErrorResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobStatusErrorResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobStatusErrorResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusErrorResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d4a43061553a241f1617977e88c74c0841c66fb6d724d3aa2c12433df422d8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBigqueryJobStatusErrorResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed7b180f89157e01ae775fc8ea27386dd8a4735f7adc2ab6263d5a0400a2290)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBigqueryJobStatusErrorResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5a54d151739c7ff2f9d803e89746abe951f543c1539125e28dd83ba0c6b93d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f526a821eb3397ad08d135a0a6f56b3abe8669d7895a03a7dffcf10b76fc2788)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc321f6ba2960c22e5a0f1860d3f41b1dded9efab8ab843dcab32cf790e8bb46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobStatusErrorResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusErrorResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e18e2f19250a082a0f9a077ed1dba1f0c8057484c13727461160c227e84237b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobStatusErrorResult]:
        return typing.cast(typing.Optional[GoogleBigqueryJobStatusErrorResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobStatusErrorResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761b453fd799b23f8050c453e7ea81e9c659714eedd856e4849ba6d090c21cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusErrors",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBigqueryJobStatusErrors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobStatusErrors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobStatusErrorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusErrorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45a9bb723a6e8993070f7c2de4297d4a26a3fae25148e3f244d73fb0249f7a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleBigqueryJobStatusErrorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207637f9de7872dcbc422be05f7698a1bb35d5433e6042201c5b73206616fd4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBigqueryJobStatusErrorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa21463fbd2f2d5dfd199a4f328c5a6d08c54a5d31bc9e4f1a881a7d0e247dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2f9659c10bc5c5a52cb3a9d81f12734372cbf7a3338bee22c3c4b12ed97375)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55dfbc1e9a8c24f572d1354ca4e3614d32b7cd38b7eb41171a17e60ed8674323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobStatusErrorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusErrorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f6f94502a55aee030717f9b26d604312a16e84470456db00e2f3fb60ca101cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobStatusErrors]:
        return typing.cast(typing.Optional[GoogleBigqueryJobStatusErrors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryJobStatusErrors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a14f21d186b4a8e67484ecfeb98e265eaecf0be0c1eddb6018c78e3089fac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5d893390c17ed60e510a55af4267eb61164fc40c4ad6a04cadef91326e8762d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleBigqueryJobStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e8fa4edebd09c0dc33caed6e8a67418215352de3f1110bad3702e47f375988)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBigqueryJobStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed46639ba275865bf0790281fbce06f620e1eeb4cf86bdc6501ec7842cac3eb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f98ae4fd9970e28476293d6ed9ef26221ffb7c48ef53a8e1d840cffa71aee91a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed190b8deeed518798712083527ad3082d3cb12721db4efa9ef54c111de24569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryJobStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fa775d03c8299e60ac2f9404302edfaa26b75696af63d98113fe2cf847358da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="errorResult")
    def error_result(self) -> GoogleBigqueryJobStatusErrorResultList:
        return typing.cast(GoogleBigqueryJobStatusErrorResultList, jsii.get(self, "errorResult"))

    @builtins.property
    @jsii.member(jsii_name="errors")
    def errors(self) -> GoogleBigqueryJobStatusErrorsList:
        return typing.cast(GoogleBigqueryJobStatusErrorsList, jsii.get(self, "errors"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryJobStatus]:
        return typing.cast(typing.Optional[GoogleBigqueryJobStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleBigqueryJobStatus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd8a621ba71b79fbf13979b5558bf1bfd190ea6f5cd2285eb891325145c8e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBigqueryJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create GoogleBigqueryJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#delete GoogleBigqueryJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#update GoogleBigqueryJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b4b01b8537db4f093b43ea26f815c387d108eba7fe50ceb77361b829268fad)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#create GoogleBigqueryJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#delete GoogleBigqueryJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_job#update GoogleBigqueryJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryJob.GoogleBigqueryJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e3f75f1134e0f5a9268f9da65624fd05b0a8900dc9205bbf85a82400197d8f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__956461b105d7d95c21c012bee5758a569df3e38023b9aa67db2f9018b3dd2750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc50fee3de8270d44baba8525a4af91a7356e6b3aaa1e128866824e95fbf1b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f14d99a8394df80fdfacd6cfc5a22ea8fdc3ea5798220053acebbec03cf4a11a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253197349a42ec3d7d15bc7a286e9847cbea83353e238b61f936435ae85c06fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBigqueryJob",
    "GoogleBigqueryJobConfig",
    "GoogleBigqueryJobCopy",
    "GoogleBigqueryJobCopyDestinationEncryptionConfiguration",
    "GoogleBigqueryJobCopyDestinationEncryptionConfigurationOutputReference",
    "GoogleBigqueryJobCopyDestinationTable",
    "GoogleBigqueryJobCopyDestinationTableOutputReference",
    "GoogleBigqueryJobCopyOutputReference",
    "GoogleBigqueryJobCopySourceTables",
    "GoogleBigqueryJobCopySourceTablesList",
    "GoogleBigqueryJobCopySourceTablesOutputReference",
    "GoogleBigqueryJobExtract",
    "GoogleBigqueryJobExtractOutputReference",
    "GoogleBigqueryJobExtractSourceModel",
    "GoogleBigqueryJobExtractSourceModelOutputReference",
    "GoogleBigqueryJobExtractSourceTable",
    "GoogleBigqueryJobExtractSourceTableOutputReference",
    "GoogleBigqueryJobLoad",
    "GoogleBigqueryJobLoadDestinationEncryptionConfiguration",
    "GoogleBigqueryJobLoadDestinationEncryptionConfigurationOutputReference",
    "GoogleBigqueryJobLoadDestinationTable",
    "GoogleBigqueryJobLoadDestinationTableOutputReference",
    "GoogleBigqueryJobLoadOutputReference",
    "GoogleBigqueryJobLoadParquetOptions",
    "GoogleBigqueryJobLoadParquetOptionsOutputReference",
    "GoogleBigqueryJobLoadTimePartitioning",
    "GoogleBigqueryJobLoadTimePartitioningOutputReference",
    "GoogleBigqueryJobQuery",
    "GoogleBigqueryJobQueryDefaultDataset",
    "GoogleBigqueryJobQueryDefaultDatasetOutputReference",
    "GoogleBigqueryJobQueryDestinationEncryptionConfiguration",
    "GoogleBigqueryJobQueryDestinationEncryptionConfigurationOutputReference",
    "GoogleBigqueryJobQueryDestinationTable",
    "GoogleBigqueryJobQueryDestinationTableOutputReference",
    "GoogleBigqueryJobQueryOutputReference",
    "GoogleBigqueryJobQueryScriptOptions",
    "GoogleBigqueryJobQueryScriptOptionsOutputReference",
    "GoogleBigqueryJobQueryUserDefinedFunctionResources",
    "GoogleBigqueryJobQueryUserDefinedFunctionResourcesList",
    "GoogleBigqueryJobQueryUserDefinedFunctionResourcesOutputReference",
    "GoogleBigqueryJobStatus",
    "GoogleBigqueryJobStatusErrorResult",
    "GoogleBigqueryJobStatusErrorResultList",
    "GoogleBigqueryJobStatusErrorResultOutputReference",
    "GoogleBigqueryJobStatusErrors",
    "GoogleBigqueryJobStatusErrorsList",
    "GoogleBigqueryJobStatusErrorsOutputReference",
    "GoogleBigqueryJobStatusList",
    "GoogleBigqueryJobStatusOutputReference",
    "GoogleBigqueryJobTimeouts",
    "GoogleBigqueryJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__64d016de9370127accbfc801d530d02bb263e20df82a9ceede54ac6b1b81ba2f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    job_id: builtins.str,
    copy: typing.Optional[typing.Union[GoogleBigqueryJobCopy, typing.Dict[builtins.str, typing.Any]]] = None,
    extract: typing.Optional[typing.Union[GoogleBigqueryJobExtract, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    job_timeout_ms: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load: typing.Optional[typing.Union[GoogleBigqueryJobLoad, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    query: typing.Optional[typing.Union[GoogleBigqueryJobQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c992fedf8d840ad912eadd0b45964382899a897197ef355ce1885f91122c82c4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2bd79b60afb85e4978ad6c85f3192931bdd423abd0bb517f42c1b3e8d43984(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20034d4695a355a01ca2738faa21ab4bdd6ee36d9cb3b6a93d01588f65694a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5571d4b3576b06994b1c2e852c02a10958967fddd3c6aead60a2c75ecd01c9b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35f71566fe67311bc83bdad796a40a414834e750903b4a59daf986bdd93ee9e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b18b6b61be1a88807d21cce1db7263c5381fc35c5bac15ba73eca6bc1833ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04693f430e4b5280be17ff83b158b94d5e8bd3f1fb423219d5c9ba410caa225b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422be9c12004b415a057025054cf812509a1b8a81c4c31f60e9a3ad38f62dd3b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    job_id: builtins.str,
    copy: typing.Optional[typing.Union[GoogleBigqueryJobCopy, typing.Dict[builtins.str, typing.Any]]] = None,
    extract: typing.Optional[typing.Union[GoogleBigqueryJobExtract, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    job_timeout_ms: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load: typing.Optional[typing.Union[GoogleBigqueryJobLoad, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    query: typing.Optional[typing.Union[GoogleBigqueryJobQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7287674d3b6ec771b37810e8c709b0fd45824b4961fa16273641289ed9a138a(
    *,
    source_tables: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryJobCopySourceTables, typing.Dict[builtins.str, typing.Any]]]],
    create_disposition: typing.Optional[builtins.str] = None,
    destination_encryption_configuration: typing.Optional[typing.Union[GoogleBigqueryJobCopyDestinationEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    destination_table: typing.Optional[typing.Union[GoogleBigqueryJobCopyDestinationTable, typing.Dict[builtins.str, typing.Any]]] = None,
    write_disposition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2b910f57b28de9cea0a17ac575a6b9d4fc3e9412d213d37121381185d7af94(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61bb7fc567a168eda78d88391c372a16180ba20b2db1c7ec72d7b8b02228f0be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cc9caa8cc9d87b638ade211e78a9a26039b8f613f789d9a772236a2e9b0279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453ab24ea25cf4ae3e19859f4db21ce1ffce823f603716c14de592233d7379e2(
    value: typing.Optional[GoogleBigqueryJobCopyDestinationEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7942fffd8225e0f837de7f4ec382d21e410f9a4153914a05ca69763b6dd9c2fb(
    *,
    table_id: builtins.str,
    dataset_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e571fb8057b8c8a0ad3e7d7f656562bc7bd20d0451edb83f17035e816f6f47f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bedefb1c8972bef19fdd9d24424e7edcfd2d4e0b0c97d9278b1436afd188eb21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4c1d75baa8cf9f5139adea93ecc59c2ed9d77552b63c89cbb1bf1c9bd816af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb548f6b9a61576f7b6c8cf9aeed958ed71c049519cddb084bfe7371fde3fce4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1509d6c5eff247e8ea7cee98a4d0903c1dfae7ad2ba8a49c7c4d3ab38cd23a(
    value: typing.Optional[GoogleBigqueryJobCopyDestinationTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631488c61265e5790e13379be726bfe6a2170a2ebc54bdfc426da88364d705fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6b5b078901dd55295e89051ed4e6689c5cdbf1cc40dbbd27f0e00c66b0338a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryJobCopySourceTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4e1e18c76693fdb1178e1953708ab7cbd3c631bb99a00c9cf530037106c300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b99339a6775944b08cfce94b3dc0f294865a81e75b4cc64c15953db964d6b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf34ec45851cc8d36eb7b26951c919ce5d7dec4754995dc4535aad4050e46bec(
    value: typing.Optional[GoogleBigqueryJobCopy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f398a8598a936143bec78bad8df5df250cdbe17e1b261dd8068bf2164f7219(
    *,
    table_id: builtins.str,
    dataset_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b911dc648a5a0e4afe4bf6be1fb8928d089d5e934a1d1731f7d7245bb7d140(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117b3ea5bb7db379e3d100bd3ff0d97ade74f6e2d5b7149525de86769f5c5765(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5675b05397e9836f8b6814ca03baa20c769deaa40126363e49c4da8cefb9c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d0e9b9010cac8aae83a9d4581f79fb774a598fa086ecf2681d8ae7e900994b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6e3192858f43fb1d14b582cdd3d43775cd5ee735063bd23a7b9a94a5d5cde2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f26748dda4e439c270949df7f9ee2fd29abb7f5772630865521298fee1ca1d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobCopySourceTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfc53ddcdbff90420d62d3c492caf4f09b37b376c6095cdd2495e018e5298b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04333cf0648c4669e4950aca3b1fc3cd187262f4c1f1e4d4d24210c022c28f10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af666690ad05b81e4555c781d4e730c8d272d6835f73f9104083c9bb9138f76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f2b026e5cc5c9d96b99294fe8d257a777fb842055bf9a2ef8f34f03f580e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b774eec45e581d8110051a8ad065ee31f495de3bb7161d70601ff6a2dd834f9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobCopySourceTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00e8a8f9c8dc8ef988b5f0a5680fa482da4f46c63fd199ef4d4d373fc12a9ce(
    *,
    destination_uris: typing.Sequence[builtins.str],
    compression: typing.Optional[builtins.str] = None,
    destination_format: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    print_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_model: typing.Optional[typing.Union[GoogleBigqueryJobExtractSourceModel, typing.Dict[builtins.str, typing.Any]]] = None,
    source_table: typing.Optional[typing.Union[GoogleBigqueryJobExtractSourceTable, typing.Dict[builtins.str, typing.Any]]] = None,
    use_avro_logical_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a1c2b7b34a8f265ac7118e30d3bb341caf8542706ccc6d5a6b07d12ae8acd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eba62947dd5a12918f34a30020c2df9ce27c6df730f1045aaf6b7a4857573be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75df51095267bfba371e5ded8ec79fab50e0f0126a3730c0bc3c8ce2b936ec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c9787158debc32e5172bb5f63d934a14465cd0e8ae206dfc392246e172d58f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8ed6d251abb4c038689d471839038fa93db29cecec60469fa02c29599c3b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caacbb8d1d6f38daa7857aa9ff5ff1c43a52d9151460c8ac24ef49f8e12e82de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3085f0d8d2e0572f8b610a3127f85ee5a7a6e35e90ed024b2b93ded7dfd075(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1937faa3ea70daad62b16971d15f338dcf103c933f0c068f4fb8b856d727f30(
    value: typing.Optional[GoogleBigqueryJobExtract],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953a33c1ad45eb37b1090a561bffcd44327027840767b0706d80d44d3269f0b9(
    *,
    dataset_id: builtins.str,
    model_id: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7120f932732dfa38e6f98d38fa1f2de0e14b77e9225ebd42a115d2e476a65f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943e849008d18d961b5053d6f41143bde6dc9b8211704ab4b304a3b4b568c09f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6ae33b9bd9f7e66ebe170c39c0086e896c9a2e55abfad8d64c4721d58bfc24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541d51b4ddc432d0913277623206222db26ad569f685868a2bbf05313be0ffe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f79f27fd394ffe7c02b0e181cadd1b027667ed4ddc35a9aedd25247c6216a38(
    value: typing.Optional[GoogleBigqueryJobExtractSourceModel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ea5274027064d1b82e2dc12be903c3fa487f501ac44081c13905c1bbd3a79a(
    *,
    table_id: builtins.str,
    dataset_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef0ac9f97b668763c6bb130640ac20ced1daee46968891bc7c357172de1853c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976611dd06e10c6d0ac269066a65306d074a93ae7074d3b0c65b6f9f6ed38622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e886643e1c43f9a395bd1f4f7bedfecd3022675d1e3eea2aa5f62f6d51cee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a73cdab3790b5d932c5983de917e239b3b352a947b1cf0d06f2f67737b4b5d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b627f9bd136a16466b9767327b2740d83ac97576c3d5db9a50af4844e9e142(
    value: typing.Optional[GoogleBigqueryJobExtractSourceTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327b4ac50c5058c33f8d9bdc8c24244a7fa32cfedc1080124b2356a18ac8f05d(
    *,
    destination_table: typing.Union[GoogleBigqueryJobLoadDestinationTable, typing.Dict[builtins.str, typing.Any]],
    source_uris: typing.Sequence[builtins.str],
    allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    autodetect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_disposition: typing.Optional[builtins.str] = None,
    destination_encryption_configuration: typing.Optional[typing.Union[GoogleBigqueryJobLoadDestinationEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    encoding: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_extension: typing.Optional[builtins.str] = None,
    max_bad_records: typing.Optional[jsii.Number] = None,
    null_marker: typing.Optional[builtins.str] = None,
    parquet_options: typing.Optional[typing.Union[GoogleBigqueryJobLoadParquetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    projection_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    quote: typing.Optional[builtins.str] = None,
    schema_update_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_leading_rows: typing.Optional[jsii.Number] = None,
    source_format: typing.Optional[builtins.str] = None,
    time_partitioning: typing.Optional[typing.Union[GoogleBigqueryJobLoadTimePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    write_disposition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970bd2c072850434de24403f52f86e1592244c053cf6eb010e586f310537a8df(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697818b1e958df6322b47a5c9039ae964515876e2f48bff76b6802821c9ef4cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e92a363631cef595d0b690a81dc931d4f6359041fc79da24cb4940a1492c2cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0dfce41562442fd0699ce30aebbc6a5f3aae752d3b4c993c09a9a0e75711dd(
    value: typing.Optional[GoogleBigqueryJobLoadDestinationEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea22afb464c998203a21c72ad410ddfb64dfec9600b70b96c9c650e25292c46b(
    *,
    table_id: builtins.str,
    dataset_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f10a6edb9759475b5af4a44e036cfc23943aa270a428b8302867b1af76d9513(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b49c09b00ea7eacbcfab5ffc72a7a04c24c7c024ccd74c48a7ff54cc00eb7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9c9e133c7f8ba609f32c88814b8089c548355c60d91a86926ec1c801aa034b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e406572499febb4a31bffeb3fdbd203462ad38fb3fcdcc327b4311f40279c96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0709b316912f08b3c23c50429db4ee7fe7f2b9c1e7eefe7eecd0227a0d8489b(
    value: typing.Optional[GoogleBigqueryJobLoadDestinationTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f130380e9a3cc3c050ffda867000f55ad39e65dfdb7e4e8e547405174da9ee4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22991294fe9a143a824a877086b413798c727eff557b1cc3fbb91442dce55acc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce621a8f2b6cfe0dcaabcbd966aff74c074ab9af4aebb4ef7f19f6960325ffd6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffdeee17ee55f3a18ea9689a13893903eea8d5f769cbeeffd8e0843d7c64683(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a258d5a90480fedfc639923c67792403ce3be0b2d41727c82acc458652116cc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b267a2e407869e13333147e48524fbc8bc8664e5663f9a5cee3a09b79484cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f004be2fcc70f7c2251f8dd816b87ee18f3c4c969c7a392cf52c5d0c4311c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13ac6bf5c45da69fe6f342ae1c6b25f49329afa4014f4caa3630a2c544a7e55(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234cfbb07a9793faf006b0e0137b4559cc513dcdfaf795e64695a33fdb6fd6e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1068f48c6e309cddbd25beee2e29c774a63d6e161eddac88ddf4c286f9f9d4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1249235b2cb0b47afef5d0595a729b5af1abd99257c8700896b83a5839bc3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b493fa0a3f7e25f8f71fdd10030b7e95f11cdf3b23148a79e17a57d968d78aa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84375c81a10d8e770089f3065e20d217e54b3d432b32e1ccf7991a85ace717f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d83ad651d8b3ca6131ed4ba5c235703d19b433f8d80135d69b0d0e8eb5ead9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6e9eb75520d4238a66d5eeba023e5e5a7d66f8675714afdf753b0915a0176e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a3c6acec268cf356f536ee974c2a55aec4fcc89ca1fcc1d3619d7ea04a0ce8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c60c801f245f54c14712014e95f813e1ca43f6db4f6364a87bafd061f8c156(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f3d3d73e645045b2360f4141da2d9a133536fd962e7fe46909fcf7b24df26a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546f6bc1273827a90a73705da1c615c7ae5e0cda431c42db30140d9c6348f09b(
    value: typing.Optional[GoogleBigqueryJobLoad],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495696a71e6a0e119da6de34dae3a153fd6b8b1ede85df734e00b4385cd266fb(
    *,
    enable_list_inference: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enum_as_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99f2d1d39a2be5e936fdc37c655a09cbca5cc86f0cc60dd837ef9b182b87573(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c38966446e68e4b9053b884926080e8b6678ab91ca4d1fa6bc8a94991220b75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9879c77040234bb63db92db08f083ff514f04e82b78e5ce464176d174907a4b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8ffeab1d526451a266f9fd027b2169d2937f2f6654786ee5d8716c59bee14a(
    value: typing.Optional[GoogleBigqueryJobLoadParquetOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f763ab8fa69b9cf9b6e148e5d772cf8b07e6a12c8494eee584d6e728aae7c6d6(
    *,
    type: builtins.str,
    expiration_ms: typing.Optional[builtins.str] = None,
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2104c536fba7bcdf6808ff105b777324f70bd3fd861c157548c2ac35cb7dae4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624ce0fc3b2524e743ac2213bcc927e62c4c3349b2f0e7f923cd81c8a3f3cf75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627fb5fdc8ee3b07ca007700d96dea119275ee32213f617e4fc2c5147dea65cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9c834cd92e9d2d3e1e3cf1b7819d51573a2aa4d092dec93a8f3a4b6b63a723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe0903c8d22ce94d9ebdda5ff08413f54d7ab080a3ef657860eed0e8bd3a3f4(
    value: typing.Optional[GoogleBigqueryJobLoadTimePartitioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d144d097002e6c8bcf69ccc2cec979440784c7c97d8cd761220ede60af74f209(
    *,
    query: builtins.str,
    allow_large_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    continuous: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_disposition: typing.Optional[builtins.str] = None,
    default_dataset: typing.Optional[typing.Union[GoogleBigqueryJobQueryDefaultDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    destination_encryption_configuration: typing.Optional[typing.Union[GoogleBigqueryJobQueryDestinationEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    destination_table: typing.Optional[typing.Union[GoogleBigqueryJobQueryDestinationTable, typing.Dict[builtins.str, typing.Any]]] = None,
    flatten_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maximum_billing_tier: typing.Optional[jsii.Number] = None,
    maximum_bytes_billed: typing.Optional[builtins.str] = None,
    parameter_mode: typing.Optional[builtins.str] = None,
    priority: typing.Optional[builtins.str] = None,
    schema_update_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    script_options: typing.Optional[typing.Union[GoogleBigqueryJobQueryScriptOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_query_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_defined_function_resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryJobQueryUserDefinedFunctionResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    write_disposition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c8d81da5295ed1dded97b87b5bd4ee36ff23649f24dde8b906f707d89d75a6(
    *,
    dataset_id: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3639fcbdedddb0126018397ca0431b3e954dc966badacefe1718c985ea03a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592aac5a22ab514852ac34cb2d743fb79ce0475b04d3018a391e228f8cb0ddcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c01550f15d1cb51c75ab61b6e82766b888cad83d2286bb647099f0b7bb173a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219444355624388ff105311f18bc93fc9c06d309576ffbb4600d1aa7bfe93852(
    value: typing.Optional[GoogleBigqueryJobQueryDefaultDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3a5566ebb120a171d4c07ba883d8e1af67a9d6e5aaefcd5c0a44dbdebc3c41(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0b1217bf1adf7ae3464a6684e51649f0eebc777bc578c3b0e676b72c9c47fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5eef71a6e3f7ba4877099d5d2056857d88ee2e1b0ab16f0c06d0505c2d2c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6e0832b1e361fdc8297f70ff30fc25a108d4818287044c4be3b3d4e67e9dfe(
    value: typing.Optional[GoogleBigqueryJobQueryDestinationEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9eb7550c451b0ff94ce57a19b0d16db80b71759e89c970836f80ce362a5024(
    *,
    table_id: builtins.str,
    dataset_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff89cd2a322730cff310fca5ea3a6ce031857a96f677792c204bb9006b1b9b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5268836032f7d3a269d748659a31015f62ce1baf9279309b5391a87437662436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddff6864f83ea06c1e2fdb5dff4a584c7dbaacf0e441d9c81ba1a3108940f37b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dce7437266a43dae1e92314f7f5b4156efd0289768f4c759899df1f2a7cfd23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e687b2cbc652428fc00f6ba545e4e0904b64afe7c46e0ffb147ff40f6b99b6(
    value: typing.Optional[GoogleBigqueryJobQueryDestinationTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196f738efdaa8c13a19ec167245d22f409d1f4c2352efbc92e23194c7a677ebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d0d47a3211910ee37b51d2449a69fe125b25fe485663a909786d20f91310ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryJobQueryUserDefinedFunctionResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f5f0ea82b4066eeacee162ac99aa30c9b8d7393ecab5b9a8c69c8d6bf6da7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607d8d40e41b8e33f8ba6e7383e08a06454ff453430f9e2c8373083c10ccee67(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b86f33d2a175f2492aeff0bbf88eaee106b6d8bca758f2c2b64379c82750d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64f5b924d91436c2a0d00673e242c331851968441b33c96c85c269a89a0df10(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94641c1e251335dd4c9d9dc05ad4648ad7b3574034eda08035c9a1607248805(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58436650a2b4c4d02831f05a1f4a916180029eff32835adfbab3ac70e3fc5565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b8da8426cbd0b4020005a8711826cd1f57ac7c872b49f6ae268714ec73de55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d2e02872b13e8558614dbbb2769cebda96056fef79c248dc259429727ad384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd1ce8f727832a365f2eac4f8d9066751bb18f287e88e7b8223c6be052b56a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66fd3b3768513861c911b1315f55091a674a75854a4ea6aa229792835133a6f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5114f10e8ff6b57831190ea84c496afc7523efe1236669862bf93a56d01f6cfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280858e3b228c34c5e0cfcb1935fc20a63621bdec5a4fe5d17f4b77ee40a42b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa5186c35f697052a97e9e7a23e0bc5c6632fbdce6c0c86b9d53f3c7dad2111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e6f40a78a34a231f1f29323ca008e49f52eec02204a2b1b2055558d42451d4(
    value: typing.Optional[GoogleBigqueryJobQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c35638596eb7d8e5f0fc8ed71649a974d90ecea7f5fed257e78889e8aa737bb(
    *,
    key_result_statement: typing.Optional[builtins.str] = None,
    statement_byte_budget: typing.Optional[builtins.str] = None,
    statement_timeout_ms: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cb051d3f23467a13130c238ab6acba033db5b9429008cc419ecbb5d40ed2c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f68c6954bd15d3c69e93254415dc3cce5a304a918ebdae6216f27ec691aec06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62862e13ee40ca21f9c411419cf87acde71e1d839acef82f1d9461919466949c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a7880a5d16cfee3f6f4c9898af4b633c7c638289fdaa78889b659372e56bda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8116558c78202f67e5e9702012dc5d2dff2535e8de66758c2f4de95747a1c5(
    value: typing.Optional[GoogleBigqueryJobQueryScriptOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485fd753924d252fd23c59db4c866dc15f7aeeaa34278b76f974124ee9f928b6(
    *,
    inline_code: typing.Optional[builtins.str] = None,
    resource_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4347bd6ec5ed8c432af8ae8e92e0bb906e01f745baa6bae207fd5b5e28e81629(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369843b0611fb2520e6b3dc8a9ab5084676f73dc04ee736fa093bf9cc7f37358(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbdfe060499c59610f10dd0ceeb7295d6266a714d65a3a9e54c519392357a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d917b51e3ba44d8c7f9240ad70b7cbb574b365cabceaf173cc28babc663b721(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32d268b376ffd62d7a939f3efd5bcb3e9a602aa62b8071ca64b6969a2af39a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331f3ae9370c5f12f4472daf8279e841de96f78fdf4792c7cfbdcac3e3316d8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryJobQueryUserDefinedFunctionResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32da890e7f9a423dbf44ce5c9e257212532c6592da9a53b142069815fed8fedd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179cef93e7558eeb6f30ec329647a8b74345ae0678d58b3f97d60a098b703442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be2ad2d661be33f6bd59e6e4a82c6674d20f58476847ae4360e51424ec85e95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58054c8d60e571a91e1445d88ba7eb59f88185af54dae4b72cb6f25062f5465(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobQueryUserDefinedFunctionResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4a43061553a241f1617977e88c74c0841c66fb6d724d3aa2c12433df422d8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed7b180f89157e01ae775fc8ea27386dd8a4735f7adc2ab6263d5a0400a2290(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5a54d151739c7ff2f9d803e89746abe951f543c1539125e28dd83ba0c6b93d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f526a821eb3397ad08d135a0a6f56b3abe8669d7895a03a7dffcf10b76fc2788(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc321f6ba2960c22e5a0f1860d3f41b1dded9efab8ab843dcab32cf790e8bb46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18e2f19250a082a0f9a077ed1dba1f0c8057484c13727461160c227e84237b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761b453fd799b23f8050c453e7ea81e9c659714eedd856e4849ba6d090c21cf9(
    value: typing.Optional[GoogleBigqueryJobStatusErrorResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45a9bb723a6e8993070f7c2de4297d4a26a3fae25148e3f244d73fb0249f7a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207637f9de7872dcbc422be05f7698a1bb35d5433e6042201c5b73206616fd4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa21463fbd2f2d5dfd199a4f328c5a6d08c54a5d31bc9e4f1a881a7d0e247dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2f9659c10bc5c5a52cb3a9d81f12734372cbf7a3338bee22c3c4b12ed97375(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55dfbc1e9a8c24f572d1354ca4e3614d32b7cd38b7eb41171a17e60ed8674323(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6f94502a55aee030717f9b26d604312a16e84470456db00e2f3fb60ca101cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a14f21d186b4a8e67484ecfeb98e265eaecf0be0c1eddb6018c78e3089fac5(
    value: typing.Optional[GoogleBigqueryJobStatusErrors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d893390c17ed60e510a55af4267eb61164fc40c4ad6a04cadef91326e8762d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e8fa4edebd09c0dc33caed6e8a67418215352de3f1110bad3702e47f375988(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed46639ba275865bf0790281fbce06f620e1eeb4cf86bdc6501ec7842cac3eb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98ae4fd9970e28476293d6ed9ef26221ffb7c48ef53a8e1d840cffa71aee91a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed190b8deeed518798712083527ad3082d3cb12721db4efa9ef54c111de24569(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa775d03c8299e60ac2f9404302edfaa26b75696af63d98113fe2cf847358da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd8a621ba71b79fbf13979b5558bf1bfd190ea6f5cd2285eb891325145c8e40(
    value: typing.Optional[GoogleBigqueryJobStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b4b01b8537db4f093b43ea26f815c387d108eba7fe50ceb77361b829268fad(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3f75f1134e0f5a9268f9da65624fd05b0a8900dc9205bbf85a82400197d8f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956461b105d7d95c21c012bee5758a569df3e38023b9aa67db2f9018b3dd2750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc50fee3de8270d44baba8525a4af91a7356e6b3aaa1e128866824e95fbf1b2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14d99a8394df80fdfacd6cfc5a22ea8fdc3ea5798220053acebbec03cf4a11a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253197349a42ec3d7d15bc7a286e9847cbea83353e238b61f936435ae85c06fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
