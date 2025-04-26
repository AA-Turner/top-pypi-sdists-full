r'''
# `snowflake_file_format`

Refer to the Terraform Registry for docs: [`snowflake_file_format`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format).
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


class FileFormat(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.fileFormat.FileFormat",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format snowflake_file_format}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        format_type: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        allow_duplicate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        binary_as_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        binary_format: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        compression: typing.Optional[builtins.str] = None,
        date_format: typing.Optional[builtins.str] = None,
        disable_auto_convert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_snowflake_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        empty_field_as_null: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_octal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        error_on_column_count_mismatch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escape: typing.Optional[builtins.str] = None,
        escape_unenclosed_field: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        field_optionally_enclosed_by: typing.Optional[builtins.str] = None,
        file_extension: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_utf8_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        null_if: typing.Optional[typing.Sequence[builtins.str]] = None,
        parse_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preserve_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_delimiter: typing.Optional[builtins.str] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_blank_lines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_byte_order_mark: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_header: typing.Optional[jsii.Number] = None,
        strip_null_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strip_outer_array: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strip_outer_element: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_format: typing.Optional[builtins.str] = None,
        timestamp_format: typing.Optional[builtins.str] = None,
        trim_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format snowflake_file_format} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the file format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#database FileFormat#database}
        :param format_type: Specifies the format of the input files (for data loading) or output files (for data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#format_type FileFormat#format_type}
        :param name: Specifies the identifier for the file format; must be unique for the database and schema in which the file format is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#name FileFormat#name}
        :param schema: The schema in which to create the file format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#schema FileFormat#schema}
        :param allow_duplicate: Boolean that specifies to allow duplicate object field names (only the last one will be preserved). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#allow_duplicate FileFormat#allow_duplicate}
        :param binary_as_text: Boolean that specifies whether to interpret columns with no defined logical data type as UTF-8 text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#binary_as_text FileFormat#binary_as_text}
        :param binary_format: Defines the encoding format for binary input or output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#binary_format FileFormat#binary_format}
        :param comment: Specifies a comment for the file format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#comment FileFormat#comment}
        :param compression: Specifies the current compression algorithm for the data file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#compression FileFormat#compression}
        :param date_format: Defines the format of date values in the data files (data loading) or table (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#date_format FileFormat#date_format}
        :param disable_auto_convert: Boolean that specifies whether the XML parser disables automatic conversion of numeric and Boolean values from text to native representation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#disable_auto_convert FileFormat#disable_auto_convert}
        :param disable_snowflake_data: Boolean that specifies whether the XML parser disables recognition of Snowflake semi-structured data tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#disable_snowflake_data FileFormat#disable_snowflake_data}
        :param empty_field_as_null: Specifies whether to insert SQL NULL for empty fields in an input file, which are represented by two successive delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#empty_field_as_null FileFormat#empty_field_as_null}
        :param enable_octal: Boolean that enables parsing of octal numbers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#enable_octal FileFormat#enable_octal}
        :param encoding: String (constant) that specifies the character set of the source data when loading data into a table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#encoding FileFormat#encoding}
        :param error_on_column_count_mismatch: Boolean that specifies whether to generate a parsing error if the number of delimited columns (i.e. fields) in an input file does not match the number of columns in the corresponding table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#error_on_column_count_mismatch FileFormat#error_on_column_count_mismatch}
        :param escape: Single character string used as the escape character for field values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#escape FileFormat#escape}
        :param escape_unenclosed_field: Single character string used as the escape character for unenclosed field values only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#escape_unenclosed_field FileFormat#escape_unenclosed_field}
        :param field_delimiter: Specifies one or more singlebyte or multibyte characters that separate fields in an input file (data loading) or unloaded file (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#field_delimiter FileFormat#field_delimiter}
        :param field_optionally_enclosed_by: Character used to enclose strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#field_optionally_enclosed_by FileFormat#field_optionally_enclosed_by}
        :param file_extension: Specifies the extension for files unloaded to a stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#file_extension FileFormat#file_extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#id FileFormat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_utf8_errors: Boolean that specifies whether UTF-8 encoding errors produce error conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#ignore_utf8_errors FileFormat#ignore_utf8_errors}
        :param null_if: String used to convert to and from SQL NULL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#null_if FileFormat#null_if}
        :param parse_header: Boolean that specifies whether to use the first row headers in the data files to determine column names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#parse_header FileFormat#parse_header}
        :param preserve_space: Boolean that specifies whether the XML parser preserves leading and trailing spaces in element content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#preserve_space FileFormat#preserve_space}
        :param record_delimiter: Specifies one or more singlebyte or multibyte characters that separate records in an input file (data loading) or unloaded file (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#record_delimiter FileFormat#record_delimiter}
        :param replace_invalid_characters: Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#replace_invalid_characters FileFormat#replace_invalid_characters}
        :param skip_blank_lines: Boolean that specifies to skip any blank lines encountered in the data files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_blank_lines FileFormat#skip_blank_lines}
        :param skip_byte_order_mark: Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_byte_order_mark FileFormat#skip_byte_order_mark}
        :param skip_header: Number of lines at the start of the file to skip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_header FileFormat#skip_header}
        :param strip_null_values: Boolean that instructs the JSON parser to remove object fields or array elements containing null values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_null_values FileFormat#strip_null_values}
        :param strip_outer_array: Boolean that instructs the JSON parser to remove outer brackets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_outer_array FileFormat#strip_outer_array}
        :param strip_outer_element: Boolean that specifies whether the XML parser strips out the outer XML element, exposing 2nd level elements as separate documents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_outer_element FileFormat#strip_outer_element}
        :param time_format: Defines the format of time values in the data files (data loading) or table (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#time_format FileFormat#time_format}
        :param timestamp_format: Defines the format of timestamp values in the data files (data loading) or table (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#timestamp_format FileFormat#timestamp_format}
        :param trim_space: Boolean that specifies whether to remove white space from fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#trim_space FileFormat#trim_space}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f871f5ae7e15dfafe2dca75b0a00526ac1d5f1c41417b02a0a659368bc613b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FileFormatConfig(
            database=database,
            format_type=format_type,
            name=name,
            schema=schema,
            allow_duplicate=allow_duplicate,
            binary_as_text=binary_as_text,
            binary_format=binary_format,
            comment=comment,
            compression=compression,
            date_format=date_format,
            disable_auto_convert=disable_auto_convert,
            disable_snowflake_data=disable_snowflake_data,
            empty_field_as_null=empty_field_as_null,
            enable_octal=enable_octal,
            encoding=encoding,
            error_on_column_count_mismatch=error_on_column_count_mismatch,
            escape=escape,
            escape_unenclosed_field=escape_unenclosed_field,
            field_delimiter=field_delimiter,
            field_optionally_enclosed_by=field_optionally_enclosed_by,
            file_extension=file_extension,
            id=id,
            ignore_utf8_errors=ignore_utf8_errors,
            null_if=null_if,
            parse_header=parse_header,
            preserve_space=preserve_space,
            record_delimiter=record_delimiter,
            replace_invalid_characters=replace_invalid_characters,
            skip_blank_lines=skip_blank_lines,
            skip_byte_order_mark=skip_byte_order_mark,
            skip_header=skip_header,
            strip_null_values=strip_null_values,
            strip_outer_array=strip_outer_array,
            strip_outer_element=strip_outer_element,
            time_format=time_format,
            timestamp_format=timestamp_format,
            trim_space=trim_space,
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
        '''Generates CDKTF code for importing a FileFormat resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FileFormat to import.
        :param import_from_id: The id of the existing FileFormat that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FileFormat to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88750afecdb446807b24440920c0bf4aa0f0a6a0ced8479840d7275e4b7dac4a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllowDuplicate")
    def reset_allow_duplicate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowDuplicate", []))

    @jsii.member(jsii_name="resetBinaryAsText")
    def reset_binary_as_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAsText", []))

    @jsii.member(jsii_name="resetBinaryFormat")
    def reset_binary_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryFormat", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetDateFormat")
    def reset_date_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateFormat", []))

    @jsii.member(jsii_name="resetDisableAutoConvert")
    def reset_disable_auto_convert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAutoConvert", []))

    @jsii.member(jsii_name="resetDisableSnowflakeData")
    def reset_disable_snowflake_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableSnowflakeData", []))

    @jsii.member(jsii_name="resetEmptyFieldAsNull")
    def reset_empty_field_as_null(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyFieldAsNull", []))

    @jsii.member(jsii_name="resetEnableOctal")
    def reset_enable_octal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableOctal", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetErrorOnColumnCountMismatch")
    def reset_error_on_column_count_mismatch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOnColumnCountMismatch", []))

    @jsii.member(jsii_name="resetEscape")
    def reset_escape(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscape", []))

    @jsii.member(jsii_name="resetEscapeUnenclosedField")
    def reset_escape_unenclosed_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscapeUnenclosedField", []))

    @jsii.member(jsii_name="resetFieldDelimiter")
    def reset_field_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldDelimiter", []))

    @jsii.member(jsii_name="resetFieldOptionallyEnclosedBy")
    def reset_field_optionally_enclosed_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldOptionallyEnclosedBy", []))

    @jsii.member(jsii_name="resetFileExtension")
    def reset_file_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileExtension", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreUtf8Errors")
    def reset_ignore_utf8_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreUtf8Errors", []))

    @jsii.member(jsii_name="resetNullIf")
    def reset_null_if(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullIf", []))

    @jsii.member(jsii_name="resetParseHeader")
    def reset_parse_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseHeader", []))

    @jsii.member(jsii_name="resetPreserveSpace")
    def reset_preserve_space(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveSpace", []))

    @jsii.member(jsii_name="resetRecordDelimiter")
    def reset_record_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordDelimiter", []))

    @jsii.member(jsii_name="resetReplaceInvalidCharacters")
    def reset_replace_invalid_characters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplaceInvalidCharacters", []))

    @jsii.member(jsii_name="resetSkipBlankLines")
    def reset_skip_blank_lines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipBlankLines", []))

    @jsii.member(jsii_name="resetSkipByteOrderMark")
    def reset_skip_byte_order_mark(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipByteOrderMark", []))

    @jsii.member(jsii_name="resetSkipHeader")
    def reset_skip_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipHeader", []))

    @jsii.member(jsii_name="resetStripNullValues")
    def reset_strip_null_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStripNullValues", []))

    @jsii.member(jsii_name="resetStripOuterArray")
    def reset_strip_outer_array(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStripOuterArray", []))

    @jsii.member(jsii_name="resetStripOuterElement")
    def reset_strip_outer_element(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStripOuterElement", []))

    @jsii.member(jsii_name="resetTimeFormat")
    def reset_time_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeFormat", []))

    @jsii.member(jsii_name="resetTimestampFormat")
    def reset_timestamp_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampFormat", []))

    @jsii.member(jsii_name="resetTrimSpace")
    def reset_trim_space(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrimSpace", []))

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
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicateInput")
    def allow_duplicate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowDuplicateInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAsTextInput")
    def binary_as_text_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "binaryAsTextInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryFormatInput")
    def binary_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="dateFormatInput")
    def date_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAutoConvertInput")
    def disable_auto_convert_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAutoConvertInput"))

    @builtins.property
    @jsii.member(jsii_name="disableSnowflakeDataInput")
    def disable_snowflake_data_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableSnowflakeDataInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyFieldAsNullInput")
    def empty_field_as_null_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emptyFieldAsNullInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOctalInput")
    def enable_octal_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableOctalInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="errorOnColumnCountMismatchInput")
    def error_on_column_count_mismatch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "errorOnColumnCountMismatchInput"))

    @builtins.property
    @jsii.member(jsii_name="escapeInput")
    def escape_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escapeInput"))

    @builtins.property
    @jsii.member(jsii_name="escapeUnenclosedFieldInput")
    def escape_unenclosed_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escapeUnenclosedFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiterInput")
    def field_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldOptionallyEnclosedByInput")
    def field_optionally_enclosed_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldOptionallyEnclosedByInput"))

    @builtins.property
    @jsii.member(jsii_name="fileExtensionInput")
    def file_extension_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileExtensionInput"))

    @builtins.property
    @jsii.member(jsii_name="formatTypeInput")
    def format_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreUtf8ErrorsInput")
    def ignore_utf8_errors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreUtf8ErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nullIfInput")
    def null_if_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nullIfInput"))

    @builtins.property
    @jsii.member(jsii_name="parseHeaderInput")
    def parse_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "parseHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveSpaceInput")
    def preserve_space_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveSpaceInput"))

    @builtins.property
    @jsii.member(jsii_name="recordDelimiterInput")
    def record_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceInvalidCharactersInput")
    def replace_invalid_characters_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceInvalidCharactersInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="skipBlankLinesInput")
    def skip_blank_lines_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipBlankLinesInput"))

    @builtins.property
    @jsii.member(jsii_name="skipByteOrderMarkInput")
    def skip_byte_order_mark_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipByteOrderMarkInput"))

    @builtins.property
    @jsii.member(jsii_name="skipHeaderInput")
    def skip_header_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "skipHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="stripNullValuesInput")
    def strip_null_values_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stripNullValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="stripOuterArrayInput")
    def strip_outer_array_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stripOuterArrayInput"))

    @builtins.property
    @jsii.member(jsii_name="stripOuterElementInput")
    def strip_outer_element_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stripOuterElementInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFormatInput")
    def time_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampFormatInput")
    def timestamp_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="trimSpaceInput")
    def trim_space_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trimSpaceInput"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicate")
    def allow_duplicate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowDuplicate"))

    @allow_duplicate.setter
    def allow_duplicate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f9fe65fab8a69b1874d7e9e1170cda8d83f232b2c5bd8e468a53ccceaa28b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowDuplicate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryAsText")
    def binary_as_text(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "binaryAsText"))

    @binary_as_text.setter
    def binary_as_text(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bad9a4b65a113847045de56fde9bf02a8b872b9b8ad3ccb965ec633f0cbb317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryAsText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryFormat")
    def binary_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryFormat"))

    @binary_format.setter
    def binary_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7418de21de9998a635806a1d382be354ec0edac5a2ad9a43deaf1f54d10636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b71ed0dba4a5badce5c96bb1c6039f38e9952376f67fa1ded4974cc690c357a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9caeb76be8337592c01b50f98af747d2ee0527db3533754964d4e5e17a408fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc0b2addd56cd81e5f6dbc07d1ca569b89505ebe8f77ce8e3f3a12d7042e200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateFormat")
    def date_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateFormat"))

    @date_format.setter
    def date_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0f1563965d0b406b11bf4c107dd1fc78b50244c983ef0b97a9247e6a3ba121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableAutoConvert")
    def disable_auto_convert(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAutoConvert"))

    @disable_auto_convert.setter
    def disable_auto_convert(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49b40fbadf8b8bc3ffecf7aa45a899018f94810680233857b46b763b43fe8c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutoConvert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableSnowflakeData")
    def disable_snowflake_data(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableSnowflakeData"))

    @disable_snowflake_data.setter
    def disable_snowflake_data(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cbeba54d97633e4e450ba8bb9441b728b7c69d31a24eb91f603f0c514e62db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableSnowflakeData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emptyFieldAsNull")
    def empty_field_as_null(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emptyFieldAsNull"))

    @empty_field_as_null.setter
    def empty_field_as_null(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1475810f03e5152da5cdea87cdb146375a237326a29dc77437b77ba2413b924c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emptyFieldAsNull", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableOctal")
    def enable_octal(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableOctal"))

    @enable_octal.setter
    def enable_octal(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ceaa52f1d5f895fae960e7012644fa209470d539de1c135063a5cf458e8a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableOctal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5602068c366959e5b207a389322ef98b7b7ac493b7e34f26961f922eb95ba30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="errorOnColumnCountMismatch")
    def error_on_column_count_mismatch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "errorOnColumnCountMismatch"))

    @error_on_column_count_mismatch.setter
    def error_on_column_count_mismatch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c2a52f4fb9ef29d3d5c5a236fd142076d4c462fac4c36339f1397a8072e99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOnColumnCountMismatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escape")
    def escape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escape"))

    @escape.setter
    def escape(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac84e97396ffc63022c94ef4ba5732464dec372e0d93415be62b4039aa3bf7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escape", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escapeUnenclosedField")
    def escape_unenclosed_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escapeUnenclosedField"))

    @escape_unenclosed_field.setter
    def escape_unenclosed_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae76af66c48fb2d14f9a8eb41f90d1d0296b2bcf726f249c51141919ae19712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escapeUnenclosedField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldDelimiter"))

    @field_delimiter.setter
    def field_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334a01c0e5ccbe8590b1630c570e0ebc43093d8a60a5d8401ac26dd2b215dd4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldOptionallyEnclosedBy")
    def field_optionally_enclosed_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldOptionallyEnclosedBy"))

    @field_optionally_enclosed_by.setter
    def field_optionally_enclosed_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2a30f2f47022a96ebff8910fdea38e5c9d677592dead3825a2d34acdd7b75a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldOptionallyEnclosedBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileExtension")
    def file_extension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileExtension"))

    @file_extension.setter
    def file_extension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2655fa2105f6f8bace8d38d159dc74b85d75770815e02ae3aa7f3f8cc6bd3398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileExtension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatType")
    def format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formatType"))

    @format_type.setter
    def format_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f866396092b62ab6473cbd91e09660cf445213b94f2b82306bb6c77abc07fd5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c374493ff6f66ab54833fe2df927ee1a41d4868ed6939a6996959f5da3e4e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreUtf8Errors")
    def ignore_utf8_errors(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreUtf8Errors"))

    @ignore_utf8_errors.setter
    def ignore_utf8_errors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e788010b1636ebe940b588530f85b7ac6ab9cbdafa0aed32cc7c45731e4511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreUtf8Errors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05749898ab7abcc173218be1fd29a22e1fc8ce8a14a4f7e6c24a2b204c0e0d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullIf")
    def null_if(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nullIf"))

    @null_if.setter
    def null_if(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f510461544f0cbc6c98e771b79f0ae5627909357ee7ecf8895a3483701f058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullIf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parseHeader")
    def parse_header(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "parseHeader"))

    @parse_header.setter
    def parse_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26816299a60b606959621ebaa848bc5b2f5de470d4cb761b856a3e4a212d676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parseHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveSpace")
    def preserve_space(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveSpace"))

    @preserve_space.setter
    def preserve_space(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236f8980ab799ad1cc0f2c1f49d30d9e93d45953f13ebc4cc39a411fc0652acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveSpace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordDelimiter")
    def record_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordDelimiter"))

    @record_delimiter.setter
    def record_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69aa06efe360cafd685fdb9899370d072a1c76e1608d717129489b83c58eb360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replaceInvalidCharacters")
    def replace_invalid_characters(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replaceInvalidCharacters"))

    @replace_invalid_characters.setter
    def replace_invalid_characters(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f757961b29372385c7512d37c5f78800d53d01ea2df6137e0a0d0a1eaad04a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceInvalidCharacters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c106b90da5012b3a9cb6f2c350404509e41b44491ae40f373885a881496abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipBlankLines")
    def skip_blank_lines(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipBlankLines"))

    @skip_blank_lines.setter
    def skip_blank_lines(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f4539abf26153bacdf555bab83cdcef879c9c3e026089a554c8e3252db60f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipBlankLines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipByteOrderMark")
    def skip_byte_order_mark(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipByteOrderMark"))

    @skip_byte_order_mark.setter
    def skip_byte_order_mark(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3f17acbf1aa9cb730f5f4fe4f9f55f748c6d11ab0aa2a2e0a7ed17325bb11f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipByteOrderMark", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipHeader")
    def skip_header(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "skipHeader"))

    @skip_header.setter
    def skip_header(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8938ec906861ee12ab164e405d8ae671f1a276bc336b71b5eae3333bed6fa653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stripNullValues")
    def strip_null_values(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stripNullValues"))

    @strip_null_values.setter
    def strip_null_values(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788c380c366c2996b17960d81b98ae1ff3948d7a14f924071545fd7f11d3d217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripNullValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stripOuterArray")
    def strip_outer_array(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stripOuterArray"))

    @strip_outer_array.setter
    def strip_outer_array(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5247ae967427dce7af082f52acdec0fef9111722606b74871ec0e24be837a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripOuterArray", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stripOuterElement")
    def strip_outer_element(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stripOuterElement"))

    @strip_outer_element.setter
    def strip_outer_element(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1c42b9f3ecc575e5f7531ffc3bb203376d2f25825035e6bd235a36dfbc6e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripOuterElement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeFormat")
    def time_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFormat"))

    @time_format.setter
    def time_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fd3575782671f332125dd53f001736ad7eafcf933087c1289888826b61a046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampFormat")
    def timestamp_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampFormat"))

    @timestamp_format.setter
    def timestamp_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320691ad2b49eb62d0293070232c1c21b309c72690bf3c58faa9f4e13126fdc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trimSpace")
    def trim_space(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trimSpace"))

    @trim_space.setter
    def trim_space(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f22f74b6d6979099cb6fc03092e84e5e92f6aca7e9442b3954ccee4f6c7df6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trimSpace", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.fileFormat.FileFormatConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "format_type": "formatType",
        "name": "name",
        "schema": "schema",
        "allow_duplicate": "allowDuplicate",
        "binary_as_text": "binaryAsText",
        "binary_format": "binaryFormat",
        "comment": "comment",
        "compression": "compression",
        "date_format": "dateFormat",
        "disable_auto_convert": "disableAutoConvert",
        "disable_snowflake_data": "disableSnowflakeData",
        "empty_field_as_null": "emptyFieldAsNull",
        "enable_octal": "enableOctal",
        "encoding": "encoding",
        "error_on_column_count_mismatch": "errorOnColumnCountMismatch",
        "escape": "escape",
        "escape_unenclosed_field": "escapeUnenclosedField",
        "field_delimiter": "fieldDelimiter",
        "field_optionally_enclosed_by": "fieldOptionallyEnclosedBy",
        "file_extension": "fileExtension",
        "id": "id",
        "ignore_utf8_errors": "ignoreUtf8Errors",
        "null_if": "nullIf",
        "parse_header": "parseHeader",
        "preserve_space": "preserveSpace",
        "record_delimiter": "recordDelimiter",
        "replace_invalid_characters": "replaceInvalidCharacters",
        "skip_blank_lines": "skipBlankLines",
        "skip_byte_order_mark": "skipByteOrderMark",
        "skip_header": "skipHeader",
        "strip_null_values": "stripNullValues",
        "strip_outer_array": "stripOuterArray",
        "strip_outer_element": "stripOuterElement",
        "time_format": "timeFormat",
        "timestamp_format": "timestampFormat",
        "trim_space": "trimSpace",
    },
)
class FileFormatConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        format_type: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        allow_duplicate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        binary_as_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        binary_format: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        compression: typing.Optional[builtins.str] = None,
        date_format: typing.Optional[builtins.str] = None,
        disable_auto_convert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_snowflake_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        empty_field_as_null: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_octal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        error_on_column_count_mismatch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escape: typing.Optional[builtins.str] = None,
        escape_unenclosed_field: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        field_optionally_enclosed_by: typing.Optional[builtins.str] = None,
        file_extension: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_utf8_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        null_if: typing.Optional[typing.Sequence[builtins.str]] = None,
        parse_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preserve_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_delimiter: typing.Optional[builtins.str] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_blank_lines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_byte_order_mark: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_header: typing.Optional[jsii.Number] = None,
        strip_null_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strip_outer_array: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strip_outer_element: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_format: typing.Optional[builtins.str] = None,
        timestamp_format: typing.Optional[builtins.str] = None,
        trim_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the file format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#database FileFormat#database}
        :param format_type: Specifies the format of the input files (for data loading) or output files (for data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#format_type FileFormat#format_type}
        :param name: Specifies the identifier for the file format; must be unique for the database and schema in which the file format is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#name FileFormat#name}
        :param schema: The schema in which to create the file format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#schema FileFormat#schema}
        :param allow_duplicate: Boolean that specifies to allow duplicate object field names (only the last one will be preserved). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#allow_duplicate FileFormat#allow_duplicate}
        :param binary_as_text: Boolean that specifies whether to interpret columns with no defined logical data type as UTF-8 text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#binary_as_text FileFormat#binary_as_text}
        :param binary_format: Defines the encoding format for binary input or output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#binary_format FileFormat#binary_format}
        :param comment: Specifies a comment for the file format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#comment FileFormat#comment}
        :param compression: Specifies the current compression algorithm for the data file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#compression FileFormat#compression}
        :param date_format: Defines the format of date values in the data files (data loading) or table (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#date_format FileFormat#date_format}
        :param disable_auto_convert: Boolean that specifies whether the XML parser disables automatic conversion of numeric and Boolean values from text to native representation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#disable_auto_convert FileFormat#disable_auto_convert}
        :param disable_snowflake_data: Boolean that specifies whether the XML parser disables recognition of Snowflake semi-structured data tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#disable_snowflake_data FileFormat#disable_snowflake_data}
        :param empty_field_as_null: Specifies whether to insert SQL NULL for empty fields in an input file, which are represented by two successive delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#empty_field_as_null FileFormat#empty_field_as_null}
        :param enable_octal: Boolean that enables parsing of octal numbers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#enable_octal FileFormat#enable_octal}
        :param encoding: String (constant) that specifies the character set of the source data when loading data into a table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#encoding FileFormat#encoding}
        :param error_on_column_count_mismatch: Boolean that specifies whether to generate a parsing error if the number of delimited columns (i.e. fields) in an input file does not match the number of columns in the corresponding table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#error_on_column_count_mismatch FileFormat#error_on_column_count_mismatch}
        :param escape: Single character string used as the escape character for field values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#escape FileFormat#escape}
        :param escape_unenclosed_field: Single character string used as the escape character for unenclosed field values only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#escape_unenclosed_field FileFormat#escape_unenclosed_field}
        :param field_delimiter: Specifies one or more singlebyte or multibyte characters that separate fields in an input file (data loading) or unloaded file (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#field_delimiter FileFormat#field_delimiter}
        :param field_optionally_enclosed_by: Character used to enclose strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#field_optionally_enclosed_by FileFormat#field_optionally_enclosed_by}
        :param file_extension: Specifies the extension for files unloaded to a stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#file_extension FileFormat#file_extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#id FileFormat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_utf8_errors: Boolean that specifies whether UTF-8 encoding errors produce error conditions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#ignore_utf8_errors FileFormat#ignore_utf8_errors}
        :param null_if: String used to convert to and from SQL NULL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#null_if FileFormat#null_if}
        :param parse_header: Boolean that specifies whether to use the first row headers in the data files to determine column names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#parse_header FileFormat#parse_header}
        :param preserve_space: Boolean that specifies whether the XML parser preserves leading and trailing spaces in element content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#preserve_space FileFormat#preserve_space}
        :param record_delimiter: Specifies one or more singlebyte or multibyte characters that separate records in an input file (data loading) or unloaded file (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#record_delimiter FileFormat#record_delimiter}
        :param replace_invalid_characters: Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#replace_invalid_characters FileFormat#replace_invalid_characters}
        :param skip_blank_lines: Boolean that specifies to skip any blank lines encountered in the data files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_blank_lines FileFormat#skip_blank_lines}
        :param skip_byte_order_mark: Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_byte_order_mark FileFormat#skip_byte_order_mark}
        :param skip_header: Number of lines at the start of the file to skip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_header FileFormat#skip_header}
        :param strip_null_values: Boolean that instructs the JSON parser to remove object fields or array elements containing null values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_null_values FileFormat#strip_null_values}
        :param strip_outer_array: Boolean that instructs the JSON parser to remove outer brackets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_outer_array FileFormat#strip_outer_array}
        :param strip_outer_element: Boolean that specifies whether the XML parser strips out the outer XML element, exposing 2nd level elements as separate documents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_outer_element FileFormat#strip_outer_element}
        :param time_format: Defines the format of time values in the data files (data loading) or table (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#time_format FileFormat#time_format}
        :param timestamp_format: Defines the format of timestamp values in the data files (data loading) or table (data unloading). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#timestamp_format FileFormat#timestamp_format}
        :param trim_space: Boolean that specifies whether to remove white space from fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#trim_space FileFormat#trim_space}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0ca45e58f9b02127267f919bdca2bf031f0eafbad9be71dab295739b89ca12)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument format_type", value=format_type, expected_type=type_hints["format_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument allow_duplicate", value=allow_duplicate, expected_type=type_hints["allow_duplicate"])
            check_type(argname="argument binary_as_text", value=binary_as_text, expected_type=type_hints["binary_as_text"])
            check_type(argname="argument binary_format", value=binary_format, expected_type=type_hints["binary_format"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument date_format", value=date_format, expected_type=type_hints["date_format"])
            check_type(argname="argument disable_auto_convert", value=disable_auto_convert, expected_type=type_hints["disable_auto_convert"])
            check_type(argname="argument disable_snowflake_data", value=disable_snowflake_data, expected_type=type_hints["disable_snowflake_data"])
            check_type(argname="argument empty_field_as_null", value=empty_field_as_null, expected_type=type_hints["empty_field_as_null"])
            check_type(argname="argument enable_octal", value=enable_octal, expected_type=type_hints["enable_octal"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument error_on_column_count_mismatch", value=error_on_column_count_mismatch, expected_type=type_hints["error_on_column_count_mismatch"])
            check_type(argname="argument escape", value=escape, expected_type=type_hints["escape"])
            check_type(argname="argument escape_unenclosed_field", value=escape_unenclosed_field, expected_type=type_hints["escape_unenclosed_field"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument field_optionally_enclosed_by", value=field_optionally_enclosed_by, expected_type=type_hints["field_optionally_enclosed_by"])
            check_type(argname="argument file_extension", value=file_extension, expected_type=type_hints["file_extension"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_utf8_errors", value=ignore_utf8_errors, expected_type=type_hints["ignore_utf8_errors"])
            check_type(argname="argument null_if", value=null_if, expected_type=type_hints["null_if"])
            check_type(argname="argument parse_header", value=parse_header, expected_type=type_hints["parse_header"])
            check_type(argname="argument preserve_space", value=preserve_space, expected_type=type_hints["preserve_space"])
            check_type(argname="argument record_delimiter", value=record_delimiter, expected_type=type_hints["record_delimiter"])
            check_type(argname="argument replace_invalid_characters", value=replace_invalid_characters, expected_type=type_hints["replace_invalid_characters"])
            check_type(argname="argument skip_blank_lines", value=skip_blank_lines, expected_type=type_hints["skip_blank_lines"])
            check_type(argname="argument skip_byte_order_mark", value=skip_byte_order_mark, expected_type=type_hints["skip_byte_order_mark"])
            check_type(argname="argument skip_header", value=skip_header, expected_type=type_hints["skip_header"])
            check_type(argname="argument strip_null_values", value=strip_null_values, expected_type=type_hints["strip_null_values"])
            check_type(argname="argument strip_outer_array", value=strip_outer_array, expected_type=type_hints["strip_outer_array"])
            check_type(argname="argument strip_outer_element", value=strip_outer_element, expected_type=type_hints["strip_outer_element"])
            check_type(argname="argument time_format", value=time_format, expected_type=type_hints["time_format"])
            check_type(argname="argument timestamp_format", value=timestamp_format, expected_type=type_hints["timestamp_format"])
            check_type(argname="argument trim_space", value=trim_space, expected_type=type_hints["trim_space"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "format_type": format_type,
            "name": name,
            "schema": schema,
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
        if allow_duplicate is not None:
            self._values["allow_duplicate"] = allow_duplicate
        if binary_as_text is not None:
            self._values["binary_as_text"] = binary_as_text
        if binary_format is not None:
            self._values["binary_format"] = binary_format
        if comment is not None:
            self._values["comment"] = comment
        if compression is not None:
            self._values["compression"] = compression
        if date_format is not None:
            self._values["date_format"] = date_format
        if disable_auto_convert is not None:
            self._values["disable_auto_convert"] = disable_auto_convert
        if disable_snowflake_data is not None:
            self._values["disable_snowflake_data"] = disable_snowflake_data
        if empty_field_as_null is not None:
            self._values["empty_field_as_null"] = empty_field_as_null
        if enable_octal is not None:
            self._values["enable_octal"] = enable_octal
        if encoding is not None:
            self._values["encoding"] = encoding
        if error_on_column_count_mismatch is not None:
            self._values["error_on_column_count_mismatch"] = error_on_column_count_mismatch
        if escape is not None:
            self._values["escape"] = escape
        if escape_unenclosed_field is not None:
            self._values["escape_unenclosed_field"] = escape_unenclosed_field
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if field_optionally_enclosed_by is not None:
            self._values["field_optionally_enclosed_by"] = field_optionally_enclosed_by
        if file_extension is not None:
            self._values["file_extension"] = file_extension
        if id is not None:
            self._values["id"] = id
        if ignore_utf8_errors is not None:
            self._values["ignore_utf8_errors"] = ignore_utf8_errors
        if null_if is not None:
            self._values["null_if"] = null_if
        if parse_header is not None:
            self._values["parse_header"] = parse_header
        if preserve_space is not None:
            self._values["preserve_space"] = preserve_space
        if record_delimiter is not None:
            self._values["record_delimiter"] = record_delimiter
        if replace_invalid_characters is not None:
            self._values["replace_invalid_characters"] = replace_invalid_characters
        if skip_blank_lines is not None:
            self._values["skip_blank_lines"] = skip_blank_lines
        if skip_byte_order_mark is not None:
            self._values["skip_byte_order_mark"] = skip_byte_order_mark
        if skip_header is not None:
            self._values["skip_header"] = skip_header
        if strip_null_values is not None:
            self._values["strip_null_values"] = strip_null_values
        if strip_outer_array is not None:
            self._values["strip_outer_array"] = strip_outer_array
        if strip_outer_element is not None:
            self._values["strip_outer_element"] = strip_outer_element
        if time_format is not None:
            self._values["time_format"] = time_format
        if timestamp_format is not None:
            self._values["timestamp_format"] = timestamp_format
        if trim_space is not None:
            self._values["trim_space"] = trim_space

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
    def database(self) -> builtins.str:
        '''The database in which to create the file format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#database FileFormat#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format_type(self) -> builtins.str:
        '''Specifies the format of the input files (for data loading) or output files (for data unloading).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#format_type FileFormat#format_type}
        '''
        result = self._values.get("format_type")
        assert result is not None, "Required property 'format_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the file format;

        must be unique for the database and schema in which the file format is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#name FileFormat#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the file format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#schema FileFormat#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_duplicate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies to allow duplicate object field names (only the last one will be preserved).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#allow_duplicate FileFormat#allow_duplicate}
        '''
        result = self._values.get("allow_duplicate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def binary_as_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether to interpret columns with no defined logical data type as UTF-8 text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#binary_as_text FileFormat#binary_as_text}
        '''
        result = self._values.get("binary_as_text")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def binary_format(self) -> typing.Optional[builtins.str]:
        '''Defines the encoding format for binary input or output.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#binary_format FileFormat#binary_format}
        '''
        result = self._values.get("binary_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the file format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#comment FileFormat#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''Specifies the current compression algorithm for the data file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#compression FileFormat#compression}
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of date values in the data files (data loading) or table (data unloading).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#date_format FileFormat#date_format}
        '''
        result = self._values.get("date_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_auto_convert(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether the XML parser disables automatic conversion of numeric and Boolean values from text to native representation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#disable_auto_convert FileFormat#disable_auto_convert}
        '''
        result = self._values.get("disable_auto_convert")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_snowflake_data(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether the XML parser disables recognition of Snowflake semi-structured data tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#disable_snowflake_data FileFormat#disable_snowflake_data}
        '''
        result = self._values.get("disable_snowflake_data")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def empty_field_as_null(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to insert SQL NULL for empty fields in an input file, which are represented by two successive delimiters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#empty_field_as_null FileFormat#empty_field_as_null}
        '''
        result = self._values.get("empty_field_as_null")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_octal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that enables parsing of octal numbers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#enable_octal FileFormat#enable_octal}
        '''
        result = self._values.get("enable_octal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''String (constant) that specifies the character set of the source data when loading data into a table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#encoding FileFormat#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_on_column_count_mismatch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether to generate a parsing error if the number of delimited columns (i.e. fields) in an input file does not match the number of columns in the corresponding table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#error_on_column_count_mismatch FileFormat#error_on_column_count_mismatch}
        '''
        result = self._values.get("error_on_column_count_mismatch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def escape(self) -> typing.Optional[builtins.str]:
        '''Single character string used as the escape character for field values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#escape FileFormat#escape}
        '''
        result = self._values.get("escape")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def escape_unenclosed_field(self) -> typing.Optional[builtins.str]:
        '''Single character string used as the escape character for unenclosed field values only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#escape_unenclosed_field FileFormat#escape_unenclosed_field}
        '''
        result = self._values.get("escape_unenclosed_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''Specifies one or more singlebyte or multibyte characters that separate fields in an input file (data loading) or unloaded file (data unloading).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#field_delimiter FileFormat#field_delimiter}
        '''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_optionally_enclosed_by(self) -> typing.Optional[builtins.str]:
        '''Character used to enclose strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#field_optionally_enclosed_by FileFormat#field_optionally_enclosed_by}
        '''
        result = self._values.get("field_optionally_enclosed_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_extension(self) -> typing.Optional[builtins.str]:
        '''Specifies the extension for files unloaded to a stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#file_extension FileFormat#file_extension}
        '''
        result = self._values.get("file_extension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#id FileFormat#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_utf8_errors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether UTF-8 encoding errors produce error conditions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#ignore_utf8_errors FileFormat#ignore_utf8_errors}
        '''
        result = self._values.get("ignore_utf8_errors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def null_if(self) -> typing.Optional[typing.List[builtins.str]]:
        '''String used to convert to and from SQL NULL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#null_if FileFormat#null_if}
        '''
        result = self._values.get("null_if")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parse_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether to use the first row headers in the data files to determine column names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#parse_header FileFormat#parse_header}
        '''
        result = self._values.get("parse_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def preserve_space(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether the XML parser preserves leading and trailing spaces in element content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#preserve_space FileFormat#preserve_space}
        '''
        result = self._values.get("preserve_space")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_delimiter(self) -> typing.Optional[builtins.str]:
        '''Specifies one or more singlebyte or multibyte characters that separate records in an input file (data loading) or unloaded file (data unloading).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#record_delimiter FileFormat#record_delimiter}
        '''
        result = self._values.get("record_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replace_invalid_characters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#replace_invalid_characters FileFormat#replace_invalid_characters}
        '''
        result = self._values.get("replace_invalid_characters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_blank_lines(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies to skip any blank lines encountered in the data files.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_blank_lines FileFormat#skip_blank_lines}
        '''
        result = self._values.get("skip_blank_lines")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_byte_order_mark(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_byte_order_mark FileFormat#skip_byte_order_mark}
        '''
        result = self._values.get("skip_byte_order_mark")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_header(self) -> typing.Optional[jsii.Number]:
        '''Number of lines at the start of the file to skip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#skip_header FileFormat#skip_header}
        '''
        result = self._values.get("skip_header")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strip_null_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that instructs the JSON parser to remove object fields or array elements containing null values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_null_values FileFormat#strip_null_values}
        '''
        result = self._values.get("strip_null_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def strip_outer_array(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that instructs the JSON parser to remove outer brackets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_outer_array FileFormat#strip_outer_array}
        '''
        result = self._values.get("strip_outer_array")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def strip_outer_element(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether the XML parser strips out the outer XML element, exposing 2nd level elements as separate documents.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#strip_outer_element FileFormat#strip_outer_element}
        '''
        result = self._values.get("strip_outer_element")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of time values in the data files (data loading) or table (data unloading).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#time_format FileFormat#time_format}
        '''
        result = self._values.get("time_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of timestamp values in the data files (data loading) or table (data unloading).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#timestamp_format FileFormat#timestamp_format}
        '''
        result = self._values.get("timestamp_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trim_space(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean that specifies whether to remove white space from fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/file_format#trim_space FileFormat#trim_space}
        '''
        result = self._values.get("trim_space")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileFormatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FileFormat",
    "FileFormatConfig",
]

publication.publish()

def _typecheckingstub__1f871f5ae7e15dfafe2dca75b0a00526ac1d5f1c41417b02a0a659368bc613b8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    format_type: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    allow_duplicate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    binary_as_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    binary_format: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    compression: typing.Optional[builtins.str] = None,
    date_format: typing.Optional[builtins.str] = None,
    disable_auto_convert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_snowflake_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    empty_field_as_null: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_octal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
    error_on_column_count_mismatch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    escape: typing.Optional[builtins.str] = None,
    escape_unenclosed_field: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    field_optionally_enclosed_by: typing.Optional[builtins.str] = None,
    file_extension: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_utf8_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    null_if: typing.Optional[typing.Sequence[builtins.str]] = None,
    parse_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preserve_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_delimiter: typing.Optional[builtins.str] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_blank_lines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_byte_order_mark: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_header: typing.Optional[jsii.Number] = None,
    strip_null_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strip_outer_array: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strip_outer_element: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_format: typing.Optional[builtins.str] = None,
    timestamp_format: typing.Optional[builtins.str] = None,
    trim_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__88750afecdb446807b24440920c0bf4aa0f0a6a0ced8479840d7275e4b7dac4a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f9fe65fab8a69b1874d7e9e1170cda8d83f232b2c5bd8e468a53ccceaa28b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bad9a4b65a113847045de56fde9bf02a8b872b9b8ad3ccb965ec633f0cbb317(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7418de21de9998a635806a1d382be354ec0edac5a2ad9a43deaf1f54d10636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b71ed0dba4a5badce5c96bb1c6039f38e9952376f67fa1ded4974cc690c357a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9caeb76be8337592c01b50f98af747d2ee0527db3533754964d4e5e17a408fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc0b2addd56cd81e5f6dbc07d1ca569b89505ebe8f77ce8e3f3a12d7042e200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0f1563965d0b406b11bf4c107dd1fc78b50244c983ef0b97a9247e6a3ba121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49b40fbadf8b8bc3ffecf7aa45a899018f94810680233857b46b763b43fe8c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbeba54d97633e4e450ba8bb9441b728b7c69d31a24eb91f603f0c514e62db8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1475810f03e5152da5cdea87cdb146375a237326a29dc77437b77ba2413b924c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ceaa52f1d5f895fae960e7012644fa209470d539de1c135063a5cf458e8a05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5602068c366959e5b207a389322ef98b7b7ac493b7e34f26961f922eb95ba30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c2a52f4fb9ef29d3d5c5a236fd142076d4c462fac4c36339f1397a8072e99a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac84e97396ffc63022c94ef4ba5732464dec372e0d93415be62b4039aa3bf7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae76af66c48fb2d14f9a8eb41f90d1d0296b2bcf726f249c51141919ae19712(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334a01c0e5ccbe8590b1630c570e0ebc43093d8a60a5d8401ac26dd2b215dd4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2a30f2f47022a96ebff8910fdea38e5c9d677592dead3825a2d34acdd7b75a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2655fa2105f6f8bace8d38d159dc74b85d75770815e02ae3aa7f3f8cc6bd3398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f866396092b62ab6473cbd91e09660cf445213b94f2b82306bb6c77abc07fd5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c374493ff6f66ab54833fe2df927ee1a41d4868ed6939a6996959f5da3e4e84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e788010b1636ebe940b588530f85b7ac6ab9cbdafa0aed32cc7c45731e4511(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05749898ab7abcc173218be1fd29a22e1fc8ce8a14a4f7e6c24a2b204c0e0d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f510461544f0cbc6c98e771b79f0ae5627909357ee7ecf8895a3483701f058(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26816299a60b606959621ebaa848bc5b2f5de470d4cb761b856a3e4a212d676(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236f8980ab799ad1cc0f2c1f49d30d9e93d45953f13ebc4cc39a411fc0652acb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69aa06efe360cafd685fdb9899370d072a1c76e1608d717129489b83c58eb360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f757961b29372385c7512d37c5f78800d53d01ea2df6137e0a0d0a1eaad04a7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c106b90da5012b3a9cb6f2c350404509e41b44491ae40f373885a881496abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f4539abf26153bacdf555bab83cdcef879c9c3e026089a554c8e3252db60f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3f17acbf1aa9cb730f5f4fe4f9f55f748c6d11ab0aa2a2e0a7ed17325bb11f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8938ec906861ee12ab164e405d8ae671f1a276bc336b71b5eae3333bed6fa653(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788c380c366c2996b17960d81b98ae1ff3948d7a14f924071545fd7f11d3d217(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5247ae967427dce7af082f52acdec0fef9111722606b74871ec0e24be837a59(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1c42b9f3ecc575e5f7531ffc3bb203376d2f25825035e6bd235a36dfbc6e28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fd3575782671f332125dd53f001736ad7eafcf933087c1289888826b61a046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320691ad2b49eb62d0293070232c1c21b309c72690bf3c58faa9f4e13126fdc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f22f74b6d6979099cb6fc03092e84e5e92f6aca7e9442b3954ccee4f6c7df6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0ca45e58f9b02127267f919bdca2bf031f0eafbad9be71dab295739b89ca12(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    format_type: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    allow_duplicate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    binary_as_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    binary_format: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    compression: typing.Optional[builtins.str] = None,
    date_format: typing.Optional[builtins.str] = None,
    disable_auto_convert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_snowflake_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    empty_field_as_null: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_octal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
    error_on_column_count_mismatch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    escape: typing.Optional[builtins.str] = None,
    escape_unenclosed_field: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    field_optionally_enclosed_by: typing.Optional[builtins.str] = None,
    file_extension: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_utf8_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    null_if: typing.Optional[typing.Sequence[builtins.str]] = None,
    parse_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preserve_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_delimiter: typing.Optional[builtins.str] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_blank_lines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_byte_order_mark: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_header: typing.Optional[jsii.Number] = None,
    strip_null_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strip_outer_array: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strip_outer_element: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_format: typing.Optional[builtins.str] = None,
    timestamp_format: typing.Optional[builtins.str] = None,
    trim_space: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
