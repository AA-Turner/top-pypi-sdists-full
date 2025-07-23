r'''
# `google_storage_insights_report_config`

Refer to the Terraform Registry for docs: [`google_storage_insights_report_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config).
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


class StorageInsightsReportConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config google_storage_insights_report_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        csv_options: typing.Optional[typing.Union["StorageInsightsReportConfigCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        frequency_options: typing.Optional[typing.Union["StorageInsightsReportConfigFrequencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        object_metadata_report_options: typing.Optional[typing.Union["StorageInsightsReportConfigObjectMetadataReportOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        parquet_options: typing.Optional[typing.Union["StorageInsightsReportConfigParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageInsightsReportConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config google_storage_insights_report_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the ReportConfig. The source and destination buckets specified in the ReportConfig must be in the same location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#location StorageInsightsReportConfig#location}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#csv_options StorageInsightsReportConfig#csv_options}
        :param display_name: The editable display name of the inventory report configuration. Has a limit of 256 characters. Can be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#display_name StorageInsightsReportConfig#display_name}
        :param frequency_options: frequency_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#frequency_options StorageInsightsReportConfig#frequency_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#id StorageInsightsReportConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param object_metadata_report_options: object_metadata_report_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#object_metadata_report_options StorageInsightsReportConfig#object_metadata_report_options}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#parquet_options StorageInsightsReportConfig#parquet_options}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#project StorageInsightsReportConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#timeouts StorageInsightsReportConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad8f561dd7f68de45878db7cc2cc6e9ca2dfe64f8d25e134e2d293403ac905e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageInsightsReportConfigConfig(
            location=location,
            csv_options=csv_options,
            display_name=display_name,
            frequency_options=frequency_options,
            id=id,
            object_metadata_report_options=object_metadata_report_options,
            parquet_options=parquet_options,
            project=project,
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
        '''Generates CDKTF code for importing a StorageInsightsReportConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageInsightsReportConfig to import.
        :param import_from_id: The id of the existing StorageInsightsReportConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageInsightsReportConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c933a3e658ce7264c8848e10569faf4413a4955850bfec57a0641e1e797eaab5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCsvOptions")
    def put_csv_options(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        header_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delimiter: The delimiter used to separate the fields in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#delimiter StorageInsightsReportConfig#delimiter}
        :param header_required: The boolean that indicates whether or not headers are included in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#header_required StorageInsightsReportConfig#header_required}
        :param record_separator: The character used to separate the records in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#record_separator StorageInsightsReportConfig#record_separator}
        '''
        value = StorageInsightsReportConfigCsvOptions(
            delimiter=delimiter,
            header_required=header_required,
            record_separator=record_separator,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvOptions", [value]))

    @jsii.member(jsii_name="putFrequencyOptions")
    def put_frequency_options(
        self,
        *,
        end_date: typing.Union["StorageInsightsReportConfigFrequencyOptionsEndDate", typing.Dict[builtins.str, typing.Any]],
        frequency: builtins.str,
        start_date: typing.Union["StorageInsightsReportConfigFrequencyOptionsStartDate", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#end_date StorageInsightsReportConfig#end_date}
        :param frequency: The frequency in which inventory reports are generated. Values are DAILY or WEEKLY. Possible values: ["DAILY", "WEEKLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#frequency StorageInsightsReportConfig#frequency}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#start_date StorageInsightsReportConfig#start_date}
        '''
        value = StorageInsightsReportConfigFrequencyOptions(
            end_date=end_date, frequency=frequency, start_date=start_date
        )

        return typing.cast(None, jsii.invoke(self, "putFrequencyOptions", [value]))

    @jsii.member(jsii_name="putObjectMetadataReportOptions")
    def put_object_metadata_report_options(
        self,
        *,
        metadata_fields: typing.Sequence[builtins.str],
        storage_destination_options: typing.Union["StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions", typing.Dict[builtins.str, typing.Any]],
        storage_filters: typing.Optional[typing.Union["StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata_fields: The metadata fields included in an inventory report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#metadata_fields StorageInsightsReportConfig#metadata_fields}
        :param storage_destination_options: storage_destination_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#storage_destination_options StorageInsightsReportConfig#storage_destination_options}
        :param storage_filters: storage_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#storage_filters StorageInsightsReportConfig#storage_filters}
        '''
        value = StorageInsightsReportConfigObjectMetadataReportOptions(
            metadata_fields=metadata_fields,
            storage_destination_options=storage_destination_options,
            storage_filters=storage_filters,
        )

        return typing.cast(None, jsii.invoke(self, "putObjectMetadataReportOptions", [value]))

    @jsii.member(jsii_name="putParquetOptions")
    def put_parquet_options(self) -> None:
        value = StorageInsightsReportConfigParquetOptions()

        return typing.cast(None, jsii.invoke(self, "putParquetOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#create StorageInsightsReportConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#delete StorageInsightsReportConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#update StorageInsightsReportConfig#update}.
        '''
        value = StorageInsightsReportConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCsvOptions")
    def reset_csv_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvOptions", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetFrequencyOptions")
    def reset_frequency_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequencyOptions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetObjectMetadataReportOptions")
    def reset_object_metadata_report_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectMetadataReportOptions", []))

    @jsii.member(jsii_name="resetParquetOptions")
    def reset_parquet_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParquetOptions", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="csvOptions")
    def csv_options(self) -> "StorageInsightsReportConfigCsvOptionsOutputReference":
        return typing.cast("StorageInsightsReportConfigCsvOptionsOutputReference", jsii.get(self, "csvOptions"))

    @builtins.property
    @jsii.member(jsii_name="frequencyOptions")
    def frequency_options(
        self,
    ) -> "StorageInsightsReportConfigFrequencyOptionsOutputReference":
        return typing.cast("StorageInsightsReportConfigFrequencyOptionsOutputReference", jsii.get(self, "frequencyOptions"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="objectMetadataReportOptions")
    def object_metadata_report_options(
        self,
    ) -> "StorageInsightsReportConfigObjectMetadataReportOptionsOutputReference":
        return typing.cast("StorageInsightsReportConfigObjectMetadataReportOptionsOutputReference", jsii.get(self, "objectMetadataReportOptions"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptions")
    def parquet_options(
        self,
    ) -> "StorageInsightsReportConfigParquetOptionsOutputReference":
        return typing.cast("StorageInsightsReportConfigParquetOptionsOutputReference", jsii.get(self, "parquetOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StorageInsightsReportConfigTimeoutsOutputReference":
        return typing.cast("StorageInsightsReportConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="csvOptionsInput")
    def csv_options_input(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigCsvOptions"]:
        return typing.cast(typing.Optional["StorageInsightsReportConfigCsvOptions"], jsii.get(self, "csvOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyOptionsInput")
    def frequency_options_input(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigFrequencyOptions"]:
        return typing.cast(typing.Optional["StorageInsightsReportConfigFrequencyOptions"], jsii.get(self, "frequencyOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectMetadataReportOptionsInput")
    def object_metadata_report_options_input(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptions"]:
        return typing.cast(typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptions"], jsii.get(self, "objectMetadataReportOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptionsInput")
    def parquet_options_input(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigParquetOptions"]:
        return typing.cast(typing.Optional["StorageInsightsReportConfigParquetOptions"], jsii.get(self, "parquetOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageInsightsReportConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageInsightsReportConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39448a9896c38efac202eecc91e5a8984653d2727b3ab26e734091c37983f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d499614d98a445201e0001a433511ca1d7c6270e0ee6d72571991965ab120ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349c98aa4070318e3b296a54b4a2f88a900c8a5d9def5d587c9c3f745747dce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b1f1c925472b892af6d1482d12de56ac562a16cbc4bbb90cb795934b2ed763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "csv_options": "csvOptions",
        "display_name": "displayName",
        "frequency_options": "frequencyOptions",
        "id": "id",
        "object_metadata_report_options": "objectMetadataReportOptions",
        "parquet_options": "parquetOptions",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class StorageInsightsReportConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        csv_options: typing.Optional[typing.Union["StorageInsightsReportConfigCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        frequency_options: typing.Optional[typing.Union["StorageInsightsReportConfigFrequencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        object_metadata_report_options: typing.Optional[typing.Union["StorageInsightsReportConfigObjectMetadataReportOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        parquet_options: typing.Optional[typing.Union["StorageInsightsReportConfigParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageInsightsReportConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the ReportConfig. The source and destination buckets specified in the ReportConfig must be in the same location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#location StorageInsightsReportConfig#location}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#csv_options StorageInsightsReportConfig#csv_options}
        :param display_name: The editable display name of the inventory report configuration. Has a limit of 256 characters. Can be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#display_name StorageInsightsReportConfig#display_name}
        :param frequency_options: frequency_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#frequency_options StorageInsightsReportConfig#frequency_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#id StorageInsightsReportConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param object_metadata_report_options: object_metadata_report_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#object_metadata_report_options StorageInsightsReportConfig#object_metadata_report_options}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#parquet_options StorageInsightsReportConfig#parquet_options}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#project StorageInsightsReportConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#timeouts StorageInsightsReportConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(csv_options, dict):
            csv_options = StorageInsightsReportConfigCsvOptions(**csv_options)
        if isinstance(frequency_options, dict):
            frequency_options = StorageInsightsReportConfigFrequencyOptions(**frequency_options)
        if isinstance(object_metadata_report_options, dict):
            object_metadata_report_options = StorageInsightsReportConfigObjectMetadataReportOptions(**object_metadata_report_options)
        if isinstance(parquet_options, dict):
            parquet_options = StorageInsightsReportConfigParquetOptions(**parquet_options)
        if isinstance(timeouts, dict):
            timeouts = StorageInsightsReportConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989ec41816eb3818c7d5767a324e110f1194d61fea982b478b271d9075d092f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument csv_options", value=csv_options, expected_type=type_hints["csv_options"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument frequency_options", value=frequency_options, expected_type=type_hints["frequency_options"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument object_metadata_report_options", value=object_metadata_report_options, expected_type=type_hints["object_metadata_report_options"])
            check_type(argname="argument parquet_options", value=parquet_options, expected_type=type_hints["parquet_options"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if csv_options is not None:
            self._values["csv_options"] = csv_options
        if display_name is not None:
            self._values["display_name"] = display_name
        if frequency_options is not None:
            self._values["frequency_options"] = frequency_options
        if id is not None:
            self._values["id"] = id
        if object_metadata_report_options is not None:
            self._values["object_metadata_report_options"] = object_metadata_report_options
        if parquet_options is not None:
            self._values["parquet_options"] = parquet_options
        if project is not None:
            self._values["project"] = project
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
    def location(self) -> builtins.str:
        '''The location of the ReportConfig. The source and destination buckets specified in the ReportConfig must be in the same location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#location StorageInsightsReportConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csv_options(self) -> typing.Optional["StorageInsightsReportConfigCsvOptions"]:
        '''csv_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#csv_options StorageInsightsReportConfig#csv_options}
        '''
        result = self._values.get("csv_options")
        return typing.cast(typing.Optional["StorageInsightsReportConfigCsvOptions"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The editable display name of the inventory report configuration. Has a limit of 256 characters. Can be empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#display_name StorageInsightsReportConfig#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frequency_options(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigFrequencyOptions"]:
        '''frequency_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#frequency_options StorageInsightsReportConfig#frequency_options}
        '''
        result = self._values.get("frequency_options")
        return typing.cast(typing.Optional["StorageInsightsReportConfigFrequencyOptions"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#id StorageInsightsReportConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_metadata_report_options(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptions"]:
        '''object_metadata_report_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#object_metadata_report_options StorageInsightsReportConfig#object_metadata_report_options}
        '''
        result = self._values.get("object_metadata_report_options")
        return typing.cast(typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptions"], result)

    @builtins.property
    def parquet_options(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigParquetOptions"]:
        '''parquet_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#parquet_options StorageInsightsReportConfig#parquet_options}
        '''
        result = self._values.get("parquet_options")
        return typing.cast(typing.Optional["StorageInsightsReportConfigParquetOptions"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#project StorageInsightsReportConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StorageInsightsReportConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#timeouts StorageInsightsReportConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageInsightsReportConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigCsvOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delimiter": "delimiter",
        "header_required": "headerRequired",
        "record_separator": "recordSeparator",
    },
)
class StorageInsightsReportConfigCsvOptions:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        header_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delimiter: The delimiter used to separate the fields in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#delimiter StorageInsightsReportConfig#delimiter}
        :param header_required: The boolean that indicates whether or not headers are included in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#header_required StorageInsightsReportConfig#header_required}
        :param record_separator: The character used to separate the records in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#record_separator StorageInsightsReportConfig#record_separator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a78c8cc174d6ddff3bf06665568d29ba4c14586b59f5d301ea28d22dbf3a0d)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument header_required", value=header_required, expected_type=type_hints["header_required"])
            check_type(argname="argument record_separator", value=record_separator, expected_type=type_hints["record_separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if header_required is not None:
            self._values["header_required"] = header_required
        if record_separator is not None:
            self._values["record_separator"] = record_separator

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''The delimiter used to separate the fields in the inventory report CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#delimiter StorageInsightsReportConfig#delimiter}
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The boolean that indicates whether or not headers are included in the inventory report CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#header_required StorageInsightsReportConfig#header_required}
        '''
        result = self._values.get("header_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_separator(self) -> typing.Optional[builtins.str]:
        '''The character used to separate the records in the inventory report CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#record_separator StorageInsightsReportConfig#record_separator}
        '''
        result = self._values.get("record_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigCsvOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigCsvOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigCsvOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf1e503edba92b063587bc0cff845dcaa6fd65c7262ac2c82bcb9266089eb6b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetHeaderRequired")
    def reset_header_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderRequired", []))

    @jsii.member(jsii_name="resetRecordSeparator")
    def reset_record_separator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordSeparator", []))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="headerRequiredInput")
    def header_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "headerRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="recordSeparatorInput")
    def record_separator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordSeparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373d517eaf482ffe09af45a41d8daba55c565b3aa4da665e3afcc7191e38a1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerRequired")
    def header_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "headerRequired"))

    @header_required.setter
    def header_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f573855adbcc14bc03bb8b7679a1bee4dbc594db06097591933e255683e9fbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordSeparator")
    def record_separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordSeparator"))

    @record_separator.setter
    def record_separator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb2bab126d43eac12b8333df5318b4ca5a280cc3d7f7250074720bb72e5514a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordSeparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageInsightsReportConfigCsvOptions]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigCsvOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigCsvOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5faf063d2c20c188cd6aca1dd279651c77e749cf251b5f4902a2747a06c4239c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigFrequencyOptions",
    jsii_struct_bases=[],
    name_mapping={
        "end_date": "endDate",
        "frequency": "frequency",
        "start_date": "startDate",
    },
)
class StorageInsightsReportConfigFrequencyOptions:
    def __init__(
        self,
        *,
        end_date: typing.Union["StorageInsightsReportConfigFrequencyOptionsEndDate", typing.Dict[builtins.str, typing.Any]],
        frequency: builtins.str,
        start_date: typing.Union["StorageInsightsReportConfigFrequencyOptionsStartDate", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#end_date StorageInsightsReportConfig#end_date}
        :param frequency: The frequency in which inventory reports are generated. Values are DAILY or WEEKLY. Possible values: ["DAILY", "WEEKLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#frequency StorageInsightsReportConfig#frequency}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#start_date StorageInsightsReportConfig#start_date}
        '''
        if isinstance(end_date, dict):
            end_date = StorageInsightsReportConfigFrequencyOptionsEndDate(**end_date)
        if isinstance(start_date, dict):
            start_date = StorageInsightsReportConfigFrequencyOptionsStartDate(**start_date)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14448c55c541814b9a974ea9cd3d55ecec7079bfc0d06958aa209b9356c3d3f4)
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_date": end_date,
            "frequency": frequency,
            "start_date": start_date,
        }

    @builtins.property
    def end_date(self) -> "StorageInsightsReportConfigFrequencyOptionsEndDate":
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#end_date StorageInsightsReportConfig#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast("StorageInsightsReportConfigFrequencyOptionsEndDate", result)

    @builtins.property
    def frequency(self) -> builtins.str:
        '''The frequency in which inventory reports are generated. Values are DAILY or WEEKLY. Possible values: ["DAILY", "WEEKLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#frequency StorageInsightsReportConfig#frequency}
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_date(self) -> "StorageInsightsReportConfigFrequencyOptionsStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#start_date StorageInsightsReportConfig#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("StorageInsightsReportConfigFrequencyOptionsStartDate", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigFrequencyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigFrequencyOptionsEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class StorageInsightsReportConfigFrequencyOptionsEndDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: The day of the month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#day StorageInsightsReportConfig#day}
        :param month: The month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#month StorageInsightsReportConfig#month}
        :param year: The year to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#year StorageInsightsReportConfig#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a397177f113861f23fa5ee236f9db3395e1793ba5cffa4ad67ba9763124ca2)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''The day of the month to stop generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#day StorageInsightsReportConfig#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''The month to stop generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#month StorageInsightsReportConfig#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''The year to stop generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#year StorageInsightsReportConfig#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigFrequencyOptionsEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigFrequencyOptionsEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigFrequencyOptionsEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c9cfd402b1368a47f6b5d9789f2cc868ecc461e6ec17c7fbc649ad464a6805)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af28edcf84d2fd5b2fcbb42d3060d69591967a34d4628fbf9393863115dff5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1e5056552f59bf78e688f1d3ebb3cd338d57ec4945bfc11bc317189b5c62cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a04c8adf8c87d749a5f9ee83fd08a06efa1afd4ec2722c6567d3a12a35b670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigFrequencyOptionsEndDate]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigFrequencyOptionsEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigFrequencyOptionsEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c61926c5aaf7d41de0c22a9ec596623f66689b2b2a1a283d8dd203f60d5eec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageInsightsReportConfigFrequencyOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigFrequencyOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e855baedcbd48cff8d4278f0c64410844c7e17773d4461a428e5d1885307418a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEndDate")
    def put_end_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: The day of the month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#day StorageInsightsReportConfig#day}
        :param month: The month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#month StorageInsightsReportConfig#month}
        :param year: The year to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#year StorageInsightsReportConfig#year}
        '''
        value = StorageInsightsReportConfigFrequencyOptionsEndDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putEndDate", [value]))

    @jsii.member(jsii_name="putStartDate")
    def put_start_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: The day of the month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#day StorageInsightsReportConfig#day}
        :param month: The month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#month StorageInsightsReportConfig#month}
        :param year: The year to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#year StorageInsightsReportConfig#year}
        '''
        value = StorageInsightsReportConfigFrequencyOptionsStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putStartDate", [value]))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(
        self,
    ) -> StorageInsightsReportConfigFrequencyOptionsEndDateOutputReference:
        return typing.cast(StorageInsightsReportConfigFrequencyOptionsEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "StorageInsightsReportConfigFrequencyOptionsStartDateOutputReference":
        return typing.cast("StorageInsightsReportConfigFrequencyOptionsStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigFrequencyOptionsEndDate]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigFrequencyOptionsEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigFrequencyOptionsStartDate"]:
        return typing.cast(typing.Optional["StorageInsightsReportConfigFrequencyOptionsStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8b49ba38f9251e3765d047819465242de7bcbf913197a2a9d26861b6cd300e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigFrequencyOptions]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigFrequencyOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigFrequencyOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b73c9cf407ad714a50f130ac29bbcfaacc36b4a1589d864fcbb49358145102db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigFrequencyOptionsStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class StorageInsightsReportConfigFrequencyOptionsStartDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: The day of the month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#day StorageInsightsReportConfig#day}
        :param month: The month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#month StorageInsightsReportConfig#month}
        :param year: The year to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#year StorageInsightsReportConfig#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfc5b1abfcea030497a00c4a70e88541d79f688528d320ea93c892ba479608d)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''The day of the month to start generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#day StorageInsightsReportConfig#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''The month to start generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#month StorageInsightsReportConfig#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''The year to start generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#year StorageInsightsReportConfig#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigFrequencyOptionsStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigFrequencyOptionsStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigFrequencyOptionsStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__395f014cbafb71ef143da83c1f57212c397fea1aa6a5c43aeb1a5a47e9e4f58f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be327a871d84ed53db6f8f3561a848b325a7063a86f6481fae064c633ba37e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0334ed42a39fa554a7741186a717ef2cac279e0e11233c11cdc630541ed4939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dcaf2653d3b74a0f0c0e897d4998229a5abbc4f27235a1cf94d65412b3eb9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigFrequencyOptionsStartDate]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigFrequencyOptionsStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigFrequencyOptionsStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a74c7a40fd5a975a13151fc4feb22e436380a3f0bb71ec974fe9d5a11e22809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigObjectMetadataReportOptions",
    jsii_struct_bases=[],
    name_mapping={
        "metadata_fields": "metadataFields",
        "storage_destination_options": "storageDestinationOptions",
        "storage_filters": "storageFilters",
    },
)
class StorageInsightsReportConfigObjectMetadataReportOptions:
    def __init__(
        self,
        *,
        metadata_fields: typing.Sequence[builtins.str],
        storage_destination_options: typing.Union["StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions", typing.Dict[builtins.str, typing.Any]],
        storage_filters: typing.Optional[typing.Union["StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata_fields: The metadata fields included in an inventory report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#metadata_fields StorageInsightsReportConfig#metadata_fields}
        :param storage_destination_options: storage_destination_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#storage_destination_options StorageInsightsReportConfig#storage_destination_options}
        :param storage_filters: storage_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#storage_filters StorageInsightsReportConfig#storage_filters}
        '''
        if isinstance(storage_destination_options, dict):
            storage_destination_options = StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions(**storage_destination_options)
        if isinstance(storage_filters, dict):
            storage_filters = StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters(**storage_filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820b4ff951dfbbf3e5fe3902df8a75788d4090f9912c7ea061988c0bfc646a4b)
            check_type(argname="argument metadata_fields", value=metadata_fields, expected_type=type_hints["metadata_fields"])
            check_type(argname="argument storage_destination_options", value=storage_destination_options, expected_type=type_hints["storage_destination_options"])
            check_type(argname="argument storage_filters", value=storage_filters, expected_type=type_hints["storage_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata_fields": metadata_fields,
            "storage_destination_options": storage_destination_options,
        }
        if storage_filters is not None:
            self._values["storage_filters"] = storage_filters

    @builtins.property
    def metadata_fields(self) -> typing.List[builtins.str]:
        '''The metadata fields included in an inventory report.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#metadata_fields StorageInsightsReportConfig#metadata_fields}
        '''
        result = self._values.get("metadata_fields")
        assert result is not None, "Required property 'metadata_fields' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def storage_destination_options(
        self,
    ) -> "StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions":
        '''storage_destination_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#storage_destination_options StorageInsightsReportConfig#storage_destination_options}
        '''
        result = self._values.get("storage_destination_options")
        assert result is not None, "Required property 'storage_destination_options' is missing"
        return typing.cast("StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions", result)

    @builtins.property
    def storage_filters(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"]:
        '''storage_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#storage_filters StorageInsightsReportConfig#storage_filters}
        '''
        result = self._values.get("storage_filters")
        return typing.cast(typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigObjectMetadataReportOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigObjectMetadataReportOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigObjectMetadataReportOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d62d9d150f9d52ca16e7dff0702c2199be3851c795e7d3de37eac43a1d6f6135)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStorageDestinationOptions")
    def put_storage_destination_options(
        self,
        *,
        bucket: builtins.str,
        destination_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The destination bucket that stores the generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#bucket StorageInsightsReportConfig#bucket}
        :param destination_path: The path within the destination bucket to store generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#destination_path StorageInsightsReportConfig#destination_path}
        '''
        value = StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions(
            bucket=bucket, destination_path=destination_path
        )

        return typing.cast(None, jsii.invoke(self, "putStorageDestinationOptions", [value]))

    @jsii.member(jsii_name="putStorageFilters")
    def put_storage_filters(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The filter to use when specifying which bucket to generate inventory reports for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#bucket StorageInsightsReportConfig#bucket}
        '''
        value = StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters(
            bucket=bucket
        )

        return typing.cast(None, jsii.invoke(self, "putStorageFilters", [value]))

    @jsii.member(jsii_name="resetStorageFilters")
    def reset_storage_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageFilters", []))

    @builtins.property
    @jsii.member(jsii_name="storageDestinationOptions")
    def storage_destination_options(
        self,
    ) -> "StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference":
        return typing.cast("StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference", jsii.get(self, "storageDestinationOptions"))

    @builtins.property
    @jsii.member(jsii_name="storageFilters")
    def storage_filters(
        self,
    ) -> "StorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference":
        return typing.cast("StorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference", jsii.get(self, "storageFilters"))

    @builtins.property
    @jsii.member(jsii_name="metadataFieldsInput")
    def metadata_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metadataFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageDestinationOptionsInput")
    def storage_destination_options_input(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions"]:
        return typing.cast(typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions"], jsii.get(self, "storageDestinationOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageFiltersInput")
    def storage_filters_input(
        self,
    ) -> typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"]:
        return typing.cast(typing.Optional["StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"], jsii.get(self, "storageFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataFields")
    def metadata_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metadataFields"))

    @metadata_fields.setter
    def metadata_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77aebe2e286156a38e8344f9763bebe540292514bbbc4955868939423507efab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptions]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78b9e8c422d3a0409a8c81e4ef8ff88c5c7c3c01bbb09ab45054057d835a4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "destination_path": "destinationPath"},
)
class StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        destination_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The destination bucket that stores the generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#bucket StorageInsightsReportConfig#bucket}
        :param destination_path: The path within the destination bucket to store generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#destination_path StorageInsightsReportConfig#destination_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b402668c167288777f6834427b7b4cb4e6cd069676362fb88229b39c9676bc7)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if destination_path is not None:
            self._values["destination_path"] = destination_path

    @builtins.property
    def bucket(self) -> builtins.str:
        '''The destination bucket that stores the generated inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#bucket StorageInsightsReportConfig#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_path(self) -> typing.Optional[builtins.str]:
        '''The path within the destination bucket to store generated inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#destination_path StorageInsightsReportConfig#destination_path}
        '''
        result = self._values.get("destination_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6b885c4fbcdd1dbe2c0c2279355cb6a00f8f826a9a155553e5b7db0e88c341)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestinationPath")
    def reset_destination_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPath", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPathInput")
    def destination_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPathInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0abf1388ef63af17b480f0694cedb1c51e8f5d837074006d23a8fa7c899f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPath")
    def destination_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPath"))

    @destination_path.setter
    def destination_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176cb40c98eef4bd14224286bbc991470f40d491348574f438e65acbddb4da4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1eaafdc0a9868c136b0f41e65ca1dd8f3588a2f01cbda1e7bb5f0abcb01903f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket"},
)
class StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters:
    def __init__(self, *, bucket: typing.Optional[builtins.str] = None) -> None:
        '''
        :param bucket: The filter to use when specifying which bucket to generate inventory reports for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#bucket StorageInsightsReportConfig#bucket}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cfb23f7d60a248c6feb26834aacfe2eff42abec7152bcbedd085a67cb6062e5)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The filter to use when specifying which bucket to generate inventory reports for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#bucket StorageInsightsReportConfig#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b969950a360074cb437e6cac240ff77670483d6f3aaf79d40391bd2c1da9bd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8d0dc2307b1fa89f2d57bbdaa426101f5fbaf4229b871ce2c896d2c851c7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fcd26c8a1826ebf652aeda8c9fd5499dccb535df9d4a4a86128f7dc37c2656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigParquetOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class StorageInsightsReportConfigParquetOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigParquetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigParquetOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigParquetOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dc08f6848982a6a505db84fccc029d2f9fd583d4fbcdf2b742ab83ad1032c97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageInsightsReportConfigParquetOptions]:
        return typing.cast(typing.Optional[StorageInsightsReportConfigParquetOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageInsightsReportConfigParquetOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da3ab7f8c05029f180e5c5d82c30e4f150690165b7b80e5674f523f9b745287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class StorageInsightsReportConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#create StorageInsightsReportConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#delete StorageInsightsReportConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#update StorageInsightsReportConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be80f1636ff60307a53be197f96e09b0b793dc27e442b516ead5622a787daa3c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#create StorageInsightsReportConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#delete StorageInsightsReportConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_insights_report_config#update StorageInsightsReportConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageInsightsReportConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageInsightsReportConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageInsightsReportConfig.StorageInsightsReportConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fab915ac38d24108d27a989db6d06aa916f2c2074ae56865d19f39e0e6204983)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9526134771c8f5d49655d2ed67a05e6840194d2b392a049924c8dccc5930dd56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ade90e47c42b4982193127de290727e789334c0b5eebee1c7e39e82978cc5e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae745252693492d53d1463f935c3fadf8eab87c588cf592d83402473fe5c99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsReportConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsReportConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsReportConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b5ab8ef351ae67e428a491c9626fc80930b5a3c806e6d5bf47c70a1db389f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageInsightsReportConfig",
    "StorageInsightsReportConfigConfig",
    "StorageInsightsReportConfigCsvOptions",
    "StorageInsightsReportConfigCsvOptionsOutputReference",
    "StorageInsightsReportConfigFrequencyOptions",
    "StorageInsightsReportConfigFrequencyOptionsEndDate",
    "StorageInsightsReportConfigFrequencyOptionsEndDateOutputReference",
    "StorageInsightsReportConfigFrequencyOptionsOutputReference",
    "StorageInsightsReportConfigFrequencyOptionsStartDate",
    "StorageInsightsReportConfigFrequencyOptionsStartDateOutputReference",
    "StorageInsightsReportConfigObjectMetadataReportOptions",
    "StorageInsightsReportConfigObjectMetadataReportOptionsOutputReference",
    "StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions",
    "StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference",
    "StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters",
    "StorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference",
    "StorageInsightsReportConfigParquetOptions",
    "StorageInsightsReportConfigParquetOptionsOutputReference",
    "StorageInsightsReportConfigTimeouts",
    "StorageInsightsReportConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cad8f561dd7f68de45878db7cc2cc6e9ca2dfe64f8d25e134e2d293403ac905e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    csv_options: typing.Optional[typing.Union[StorageInsightsReportConfigCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    frequency_options: typing.Optional[typing.Union[StorageInsightsReportConfigFrequencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    object_metadata_report_options: typing.Optional[typing.Union[StorageInsightsReportConfigObjectMetadataReportOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    parquet_options: typing.Optional[typing.Union[StorageInsightsReportConfigParquetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageInsightsReportConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c933a3e658ce7264c8848e10569faf4413a4955850bfec57a0641e1e797eaab5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39448a9896c38efac202eecc91e5a8984653d2727b3ab26e734091c37983f78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d499614d98a445201e0001a433511ca1d7c6270e0ee6d72571991965ab120ee1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349c98aa4070318e3b296a54b4a2f88a900c8a5d9def5d587c9c3f745747dce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b1f1c925472b892af6d1482d12de56ac562a16cbc4bbb90cb795934b2ed763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989ec41816eb3818c7d5767a324e110f1194d61fea982b478b271d9075d092f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    csv_options: typing.Optional[typing.Union[StorageInsightsReportConfigCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    frequency_options: typing.Optional[typing.Union[StorageInsightsReportConfigFrequencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    object_metadata_report_options: typing.Optional[typing.Union[StorageInsightsReportConfigObjectMetadataReportOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    parquet_options: typing.Optional[typing.Union[StorageInsightsReportConfigParquetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageInsightsReportConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a78c8cc174d6ddff3bf06665568d29ba4c14586b59f5d301ea28d22dbf3a0d(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    header_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1e503edba92b063587bc0cff845dcaa6fd65c7262ac2c82bcb9266089eb6b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373d517eaf482ffe09af45a41d8daba55c565b3aa4da665e3afcc7191e38a1ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f573855adbcc14bc03bb8b7679a1bee4dbc594db06097591933e255683e9fbb9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb2bab126d43eac12b8333df5318b4ca5a280cc3d7f7250074720bb72e5514a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faf063d2c20c188cd6aca1dd279651c77e749cf251b5f4902a2747a06c4239c(
    value: typing.Optional[StorageInsightsReportConfigCsvOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14448c55c541814b9a974ea9cd3d55ecec7079bfc0d06958aa209b9356c3d3f4(
    *,
    end_date: typing.Union[StorageInsightsReportConfigFrequencyOptionsEndDate, typing.Dict[builtins.str, typing.Any]],
    frequency: builtins.str,
    start_date: typing.Union[StorageInsightsReportConfigFrequencyOptionsStartDate, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a397177f113861f23fa5ee236f9db3395e1793ba5cffa4ad67ba9763124ca2(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c9cfd402b1368a47f6b5d9789f2cc868ecc461e6ec17c7fbc649ad464a6805(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af28edcf84d2fd5b2fcbb42d3060d69591967a34d4628fbf9393863115dff5b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1e5056552f59bf78e688f1d3ebb3cd338d57ec4945bfc11bc317189b5c62cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a04c8adf8c87d749a5f9ee83fd08a06efa1afd4ec2722c6567d3a12a35b670(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c61926c5aaf7d41de0c22a9ec596623f66689b2b2a1a283d8dd203f60d5eec4(
    value: typing.Optional[StorageInsightsReportConfigFrequencyOptionsEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e855baedcbd48cff8d4278f0c64410844c7e17773d4461a428e5d1885307418a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8b49ba38f9251e3765d047819465242de7bcbf913197a2a9d26861b6cd300e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73c9cf407ad714a50f130ac29bbcfaacc36b4a1589d864fcbb49358145102db(
    value: typing.Optional[StorageInsightsReportConfigFrequencyOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfc5b1abfcea030497a00c4a70e88541d79f688528d320ea93c892ba479608d(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395f014cbafb71ef143da83c1f57212c397fea1aa6a5c43aeb1a5a47e9e4f58f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be327a871d84ed53db6f8f3561a848b325a7063a86f6481fae064c633ba37e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0334ed42a39fa554a7741186a717ef2cac279e0e11233c11cdc630541ed4939(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dcaf2653d3b74a0f0c0e897d4998229a5abbc4f27235a1cf94d65412b3eb9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a74c7a40fd5a975a13151fc4feb22e436380a3f0bb71ec974fe9d5a11e22809(
    value: typing.Optional[StorageInsightsReportConfigFrequencyOptionsStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820b4ff951dfbbf3e5fe3902df8a75788d4090f9912c7ea061988c0bfc646a4b(
    *,
    metadata_fields: typing.Sequence[builtins.str],
    storage_destination_options: typing.Union[StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions, typing.Dict[builtins.str, typing.Any]],
    storage_filters: typing.Optional[typing.Union[StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62d9d150f9d52ca16e7dff0702c2199be3851c795e7d3de37eac43a1d6f6135(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77aebe2e286156a38e8344f9763bebe540292514bbbc4955868939423507efab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78b9e8c422d3a0409a8c81e4ef8ff88c5c7c3c01bbb09ab45054057d835a4f8(
    value: typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b402668c167288777f6834427b7b4cb4e6cd069676362fb88229b39c9676bc7(
    *,
    bucket: builtins.str,
    destination_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6b885c4fbcdd1dbe2c0c2279355cb6a00f8f826a9a155553e5b7db0e88c341(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0abf1388ef63af17b480f0694cedb1c51e8f5d837074006d23a8fa7c899f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176cb40c98eef4bd14224286bbc991470f40d491348574f438e65acbddb4da4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1eaafdc0a9868c136b0f41e65ca1dd8f3588a2f01cbda1e7bb5f0abcb01903f(
    value: typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cfb23f7d60a248c6feb26834aacfe2eff42abec7152bcbedd085a67cb6062e5(
    *,
    bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b969950a360074cb437e6cac240ff77670483d6f3aaf79d40391bd2c1da9bd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8d0dc2307b1fa89f2d57bbdaa426101f5fbaf4229b871ce2c896d2c851c7de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fcd26c8a1826ebf652aeda8c9fd5499dccb535df9d4a4a86128f7dc37c2656(
    value: typing.Optional[StorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc08f6848982a6a505db84fccc029d2f9fd583d4fbcdf2b742ab83ad1032c97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da3ab7f8c05029f180e5c5d82c30e4f150690165b7b80e5674f523f9b745287(
    value: typing.Optional[StorageInsightsReportConfigParquetOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be80f1636ff60307a53be197f96e09b0b793dc27e442b516ead5622a787daa3c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab915ac38d24108d27a989db6d06aa916f2c2074ae56865d19f39e0e6204983(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9526134771c8f5d49655d2ed67a05e6840194d2b392a049924c8dccc5930dd56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ade90e47c42b4982193127de290727e789334c0b5eebee1c7e39e82978cc5e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae745252693492d53d1463f935c3fadf8eab87c588cf592d83402473fe5c99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b5ab8ef351ae67e428a491c9626fc80930b5a3c806e6d5bf47c70a1db389f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageInsightsReportConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
