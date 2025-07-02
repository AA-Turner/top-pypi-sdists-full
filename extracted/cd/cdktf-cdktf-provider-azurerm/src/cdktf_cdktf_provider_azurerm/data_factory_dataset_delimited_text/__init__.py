r'''
# `azurerm_data_factory_dataset_delimited_text`

Refer to the Terraform Registry for docs: [`azurerm_data_factory_dataset_delimited_text`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text).
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


class DataFactoryDatasetDelimitedText(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedText",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text azurerm_data_factory_dataset_delimited_text}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_factory_id: builtins.str,
        linked_service_name: builtins.str,
        name: builtins.str,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_blob_fs_location: typing.Optional[typing.Union["DataFactoryDatasetDelimitedTextAzureBlobFsLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_blob_storage_location: typing.Optional[typing.Union["DataFactoryDatasetDelimitedTextAzureBlobStorageLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        column_delimiter: typing.Optional[builtins.str] = None,
        compression_codec: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[builtins.str] = None,
        escape_character: typing.Optional[builtins.str] = None,
        first_row_as_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        folder: typing.Optional[builtins.str] = None,
        http_server_location: typing.Optional[typing.Union["DataFactoryDatasetDelimitedTextHttpServerLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        null_value: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        quote_character: typing.Optional[builtins.str] = None,
        row_delimiter: typing.Optional[builtins.str] = None,
        schema_column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryDatasetDelimitedTextSchemaColumn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryDatasetDelimitedTextTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text azurerm_data_factory_dataset_delimited_text} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#data_factory_id DataFactoryDatasetDelimitedText#data_factory_id}.
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#linked_service_name DataFactoryDatasetDelimitedText#linked_service_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#name DataFactoryDatasetDelimitedText#name}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#additional_properties DataFactoryDatasetDelimitedText#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#annotations DataFactoryDatasetDelimitedText#annotations}.
        :param azure_blob_fs_location: azure_blob_fs_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#azure_blob_fs_location DataFactoryDatasetDelimitedText#azure_blob_fs_location}
        :param azure_blob_storage_location: azure_blob_storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#azure_blob_storage_location DataFactoryDatasetDelimitedText#azure_blob_storage_location}
        :param column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#column_delimiter DataFactoryDatasetDelimitedText#column_delimiter}.
        :param compression_codec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#compression_codec DataFactoryDatasetDelimitedText#compression_codec}.
        :param compression_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#compression_level DataFactoryDatasetDelimitedText#compression_level}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#description DataFactoryDatasetDelimitedText#description}.
        :param encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#encoding DataFactoryDatasetDelimitedText#encoding}.
        :param escape_character: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#escape_character DataFactoryDatasetDelimitedText#escape_character}.
        :param first_row_as_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#first_row_as_header DataFactoryDatasetDelimitedText#first_row_as_header}.
        :param folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#folder DataFactoryDatasetDelimitedText#folder}.
        :param http_server_location: http_server_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#http_server_location DataFactoryDatasetDelimitedText#http_server_location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#id DataFactoryDatasetDelimitedText#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param null_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#null_value DataFactoryDatasetDelimitedText#null_value}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#parameters DataFactoryDatasetDelimitedText#parameters}.
        :param quote_character: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#quote_character DataFactoryDatasetDelimitedText#quote_character}.
        :param row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#row_delimiter DataFactoryDatasetDelimitedText#row_delimiter}.
        :param schema_column: schema_column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#schema_column DataFactoryDatasetDelimitedText#schema_column}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#timeouts DataFactoryDatasetDelimitedText#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23a15b24b141e3cdd5b093e1dd14635df9f09c6c8ba522fe25133e3c09eac9c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataFactoryDatasetDelimitedTextConfig(
            data_factory_id=data_factory_id,
            linked_service_name=linked_service_name,
            name=name,
            additional_properties=additional_properties,
            annotations=annotations,
            azure_blob_fs_location=azure_blob_fs_location,
            azure_blob_storage_location=azure_blob_storage_location,
            column_delimiter=column_delimiter,
            compression_codec=compression_codec,
            compression_level=compression_level,
            description=description,
            encoding=encoding,
            escape_character=escape_character,
            first_row_as_header=first_row_as_header,
            folder=folder,
            http_server_location=http_server_location,
            id=id,
            null_value=null_value,
            parameters=parameters,
            quote_character=quote_character,
            row_delimiter=row_delimiter,
            schema_column=schema_column,
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
        '''Generates CDKTF code for importing a DataFactoryDatasetDelimitedText resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataFactoryDatasetDelimitedText to import.
        :param import_from_id: The id of the existing DataFactoryDatasetDelimitedText that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataFactoryDatasetDelimitedText to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519b67a0f90c6e48bc87f893fc050c1958269d7950e6667ba4ba7f9ca579cf7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureBlobFsLocation")
    def put_azure_blob_fs_location(
        self,
        *,
        dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_file_system_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        file_system: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dynamic_filename_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.
        :param dynamic_file_system_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_file_system_enabled DataFactoryDatasetDelimitedText#dynamic_file_system_enabled}.
        :param dynamic_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.
        :param file_system: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#file_system DataFactoryDatasetDelimitedText#file_system}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.
        '''
        value = DataFactoryDatasetDelimitedTextAzureBlobFsLocation(
            dynamic_filename_enabled=dynamic_filename_enabled,
            dynamic_file_system_enabled=dynamic_file_system_enabled,
            dynamic_path_enabled=dynamic_path_enabled,
            filename=filename,
            file_system=file_system,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureBlobFsLocation", [value]))

    @jsii.member(jsii_name="putAzureBlobStorageLocation")
    def put_azure_blob_storage_location(
        self,
        *,
        container: builtins.str,
        dynamic_container_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#container DataFactoryDatasetDelimitedText#container}.
        :param dynamic_container_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_container_enabled DataFactoryDatasetDelimitedText#dynamic_container_enabled}.
        :param dynamic_filename_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.
        :param dynamic_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.
        '''
        value = DataFactoryDatasetDelimitedTextAzureBlobStorageLocation(
            container=container,
            dynamic_container_enabled=dynamic_container_enabled,
            dynamic_filename_enabled=dynamic_filename_enabled,
            dynamic_path_enabled=dynamic_path_enabled,
            filename=filename,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureBlobStorageLocation", [value]))

    @jsii.member(jsii_name="putHttpServerLocation")
    def put_http_server_location(
        self,
        *,
        filename: builtins.str,
        path: builtins.str,
        relative_url: builtins.str,
        dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.
        :param relative_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#relative_url DataFactoryDatasetDelimitedText#relative_url}.
        :param dynamic_filename_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.
        :param dynamic_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.
        '''
        value = DataFactoryDatasetDelimitedTextHttpServerLocation(
            filename=filename,
            path=path,
            relative_url=relative_url,
            dynamic_filename_enabled=dynamic_filename_enabled,
            dynamic_path_enabled=dynamic_path_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpServerLocation", [value]))

    @jsii.member(jsii_name="putSchemaColumn")
    def put_schema_column(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryDatasetDelimitedTextSchemaColumn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82e74bbc97c18d7e22f5fe4945a96ac40b7dee56df88d179ebc6174e0ab1ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaColumn", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#create DataFactoryDatasetDelimitedText#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#delete DataFactoryDatasetDelimitedText#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#read DataFactoryDatasetDelimitedText#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#update DataFactoryDatasetDelimitedText#update}.
        '''
        value = DataFactoryDatasetDelimitedTextTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAzureBlobFsLocation")
    def reset_azure_blob_fs_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureBlobFsLocation", []))

    @jsii.member(jsii_name="resetAzureBlobStorageLocation")
    def reset_azure_blob_storage_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureBlobStorageLocation", []))

    @jsii.member(jsii_name="resetColumnDelimiter")
    def reset_column_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnDelimiter", []))

    @jsii.member(jsii_name="resetCompressionCodec")
    def reset_compression_codec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionCodec", []))

    @jsii.member(jsii_name="resetCompressionLevel")
    def reset_compression_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionLevel", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetEscapeCharacter")
    def reset_escape_character(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscapeCharacter", []))

    @jsii.member(jsii_name="resetFirstRowAsHeader")
    def reset_first_row_as_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstRowAsHeader", []))

    @jsii.member(jsii_name="resetFolder")
    def reset_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFolder", []))

    @jsii.member(jsii_name="resetHttpServerLocation")
    def reset_http_server_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpServerLocation", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNullValue")
    def reset_null_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullValue", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetQuoteCharacter")
    def reset_quote_character(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuoteCharacter", []))

    @jsii.member(jsii_name="resetRowDelimiter")
    def reset_row_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowDelimiter", []))

    @jsii.member(jsii_name="resetSchemaColumn")
    def reset_schema_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaColumn", []))

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
    @jsii.member(jsii_name="azureBlobFsLocation")
    def azure_blob_fs_location(
        self,
    ) -> "DataFactoryDatasetDelimitedTextAzureBlobFsLocationOutputReference":
        return typing.cast("DataFactoryDatasetDelimitedTextAzureBlobFsLocationOutputReference", jsii.get(self, "azureBlobFsLocation"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobStorageLocation")
    def azure_blob_storage_location(
        self,
    ) -> "DataFactoryDatasetDelimitedTextAzureBlobStorageLocationOutputReference":
        return typing.cast("DataFactoryDatasetDelimitedTextAzureBlobStorageLocationOutputReference", jsii.get(self, "azureBlobStorageLocation"))

    @builtins.property
    @jsii.member(jsii_name="httpServerLocation")
    def http_server_location(
        self,
    ) -> "DataFactoryDatasetDelimitedTextHttpServerLocationOutputReference":
        return typing.cast("DataFactoryDatasetDelimitedTextHttpServerLocationOutputReference", jsii.get(self, "httpServerLocation"))

    @builtins.property
    @jsii.member(jsii_name="schemaColumn")
    def schema_column(self) -> "DataFactoryDatasetDelimitedTextSchemaColumnList":
        return typing.cast("DataFactoryDatasetDelimitedTextSchemaColumnList", jsii.get(self, "schemaColumn"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataFactoryDatasetDelimitedTextTimeoutsOutputReference":
        return typing.cast("DataFactoryDatasetDelimitedTextTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="additionalPropertiesInput")
    def additional_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobFsLocationInput")
    def azure_blob_fs_location_input(
        self,
    ) -> typing.Optional["DataFactoryDatasetDelimitedTextAzureBlobFsLocation"]:
        return typing.cast(typing.Optional["DataFactoryDatasetDelimitedTextAzureBlobFsLocation"], jsii.get(self, "azureBlobFsLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobStorageLocationInput")
    def azure_blob_storage_location_input(
        self,
    ) -> typing.Optional["DataFactoryDatasetDelimitedTextAzureBlobStorageLocation"]:
        return typing.cast(typing.Optional["DataFactoryDatasetDelimitedTextAzureBlobStorageLocation"], jsii.get(self, "azureBlobStorageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="columnDelimiterInput")
    def column_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionCodecInput")
    def compression_codec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionCodecInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionLevelInput")
    def compression_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryIdInput")
    def data_factory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFactoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="escapeCharacterInput")
    def escape_character_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escapeCharacterInput"))

    @builtins.property
    @jsii.member(jsii_name="firstRowAsHeaderInput")
    def first_row_as_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "firstRowAsHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="folderInput")
    def folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderInput"))

    @builtins.property
    @jsii.member(jsii_name="httpServerLocationInput")
    def http_server_location_input(
        self,
    ) -> typing.Optional["DataFactoryDatasetDelimitedTextHttpServerLocation"]:
        return typing.cast(typing.Optional["DataFactoryDatasetDelimitedTextHttpServerLocation"], jsii.get(self, "httpServerLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceNameInput")
    def linked_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nullValueInput")
    def null_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nullValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteCharacterInput")
    def quote_character_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteCharacterInput"))

    @builtins.property
    @jsii.member(jsii_name="rowDelimiterInput")
    def row_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rowDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaColumnInput")
    def schema_column_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryDatasetDelimitedTextSchemaColumn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryDatasetDelimitedTextSchemaColumn"]]], jsii.get(self, "schemaColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryDatasetDelimitedTextTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryDatasetDelimitedTextTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalProperties")
    def additional_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalProperties"))

    @additional_properties.setter
    def additional_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce2a1c68a71eb7e73110b3439db16c2aad47d7098ca22f51361ce2225884c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae637bbfa6fed9f49778a2962ecadb53bf3a59abcb2ef3a8bb607688f479efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="columnDelimiter")
    def column_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnDelimiter"))

    @column_delimiter.setter
    def column_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ceabe840a04b53cd367e77934e8ab655bc79317bc7590fda32b34edac0cd11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compressionCodec")
    def compression_codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionCodec"))

    @compression_codec.setter
    def compression_codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829c9e023d25e10431ebcb063080be1678f2f677b4dac61bf076e3f530b82e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionCodec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compressionLevel")
    def compression_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionLevel"))

    @compression_level.setter
    def compression_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471c7a00ab5dffe0cc6790539e8ac4a409f157210990325787a3ea5caf6c5c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFactoryId")
    def data_factory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFactoryId"))

    @data_factory_id.setter
    def data_factory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6d47944af6d40999a0afb1e78ba012fb0ce6a1e7cbeda4275b11574277c21c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFactoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9da70ad315ef5514eccc690988d116e85a93a3dab32c5e0e48f1c08de9d56cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36830c1a82e4ab09a6161f0a846008db3db4e43a8c8943d8a1b7c5c08a67a9b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escapeCharacter")
    def escape_character(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escapeCharacter"))

    @escape_character.setter
    def escape_character(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da56dce8ad10af473ba8dc09ac0e1cc1844eed3524d60828890b53e12518f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escapeCharacter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstRowAsHeader")
    def first_row_as_header(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "firstRowAsHeader"))

    @first_row_as_header.setter
    def first_row_as_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c8fae992c1fdf7ec46e1be74a3564172f1d7ef69af4f106e821656bff646d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstRowAsHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7805a989809ddbac40362908f0020c92caab07f6f716f3ed98f456784e06f146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79f5e3004c65a153f794dfd6e6635eac006c0d0a14283f8eb80665141177e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedServiceName")
    def linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedServiceName"))

    @linked_service_name.setter
    def linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4774e59d77d2c8ac84c1e1e41c3c516e1cf4f46fd20b11e71dd91adaa7755b60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac272762a4cc5247712c4d75b978eb410ddfe01c047652e996d69f98c87cb01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullValue")
    def null_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullValue"))

    @null_value.setter
    def null_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672a9e6f9e0e03f39db6c92aeba3111f689622ecb73be62008b92c1981642416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de763aedbeb1074387f504f98d6b84d6fd9b0d582a85783756fb3d1051f2dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteCharacter")
    def quote_character(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quoteCharacter"))

    @quote_character.setter
    def quote_character(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c52f7652c994cc324e6bfd4aa4496854eb2fa078782f8832c7c7821cca3a71b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteCharacter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowDelimiter")
    def row_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rowDelimiter"))

    @row_delimiter.setter
    def row_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24230c043b355ab0d4af309ce9d0f1afcddfc64ad5f0ade24209cb96fdc19a75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowDelimiter", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextAzureBlobFsLocation",
    jsii_struct_bases=[],
    name_mapping={
        "dynamic_filename_enabled": "dynamicFilenameEnabled",
        "dynamic_file_system_enabled": "dynamicFileSystemEnabled",
        "dynamic_path_enabled": "dynamicPathEnabled",
        "filename": "filename",
        "file_system": "fileSystem",
        "path": "path",
    },
)
class DataFactoryDatasetDelimitedTextAzureBlobFsLocation:
    def __init__(
        self,
        *,
        dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_file_system_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        file_system: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dynamic_filename_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.
        :param dynamic_file_system_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_file_system_enabled DataFactoryDatasetDelimitedText#dynamic_file_system_enabled}.
        :param dynamic_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.
        :param file_system: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#file_system DataFactoryDatasetDelimitedText#file_system}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bdd3da741f07fd1b95fe7d4e205562684e3e91605591edd3717b1e4045648fa)
            check_type(argname="argument dynamic_filename_enabled", value=dynamic_filename_enabled, expected_type=type_hints["dynamic_filename_enabled"])
            check_type(argname="argument dynamic_file_system_enabled", value=dynamic_file_system_enabled, expected_type=type_hints["dynamic_file_system_enabled"])
            check_type(argname="argument dynamic_path_enabled", value=dynamic_path_enabled, expected_type=type_hints["dynamic_path_enabled"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument file_system", value=file_system, expected_type=type_hints["file_system"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dynamic_filename_enabled is not None:
            self._values["dynamic_filename_enabled"] = dynamic_filename_enabled
        if dynamic_file_system_enabled is not None:
            self._values["dynamic_file_system_enabled"] = dynamic_file_system_enabled
        if dynamic_path_enabled is not None:
            self._values["dynamic_path_enabled"] = dynamic_path_enabled
        if filename is not None:
            self._values["filename"] = filename
        if file_system is not None:
            self._values["file_system"] = file_system
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def dynamic_filename_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.'''
        result = self._values.get("dynamic_filename_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dynamic_file_system_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_file_system_enabled DataFactoryDatasetDelimitedText#dynamic_file_system_enabled}.'''
        result = self._values.get("dynamic_file_system_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dynamic_path_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.'''
        result = self._values.get("dynamic_path_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.'''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#file_system DataFactoryDatasetDelimitedText#file_system}.'''
        result = self._values.get("file_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryDatasetDelimitedTextAzureBlobFsLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryDatasetDelimitedTextAzureBlobFsLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextAzureBlobFsLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc606f949fd3e7eafa70dbbb899fdb01806011eff66ef647b18c1303899607e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDynamicFilenameEnabled")
    def reset_dynamic_filename_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicFilenameEnabled", []))

    @jsii.member(jsii_name="resetDynamicFileSystemEnabled")
    def reset_dynamic_file_system_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicFileSystemEnabled", []))

    @jsii.member(jsii_name="resetDynamicPathEnabled")
    def reset_dynamic_path_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicPathEnabled", []))

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetFileSystem")
    def reset_file_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileSystem", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="dynamicFilenameEnabledInput")
    def dynamic_filename_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicFilenameEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicFileSystemEnabledInput")
    def dynamic_file_system_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicFileSystemEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicPathEnabledInput")
    def dynamic_path_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicPathEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemInput")
    def file_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicFilenameEnabled")
    def dynamic_filename_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicFilenameEnabled"))

    @dynamic_filename_enabled.setter
    def dynamic_filename_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d4a7e0417757f91b28568443f113a32fdf87c441d64ae335d897ab5f3cb8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicFilenameEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicFileSystemEnabled")
    def dynamic_file_system_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicFileSystemEnabled"))

    @dynamic_file_system_enabled.setter
    def dynamic_file_system_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c7407e3b2da204b404d3c088337db0dfd09486a6b84e39292475a337cbfbd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicFileSystemEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicPathEnabled")
    def dynamic_path_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicPathEnabled"))

    @dynamic_path_enabled.setter
    def dynamic_path_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ab3bd73b8742183f2e3136f59260a72c41944157fa232ff364f3b54f6ed2d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicPathEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60be01b3dd110d619aabc0fd8b568696329f6dfbe1fc445b9bbcbf537608d5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSystem"))

    @file_system.setter
    def file_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca4ef61069037c572294490d331dfed1860228d933ae23aed85c1be35a16056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d23f417370b5f81bad169502e9a9c88f802dbba40849a8d253f98bc93fd5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobFsLocation]:
        return typing.cast(typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobFsLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobFsLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e20f55e811badd0234a1808d3bd5ae9e52ef1d0514740b85c402e31110cd3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextAzureBlobStorageLocation",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "dynamic_container_enabled": "dynamicContainerEnabled",
        "dynamic_filename_enabled": "dynamicFilenameEnabled",
        "dynamic_path_enabled": "dynamicPathEnabled",
        "filename": "filename",
        "path": "path",
    },
)
class DataFactoryDatasetDelimitedTextAzureBlobStorageLocation:
    def __init__(
        self,
        *,
        container: builtins.str,
        dynamic_container_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filename: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#container DataFactoryDatasetDelimitedText#container}.
        :param dynamic_container_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_container_enabled DataFactoryDatasetDelimitedText#dynamic_container_enabled}.
        :param dynamic_filename_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.
        :param dynamic_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d481ea32139c44f486a7dd066be9b24acdac3eddae55c96abf7d8c6cd1690a)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument dynamic_container_enabled", value=dynamic_container_enabled, expected_type=type_hints["dynamic_container_enabled"])
            check_type(argname="argument dynamic_filename_enabled", value=dynamic_filename_enabled, expected_type=type_hints["dynamic_filename_enabled"])
            check_type(argname="argument dynamic_path_enabled", value=dynamic_path_enabled, expected_type=type_hints["dynamic_path_enabled"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
        }
        if dynamic_container_enabled is not None:
            self._values["dynamic_container_enabled"] = dynamic_container_enabled
        if dynamic_filename_enabled is not None:
            self._values["dynamic_filename_enabled"] = dynamic_filename_enabled
        if dynamic_path_enabled is not None:
            self._values["dynamic_path_enabled"] = dynamic_path_enabled
        if filename is not None:
            self._values["filename"] = filename
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def container(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#container DataFactoryDatasetDelimitedText#container}.'''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dynamic_container_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_container_enabled DataFactoryDatasetDelimitedText#dynamic_container_enabled}.'''
        result = self._values.get("dynamic_container_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dynamic_filename_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.'''
        result = self._values.get("dynamic_filename_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dynamic_path_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.'''
        result = self._values.get("dynamic_path_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.'''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryDatasetDelimitedTextAzureBlobStorageLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryDatasetDelimitedTextAzureBlobStorageLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextAzureBlobStorageLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be31de8055c3be4623b73f500b2425a0eb268a0d21f51b18955494cf0eecaca9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDynamicContainerEnabled")
    def reset_dynamic_container_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicContainerEnabled", []))

    @jsii.member(jsii_name="resetDynamicFilenameEnabled")
    def reset_dynamic_filename_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicFilenameEnabled", []))

    @jsii.member(jsii_name="resetDynamicPathEnabled")
    def reset_dynamic_path_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicPathEnabled", []))

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicContainerEnabledInput")
    def dynamic_container_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicContainerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicFilenameEnabledInput")
    def dynamic_filename_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicFilenameEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicPathEnabledInput")
    def dynamic_path_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicPathEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7e553fddb3ef0a77689fb075f4c02fbea3586fa11af97e57e20accb696bcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicContainerEnabled")
    def dynamic_container_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicContainerEnabled"))

    @dynamic_container_enabled.setter
    def dynamic_container_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b09fa5b659284c549406b3e6bf179ee68494324bf722e73e10577b1ef8f934d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicContainerEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicFilenameEnabled")
    def dynamic_filename_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicFilenameEnabled"))

    @dynamic_filename_enabled.setter
    def dynamic_filename_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38e1ced0554f695c5c41f3c1e590609d19994cd984b9014708d98451b7a1649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicFilenameEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicPathEnabled")
    def dynamic_path_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicPathEnabled"))

    @dynamic_path_enabled.setter
    def dynamic_path_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55dc55cd0c10cf3f098266bb6819804884f110e5ad5badc4b4017627ee2ea961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicPathEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd85e71dc0bc2643742ea530310eadfbb2bfc105675ec740c9b57af775a0900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be115e1cb1b820ac4f4b6f3e27403c7820594dba631540ec1302950522a9c039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation]:
        return typing.cast(typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80707f6c5d2f37eb9ae6529cd9dcc67397fc7a518783bcac277060457bed458c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_factory_id": "dataFactoryId",
        "linked_service_name": "linkedServiceName",
        "name": "name",
        "additional_properties": "additionalProperties",
        "annotations": "annotations",
        "azure_blob_fs_location": "azureBlobFsLocation",
        "azure_blob_storage_location": "azureBlobStorageLocation",
        "column_delimiter": "columnDelimiter",
        "compression_codec": "compressionCodec",
        "compression_level": "compressionLevel",
        "description": "description",
        "encoding": "encoding",
        "escape_character": "escapeCharacter",
        "first_row_as_header": "firstRowAsHeader",
        "folder": "folder",
        "http_server_location": "httpServerLocation",
        "id": "id",
        "null_value": "nullValue",
        "parameters": "parameters",
        "quote_character": "quoteCharacter",
        "row_delimiter": "rowDelimiter",
        "schema_column": "schemaColumn",
        "timeouts": "timeouts",
    },
)
class DataFactoryDatasetDelimitedTextConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_factory_id: builtins.str,
        linked_service_name: builtins.str,
        name: builtins.str,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_blob_fs_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextAzureBlobFsLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        azure_blob_storage_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation, typing.Dict[builtins.str, typing.Any]]] = None,
        column_delimiter: typing.Optional[builtins.str] = None,
        compression_codec: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[builtins.str] = None,
        escape_character: typing.Optional[builtins.str] = None,
        first_row_as_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        folder: typing.Optional[builtins.str] = None,
        http_server_location: typing.Optional[typing.Union["DataFactoryDatasetDelimitedTextHttpServerLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        null_value: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        quote_character: typing.Optional[builtins.str] = None,
        row_delimiter: typing.Optional[builtins.str] = None,
        schema_column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryDatasetDelimitedTextSchemaColumn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryDatasetDelimitedTextTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#data_factory_id DataFactoryDatasetDelimitedText#data_factory_id}.
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#linked_service_name DataFactoryDatasetDelimitedText#linked_service_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#name DataFactoryDatasetDelimitedText#name}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#additional_properties DataFactoryDatasetDelimitedText#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#annotations DataFactoryDatasetDelimitedText#annotations}.
        :param azure_blob_fs_location: azure_blob_fs_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#azure_blob_fs_location DataFactoryDatasetDelimitedText#azure_blob_fs_location}
        :param azure_blob_storage_location: azure_blob_storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#azure_blob_storage_location DataFactoryDatasetDelimitedText#azure_blob_storage_location}
        :param column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#column_delimiter DataFactoryDatasetDelimitedText#column_delimiter}.
        :param compression_codec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#compression_codec DataFactoryDatasetDelimitedText#compression_codec}.
        :param compression_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#compression_level DataFactoryDatasetDelimitedText#compression_level}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#description DataFactoryDatasetDelimitedText#description}.
        :param encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#encoding DataFactoryDatasetDelimitedText#encoding}.
        :param escape_character: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#escape_character DataFactoryDatasetDelimitedText#escape_character}.
        :param first_row_as_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#first_row_as_header DataFactoryDatasetDelimitedText#first_row_as_header}.
        :param folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#folder DataFactoryDatasetDelimitedText#folder}.
        :param http_server_location: http_server_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#http_server_location DataFactoryDatasetDelimitedText#http_server_location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#id DataFactoryDatasetDelimitedText#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param null_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#null_value DataFactoryDatasetDelimitedText#null_value}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#parameters DataFactoryDatasetDelimitedText#parameters}.
        :param quote_character: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#quote_character DataFactoryDatasetDelimitedText#quote_character}.
        :param row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#row_delimiter DataFactoryDatasetDelimitedText#row_delimiter}.
        :param schema_column: schema_column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#schema_column DataFactoryDatasetDelimitedText#schema_column}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#timeouts DataFactoryDatasetDelimitedText#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(azure_blob_fs_location, dict):
            azure_blob_fs_location = DataFactoryDatasetDelimitedTextAzureBlobFsLocation(**azure_blob_fs_location)
        if isinstance(azure_blob_storage_location, dict):
            azure_blob_storage_location = DataFactoryDatasetDelimitedTextAzureBlobStorageLocation(**azure_blob_storage_location)
        if isinstance(http_server_location, dict):
            http_server_location = DataFactoryDatasetDelimitedTextHttpServerLocation(**http_server_location)
        if isinstance(timeouts, dict):
            timeouts = DataFactoryDatasetDelimitedTextTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62be46ee6cb24c4100b0c449c98a682a44b09f206e755d83785c4113ae54003)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_factory_id", value=data_factory_id, expected_type=type_hints["data_factory_id"])
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument azure_blob_fs_location", value=azure_blob_fs_location, expected_type=type_hints["azure_blob_fs_location"])
            check_type(argname="argument azure_blob_storage_location", value=azure_blob_storage_location, expected_type=type_hints["azure_blob_storage_location"])
            check_type(argname="argument column_delimiter", value=column_delimiter, expected_type=type_hints["column_delimiter"])
            check_type(argname="argument compression_codec", value=compression_codec, expected_type=type_hints["compression_codec"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument escape_character", value=escape_character, expected_type=type_hints["escape_character"])
            check_type(argname="argument first_row_as_header", value=first_row_as_header, expected_type=type_hints["first_row_as_header"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument http_server_location", value=http_server_location, expected_type=type_hints["http_server_location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument null_value", value=null_value, expected_type=type_hints["null_value"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument quote_character", value=quote_character, expected_type=type_hints["quote_character"])
            check_type(argname="argument row_delimiter", value=row_delimiter, expected_type=type_hints["row_delimiter"])
            check_type(argname="argument schema_column", value=schema_column, expected_type=type_hints["schema_column"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_factory_id": data_factory_id,
            "linked_service_name": linked_service_name,
            "name": name,
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
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if annotations is not None:
            self._values["annotations"] = annotations
        if azure_blob_fs_location is not None:
            self._values["azure_blob_fs_location"] = azure_blob_fs_location
        if azure_blob_storage_location is not None:
            self._values["azure_blob_storage_location"] = azure_blob_storage_location
        if column_delimiter is not None:
            self._values["column_delimiter"] = column_delimiter
        if compression_codec is not None:
            self._values["compression_codec"] = compression_codec
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if description is not None:
            self._values["description"] = description
        if encoding is not None:
            self._values["encoding"] = encoding
        if escape_character is not None:
            self._values["escape_character"] = escape_character
        if first_row_as_header is not None:
            self._values["first_row_as_header"] = first_row_as_header
        if folder is not None:
            self._values["folder"] = folder
        if http_server_location is not None:
            self._values["http_server_location"] = http_server_location
        if id is not None:
            self._values["id"] = id
        if null_value is not None:
            self._values["null_value"] = null_value
        if parameters is not None:
            self._values["parameters"] = parameters
        if quote_character is not None:
            self._values["quote_character"] = quote_character
        if row_delimiter is not None:
            self._values["row_delimiter"] = row_delimiter
        if schema_column is not None:
            self._values["schema_column"] = schema_column
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
    def data_factory_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#data_factory_id DataFactoryDatasetDelimitedText#data_factory_id}.'''
        result = self._values.get("data_factory_id")
        assert result is not None, "Required property 'data_factory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#linked_service_name DataFactoryDatasetDelimitedText#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#name DataFactoryDatasetDelimitedText#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#additional_properties DataFactoryDatasetDelimitedText#additional_properties}.'''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def annotations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#annotations DataFactoryDatasetDelimitedText#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def azure_blob_fs_location(
        self,
    ) -> typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobFsLocation]:
        '''azure_blob_fs_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#azure_blob_fs_location DataFactoryDatasetDelimitedText#azure_blob_fs_location}
        '''
        result = self._values.get("azure_blob_fs_location")
        return typing.cast(typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobFsLocation], result)

    @builtins.property
    def azure_blob_storage_location(
        self,
    ) -> typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation]:
        '''azure_blob_storage_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#azure_blob_storage_location DataFactoryDatasetDelimitedText#azure_blob_storage_location}
        '''
        result = self._values.get("azure_blob_storage_location")
        return typing.cast(typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation], result)

    @builtins.property
    def column_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#column_delimiter DataFactoryDatasetDelimitedText#column_delimiter}.'''
        result = self._values.get("column_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_codec(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#compression_codec DataFactoryDatasetDelimitedText#compression_codec}.'''
        result = self._values.get("compression_codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#compression_level DataFactoryDatasetDelimitedText#compression_level}.'''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#description DataFactoryDatasetDelimitedText#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#encoding DataFactoryDatasetDelimitedText#encoding}.'''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def escape_character(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#escape_character DataFactoryDatasetDelimitedText#escape_character}.'''
        result = self._values.get("escape_character")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_row_as_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#first_row_as_header DataFactoryDatasetDelimitedText#first_row_as_header}.'''
        result = self._values.get("first_row_as_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def folder(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#folder DataFactoryDatasetDelimitedText#folder}.'''
        result = self._values.get("folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_server_location(
        self,
    ) -> typing.Optional["DataFactoryDatasetDelimitedTextHttpServerLocation"]:
        '''http_server_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#http_server_location DataFactoryDatasetDelimitedText#http_server_location}
        '''
        result = self._values.get("http_server_location")
        return typing.cast(typing.Optional["DataFactoryDatasetDelimitedTextHttpServerLocation"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#id DataFactoryDatasetDelimitedText#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def null_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#null_value DataFactoryDatasetDelimitedText#null_value}.'''
        result = self._values.get("null_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#parameters DataFactoryDatasetDelimitedText#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def quote_character(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#quote_character DataFactoryDatasetDelimitedText#quote_character}.'''
        result = self._values.get("quote_character")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def row_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#row_delimiter DataFactoryDatasetDelimitedText#row_delimiter}.'''
        result = self._values.get("row_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_column(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryDatasetDelimitedTextSchemaColumn"]]]:
        '''schema_column block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#schema_column DataFactoryDatasetDelimitedText#schema_column}
        '''
        result = self._values.get("schema_column")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryDatasetDelimitedTextSchemaColumn"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataFactoryDatasetDelimitedTextTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#timeouts DataFactoryDatasetDelimitedText#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataFactoryDatasetDelimitedTextTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryDatasetDelimitedTextConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextHttpServerLocation",
    jsii_struct_bases=[],
    name_mapping={
        "filename": "filename",
        "path": "path",
        "relative_url": "relativeUrl",
        "dynamic_filename_enabled": "dynamicFilenameEnabled",
        "dynamic_path_enabled": "dynamicPathEnabled",
    },
)
class DataFactoryDatasetDelimitedTextHttpServerLocation:
    def __init__(
        self,
        *,
        filename: builtins.str,
        path: builtins.str,
        relative_url: builtins.str,
        dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.
        :param relative_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#relative_url DataFactoryDatasetDelimitedText#relative_url}.
        :param dynamic_filename_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.
        :param dynamic_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad21cd667f233bdd64a4b721248614451279ca14ad2b7ed3bf4bc76d605876b)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument relative_url", value=relative_url, expected_type=type_hints["relative_url"])
            check_type(argname="argument dynamic_filename_enabled", value=dynamic_filename_enabled, expected_type=type_hints["dynamic_filename_enabled"])
            check_type(argname="argument dynamic_path_enabled", value=dynamic_path_enabled, expected_type=type_hints["dynamic_path_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filename": filename,
            "path": path,
            "relative_url": relative_url,
        }
        if dynamic_filename_enabled is not None:
            self._values["dynamic_filename_enabled"] = dynamic_filename_enabled
        if dynamic_path_enabled is not None:
            self._values["dynamic_path_enabled"] = dynamic_path_enabled

    @builtins.property
    def filename(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#filename DataFactoryDatasetDelimitedText#filename}.'''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#path DataFactoryDatasetDelimitedText#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def relative_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#relative_url DataFactoryDatasetDelimitedText#relative_url}.'''
        result = self._values.get("relative_url")
        assert result is not None, "Required property 'relative_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dynamic_filename_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_filename_enabled DataFactoryDatasetDelimitedText#dynamic_filename_enabled}.'''
        result = self._values.get("dynamic_filename_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dynamic_path_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#dynamic_path_enabled DataFactoryDatasetDelimitedText#dynamic_path_enabled}.'''
        result = self._values.get("dynamic_path_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryDatasetDelimitedTextHttpServerLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryDatasetDelimitedTextHttpServerLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextHttpServerLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f1c131a9c218204fe6f4360e0e480a3cef8c08661321a1ad5f69c29b84f4e62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDynamicFilenameEnabled")
    def reset_dynamic_filename_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicFilenameEnabled", []))

    @jsii.member(jsii_name="resetDynamicPathEnabled")
    def reset_dynamic_path_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicPathEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="dynamicFilenameEnabledInput")
    def dynamic_filename_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicFilenameEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicPathEnabledInput")
    def dynamic_path_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicPathEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeUrlInput")
    def relative_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativeUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicFilenameEnabled")
    def dynamic_filename_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicFilenameEnabled"))

    @dynamic_filename_enabled.setter
    def dynamic_filename_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c77e309c4e5d872e6863dae5e1df3e300c71c5a28f61bf84ec8c14db24c227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicFilenameEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicPathEnabled")
    def dynamic_path_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicPathEnabled"))

    @dynamic_path_enabled.setter
    def dynamic_path_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c8e91946dcc9d72c1388c5d4c9c737badf1519ea444422d5c8b4912f595b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicPathEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b06354efd1605cf138cc5625d6816044d0818ab0bb55f9be9122c53a9060423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a047cc9b6acf5a7318dcdfe95443f6c4af4c17d64e12443c6c6b3732d92b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeUrl")
    def relative_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativeUrl"))

    @relative_url.setter
    def relative_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30468fb712181eac2fd336a2a97b08fe6f90dccc3046e86557e5d1855d7e3fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryDatasetDelimitedTextHttpServerLocation]:
        return typing.cast(typing.Optional[DataFactoryDatasetDelimitedTextHttpServerLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryDatasetDelimitedTextHttpServerLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525b4e200e82f87b2c01a8748067598a35c71f0c69c811f728f72468eda032a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextSchemaColumn",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "type": "type"},
)
class DataFactoryDatasetDelimitedTextSchemaColumn:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#name DataFactoryDatasetDelimitedText#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#description DataFactoryDatasetDelimitedText#description}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#type DataFactoryDatasetDelimitedText#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dda65d9d9313e6014ba404a00e1fc6b18c9f6d311de824a39515bf38166a7c3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#name DataFactoryDatasetDelimitedText#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#description DataFactoryDatasetDelimitedText#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#type DataFactoryDatasetDelimitedText#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryDatasetDelimitedTextSchemaColumn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryDatasetDelimitedTextSchemaColumnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextSchemaColumnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67063c52c38b2da492cdd84d6000ae27610a4a46d8227fec28e974a4458a09e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryDatasetDelimitedTextSchemaColumnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe7788d9cbfa21c15a9c503a25cac75c7cc29683e4da875af6477ce1e53d594)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryDatasetDelimitedTextSchemaColumnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d541084f17a0f3be19dfdb6a9bb8ca0087e517ba07a76eafb1f8bb7356cc61b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45dd0f7d7d019d1bc76dea742aec1e22bbefad2eff74ad626b3ed70d03ae413b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da9d73c721bf9161484ccc0779094e939f03f291416bd944cf562e67b11c3210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryDatasetDelimitedTextSchemaColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryDatasetDelimitedTextSchemaColumn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryDatasetDelimitedTextSchemaColumn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f243f0c88051ae6942b38766acab0d964863461ebf52c9c93ba8577a9561e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryDatasetDelimitedTextSchemaColumnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextSchemaColumnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__305427dc8b7667ac686a047546e49d1239d50e9256a30cdfd4437879063a88e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772214a67190b233eee9b7f14f6fb1ea49ed39d776761bd71f225890399cb0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7611c74c0ed989db4ff3d5533a6bd8e82e9f5c45e08a2ab2f80d57d2db53a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf29e538e9571289fbc6d0c0af3560321df8e90ac4d127527aaf5684166cafb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextSchemaColumn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextSchemaColumn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextSchemaColumn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1792906eccbfea459bc74139a93ba9d89a325f643713f40f5af12e09a7138146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataFactoryDatasetDelimitedTextTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#create DataFactoryDatasetDelimitedText#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#delete DataFactoryDatasetDelimitedText#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#read DataFactoryDatasetDelimitedText#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#update DataFactoryDatasetDelimitedText#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e7f07ddce988a18fc1148e2e9994f011549aad6201f23805bde7d831ba1dcf)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#create DataFactoryDatasetDelimitedText#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#delete DataFactoryDatasetDelimitedText#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#read DataFactoryDatasetDelimitedText#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_dataset_delimited_text#update DataFactoryDatasetDelimitedText#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryDatasetDelimitedTextTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryDatasetDelimitedTextTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryDatasetDelimitedText.DataFactoryDatasetDelimitedTextTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e6c6fed122c2053698336cf7779f54797a846cf131ff301dff8226049137c9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8e69cb77cdca784e7519eb060a9cd30f1588b1a0787dc7c973411161e55ad1ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d20cb0ee513ad380a9b167a250265aeb8f785bcc167af83c64af6a8d53af6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7662a1e74508e27695a7cedc35a71fa849ae3fabc93210079fa854fb774ddc08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f00ec3253e173d2a1e2e95313d9a3f3a8b5df388135f16f50e4f64334217825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a04db6fc638f818b624e66a80966cf508ffa8d406b5d28f80ee086e95e025c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataFactoryDatasetDelimitedText",
    "DataFactoryDatasetDelimitedTextAzureBlobFsLocation",
    "DataFactoryDatasetDelimitedTextAzureBlobFsLocationOutputReference",
    "DataFactoryDatasetDelimitedTextAzureBlobStorageLocation",
    "DataFactoryDatasetDelimitedTextAzureBlobStorageLocationOutputReference",
    "DataFactoryDatasetDelimitedTextConfig",
    "DataFactoryDatasetDelimitedTextHttpServerLocation",
    "DataFactoryDatasetDelimitedTextHttpServerLocationOutputReference",
    "DataFactoryDatasetDelimitedTextSchemaColumn",
    "DataFactoryDatasetDelimitedTextSchemaColumnList",
    "DataFactoryDatasetDelimitedTextSchemaColumnOutputReference",
    "DataFactoryDatasetDelimitedTextTimeouts",
    "DataFactoryDatasetDelimitedTextTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b23a15b24b141e3cdd5b093e1dd14635df9f09c6c8ba522fe25133e3c09eac9c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_factory_id: builtins.str,
    linked_service_name: builtins.str,
    name: builtins.str,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_blob_fs_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextAzureBlobFsLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_blob_storage_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    column_delimiter: typing.Optional[builtins.str] = None,
    compression_codec: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[builtins.str] = None,
    escape_character: typing.Optional[builtins.str] = None,
    first_row_as_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    folder: typing.Optional[builtins.str] = None,
    http_server_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextHttpServerLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    null_value: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    quote_character: typing.Optional[builtins.str] = None,
    row_delimiter: typing.Optional[builtins.str] = None,
    schema_column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryDatasetDelimitedTextSchemaColumn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__519b67a0f90c6e48bc87f893fc050c1958269d7950e6667ba4ba7f9ca579cf7b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82e74bbc97c18d7e22f5fe4945a96ac40b7dee56df88d179ebc6174e0ab1ea2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryDatasetDelimitedTextSchemaColumn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce2a1c68a71eb7e73110b3439db16c2aad47d7098ca22f51361ce2225884c1a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae637bbfa6fed9f49778a2962ecadb53bf3a59abcb2ef3a8bb607688f479efa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ceabe840a04b53cd367e77934e8ab655bc79317bc7590fda32b34edac0cd11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829c9e023d25e10431ebcb063080be1678f2f677b4dac61bf076e3f530b82e50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471c7a00ab5dffe0cc6790539e8ac4a409f157210990325787a3ea5caf6c5c0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6d47944af6d40999a0afb1e78ba012fb0ce6a1e7cbeda4275b11574277c21c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9da70ad315ef5514eccc690988d116e85a93a3dab32c5e0e48f1c08de9d56cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36830c1a82e4ab09a6161f0a846008db3db4e43a8c8943d8a1b7c5c08a67a9b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da56dce8ad10af473ba8dc09ac0e1cc1844eed3524d60828890b53e12518f4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c8fae992c1fdf7ec46e1be74a3564172f1d7ef69af4f106e821656bff646d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7805a989809ddbac40362908f0020c92caab07f6f716f3ed98f456784e06f146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79f5e3004c65a153f794dfd6e6635eac006c0d0a14283f8eb80665141177e08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4774e59d77d2c8ac84c1e1e41c3c516e1cf4f46fd20b11e71dd91adaa7755b60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac272762a4cc5247712c4d75b978eb410ddfe01c047652e996d69f98c87cb01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672a9e6f9e0e03f39db6c92aeba3111f689622ecb73be62008b92c1981642416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de763aedbeb1074387f504f98d6b84d6fd9b0d582a85783756fb3d1051f2dfc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c52f7652c994cc324e6bfd4aa4496854eb2fa078782f8832c7c7821cca3a71b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24230c043b355ab0d4af309ce9d0f1afcddfc64ad5f0ade24209cb96fdc19a75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bdd3da741f07fd1b95fe7d4e205562684e3e91605591edd3717b1e4045648fa(
    *,
    dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_file_system_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filename: typing.Optional[builtins.str] = None,
    file_system: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc606f949fd3e7eafa70dbbb899fdb01806011eff66ef647b18c1303899607e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d4a7e0417757f91b28568443f113a32fdf87c441d64ae335d897ab5f3cb8fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c7407e3b2da204b404d3c088337db0dfd09486a6b84e39292475a337cbfbd0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ab3bd73b8742183f2e3136f59260a72c41944157fa232ff364f3b54f6ed2d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60be01b3dd110d619aabc0fd8b568696329f6dfbe1fc445b9bbcbf537608d5a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca4ef61069037c572294490d331dfed1860228d933ae23aed85c1be35a16056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d23f417370b5f81bad169502e9a9c88f802dbba40849a8d253f98bc93fd5ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e20f55e811badd0234a1808d3bd5ae9e52ef1d0514740b85c402e31110cd3b3(
    value: typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobFsLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d481ea32139c44f486a7dd066be9b24acdac3eddae55c96abf7d8c6cd1690a(
    *,
    container: builtins.str,
    dynamic_container_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filename: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be31de8055c3be4623b73f500b2425a0eb268a0d21f51b18955494cf0eecaca9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7e553fddb3ef0a77689fb075f4c02fbea3586fa11af97e57e20accb696bcc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b09fa5b659284c549406b3e6bf179ee68494324bf722e73e10577b1ef8f934d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38e1ced0554f695c5c41f3c1e590609d19994cd984b9014708d98451b7a1649(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55dc55cd0c10cf3f098266bb6819804884f110e5ad5badc4b4017627ee2ea961(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd85e71dc0bc2643742ea530310eadfbb2bfc105675ec740c9b57af775a0900(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be115e1cb1b820ac4f4b6f3e27403c7820594dba631540ec1302950522a9c039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80707f6c5d2f37eb9ae6529cd9dcc67397fc7a518783bcac277060457bed458c(
    value: typing.Optional[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62be46ee6cb24c4100b0c449c98a682a44b09f206e755d83785c4113ae54003(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_factory_id: builtins.str,
    linked_service_name: builtins.str,
    name: builtins.str,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_blob_fs_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextAzureBlobFsLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_blob_storage_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextAzureBlobStorageLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    column_delimiter: typing.Optional[builtins.str] = None,
    compression_codec: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[builtins.str] = None,
    escape_character: typing.Optional[builtins.str] = None,
    first_row_as_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    folder: typing.Optional[builtins.str] = None,
    http_server_location: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextHttpServerLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    null_value: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    quote_character: typing.Optional[builtins.str] = None,
    row_delimiter: typing.Optional[builtins.str] = None,
    schema_column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryDatasetDelimitedTextSchemaColumn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryDatasetDelimitedTextTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad21cd667f233bdd64a4b721248614451279ca14ad2b7ed3bf4bc76d605876b(
    *,
    filename: builtins.str,
    path: builtins.str,
    relative_url: builtins.str,
    dynamic_filename_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1c131a9c218204fe6f4360e0e480a3cef8c08661321a1ad5f69c29b84f4e62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c77e309c4e5d872e6863dae5e1df3e300c71c5a28f61bf84ec8c14db24c227(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c8e91946dcc9d72c1388c5d4c9c737badf1519ea444422d5c8b4912f595b8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b06354efd1605cf138cc5625d6816044d0818ab0bb55f9be9122c53a9060423(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a047cc9b6acf5a7318dcdfe95443f6c4af4c17d64e12443c6c6b3732d92b3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30468fb712181eac2fd336a2a97b08fe6f90dccc3046e86557e5d1855d7e3fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525b4e200e82f87b2c01a8748067598a35c71f0c69c811f728f72468eda032a5(
    value: typing.Optional[DataFactoryDatasetDelimitedTextHttpServerLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dda65d9d9313e6014ba404a00e1fc6b18c9f6d311de824a39515bf38166a7c3(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67063c52c38b2da492cdd84d6000ae27610a4a46d8227fec28e974a4458a09e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe7788d9cbfa21c15a9c503a25cac75c7cc29683e4da875af6477ce1e53d594(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d541084f17a0f3be19dfdb6a9bb8ca0087e517ba07a76eafb1f8bb7356cc61b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dd0f7d7d019d1bc76dea742aec1e22bbefad2eff74ad626b3ed70d03ae413b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9d73c721bf9161484ccc0779094e939f03f291416bd944cf562e67b11c3210(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f243f0c88051ae6942b38766acab0d964863461ebf52c9c93ba8577a9561e49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryDatasetDelimitedTextSchemaColumn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305427dc8b7667ac686a047546e49d1239d50e9256a30cdfd4437879063a88e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772214a67190b233eee9b7f14f6fb1ea49ed39d776761bd71f225890399cb0af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7611c74c0ed989db4ff3d5533a6bd8e82e9f5c45e08a2ab2f80d57d2db53a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf29e538e9571289fbc6d0c0af3560321df8e90ac4d127527aaf5684166cafb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1792906eccbfea459bc74139a93ba9d89a325f643713f40f5af12e09a7138146(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextSchemaColumn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e7f07ddce988a18fc1148e2e9994f011549aad6201f23805bde7d831ba1dcf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6c6fed122c2053698336cf7779f54797a846cf131ff301dff8226049137c9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e69cb77cdca784e7519eb060a9cd30f1588b1a0787dc7c973411161e55ad1ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d20cb0ee513ad380a9b167a250265aeb8f785bcc167af83c64af6a8d53af6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7662a1e74508e27695a7cedc35a71fa849ae3fabc93210079fa854fb774ddc08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f00ec3253e173d2a1e2e95313d9a3f3a8b5df388135f16f50e4f64334217825(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a04db6fc638f818b624e66a80966cf508ffa8d406b5d28f80ee086e95e025c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryDatasetDelimitedTextTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
