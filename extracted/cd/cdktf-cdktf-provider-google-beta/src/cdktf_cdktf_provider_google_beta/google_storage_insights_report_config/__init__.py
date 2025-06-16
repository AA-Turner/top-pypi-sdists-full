r'''
# `google_storage_insights_report_config`

Refer to the Terraform Registry for docs: [`google_storage_insights_report_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config).
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


class GoogleStorageInsightsReportConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config google_storage_insights_report_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        csv_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        frequency_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigFrequencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        object_metadata_report_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigObjectMetadataReportOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        parquet_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config google_storage_insights_report_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the ReportConfig. The source and destination buckets specified in the ReportConfig must be in the same location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#location GoogleStorageInsightsReportConfig#location}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#csv_options GoogleStorageInsightsReportConfig#csv_options}
        :param display_name: The editable display name of the inventory report configuration. Has a limit of 256 characters. Can be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#display_name GoogleStorageInsightsReportConfig#display_name}
        :param frequency_options: frequency_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#frequency_options GoogleStorageInsightsReportConfig#frequency_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#id GoogleStorageInsightsReportConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param object_metadata_report_options: object_metadata_report_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#object_metadata_report_options GoogleStorageInsightsReportConfig#object_metadata_report_options}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#parquet_options GoogleStorageInsightsReportConfig#parquet_options}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#project GoogleStorageInsightsReportConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#timeouts GoogleStorageInsightsReportConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36546cf3f0bac8c9505bfe89156687976eaf94c1093017580c80d2473b3089b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleStorageInsightsReportConfigConfig(
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
        '''Generates CDKTF code for importing a GoogleStorageInsightsReportConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleStorageInsightsReportConfig to import.
        :param import_from_id: The id of the existing GoogleStorageInsightsReportConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleStorageInsightsReportConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05241e2a31b2e680fd64751f74964943427e58af9715ff20c93f4b9e4dcf4345)
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
        :param delimiter: The delimiter used to separate the fields in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#delimiter GoogleStorageInsightsReportConfig#delimiter}
        :param header_required: The boolean that indicates whether or not headers are included in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#header_required GoogleStorageInsightsReportConfig#header_required}
        :param record_separator: The character used to separate the records in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#record_separator GoogleStorageInsightsReportConfig#record_separator}
        '''
        value = GoogleStorageInsightsReportConfigCsvOptions(
            delimiter=delimiter,
            header_required=header_required,
            record_separator=record_separator,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvOptions", [value]))

    @jsii.member(jsii_name="putFrequencyOptions")
    def put_frequency_options(
        self,
        *,
        end_date: typing.Union["GoogleStorageInsightsReportConfigFrequencyOptionsEndDate", typing.Dict[builtins.str, typing.Any]],
        frequency: builtins.str,
        start_date: typing.Union["GoogleStorageInsightsReportConfigFrequencyOptionsStartDate", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#end_date GoogleStorageInsightsReportConfig#end_date}
        :param frequency: The frequency in which inventory reports are generated. Values are DAILY or WEEKLY. Possible values: ["DAILY", "WEEKLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#frequency GoogleStorageInsightsReportConfig#frequency}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#start_date GoogleStorageInsightsReportConfig#start_date}
        '''
        value = GoogleStorageInsightsReportConfigFrequencyOptions(
            end_date=end_date, frequency=frequency, start_date=start_date
        )

        return typing.cast(None, jsii.invoke(self, "putFrequencyOptions", [value]))

    @jsii.member(jsii_name="putObjectMetadataReportOptions")
    def put_object_metadata_report_options(
        self,
        *,
        metadata_fields: typing.Sequence[builtins.str],
        storage_destination_options: typing.Union["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions", typing.Dict[builtins.str, typing.Any]],
        storage_filters: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata_fields: The metadata fields included in an inventory report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#metadata_fields GoogleStorageInsightsReportConfig#metadata_fields}
        :param storage_destination_options: storage_destination_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#storage_destination_options GoogleStorageInsightsReportConfig#storage_destination_options}
        :param storage_filters: storage_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#storage_filters GoogleStorageInsightsReportConfig#storage_filters}
        '''
        value = GoogleStorageInsightsReportConfigObjectMetadataReportOptions(
            metadata_fields=metadata_fields,
            storage_destination_options=storage_destination_options,
            storage_filters=storage_filters,
        )

        return typing.cast(None, jsii.invoke(self, "putObjectMetadataReportOptions", [value]))

    @jsii.member(jsii_name="putParquetOptions")
    def put_parquet_options(self) -> None:
        value = GoogleStorageInsightsReportConfigParquetOptions()

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#create GoogleStorageInsightsReportConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#delete GoogleStorageInsightsReportConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#update GoogleStorageInsightsReportConfig#update}.
        '''
        value = GoogleStorageInsightsReportConfigTimeouts(
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
    def csv_options(
        self,
    ) -> "GoogleStorageInsightsReportConfigCsvOptionsOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigCsvOptionsOutputReference", jsii.get(self, "csvOptions"))

    @builtins.property
    @jsii.member(jsii_name="frequencyOptions")
    def frequency_options(
        self,
    ) -> "GoogleStorageInsightsReportConfigFrequencyOptionsOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigFrequencyOptionsOutputReference", jsii.get(self, "frequencyOptions"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="objectMetadataReportOptions")
    def object_metadata_report_options(
        self,
    ) -> "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigObjectMetadataReportOptionsOutputReference", jsii.get(self, "objectMetadataReportOptions"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptions")
    def parquet_options(
        self,
    ) -> "GoogleStorageInsightsReportConfigParquetOptionsOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigParquetOptionsOutputReference", jsii.get(self, "parquetOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleStorageInsightsReportConfigTimeoutsOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="csvOptionsInput")
    def csv_options_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigCsvOptions"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigCsvOptions"], jsii.get(self, "csvOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyOptionsInput")
    def frequency_options_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigFrequencyOptions"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigFrequencyOptions"], jsii.get(self, "frequencyOptionsInput"))

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
    ) -> typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptions"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptions"], jsii.get(self, "objectMetadataReportOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="parquetOptionsInput")
    def parquet_options_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigParquetOptions"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigParquetOptions"], jsii.get(self, "parquetOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageInsightsReportConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageInsightsReportConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb83387f715946e5e969b9eba8108e588f5d489178e98282d5963506ca267976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff4a380d0ba4c59263b4eedd5b7ff0b47e7204bc4956d3adb3012ad7ff21048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca46df2aea8cc824d2d6dd08f781d6711252f89edd36e73f0fced1cfe058b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b33e8ac3e1450401133be589a69a0a89d5feeeb3c6f75850b8e745d54512fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigConfig",
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
class GoogleStorageInsightsReportConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        csv_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        frequency_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigFrequencyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        object_metadata_report_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigObjectMetadataReportOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        parquet_options: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigParquetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the ReportConfig. The source and destination buckets specified in the ReportConfig must be in the same location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#location GoogleStorageInsightsReportConfig#location}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#csv_options GoogleStorageInsightsReportConfig#csv_options}
        :param display_name: The editable display name of the inventory report configuration. Has a limit of 256 characters. Can be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#display_name GoogleStorageInsightsReportConfig#display_name}
        :param frequency_options: frequency_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#frequency_options GoogleStorageInsightsReportConfig#frequency_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#id GoogleStorageInsightsReportConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param object_metadata_report_options: object_metadata_report_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#object_metadata_report_options GoogleStorageInsightsReportConfig#object_metadata_report_options}
        :param parquet_options: parquet_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#parquet_options GoogleStorageInsightsReportConfig#parquet_options}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#project GoogleStorageInsightsReportConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#timeouts GoogleStorageInsightsReportConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(csv_options, dict):
            csv_options = GoogleStorageInsightsReportConfigCsvOptions(**csv_options)
        if isinstance(frequency_options, dict):
            frequency_options = GoogleStorageInsightsReportConfigFrequencyOptions(**frequency_options)
        if isinstance(object_metadata_report_options, dict):
            object_metadata_report_options = GoogleStorageInsightsReportConfigObjectMetadataReportOptions(**object_metadata_report_options)
        if isinstance(parquet_options, dict):
            parquet_options = GoogleStorageInsightsReportConfigParquetOptions(**parquet_options)
        if isinstance(timeouts, dict):
            timeouts = GoogleStorageInsightsReportConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6380f83e0074381db72b242b2e03eb7e6cee7c6bd4869dedf4ad2a000405e91)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#location GoogleStorageInsightsReportConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csv_options(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigCsvOptions"]:
        '''csv_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#csv_options GoogleStorageInsightsReportConfig#csv_options}
        '''
        result = self._values.get("csv_options")
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigCsvOptions"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The editable display name of the inventory report configuration. Has a limit of 256 characters. Can be empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#display_name GoogleStorageInsightsReportConfig#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frequency_options(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigFrequencyOptions"]:
        '''frequency_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#frequency_options GoogleStorageInsightsReportConfig#frequency_options}
        '''
        result = self._values.get("frequency_options")
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigFrequencyOptions"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#id GoogleStorageInsightsReportConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_metadata_report_options(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptions"]:
        '''object_metadata_report_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#object_metadata_report_options GoogleStorageInsightsReportConfig#object_metadata_report_options}
        '''
        result = self._values.get("object_metadata_report_options")
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptions"], result)

    @builtins.property
    def parquet_options(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigParquetOptions"]:
        '''parquet_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#parquet_options GoogleStorageInsightsReportConfig#parquet_options}
        '''
        result = self._values.get("parquet_options")
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigParquetOptions"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#project GoogleStorageInsightsReportConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleStorageInsightsReportConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#timeouts GoogleStorageInsightsReportConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigCsvOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delimiter": "delimiter",
        "header_required": "headerRequired",
        "record_separator": "recordSeparator",
    },
)
class GoogleStorageInsightsReportConfigCsvOptions:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        header_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delimiter: The delimiter used to separate the fields in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#delimiter GoogleStorageInsightsReportConfig#delimiter}
        :param header_required: The boolean that indicates whether or not headers are included in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#header_required GoogleStorageInsightsReportConfig#header_required}
        :param record_separator: The character used to separate the records in the inventory report CSV file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#record_separator GoogleStorageInsightsReportConfig#record_separator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d22ac4e9c8e04ba0aeb3790afd17acdeabc704644b7b0b571404e0dedafc0c3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#delimiter GoogleStorageInsightsReportConfig#delimiter}
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The boolean that indicates whether or not headers are included in the inventory report CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#header_required GoogleStorageInsightsReportConfig#header_required}
        '''
        result = self._values.get("header_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_separator(self) -> typing.Optional[builtins.str]:
        '''The character used to separate the records in the inventory report CSV file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#record_separator GoogleStorageInsightsReportConfig#record_separator}
        '''
        result = self._values.get("record_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigCsvOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigCsvOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigCsvOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2fe1d2cb0148de4e4b6a0b689ecbbc82ff5d7c54eba23a412d896124d559699)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a6248bbfee4d2680e3ee0c1b2df7c4573cc5e1c2bb9130cbb1ac9b91472ceab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6847f8e739090753afe34372d792740095033a8756a15a203b0f113ac212b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordSeparator")
    def record_separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordSeparator"))

    @record_separator.setter
    def record_separator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d27638a2e355da2e64c59abf33d15e34902ce59530d85da9444bf55738da403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordSeparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigCsvOptions]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigCsvOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigCsvOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfc07e7a53272f098726fc8a8cbfae404945abd7ac6b8e07f8dbd5f91fa0386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigFrequencyOptions",
    jsii_struct_bases=[],
    name_mapping={
        "end_date": "endDate",
        "frequency": "frequency",
        "start_date": "startDate",
    },
)
class GoogleStorageInsightsReportConfigFrequencyOptions:
    def __init__(
        self,
        *,
        end_date: typing.Union["GoogleStorageInsightsReportConfigFrequencyOptionsEndDate", typing.Dict[builtins.str, typing.Any]],
        frequency: builtins.str,
        start_date: typing.Union["GoogleStorageInsightsReportConfigFrequencyOptionsStartDate", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#end_date GoogleStorageInsightsReportConfig#end_date}
        :param frequency: The frequency in which inventory reports are generated. Values are DAILY or WEEKLY. Possible values: ["DAILY", "WEEKLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#frequency GoogleStorageInsightsReportConfig#frequency}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#start_date GoogleStorageInsightsReportConfig#start_date}
        '''
        if isinstance(end_date, dict):
            end_date = GoogleStorageInsightsReportConfigFrequencyOptionsEndDate(**end_date)
        if isinstance(start_date, dict):
            start_date = GoogleStorageInsightsReportConfigFrequencyOptionsStartDate(**start_date)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfec99c93e90d6cf7da62caf7dbdaf9b66b8e6f5a5b51ae2324568d6a113f64d)
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_date": end_date,
            "frequency": frequency,
            "start_date": start_date,
        }

    @builtins.property
    def end_date(self) -> "GoogleStorageInsightsReportConfigFrequencyOptionsEndDate":
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#end_date GoogleStorageInsightsReportConfig#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast("GoogleStorageInsightsReportConfigFrequencyOptionsEndDate", result)

    @builtins.property
    def frequency(self) -> builtins.str:
        '''The frequency in which inventory reports are generated. Values are DAILY or WEEKLY. Possible values: ["DAILY", "WEEKLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#frequency GoogleStorageInsightsReportConfig#frequency}
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_date(
        self,
    ) -> "GoogleStorageInsightsReportConfigFrequencyOptionsStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#start_date GoogleStorageInsightsReportConfig#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("GoogleStorageInsightsReportConfigFrequencyOptionsStartDate", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigFrequencyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigFrequencyOptionsEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleStorageInsightsReportConfigFrequencyOptionsEndDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: The day of the month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#day GoogleStorageInsightsReportConfig#day}
        :param month: The month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#month GoogleStorageInsightsReportConfig#month}
        :param year: The year to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#year GoogleStorageInsightsReportConfig#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b4b5ad6c312c0e690e8a8edbb7d22c483d3a5ffb0921eae6ec22f1e02969f8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#day GoogleStorageInsightsReportConfig#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''The month to stop generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#month GoogleStorageInsightsReportConfig#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''The year to stop generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#year GoogleStorageInsightsReportConfig#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigFrequencyOptionsEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigFrequencyOptionsEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigFrequencyOptionsEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5be67fc2b954da2bf6d831964c605765c355e52ebc06a6ff8d4dee5d817552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51afbcf48c189498b5b32959026df35f872c35ce6a682f8862fa33bc8988f1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972615d6cf50c4654e1ff3f9c8bc4c9297e468df30d3a84f9bd626a7daff4ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5e0bbf384cdbeaca9629b0484b4c9ac560b677a7307cd04574c0d80cf3b7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsEndDate]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a9b1ef3833a9035cd8824deaf24d8fd0bd2a4de478a1a738edc6d8fc9e43a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageInsightsReportConfigFrequencyOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigFrequencyOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd38ef0ca1fa549610164fba0b963c854919136c4ab552f8520bb8678fdc323b)
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
        :param day: The day of the month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#day GoogleStorageInsightsReportConfig#day}
        :param month: The month to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#month GoogleStorageInsightsReportConfig#month}
        :param year: The year to stop generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#year GoogleStorageInsightsReportConfig#year}
        '''
        value = GoogleStorageInsightsReportConfigFrequencyOptionsEndDate(
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
        :param day: The day of the month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#day GoogleStorageInsightsReportConfig#day}
        :param month: The month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#month GoogleStorageInsightsReportConfig#month}
        :param year: The year to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#year GoogleStorageInsightsReportConfig#year}
        '''
        value = GoogleStorageInsightsReportConfigFrequencyOptionsStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putStartDate", [value]))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(
        self,
    ) -> GoogleStorageInsightsReportConfigFrequencyOptionsEndDateOutputReference:
        return typing.cast(GoogleStorageInsightsReportConfigFrequencyOptionsEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "GoogleStorageInsightsReportConfigFrequencyOptionsStartDateOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigFrequencyOptionsStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsEndDate]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigFrequencyOptionsStartDate"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigFrequencyOptionsStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1a82e309714a7ce657638892ad690a3abecc11baf573bf8b21cf2bcb24b6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptions]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c965aa15c527c5c57d010d95a24916e2981a9bd0c248be26f2826b82f67908af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigFrequencyOptionsStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleStorageInsightsReportConfigFrequencyOptionsStartDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: The day of the month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#day GoogleStorageInsightsReportConfig#day}
        :param month: The month to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#month GoogleStorageInsightsReportConfig#month}
        :param year: The year to start generating inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#year GoogleStorageInsightsReportConfig#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfdb4d737683ffbab6bc30f84534b22e6874e07631d67c9f57d54f142a69de5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#day GoogleStorageInsightsReportConfig#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''The month to start generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#month GoogleStorageInsightsReportConfig#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''The year to start generating inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#year GoogleStorageInsightsReportConfig#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigFrequencyOptionsStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigFrequencyOptionsStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigFrequencyOptionsStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c798e3206fbbd6e914861074a3bde554c5ba8e0154472cc677ca143bf570c72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7371237db528700ac329281045e7292864bf69b5df7b810fddcaa255e5fc7ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a38c0cc22a51cf59de5597aaf1169f2da5d997665fc882d3598553042429514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a749226f1cf97faee360f0fd06347c989a9c736fa426f6d3db42a9f9509f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsStartDate]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0abdea9d6951e3d45f88719db9761c9aa1596bb9500f735fb969d99e16d1730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigObjectMetadataReportOptions",
    jsii_struct_bases=[],
    name_mapping={
        "metadata_fields": "metadataFields",
        "storage_destination_options": "storageDestinationOptions",
        "storage_filters": "storageFilters",
    },
)
class GoogleStorageInsightsReportConfigObjectMetadataReportOptions:
    def __init__(
        self,
        *,
        metadata_fields: typing.Sequence[builtins.str],
        storage_destination_options: typing.Union["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions", typing.Dict[builtins.str, typing.Any]],
        storage_filters: typing.Optional[typing.Union["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata_fields: The metadata fields included in an inventory report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#metadata_fields GoogleStorageInsightsReportConfig#metadata_fields}
        :param storage_destination_options: storage_destination_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#storage_destination_options GoogleStorageInsightsReportConfig#storage_destination_options}
        :param storage_filters: storage_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#storage_filters GoogleStorageInsightsReportConfig#storage_filters}
        '''
        if isinstance(storage_destination_options, dict):
            storage_destination_options = GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions(**storage_destination_options)
        if isinstance(storage_filters, dict):
            storage_filters = GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters(**storage_filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f142efc21f608290a4f0e2457742c9bfbd2ddec36fbfa7a40f6eff9d0908a727)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#metadata_fields GoogleStorageInsightsReportConfig#metadata_fields}
        '''
        result = self._values.get("metadata_fields")
        assert result is not None, "Required property 'metadata_fields' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def storage_destination_options(
        self,
    ) -> "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions":
        '''storage_destination_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#storage_destination_options GoogleStorageInsightsReportConfig#storage_destination_options}
        '''
        result = self._values.get("storage_destination_options")
        assert result is not None, "Required property 'storage_destination_options' is missing"
        return typing.cast("GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions", result)

    @builtins.property
    def storage_filters(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"]:
        '''storage_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#storage_filters GoogleStorageInsightsReportConfig#storage_filters}
        '''
        result = self._values.get("storage_filters")
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigObjectMetadataReportOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigObjectMetadataReportOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigObjectMetadataReportOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d361338576841f495c27103b6a9f4189a01d6c465d8703ac9b3ef9a088e274fb)
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
        :param bucket: The destination bucket that stores the generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#bucket GoogleStorageInsightsReportConfig#bucket}
        :param destination_path: The path within the destination bucket to store generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#destination_path GoogleStorageInsightsReportConfig#destination_path}
        '''
        value = GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions(
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
        :param bucket: The filter to use when specifying which bucket to generate inventory reports for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#bucket GoogleStorageInsightsReportConfig#bucket}
        '''
        value = GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters(
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
    ) -> "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference", jsii.get(self, "storageDestinationOptions"))

    @builtins.property
    @jsii.member(jsii_name="storageFilters")
    def storage_filters(
        self,
    ) -> "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference":
        return typing.cast("GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference", jsii.get(self, "storageFilters"))

    @builtins.property
    @jsii.member(jsii_name="metadataFieldsInput")
    def metadata_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metadataFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageDestinationOptionsInput")
    def storage_destination_options_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions"], jsii.get(self, "storageDestinationOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageFiltersInput")
    def storage_filters_input(
        self,
    ) -> typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"]:
        return typing.cast(typing.Optional["GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters"], jsii.get(self, "storageFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataFields")
    def metadata_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metadataFields"))

    @metadata_fields.setter
    def metadata_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a782e9e730447079006d0d7a5958df606f8248697847238eae773bdaf386a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptions]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397aed3a6af595cb00764e52f00d5d5b3ab56aa09f494452200a9897bce041e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "destination_path": "destinationPath"},
)
class GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        destination_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The destination bucket that stores the generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#bucket GoogleStorageInsightsReportConfig#bucket}
        :param destination_path: The path within the destination bucket to store generated inventory reports. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#destination_path GoogleStorageInsightsReportConfig#destination_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f33f8ee608617316c7e56934898a69fdf2f8c10e50391f54c4a9c97e1115274)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#bucket GoogleStorageInsightsReportConfig#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_path(self) -> typing.Optional[builtins.str]:
        '''The path within the destination bucket to store generated inventory reports.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#destination_path GoogleStorageInsightsReportConfig#destination_path}
        '''
        result = self._values.get("destination_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35b58d5c27b17dbb58b23a2a9049e6601877ee55f99c5f0da89cbd219b453ff7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e0ee3794114fb7c8ae1c4058541f8a446e957de0bc932137dd2bc340c99e9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPath")
    def destination_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPath"))

    @destination_path.setter
    def destination_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ff9aba369be953a279ce70321f5c650de763a77800fdf90cc49a6bb99acb56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4eade45fc099fedd329daf6013395eb9a4a514de35691d8e8a802e0a6b347a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket"},
)
class GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters:
    def __init__(self, *, bucket: typing.Optional[builtins.str] = None) -> None:
        '''
        :param bucket: The filter to use when specifying which bucket to generate inventory reports for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#bucket GoogleStorageInsightsReportConfig#bucket}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1160236dc103ab03182e40ce212d4ea31c724292fb9f2aaa2478962ea701d10c)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The filter to use when specifying which bucket to generate inventory reports for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#bucket GoogleStorageInsightsReportConfig#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3ba8f4206ede31aa48648bc6016b896e2c02d2eeb9210684aca051156c88a66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21f275f1574bee5f3429d50f20a194b1cea28f9eae1e55978f0c02e62a4f5fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633a73b5a30469e931b3e012698aff1bbdc242f471746a4dddb84d6301ae49ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigParquetOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleStorageInsightsReportConfigParquetOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigParquetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigParquetOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigParquetOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8615efb96217502f9a8cb3c5202ad67b3e2205b331cb985fa78abaf609df5714)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageInsightsReportConfigParquetOptions]:
        return typing.cast(typing.Optional[GoogleStorageInsightsReportConfigParquetOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageInsightsReportConfigParquetOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6a40ee98ec5d78265909f67cd6ad53f836e3955a29167d460ed0337d8beb38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleStorageInsightsReportConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#create GoogleStorageInsightsReportConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#delete GoogleStorageInsightsReportConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#update GoogleStorageInsightsReportConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff929c1705d24eac9fdfc59654645aba336eea43f645b418d8d0e07630759a5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#create GoogleStorageInsightsReportConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#delete GoogleStorageInsightsReportConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_insights_report_config#update GoogleStorageInsightsReportConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageInsightsReportConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageInsightsReportConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageInsightsReportConfig.GoogleStorageInsightsReportConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e18e4f6556224b54c45904711aa3cd33c47c01e89d6c1816af59de4bbd372ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cc9a09797872b28217c0d5b95ec5f7713d45988fd3ce40fef5d871977956c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cb4dc5a9b50320a0bd417a93f4b3d61dc0afcea81838c7e34f2363821470c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7402e294ff65ce210611b3d783b4c275b3be5c152555311aba07478b8cc3db94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsReportConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsReportConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsReportConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1d3dfb4f9a863a20abfc1f55121f80540ff2f5e5773c37224e9483701b4bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleStorageInsightsReportConfig",
    "GoogleStorageInsightsReportConfigConfig",
    "GoogleStorageInsightsReportConfigCsvOptions",
    "GoogleStorageInsightsReportConfigCsvOptionsOutputReference",
    "GoogleStorageInsightsReportConfigFrequencyOptions",
    "GoogleStorageInsightsReportConfigFrequencyOptionsEndDate",
    "GoogleStorageInsightsReportConfigFrequencyOptionsEndDateOutputReference",
    "GoogleStorageInsightsReportConfigFrequencyOptionsOutputReference",
    "GoogleStorageInsightsReportConfigFrequencyOptionsStartDate",
    "GoogleStorageInsightsReportConfigFrequencyOptionsStartDateOutputReference",
    "GoogleStorageInsightsReportConfigObjectMetadataReportOptions",
    "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsOutputReference",
    "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions",
    "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptionsOutputReference",
    "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters",
    "GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFiltersOutputReference",
    "GoogleStorageInsightsReportConfigParquetOptions",
    "GoogleStorageInsightsReportConfigParquetOptionsOutputReference",
    "GoogleStorageInsightsReportConfigTimeouts",
    "GoogleStorageInsightsReportConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b36546cf3f0bac8c9505bfe89156687976eaf94c1093017580c80d2473b3089b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    csv_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    frequency_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigFrequencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    object_metadata_report_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigObjectMetadataReportOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    parquet_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigParquetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__05241e2a31b2e680fd64751f74964943427e58af9715ff20c93f4b9e4dcf4345(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb83387f715946e5e969b9eba8108e588f5d489178e98282d5963506ca267976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff4a380d0ba4c59263b4eedd5b7ff0b47e7204bc4956d3adb3012ad7ff21048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca46df2aea8cc824d2d6dd08f781d6711252f89edd36e73f0fced1cfe058b42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b33e8ac3e1450401133be589a69a0a89d5feeeb3c6f75850b8e745d54512fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6380f83e0074381db72b242b2e03eb7e6cee7c6bd4869dedf4ad2a000405e91(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    csv_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    frequency_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigFrequencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    object_metadata_report_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigObjectMetadataReportOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    parquet_options: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigParquetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d22ac4e9c8e04ba0aeb3790afd17acdeabc704644b7b0b571404e0dedafc0c3(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    header_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fe1d2cb0148de4e4b6a0b689ecbbc82ff5d7c54eba23a412d896124d559699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6248bbfee4d2680e3ee0c1b2df7c4573cc5e1c2bb9130cbb1ac9b91472ceab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6847f8e739090753afe34372d792740095033a8756a15a203b0f113ac212b37(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d27638a2e355da2e64c59abf33d15e34902ce59530d85da9444bf55738da403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfc07e7a53272f098726fc8a8cbfae404945abd7ac6b8e07f8dbd5f91fa0386(
    value: typing.Optional[GoogleStorageInsightsReportConfigCsvOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfec99c93e90d6cf7da62caf7dbdaf9b66b8e6f5a5b51ae2324568d6a113f64d(
    *,
    end_date: typing.Union[GoogleStorageInsightsReportConfigFrequencyOptionsEndDate, typing.Dict[builtins.str, typing.Any]],
    frequency: builtins.str,
    start_date: typing.Union[GoogleStorageInsightsReportConfigFrequencyOptionsStartDate, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b4b5ad6c312c0e690e8a8edbb7d22c483d3a5ffb0921eae6ec22f1e02969f8(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5be67fc2b954da2bf6d831964c605765c355e52ebc06a6ff8d4dee5d817552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51afbcf48c189498b5b32959026df35f872c35ce6a682f8862fa33bc8988f1aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972615d6cf50c4654e1ff3f9c8bc4c9297e468df30d3a84f9bd626a7daff4ee5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5e0bbf384cdbeaca9629b0484b4c9ac560b677a7307cd04574c0d80cf3b7ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a9b1ef3833a9035cd8824deaf24d8fd0bd2a4de478a1a738edc6d8fc9e43a3(
    value: typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd38ef0ca1fa549610164fba0b963c854919136c4ab552f8520bb8678fdc323b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1a82e309714a7ce657638892ad690a3abecc11baf573bf8b21cf2bcb24b6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c965aa15c527c5c57d010d95a24916e2981a9bd0c248be26f2826b82f67908af(
    value: typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfdb4d737683ffbab6bc30f84534b22e6874e07631d67c9f57d54f142a69de5(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c798e3206fbbd6e914861074a3bde554c5ba8e0154472cc677ca143bf570c72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7371237db528700ac329281045e7292864bf69b5df7b810fddcaa255e5fc7ee4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a38c0cc22a51cf59de5597aaf1169f2da5d997665fc882d3598553042429514(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a749226f1cf97faee360f0fd06347c989a9c736fa426f6d3db42a9f9509f5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0abdea9d6951e3d45f88719db9761c9aa1596bb9500f735fb969d99e16d1730(
    value: typing.Optional[GoogleStorageInsightsReportConfigFrequencyOptionsStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f142efc21f608290a4f0e2457742c9bfbd2ddec36fbfa7a40f6eff9d0908a727(
    *,
    metadata_fields: typing.Sequence[builtins.str],
    storage_destination_options: typing.Union[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions, typing.Dict[builtins.str, typing.Any]],
    storage_filters: typing.Optional[typing.Union[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d361338576841f495c27103b6a9f4189a01d6c465d8703ac9b3ef9a088e274fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a782e9e730447079006d0d7a5958df606f8248697847238eae773bdaf386a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397aed3a6af595cb00764e52f00d5d5b3ab56aa09f494452200a9897bce041e4(
    value: typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f33f8ee608617316c7e56934898a69fdf2f8c10e50391f54c4a9c97e1115274(
    *,
    bucket: builtins.str,
    destination_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b58d5c27b17dbb58b23a2a9049e6601877ee55f99c5f0da89cbd219b453ff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0ee3794114fb7c8ae1c4058541f8a446e957de0bc932137dd2bc340c99e9bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ff9aba369be953a279ce70321f5c650de763a77800fdf90cc49a6bb99acb56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4eade45fc099fedd329daf6013395eb9a4a514de35691d8e8a802e0a6b347a9(
    value: typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageDestinationOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1160236dc103ab03182e40ce212d4ea31c724292fb9f2aaa2478962ea701d10c(
    *,
    bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ba8f4206ede31aa48648bc6016b896e2c02d2eeb9210684aca051156c88a66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f275f1574bee5f3429d50f20a194b1cea28f9eae1e55978f0c02e62a4f5fa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633a73b5a30469e931b3e012698aff1bbdc242f471746a4dddb84d6301ae49ce(
    value: typing.Optional[GoogleStorageInsightsReportConfigObjectMetadataReportOptionsStorageFilters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8615efb96217502f9a8cb3c5202ad67b3e2205b331cb985fa78abaf609df5714(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6a40ee98ec5d78265909f67cd6ad53f836e3955a29167d460ed0337d8beb38(
    value: typing.Optional[GoogleStorageInsightsReportConfigParquetOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff929c1705d24eac9fdfc59654645aba336eea43f645b418d8d0e07630759a5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e18e4f6556224b54c45904711aa3cd33c47c01e89d6c1816af59de4bbd372ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc9a09797872b28217c0d5b95ec5f7713d45988fd3ce40fef5d871977956c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cb4dc5a9b50320a0bd417a93f4b3d61dc0afcea81838c7e34f2363821470c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7402e294ff65ce210611b3d783b4c275b3be5c152555311aba07478b8cc3db94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1d3dfb4f9a863a20abfc1f55121f80540ff2f5e5773c37224e9483701b4bbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageInsightsReportConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
