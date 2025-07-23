r'''
# `google_dataplex_datascan`

Refer to the Terraform Registry for docs: [`google_dataplex_datascan`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan).
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


class DataplexDatascan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan google_dataplex_datascan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data: typing.Union["DataplexDatascanData", typing.Dict[builtins.str, typing.Any]],
        data_scan_id: builtins.str,
        execution_spec: typing.Union["DataplexDatascanExecutionSpec", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        data_discovery_spec: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        data_profile_spec: typing.Optional[typing.Union["DataplexDatascanDataProfileSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        data_quality_spec: typing.Optional[typing.Union["DataplexDatascanDataQualitySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexDatascanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan google_dataplex_datascan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data: data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data DataplexDatascan#data}
        :param data_scan_id: DataScan identifier. Must contain only lowercase letters, numbers and hyphens. Must start with a letter. Must end with a number or a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_scan_id DataplexDatascan#data_scan_id}
        :param execution_spec: execution_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#execution_spec DataplexDatascan#execution_spec}
        :param location: The location where the data scan should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#location DataplexDatascan#location}
        :param data_discovery_spec: data_discovery_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_discovery_spec DataplexDatascan#data_discovery_spec}
        :param data_profile_spec: data_profile_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_profile_spec DataplexDatascan#data_profile_spec}
        :param data_quality_spec: data_quality_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_quality_spec DataplexDatascan#data_quality_spec}
        :param description: Description of the scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#description DataplexDatascan#description}
        :param display_name: User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#display_name DataplexDatascan#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#id DataplexDatascan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the scan. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#labels DataplexDatascan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#project DataplexDatascan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#timeouts DataplexDatascan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d978d3a14103b3ef12c1f35fc9a0641f3a0e983ba57bcdb6a7dd8fa7392d37)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataplexDatascanConfig(
            data=data,
            data_scan_id=data_scan_id,
            execution_spec=execution_spec,
            location=location,
            data_discovery_spec=data_discovery_spec,
            data_profile_spec=data_profile_spec,
            data_quality_spec=data_quality_spec,
            description=description,
            display_name=display_name,
            id=id,
            labels=labels,
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
        '''Generates CDKTF code for importing a DataplexDatascan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataplexDatascan to import.
        :param import_from_id: The id of the existing DataplexDatascan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataplexDatascan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79426be3928dab88c96febb41f5a5cf41f97167357d7fd4c1ff34fc7df5d0c90)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putData")
    def put_data(
        self,
        *,
        entity: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity: The Dataplex entity that represents the data source(e.g. BigQuery table) for Datascan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#entity DataplexDatascan#entity}
        :param resource: The service-qualified full resource name of the cloud resource for a DataScan job to scan against. The field could be: Cloud Storage bucket (//storage.googleapis.com/projects/PROJECT_ID/buckets/BUCKET_ID) for DataDiscoveryScan OR BigQuery table of type "TABLE" (/bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID) for DataProfileScan/DataQualityScan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#resource DataplexDatascan#resource}
        '''
        value = DataplexDatascanData(entity=entity, resource=resource)

        return typing.cast(None, jsii.invoke(self, "putData", [value]))

    @jsii.member(jsii_name="putDataDiscoverySpec")
    def put_data_discovery_spec(
        self,
        *,
        bigquery_publishing_config: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_config: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bigquery_publishing_config: bigquery_publishing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_publishing_config DataplexDatascan#bigquery_publishing_config}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#storage_config DataplexDatascan#storage_config}
        '''
        value = DataplexDatascanDataDiscoverySpec(
            bigquery_publishing_config=bigquery_publishing_config,
            storage_config=storage_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDataDiscoverySpec", [value]))

    @jsii.member(jsii_name="putDataProfileSpec")
    def put_data_profile_spec(
        self,
        *,
        exclude_fields: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecExcludeFields", typing.Dict[builtins.str, typing.Any]]] = None,
        include_fields: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecIncludeFields", typing.Dict[builtins.str, typing.Any]]] = None,
        post_scan_actions: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecPostScanActions", typing.Dict[builtins.str, typing.Any]]] = None,
        row_filter: typing.Optional[builtins.str] = None,
        sampling_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exclude_fields: exclude_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#exclude_fields DataplexDatascan#exclude_fields}
        :param include_fields: include_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#include_fields DataplexDatascan#include_fields}
        :param post_scan_actions: post_scan_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#post_scan_actions DataplexDatascan#post_scan_actions}
        :param row_filter: A filter applied to all rows in a single DataScan job. The filter needs to be a valid SQL expression for a WHERE clause in BigQuery standard SQL syntax. Example: col1 >= 0 AND col2 < 10 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_filter DataplexDatascan#row_filter}
        :param sampling_percent: The percentage of the records to be selected from the dataset for DataScan. Value can range between 0.0 and 100.0 with up to 3 significant decimal digits. Sampling is not applied if 'sampling_percent' is not specified, 0 or 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sampling_percent DataplexDatascan#sampling_percent}
        '''
        value = DataplexDatascanDataProfileSpec(
            exclude_fields=exclude_fields,
            include_fields=include_fields,
            post_scan_actions=post_scan_actions,
            row_filter=row_filter,
            sampling_percent=sampling_percent,
        )

        return typing.cast(None, jsii.invoke(self, "putDataProfileSpec", [value]))

    @jsii.member(jsii_name="putDataQualitySpec")
    def put_data_quality_spec(
        self,
        *,
        catalog_publishing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_scan_actions: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActions", typing.Dict[builtins.str, typing.Any]]] = None,
        row_filter: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataplexDatascanDataQualitySpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sampling_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param catalog_publishing_enabled: If set, the latest DataScan job result will be published to Dataplex Catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#catalog_publishing_enabled DataplexDatascan#catalog_publishing_enabled}
        :param post_scan_actions: post_scan_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#post_scan_actions DataplexDatascan#post_scan_actions}
        :param row_filter: A filter applied to all rows in a single DataScan job. The filter needs to be a valid SQL expression for a WHERE clause in BigQuery standard SQL syntax. Example: col1 >= 0 AND col2 < 10 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_filter DataplexDatascan#row_filter}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#rules DataplexDatascan#rules}
        :param sampling_percent: The percentage of the records to be selected from the dataset for DataScan. Value can range between 0.0 and 100.0 with up to 3 significant decimal digits. Sampling is not applied if 'sampling_percent' is not specified, 0 or 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sampling_percent DataplexDatascan#sampling_percent}
        '''
        value = DataplexDatascanDataQualitySpec(
            catalog_publishing_enabled=catalog_publishing_enabled,
            post_scan_actions=post_scan_actions,
            row_filter=row_filter,
            rules=rules,
            sampling_percent=sampling_percent,
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualitySpec", [value]))

    @jsii.member(jsii_name="putExecutionSpec")
    def put_execution_spec(
        self,
        *,
        trigger: typing.Union["DataplexDatascanExecutionSpecTrigger", typing.Dict[builtins.str, typing.Any]],
        field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#trigger DataplexDatascan#trigger}
        :param field: The unnested field (of type Date or Timestamp) that contains values which monotonically increase over time. If not specified, a data scan will run for all data in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field DataplexDatascan#field}
        '''
        value = DataplexDatascanExecutionSpec(trigger=trigger, field=field)

        return typing.cast(None, jsii.invoke(self, "putExecutionSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#create DataplexDatascan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#delete DataplexDatascan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#update DataplexDatascan#update}.
        '''
        value = DataplexDatascanTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataDiscoverySpec")
    def reset_data_discovery_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiscoverySpec", []))

    @jsii.member(jsii_name="resetDataProfileSpec")
    def reset_data_profile_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProfileSpec", []))

    @jsii.member(jsii_name="resetDataQualitySpec")
    def reset_data_quality_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataQualitySpec", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> "DataplexDatascanDataOutputReference":
        return typing.cast("DataplexDatascanDataOutputReference", jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="dataDiscoverySpec")
    def data_discovery_spec(self) -> "DataplexDatascanDataDiscoverySpecOutputReference":
        return typing.cast("DataplexDatascanDataDiscoverySpecOutputReference", jsii.get(self, "dataDiscoverySpec"))

    @builtins.property
    @jsii.member(jsii_name="dataProfileSpec")
    def data_profile_spec(self) -> "DataplexDatascanDataProfileSpecOutputReference":
        return typing.cast("DataplexDatascanDataProfileSpecOutputReference", jsii.get(self, "dataProfileSpec"))

    @builtins.property
    @jsii.member(jsii_name="dataQualitySpec")
    def data_quality_spec(self) -> "DataplexDatascanDataQualitySpecOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecOutputReference", jsii.get(self, "dataQualitySpec"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="executionSpec")
    def execution_spec(self) -> "DataplexDatascanExecutionSpecOutputReference":
        return typing.cast("DataplexDatascanExecutionSpecOutputReference", jsii.get(self, "executionSpec"))

    @builtins.property
    @jsii.member(jsii_name="executionStatus")
    def execution_status(self) -> "DataplexDatascanExecutionStatusList":
        return typing.cast("DataplexDatascanExecutionStatusList", jsii.get(self, "executionStatus"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataplexDatascanTimeoutsOutputReference":
        return typing.cast("DataplexDatascanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="dataDiscoverySpecInput")
    def data_discovery_spec_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataDiscoverySpec"]:
        return typing.cast(typing.Optional["DataplexDatascanDataDiscoverySpec"], jsii.get(self, "dataDiscoverySpecInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional["DataplexDatascanData"]:
        return typing.cast(typing.Optional["DataplexDatascanData"], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProfileSpecInput")
    def data_profile_spec_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataProfileSpec"]:
        return typing.cast(typing.Optional["DataplexDatascanDataProfileSpec"], jsii.get(self, "dataProfileSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualitySpecInput")
    def data_quality_spec_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpec"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpec"], jsii.get(self, "dataQualitySpecInput"))

    @builtins.property
    @jsii.member(jsii_name="dataScanIdInput")
    def data_scan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataScanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionSpecInput")
    def execution_spec_input(self) -> typing.Optional["DataplexDatascanExecutionSpec"]:
        return typing.cast(typing.Optional["DataplexDatascanExecutionSpec"], jsii.get(self, "executionSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexDatascanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexDatascanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataScanId")
    def data_scan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataScanId"))

    @data_scan_id.setter
    def data_scan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e599fb759e13751ed4e9d77184f41e10d6c3e05dc3490fedfd53a40515ed90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataScanId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9177039bf399af0070309fe327788cbf0f4a3ba85ca45b30ca264e3821ebe69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7acddc10756adbd43ebd70f29476a8202acf88a6d91e235c4ceb847ca2e99d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01402634ddabb6c346b4cb2c18c6624021a009b09431401735ca8c1d779f9d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f3d64f33812a62d780f892003e5f8802daa4860abf27562a4a358eb53e212c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8453c5d69cbc241fd463cde478b1c8b4320b9f09468b4be2f475d7f47adcc2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6e3f10a1999fb9aa8f39e401feeeb6b48be2e9b7d28ede14ab07b3a7571f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data": "data",
        "data_scan_id": "dataScanId",
        "execution_spec": "executionSpec",
        "location": "location",
        "data_discovery_spec": "dataDiscoverySpec",
        "data_profile_spec": "dataProfileSpec",
        "data_quality_spec": "dataQualitySpec",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DataplexDatascanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data: typing.Union["DataplexDatascanData", typing.Dict[builtins.str, typing.Any]],
        data_scan_id: builtins.str,
        execution_spec: typing.Union["DataplexDatascanExecutionSpec", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        data_discovery_spec: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        data_profile_spec: typing.Optional[typing.Union["DataplexDatascanDataProfileSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        data_quality_spec: typing.Optional[typing.Union["DataplexDatascanDataQualitySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexDatascanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data: data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data DataplexDatascan#data}
        :param data_scan_id: DataScan identifier. Must contain only lowercase letters, numbers and hyphens. Must start with a letter. Must end with a number or a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_scan_id DataplexDatascan#data_scan_id}
        :param execution_spec: execution_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#execution_spec DataplexDatascan#execution_spec}
        :param location: The location where the data scan should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#location DataplexDatascan#location}
        :param data_discovery_spec: data_discovery_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_discovery_spec DataplexDatascan#data_discovery_spec}
        :param data_profile_spec: data_profile_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_profile_spec DataplexDatascan#data_profile_spec}
        :param data_quality_spec: data_quality_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_quality_spec DataplexDatascan#data_quality_spec}
        :param description: Description of the scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#description DataplexDatascan#description}
        :param display_name: User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#display_name DataplexDatascan#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#id DataplexDatascan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the scan. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#labels DataplexDatascan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#project DataplexDatascan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#timeouts DataplexDatascan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data, dict):
            data = DataplexDatascanData(**data)
        if isinstance(execution_spec, dict):
            execution_spec = DataplexDatascanExecutionSpec(**execution_spec)
        if isinstance(data_discovery_spec, dict):
            data_discovery_spec = DataplexDatascanDataDiscoverySpec(**data_discovery_spec)
        if isinstance(data_profile_spec, dict):
            data_profile_spec = DataplexDatascanDataProfileSpec(**data_profile_spec)
        if isinstance(data_quality_spec, dict):
            data_quality_spec = DataplexDatascanDataQualitySpec(**data_quality_spec)
        if isinstance(timeouts, dict):
            timeouts = DataplexDatascanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59b584f3c2ab4707c1e0552da13804a76b02aef972499ba94c6adac30ad061a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument data_scan_id", value=data_scan_id, expected_type=type_hints["data_scan_id"])
            check_type(argname="argument execution_spec", value=execution_spec, expected_type=type_hints["execution_spec"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument data_discovery_spec", value=data_discovery_spec, expected_type=type_hints["data_discovery_spec"])
            check_type(argname="argument data_profile_spec", value=data_profile_spec, expected_type=type_hints["data_profile_spec"])
            check_type(argname="argument data_quality_spec", value=data_quality_spec, expected_type=type_hints["data_quality_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "data_scan_id": data_scan_id,
            "execution_spec": execution_spec,
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
        if data_discovery_spec is not None:
            self._values["data_discovery_spec"] = data_discovery_spec
        if data_profile_spec is not None:
            self._values["data_profile_spec"] = data_profile_spec
        if data_quality_spec is not None:
            self._values["data_quality_spec"] = data_quality_spec
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
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
    def data(self) -> "DataplexDatascanData":
        '''data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data DataplexDatascan#data}
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast("DataplexDatascanData", result)

    @builtins.property
    def data_scan_id(self) -> builtins.str:
        '''DataScan identifier.

        Must contain only lowercase letters, numbers and hyphens. Must start with a letter. Must end with a number or a letter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_scan_id DataplexDatascan#data_scan_id}
        '''
        result = self._values.get("data_scan_id")
        assert result is not None, "Required property 'data_scan_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_spec(self) -> "DataplexDatascanExecutionSpec":
        '''execution_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#execution_spec DataplexDatascan#execution_spec}
        '''
        result = self._values.get("execution_spec")
        assert result is not None, "Required property 'execution_spec' is missing"
        return typing.cast("DataplexDatascanExecutionSpec", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location where the data scan should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#location DataplexDatascan#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_discovery_spec(
        self,
    ) -> typing.Optional["DataplexDatascanDataDiscoverySpec"]:
        '''data_discovery_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_discovery_spec DataplexDatascan#data_discovery_spec}
        '''
        result = self._values.get("data_discovery_spec")
        return typing.cast(typing.Optional["DataplexDatascanDataDiscoverySpec"], result)

    @builtins.property
    def data_profile_spec(self) -> typing.Optional["DataplexDatascanDataProfileSpec"]:
        '''data_profile_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_profile_spec DataplexDatascan#data_profile_spec}
        '''
        result = self._values.get("data_profile_spec")
        return typing.cast(typing.Optional["DataplexDatascanDataProfileSpec"], result)

    @builtins.property
    def data_quality_spec(self) -> typing.Optional["DataplexDatascanDataQualitySpec"]:
        '''data_quality_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#data_quality_spec DataplexDatascan#data_quality_spec}
        '''
        result = self._values.get("data_quality_spec")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpec"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#description DataplexDatascan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User friendly display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#display_name DataplexDatascan#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#id DataplexDatascan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the scan. A list of key->value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#labels DataplexDatascan#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#project DataplexDatascan#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataplexDatascanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#timeouts DataplexDatascan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataplexDatascanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanData",
    jsii_struct_bases=[],
    name_mapping={"entity": "entity", "resource": "resource"},
)
class DataplexDatascanData:
    def __init__(
        self,
        *,
        entity: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity: The Dataplex entity that represents the data source(e.g. BigQuery table) for Datascan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#entity DataplexDatascan#entity}
        :param resource: The service-qualified full resource name of the cloud resource for a DataScan job to scan against. The field could be: Cloud Storage bucket (//storage.googleapis.com/projects/PROJECT_ID/buckets/BUCKET_ID) for DataDiscoveryScan OR BigQuery table of type "TABLE" (/bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID) for DataProfileScan/DataQualityScan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#resource DataplexDatascan#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887b51eb9dc74c5797b8b0d833c1f65c3c1c65e4e91004ea510fa663bde76d5d)
            check_type(argname="argument entity", value=entity, expected_type=type_hints["entity"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entity is not None:
            self._values["entity"] = entity
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def entity(self) -> typing.Optional[builtins.str]:
        '''The Dataplex entity that represents the data source(e.g. BigQuery table) for Datascan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#entity DataplexDatascan#entity}
        '''
        result = self._values.get("entity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''The service-qualified full resource name of the cloud resource for a DataScan job to scan against.

        The field could be:
        Cloud Storage bucket (//storage.googleapis.com/projects/PROJECT_ID/buckets/BUCKET_ID) for DataDiscoveryScan OR BigQuery table of type "TABLE" (/bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID) for DataProfileScan/DataQualityScan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#resource DataplexDatascan#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpec",
    jsii_struct_bases=[],
    name_mapping={
        "bigquery_publishing_config": "bigqueryPublishingConfig",
        "storage_config": "storageConfig",
    },
)
class DataplexDatascanDataDiscoverySpec:
    def __init__(
        self,
        *,
        bigquery_publishing_config: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_config: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bigquery_publishing_config: bigquery_publishing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_publishing_config DataplexDatascan#bigquery_publishing_config}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#storage_config DataplexDatascan#storage_config}
        '''
        if isinstance(bigquery_publishing_config, dict):
            bigquery_publishing_config = DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig(**bigquery_publishing_config)
        if isinstance(storage_config, dict):
            storage_config = DataplexDatascanDataDiscoverySpecStorageConfig(**storage_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a941c0030179ccbc60700b68120ec74c77aab2dfa6e4864727b01225fb639c15)
            check_type(argname="argument bigquery_publishing_config", value=bigquery_publishing_config, expected_type=type_hints["bigquery_publishing_config"])
            check_type(argname="argument storage_config", value=storage_config, expected_type=type_hints["storage_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bigquery_publishing_config is not None:
            self._values["bigquery_publishing_config"] = bigquery_publishing_config
        if storage_config is not None:
            self._values["storage_config"] = storage_config

    @builtins.property
    def bigquery_publishing_config(
        self,
    ) -> typing.Optional["DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig"]:
        '''bigquery_publishing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_publishing_config DataplexDatascan#bigquery_publishing_config}
        '''
        result = self._values.get("bigquery_publishing_config")
        return typing.cast(typing.Optional["DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig"], result)

    @builtins.property
    def storage_config(
        self,
    ) -> typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfig"]:
        '''storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#storage_config DataplexDatascan#storage_config}
        '''
        result = self._values.get("storage_config")
        return typing.cast(typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataDiscoverySpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connection": "connection",
        "location": "location",
        "project": "project",
        "table_type": "tableType",
    },
)
class DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig:
    def __init__(
        self,
        *,
        connection: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        table_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: The BigQuery connection used to create BigLake tables. Must be in the form 'projects/{projectId}/locations/{locationId}/connections/{connection_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#connection DataplexDatascan#connection}
        :param location: The location of the BigQuery dataset to publish BigLake external or non-BigLake external tables to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#location DataplexDatascan#location}
        :param project: The project of the BigQuery dataset to publish BigLake external or non-BigLake external tables to. If not specified, the project of the Cloud Storage bucket will be used. The format is "projects/{project_id_or_number}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#project DataplexDatascan#project}
        :param table_type: Determines whether to publish discovered tables as BigLake external tables or non-BigLake external tables. Possible values: ["TABLE_TYPE_UNSPECIFIED", "EXTERNAL", "BIGLAKE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#table_type DataplexDatascan#table_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536b9cfd09a6268ad88ae10e29aaf044d866cd2e80160e1588a8bb1ab33e728f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument table_type", value=table_type, expected_type=type_hints["table_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if table_type is not None:
            self._values["table_type"] = table_type

    @builtins.property
    def connection(self) -> typing.Optional[builtins.str]:
        '''The BigQuery connection used to create BigLake tables. Must be in the form 'projects/{projectId}/locations/{locationId}/connections/{connection_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#connection DataplexDatascan#connection}
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location of the BigQuery dataset to publish BigLake external or non-BigLake external tables to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#location DataplexDatascan#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project of the BigQuery dataset to publish BigLake external or non-BigLake external tables to.

        If not specified, the project of the Cloud Storage bucket will be used. The format is "projects/{project_id_or_number}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#project DataplexDatascan#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_type(self) -> typing.Optional[builtins.str]:
        '''Determines whether to publish discovered tables as BigLake external tables or non-BigLake external tables. Possible values: ["TABLE_TYPE_UNSPECIFIED", "EXTERNAL", "BIGLAKE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#table_type DataplexDatascan#table_type}
        '''
        result = self._values.get("table_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataDiscoverySpecBigqueryPublishingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecBigqueryPublishingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__803774bfad0a4bc28839bbd88c07261e9e19a6069bc88286c8a0f3c923090d49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnection")
    def reset_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnection", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTableType")
    def reset_table_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableType", []))

    @builtins.property
    @jsii.member(jsii_name="connectionInput")
    def connection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="tableTypeInput")
    def table_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connection"))

    @connection.setter
    def connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d773a76393b1e670bb8dba04fe66b8d269935ebde00da0f8823ddca69475f30b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3e0c2e32ce9f6a72f0a5d103157e9af243f4a66edb22484abcf0f23f665982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53fe3ad89fb88260be8b7cbc2d5d13cb3e80f9d2835d84ee1de8965e545d73b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableType")
    def table_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableType"))

    @table_type.setter
    def table_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249ae6b737fbf6f8346ba709f7e2ef1c5cf2c0b4714bcabeef397a3cdea83853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8a617005d9dcff9f732e58114a23820e6d0b7f3018077e846f8b9503d563b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataDiscoverySpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a4f845937cc2789fe26b104a37067ac447c2bd83113daf3f2badf5ea4944bf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigqueryPublishingConfig")
    def put_bigquery_publishing_config(
        self,
        *,
        connection: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        table_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: The BigQuery connection used to create BigLake tables. Must be in the form 'projects/{projectId}/locations/{locationId}/connections/{connection_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#connection DataplexDatascan#connection}
        :param location: The location of the BigQuery dataset to publish BigLake external or non-BigLake external tables to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#location DataplexDatascan#location}
        :param project: The project of the BigQuery dataset to publish BigLake external or non-BigLake external tables to. If not specified, the project of the Cloud Storage bucket will be used. The format is "projects/{project_id_or_number}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#project DataplexDatascan#project}
        :param table_type: Determines whether to publish discovered tables as BigLake external tables or non-BigLake external tables. Possible values: ["TABLE_TYPE_UNSPECIFIED", "EXTERNAL", "BIGLAKE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#table_type DataplexDatascan#table_type}
        '''
        value = DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig(
            connection=connection,
            location=location,
            project=project,
            table_type=table_type,
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryPublishingConfig", [value]))

    @jsii.member(jsii_name="putStorageConfig")
    def put_storage_config(
        self,
        *,
        csv_options: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_options: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#csv_options DataplexDatascan#csv_options}
        :param exclude_patterns: Defines the data to exclude during discovery. Provide a list of patterns that identify the data to exclude. For Cloud Storage bucket assets, these patterns are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these patterns are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#exclude_patterns DataplexDatascan#exclude_patterns}
        :param include_patterns: Defines the data to include during discovery when only a subset of the data should be considered. Provide a list of patterns that identify the data to include. For Cloud Storage bucket assets, these patterns are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these patterns are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#include_patterns DataplexDatascan#include_patterns}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#json_options DataplexDatascan#json_options}
        '''
        value = DataplexDatascanDataDiscoverySpecStorageConfig(
            csv_options=csv_options,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
            json_options=json_options,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageConfig", [value]))

    @jsii.member(jsii_name="resetBigqueryPublishingConfig")
    def reset_bigquery_publishing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryPublishingConfig", []))

    @jsii.member(jsii_name="resetStorageConfig")
    def reset_storage_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageConfig", []))

    @builtins.property
    @jsii.member(jsii_name="bigqueryPublishingConfig")
    def bigquery_publishing_config(
        self,
    ) -> DataplexDatascanDataDiscoverySpecBigqueryPublishingConfigOutputReference:
        return typing.cast(DataplexDatascanDataDiscoverySpecBigqueryPublishingConfigOutputReference, jsii.get(self, "bigqueryPublishingConfig"))

    @builtins.property
    @jsii.member(jsii_name="storageConfig")
    def storage_config(
        self,
    ) -> "DataplexDatascanDataDiscoverySpecStorageConfigOutputReference":
        return typing.cast("DataplexDatascanDataDiscoverySpecStorageConfigOutputReference", jsii.get(self, "storageConfig"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryPublishingConfigInput")
    def bigquery_publishing_config_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig], jsii.get(self, "bigqueryPublishingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConfigInput")
    def storage_config_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfig"]:
        return typing.cast(typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfig"], jsii.get(self, "storageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexDatascanDataDiscoverySpec]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataDiscoverySpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6972dc10e679f84106050b855fc71fe1e37d799bcf8ecf4f1838cb0c8f4248e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecStorageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "csv_options": "csvOptions",
        "exclude_patterns": "excludePatterns",
        "include_patterns": "includePatterns",
        "json_options": "jsonOptions",
    },
)
class DataplexDatascanDataDiscoverySpecStorageConfig:
    def __init__(
        self,
        *,
        csv_options: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_options: typing.Optional[typing.Union["DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#csv_options DataplexDatascan#csv_options}
        :param exclude_patterns: Defines the data to exclude during discovery. Provide a list of patterns that identify the data to exclude. For Cloud Storage bucket assets, these patterns are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these patterns are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#exclude_patterns DataplexDatascan#exclude_patterns}
        :param include_patterns: Defines the data to include during discovery when only a subset of the data should be considered. Provide a list of patterns that identify the data to include. For Cloud Storage bucket assets, these patterns are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these patterns are interpreted as patterns to match table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#include_patterns DataplexDatascan#include_patterns}
        :param json_options: json_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#json_options DataplexDatascan#json_options}
        '''
        if isinstance(csv_options, dict):
            csv_options = DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions(**csv_options)
        if isinstance(json_options, dict):
            json_options = DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions(**json_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0fdc670747f0bc0893fbf643e659bf559fd9c0237b856286b0d90e7da25aae)
            check_type(argname="argument csv_options", value=csv_options, expected_type=type_hints["csv_options"])
            check_type(argname="argument exclude_patterns", value=exclude_patterns, expected_type=type_hints["exclude_patterns"])
            check_type(argname="argument include_patterns", value=include_patterns, expected_type=type_hints["include_patterns"])
            check_type(argname="argument json_options", value=json_options, expected_type=type_hints["json_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv_options is not None:
            self._values["csv_options"] = csv_options
        if exclude_patterns is not None:
            self._values["exclude_patterns"] = exclude_patterns
        if include_patterns is not None:
            self._values["include_patterns"] = include_patterns
        if json_options is not None:
            self._values["json_options"] = json_options

    @builtins.property
    def csv_options(
        self,
    ) -> typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions"]:
        '''csv_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#csv_options DataplexDatascan#csv_options}
        '''
        result = self._values.get("csv_options")
        return typing.cast(typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions"], result)

    @builtins.property
    def exclude_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Defines the data to exclude during discovery.

        Provide a list of patterns that identify the data to exclude. For Cloud Storage bucket assets, these patterns are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these patterns are interpreted as patterns to match table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#exclude_patterns DataplexDatascan#exclude_patterns}
        '''
        result = self._values.get("exclude_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Defines the data to include during discovery when only a subset of the data should be considered.

        Provide a list of patterns that identify the data to include. For Cloud Storage bucket assets, these patterns are interpreted as glob patterns used to match object names. For BigQuery dataset assets, these patterns are interpreted as patterns to match table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#include_patterns DataplexDatascan#include_patterns}
        '''
        result = self._values.get("include_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def json_options(
        self,
    ) -> typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions"]:
        '''json_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#json_options DataplexDatascan#json_options}
        '''
        result = self._values.get("json_options")
        return typing.cast(typing.Optional["DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataDiscoverySpecStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delimiter": "delimiter",
        "encoding": "encoding",
        "header_rows": "headerRows",
        "quote": "quote",
        "type_inference_disabled": "typeInferenceDisabled",
    },
)
class DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[builtins.str] = None,
        header_rows: typing.Optional[jsii.Number] = None,
        quote: typing.Optional[builtins.str] = None,
        type_inference_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param delimiter: The delimiter that is used to separate values. The default is ',' (comma). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#delimiter DataplexDatascan#delimiter}
        :param encoding: The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#encoding DataplexDatascan#encoding}
        :param header_rows: The number of rows to interpret as header rows that should be skipped when reading data rows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#header_rows DataplexDatascan#header_rows}
        :param quote: The character used to quote column values. Accepts '"' (double quotation mark) or ``` (single quotation mark). If unspecified, defaults to '"' (double quotation mark). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#quote DataplexDatascan#quote}
        :param type_inference_disabled: Whether to disable the inference of data types for CSV data. If true, all columns are registered as strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#type_inference_disabled DataplexDatascan#type_inference_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2718cb44b7122d0b4191c453c2cfc2d7f47e1d4f1eb2472307e703cee78c79)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument header_rows", value=header_rows, expected_type=type_hints["header_rows"])
            check_type(argname="argument quote", value=quote, expected_type=type_hints["quote"])
            check_type(argname="argument type_inference_disabled", value=type_inference_disabled, expected_type=type_hints["type_inference_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if encoding is not None:
            self._values["encoding"] = encoding
        if header_rows is not None:
            self._values["header_rows"] = header_rows
        if quote is not None:
            self._values["quote"] = quote
        if type_inference_disabled is not None:
            self._values["type_inference_disabled"] = type_inference_disabled

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''The delimiter that is used to separate values. The default is ',' (comma).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#delimiter DataplexDatascan#delimiter}
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The character encoding of the data. The default is UTF-8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#encoding DataplexDatascan#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_rows(self) -> typing.Optional[jsii.Number]:
        '''The number of rows to interpret as header rows that should be skipped when reading data rows.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#header_rows DataplexDatascan#header_rows}
        '''
        result = self._values.get("header_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quote(self) -> typing.Optional[builtins.str]:
        '''The character used to quote column values.

        Accepts '"' (double quotation mark) or ``` (single quotation mark). If unspecified, defaults to '"' (double quotation mark).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#quote DataplexDatascan#quote}
        '''
        result = self._values.get("quote")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_inference_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable the inference of data types for CSV data. If true, all columns are registered as strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#type_inference_disabled DataplexDatascan#type_inference_disabled}
        '''
        result = self._values.get("type_inference_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataDiscoverySpecStorageConfigCsvOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecStorageConfigCsvOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb023934ba7711d76022197021c85d06614b5da3bcc2d7c34b699d7656586fae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetHeaderRows")
    def reset_header_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderRows", []))

    @jsii.member(jsii_name="resetQuote")
    def reset_quote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuote", []))

    @jsii.member(jsii_name="resetTypeInferenceDisabled")
    def reset_type_inference_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeInferenceDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="headerRowsInput")
    def header_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "headerRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteInput")
    def quote_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInferenceDisabledInput")
    def type_inference_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "typeInferenceDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3885bab5067f5700c9639dc06f15fd582f7049784ff53b4a98639f34a53de5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5fe1cf9734c37af90c6c172860c19940d636bbbcfafb30a964432ff9d76071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerRows")
    def header_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "headerRows"))

    @header_rows.setter
    def header_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67424a1680eedabc8bdaa6bc2abef4e1807166e1f837124cc4b7c23ab33941f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quote")
    def quote(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quote"))

    @quote.setter
    def quote(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c26ff7b2b1ddaaccfdc1b5fb5b750dd06e39e40ef9474cf341f1e6d047df449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="typeInferenceDisabled")
    def type_inference_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "typeInferenceDisabled"))

    @type_inference_disabled.setter
    def type_inference_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965d24242984ce0a96e27587751a1a12d918d9f00061075b126cf78e37c96f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeInferenceDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc029051bed29523ac2fbc611f63560483f7a1b4087450cf9a1fe7676a4af042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions",
    jsii_struct_bases=[],
    name_mapping={
        "encoding": "encoding",
        "type_inference_disabled": "typeInferenceDisabled",
    },
)
class DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions:
    def __init__(
        self,
        *,
        encoding: typing.Optional[builtins.str] = None,
        type_inference_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param encoding: The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#encoding DataplexDatascan#encoding}
        :param type_inference_disabled: Whether to disable the inference of data types for JSON data. If true, all columns are registered as their primitive types (strings, number, or boolean). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#type_inference_disabled DataplexDatascan#type_inference_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6d83a25a17a2a2bc50d5c5aa6696013f9f6c2cb474e72eec88c4be20f75ee9)
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument type_inference_disabled", value=type_inference_disabled, expected_type=type_hints["type_inference_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encoding is not None:
            self._values["encoding"] = encoding
        if type_inference_disabled is not None:
            self._values["type_inference_disabled"] = type_inference_disabled

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The character encoding of the data. The default is UTF-8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#encoding DataplexDatascan#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_inference_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable the inference of data types for JSON data.

        If true, all columns are registered as their primitive types (strings, number, or boolean).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#type_inference_disabled DataplexDatascan#type_inference_disabled}
        '''
        result = self._values.get("type_inference_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataDiscoverySpecStorageConfigJsonOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecStorageConfigJsonOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4452c32dcc21475c8eb94d5fcfc78e65571cfbb8a129e82012e8786bc556d13d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetTypeInferenceDisabled")
    def reset_type_inference_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeInferenceDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInferenceDisabledInput")
    def type_inference_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "typeInferenceDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40abab90cd182f29c5912232d099a40a2586a36952f2e83a474b3c6bc4bc356f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="typeInferenceDisabled")
    def type_inference_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "typeInferenceDisabled"))

    @type_inference_disabled.setter
    def type_inference_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7427aac116f15901bd921c62a5cfaa0c07ddbdaee89564a4433d35307829a037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeInferenceDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66020970399977943c6fb8ec63da0db1978a7397886da70a1de153fb622a4764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataDiscoverySpecStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataDiscoverySpecStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91418feb6e952ba20e3661b3ba2b497372e4bb56bec2f237ccfd25e1611ebd56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsvOptions")
    def put_csv_options(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[builtins.str] = None,
        header_rows: typing.Optional[jsii.Number] = None,
        quote: typing.Optional[builtins.str] = None,
        type_inference_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param delimiter: The delimiter that is used to separate values. The default is ',' (comma). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#delimiter DataplexDatascan#delimiter}
        :param encoding: The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#encoding DataplexDatascan#encoding}
        :param header_rows: The number of rows to interpret as header rows that should be skipped when reading data rows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#header_rows DataplexDatascan#header_rows}
        :param quote: The character used to quote column values. Accepts '"' (double quotation mark) or ``` (single quotation mark). If unspecified, defaults to '"' (double quotation mark). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#quote DataplexDatascan#quote}
        :param type_inference_disabled: Whether to disable the inference of data types for CSV data. If true, all columns are registered as strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#type_inference_disabled DataplexDatascan#type_inference_disabled}
        '''
        value = DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions(
            delimiter=delimiter,
            encoding=encoding,
            header_rows=header_rows,
            quote=quote,
            type_inference_disabled=type_inference_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvOptions", [value]))

    @jsii.member(jsii_name="putJsonOptions")
    def put_json_options(
        self,
        *,
        encoding: typing.Optional[builtins.str] = None,
        type_inference_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param encoding: The character encoding of the data. The default is UTF-8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#encoding DataplexDatascan#encoding}
        :param type_inference_disabled: Whether to disable the inference of data types for JSON data. If true, all columns are registered as their primitive types (strings, number, or boolean). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#type_inference_disabled DataplexDatascan#type_inference_disabled}
        '''
        value = DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions(
            encoding=encoding, type_inference_disabled=type_inference_disabled
        )

        return typing.cast(None, jsii.invoke(self, "putJsonOptions", [value]))

    @jsii.member(jsii_name="resetCsvOptions")
    def reset_csv_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvOptions", []))

    @jsii.member(jsii_name="resetExcludePatterns")
    def reset_exclude_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludePatterns", []))

    @jsii.member(jsii_name="resetIncludePatterns")
    def reset_include_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePatterns", []))

    @jsii.member(jsii_name="resetJsonOptions")
    def reset_json_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonOptions", []))

    @builtins.property
    @jsii.member(jsii_name="csvOptions")
    def csv_options(
        self,
    ) -> DataplexDatascanDataDiscoverySpecStorageConfigCsvOptionsOutputReference:
        return typing.cast(DataplexDatascanDataDiscoverySpecStorageConfigCsvOptionsOutputReference, jsii.get(self, "csvOptions"))

    @builtins.property
    @jsii.member(jsii_name="jsonOptions")
    def json_options(
        self,
    ) -> DataplexDatascanDataDiscoverySpecStorageConfigJsonOptionsOutputReference:
        return typing.cast(DataplexDatascanDataDiscoverySpecStorageConfigJsonOptionsOutputReference, jsii.get(self, "jsonOptions"))

    @builtins.property
    @jsii.member(jsii_name="csvOptionsInput")
    def csv_options_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions], jsii.get(self, "csvOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludePatternsInput")
    def exclude_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludePatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="includePatternsInput")
    def include_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includePatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonOptionsInput")
    def json_options_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions], jsii.get(self, "jsonOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludePatterns")
    def exclude_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludePatterns"))

    @exclude_patterns.setter
    def exclude_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b582a869c6693ed5d8c5f5747594bfc0b4503f2e653c8cd95e0beacede91aacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePatterns")
    def include_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includePatterns"))

    @include_patterns.setter
    def include_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7019cd9b411c1c00ec2baa5471e65abb57db72b0aacbbb0de0abc7b904f1fac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfig]:
        return typing.cast(typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20e9f97ba110b68631183bf473ed0fc78d0a808269d4b356eb0474adfa3f319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d07a3087d95dce1b616a931956230cfd53d601f3db40f9da601a820db8924c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEntity")
    def reset_entity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntity", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="entityInput")
    def entity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="entity")
    def entity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entity"))

    @entity.setter
    def entity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8b1ee53c0d22ea8df64f3ec598e967dc156a10fed885a0f729cf7f651bdf06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d02c9fc495878cbebd90c932cc5aeefd43e50d9834c4799b71ac8a184cf05d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexDatascanData]:
        return typing.cast(typing.Optional[DataplexDatascanData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexDatascanData]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ecfe3da18a82a79c7d4e90e51f374b6340929ff8062d6c77258151ec9f7f51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpec",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_fields": "excludeFields",
        "include_fields": "includeFields",
        "post_scan_actions": "postScanActions",
        "row_filter": "rowFilter",
        "sampling_percent": "samplingPercent",
    },
)
class DataplexDatascanDataProfileSpec:
    def __init__(
        self,
        *,
        exclude_fields: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecExcludeFields", typing.Dict[builtins.str, typing.Any]]] = None,
        include_fields: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecIncludeFields", typing.Dict[builtins.str, typing.Any]]] = None,
        post_scan_actions: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecPostScanActions", typing.Dict[builtins.str, typing.Any]]] = None,
        row_filter: typing.Optional[builtins.str] = None,
        sampling_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exclude_fields: exclude_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#exclude_fields DataplexDatascan#exclude_fields}
        :param include_fields: include_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#include_fields DataplexDatascan#include_fields}
        :param post_scan_actions: post_scan_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#post_scan_actions DataplexDatascan#post_scan_actions}
        :param row_filter: A filter applied to all rows in a single DataScan job. The filter needs to be a valid SQL expression for a WHERE clause in BigQuery standard SQL syntax. Example: col1 >= 0 AND col2 < 10 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_filter DataplexDatascan#row_filter}
        :param sampling_percent: The percentage of the records to be selected from the dataset for DataScan. Value can range between 0.0 and 100.0 with up to 3 significant decimal digits. Sampling is not applied if 'sampling_percent' is not specified, 0 or 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sampling_percent DataplexDatascan#sampling_percent}
        '''
        if isinstance(exclude_fields, dict):
            exclude_fields = DataplexDatascanDataProfileSpecExcludeFields(**exclude_fields)
        if isinstance(include_fields, dict):
            include_fields = DataplexDatascanDataProfileSpecIncludeFields(**include_fields)
        if isinstance(post_scan_actions, dict):
            post_scan_actions = DataplexDatascanDataProfileSpecPostScanActions(**post_scan_actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97359cc1586f9deb4de9c7e12f4682dac9e7dd4d4fca628be49da0ff075b12f8)
            check_type(argname="argument exclude_fields", value=exclude_fields, expected_type=type_hints["exclude_fields"])
            check_type(argname="argument include_fields", value=include_fields, expected_type=type_hints["include_fields"])
            check_type(argname="argument post_scan_actions", value=post_scan_actions, expected_type=type_hints["post_scan_actions"])
            check_type(argname="argument row_filter", value=row_filter, expected_type=type_hints["row_filter"])
            check_type(argname="argument sampling_percent", value=sampling_percent, expected_type=type_hints["sampling_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_fields is not None:
            self._values["exclude_fields"] = exclude_fields
        if include_fields is not None:
            self._values["include_fields"] = include_fields
        if post_scan_actions is not None:
            self._values["post_scan_actions"] = post_scan_actions
        if row_filter is not None:
            self._values["row_filter"] = row_filter
        if sampling_percent is not None:
            self._values["sampling_percent"] = sampling_percent

    @builtins.property
    def exclude_fields(
        self,
    ) -> typing.Optional["DataplexDatascanDataProfileSpecExcludeFields"]:
        '''exclude_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#exclude_fields DataplexDatascan#exclude_fields}
        '''
        result = self._values.get("exclude_fields")
        return typing.cast(typing.Optional["DataplexDatascanDataProfileSpecExcludeFields"], result)

    @builtins.property
    def include_fields(
        self,
    ) -> typing.Optional["DataplexDatascanDataProfileSpecIncludeFields"]:
        '''include_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#include_fields DataplexDatascan#include_fields}
        '''
        result = self._values.get("include_fields")
        return typing.cast(typing.Optional["DataplexDatascanDataProfileSpecIncludeFields"], result)

    @builtins.property
    def post_scan_actions(
        self,
    ) -> typing.Optional["DataplexDatascanDataProfileSpecPostScanActions"]:
        '''post_scan_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#post_scan_actions DataplexDatascan#post_scan_actions}
        '''
        result = self._values.get("post_scan_actions")
        return typing.cast(typing.Optional["DataplexDatascanDataProfileSpecPostScanActions"], result)

    @builtins.property
    def row_filter(self) -> typing.Optional[builtins.str]:
        '''A filter applied to all rows in a single DataScan job.

        The filter needs to be a valid SQL expression for a WHERE clause in BigQuery standard SQL syntax. Example: col1 >= 0 AND col2 < 10

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_filter DataplexDatascan#row_filter}
        '''
        result = self._values.get("row_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of the records to be selected from the dataset for DataScan.

        Value can range between 0.0 and 100.0 with up to 3 significant decimal digits.
        Sampling is not applied if 'sampling_percent' is not specified, 0 or 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sampling_percent DataplexDatascan#sampling_percent}
        '''
        result = self._values.get("sampling_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataProfileSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecExcludeFields",
    jsii_struct_bases=[],
    name_mapping={"field_names": "fieldNames"},
)
class DataplexDatascanDataProfileSpecExcludeFields:
    def __init__(
        self,
        *,
        field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param field_names: Expected input is a list of fully qualified names of fields as in the schema. Only top-level field names for nested fields are supported. For instance, if 'x' is of nested field type, listing 'x' is supported but 'x.y.z' is not supported. Here 'y' and 'y.z' are nested fields of 'x'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field_names DataplexDatascan#field_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317b91e781a70d6fad6013a374886068dda8ff121929bec9c8d0657b1c3d5c9d)
            check_type(argname="argument field_names", value=field_names, expected_type=type_hints["field_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if field_names is not None:
            self._values["field_names"] = field_names

    @builtins.property
    def field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Expected input is a list of fully qualified names of fields as in the schema.

        Only top-level field names for nested fields are supported.
        For instance, if 'x' is of nested field type, listing 'x' is supported but 'x.y.z' is not supported. Here 'y' and 'y.z' are nested fields of 'x'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field_names DataplexDatascan#field_names}
        '''
        result = self._values.get("field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataProfileSpecExcludeFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataProfileSpecExcludeFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecExcludeFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dab82f93c5b430d1788ef410438ff3eab940d106ffbb978fe7152cc4d80febe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFieldNames")
    def reset_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldNames", []))

    @builtins.property
    @jsii.member(jsii_name="fieldNamesInput")
    def field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldNames")
    def field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fieldNames"))

    @field_names.setter
    def field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bdcac021b9965491bda49fa6b9d1406131d6d600cb12123b8c19c44c5395a09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataProfileSpecExcludeFields]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpecExcludeFields], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataProfileSpecExcludeFields],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514fe3bbc8323bba64096b62898c41318dc3be0ce5781178f037e79d6403a6cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecIncludeFields",
    jsii_struct_bases=[],
    name_mapping={"field_names": "fieldNames"},
)
class DataplexDatascanDataProfileSpecIncludeFields:
    def __init__(
        self,
        *,
        field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param field_names: Expected input is a list of fully qualified names of fields as in the schema. Only top-level field names for nested fields are supported. For instance, if 'x' is of nested field type, listing 'x' is supported but 'x.y.z' is not supported. Here 'y' and 'y.z' are nested fields of 'x'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field_names DataplexDatascan#field_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12cc9d674cdfa8f3c1724cafe1f5a3fb480acc9c68cd6b5ddd424cfed9fa399f)
            check_type(argname="argument field_names", value=field_names, expected_type=type_hints["field_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if field_names is not None:
            self._values["field_names"] = field_names

    @builtins.property
    def field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Expected input is a list of fully qualified names of fields as in the schema.

        Only top-level field names for nested fields are supported.
        For instance, if 'x' is of nested field type, listing 'x' is supported but 'x.y.z' is not supported. Here 'y' and 'y.z' are nested fields of 'x'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field_names DataplexDatascan#field_names}
        '''
        result = self._values.get("field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataProfileSpecIncludeFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataProfileSpecIncludeFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecIncludeFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31d1fb585271177c44c468dd93dcad4ad5389daaec077cbe2bbb1992aaa20e28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFieldNames")
    def reset_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldNames", []))

    @builtins.property
    @jsii.member(jsii_name="fieldNamesInput")
    def field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldNames")
    def field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fieldNames"))

    @field_names.setter
    def field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90af2e7104018dd67faba658bf81aa1f23ddf543605d7aae58e7263e7ce1311a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataProfileSpecIncludeFields]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpecIncludeFields], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataProfileSpecIncludeFields],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4137798a894c7cadf23b6e98b2ce6982be340029ba4d8aac394476d64d9cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataProfileSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__249c1b17060819390364350da4fc04f801484cad1eea5c334ddd06a25e947453)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludeFields")
    def put_exclude_fields(
        self,
        *,
        field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param field_names: Expected input is a list of fully qualified names of fields as in the schema. Only top-level field names for nested fields are supported. For instance, if 'x' is of nested field type, listing 'x' is supported but 'x.y.z' is not supported. Here 'y' and 'y.z' are nested fields of 'x'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field_names DataplexDatascan#field_names}
        '''
        value = DataplexDatascanDataProfileSpecExcludeFields(field_names=field_names)

        return typing.cast(None, jsii.invoke(self, "putExcludeFields", [value]))

    @jsii.member(jsii_name="putIncludeFields")
    def put_include_fields(
        self,
        *,
        field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param field_names: Expected input is a list of fully qualified names of fields as in the schema. Only top-level field names for nested fields are supported. For instance, if 'x' is of nested field type, listing 'x' is supported but 'x.y.z' is not supported. Here 'y' and 'y.z' are nested fields of 'x'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field_names DataplexDatascan#field_names}
        '''
        value = DataplexDatascanDataProfileSpecIncludeFields(field_names=field_names)

        return typing.cast(None, jsii.invoke(self, "putIncludeFields", [value]))

    @jsii.member(jsii_name="putPostScanActions")
    def put_post_scan_actions(
        self,
        *,
        bigquery_export: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bigquery_export: bigquery_export block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_export DataplexDatascan#bigquery_export}
        '''
        value = DataplexDatascanDataProfileSpecPostScanActions(
            bigquery_export=bigquery_export
        )

        return typing.cast(None, jsii.invoke(self, "putPostScanActions", [value]))

    @jsii.member(jsii_name="resetExcludeFields")
    def reset_exclude_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeFields", []))

    @jsii.member(jsii_name="resetIncludeFields")
    def reset_include_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeFields", []))

    @jsii.member(jsii_name="resetPostScanActions")
    def reset_post_scan_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostScanActions", []))

    @jsii.member(jsii_name="resetRowFilter")
    def reset_row_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowFilter", []))

    @jsii.member(jsii_name="resetSamplingPercent")
    def reset_sampling_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamplingPercent", []))

    @builtins.property
    @jsii.member(jsii_name="excludeFields")
    def exclude_fields(
        self,
    ) -> DataplexDatascanDataProfileSpecExcludeFieldsOutputReference:
        return typing.cast(DataplexDatascanDataProfileSpecExcludeFieldsOutputReference, jsii.get(self, "excludeFields"))

    @builtins.property
    @jsii.member(jsii_name="includeFields")
    def include_fields(
        self,
    ) -> DataplexDatascanDataProfileSpecIncludeFieldsOutputReference:
        return typing.cast(DataplexDatascanDataProfileSpecIncludeFieldsOutputReference, jsii.get(self, "includeFields"))

    @builtins.property
    @jsii.member(jsii_name="postScanActions")
    def post_scan_actions(
        self,
    ) -> "DataplexDatascanDataProfileSpecPostScanActionsOutputReference":
        return typing.cast("DataplexDatascanDataProfileSpecPostScanActionsOutputReference", jsii.get(self, "postScanActions"))

    @builtins.property
    @jsii.member(jsii_name="excludeFieldsInput")
    def exclude_fields_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataProfileSpecExcludeFields]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpecExcludeFields], jsii.get(self, "excludeFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeFieldsInput")
    def include_fields_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataProfileSpecIncludeFields]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpecIncludeFields], jsii.get(self, "includeFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="postScanActionsInput")
    def post_scan_actions_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataProfileSpecPostScanActions"]:
        return typing.cast(typing.Optional["DataplexDatascanDataProfileSpecPostScanActions"], jsii.get(self, "postScanActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rowFilterInput")
    def row_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rowFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingPercentInput")
    def sampling_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="rowFilter")
    def row_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rowFilter"))

    @row_filter.setter
    def row_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7258d6e996ed8fc69dfd98fa4ea5915f2f62b8f0221713857a361f4c50a1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingPercent")
    def sampling_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingPercent"))

    @sampling_percent.setter
    def sampling_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3d642e4e66f780a58eed116cc3f089bd8e13713e1e836c1f427d6ea4b8edd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexDatascanDataProfileSpec]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataProfileSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ebfe7dbf82ace6f2dc587fc4a14e5eef3cdbe8a0d7af1cf282b0ec0e78fdba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecPostScanActions",
    jsii_struct_bases=[],
    name_mapping={"bigquery_export": "bigqueryExport"},
)
class DataplexDatascanDataProfileSpecPostScanActions:
    def __init__(
        self,
        *,
        bigquery_export: typing.Optional[typing.Union["DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bigquery_export: bigquery_export block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_export DataplexDatascan#bigquery_export}
        '''
        if isinstance(bigquery_export, dict):
            bigquery_export = DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport(**bigquery_export)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2420faf9c7d516a166319fa522692d6f12166431d6e6c3d20dc893e930b081)
            check_type(argname="argument bigquery_export", value=bigquery_export, expected_type=type_hints["bigquery_export"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bigquery_export is not None:
            self._values["bigquery_export"] = bigquery_export

    @builtins.property
    def bigquery_export(
        self,
    ) -> typing.Optional["DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport"]:
        '''bigquery_export block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_export DataplexDatascan#bigquery_export}
        '''
        result = self._values.get("bigquery_export")
        return typing.cast(typing.Optional["DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataProfileSpecPostScanActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport",
    jsii_struct_bases=[],
    name_mapping={"results_table": "resultsTable"},
)
class DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport:
    def __init__(self, *, results_table: typing.Optional[builtins.str] = None) -> None:
        '''
        :param results_table: The BigQuery table to export DataProfileScan results to. Format://bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#results_table DataplexDatascan#results_table}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ff25a7f34bc05f1c2964df3baba773c1bd7f5fd73c27abde8ff1d63ca483a1)
            check_type(argname="argument results_table", value=results_table, expected_type=type_hints["results_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if results_table is not None:
            self._values["results_table"] = results_table

    @builtins.property
    def results_table(self) -> typing.Optional[builtins.str]:
        '''The BigQuery table to export DataProfileScan results to. Format://bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#results_table DataplexDatascan#results_table}
        '''
        result = self._values.get("results_table")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataProfileSpecPostScanActionsBigqueryExportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecPostScanActionsBigqueryExportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f2d719ea688fb37587f352bdc503c8570b92b2b73b01633d9c4fb5bd1238ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResultsTable")
    def reset_results_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResultsTable", []))

    @builtins.property
    @jsii.member(jsii_name="resultsTableInput")
    def results_table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resultsTableInput"))

    @builtins.property
    @jsii.member(jsii_name="resultsTable")
    def results_table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resultsTable"))

    @results_table.setter
    def results_table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0523fdb60e6c58d72823452f982496b52d9bd851de801ee582959968a2ccb189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resultsTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1376163de2a44cd1f2ea700e708602a69aabb542d6697dd07af9f3842980d19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataProfileSpecPostScanActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataProfileSpecPostScanActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd7e37c13b20d42c56e72f6294c14dd314bb931cf25dd59bfa022a8a963d77ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigqueryExport")
    def put_bigquery_export(
        self,
        *,
        results_table: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param results_table: The BigQuery table to export DataProfileScan results to. Format://bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#results_table DataplexDatascan#results_table}
        '''
        value = DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport(
            results_table=results_table
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryExport", [value]))

    @jsii.member(jsii_name="resetBigqueryExport")
    def reset_bigquery_export(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryExport", []))

    @builtins.property
    @jsii.member(jsii_name="bigqueryExport")
    def bigquery_export(
        self,
    ) -> DataplexDatascanDataProfileSpecPostScanActionsBigqueryExportOutputReference:
        return typing.cast(DataplexDatascanDataProfileSpecPostScanActionsBigqueryExportOutputReference, jsii.get(self, "bigqueryExport"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryExportInput")
    def bigquery_export_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport], jsii.get(self, "bigqueryExportInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataProfileSpecPostScanActions]:
        return typing.cast(typing.Optional[DataplexDatascanDataProfileSpecPostScanActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataProfileSpecPostScanActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d8b9c26ad5ee444d69a6d0d5affdaa135f0cd75916453d317c13c29d7e23a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpec",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_publishing_enabled": "catalogPublishingEnabled",
        "post_scan_actions": "postScanActions",
        "row_filter": "rowFilter",
        "rules": "rules",
        "sampling_percent": "samplingPercent",
    },
)
class DataplexDatascanDataQualitySpec:
    def __init__(
        self,
        *,
        catalog_publishing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_scan_actions: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActions", typing.Dict[builtins.str, typing.Any]]] = None,
        row_filter: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataplexDatascanDataQualitySpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sampling_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param catalog_publishing_enabled: If set, the latest DataScan job result will be published to Dataplex Catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#catalog_publishing_enabled DataplexDatascan#catalog_publishing_enabled}
        :param post_scan_actions: post_scan_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#post_scan_actions DataplexDatascan#post_scan_actions}
        :param row_filter: A filter applied to all rows in a single DataScan job. The filter needs to be a valid SQL expression for a WHERE clause in BigQuery standard SQL syntax. Example: col1 >= 0 AND col2 < 10 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_filter DataplexDatascan#row_filter}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#rules DataplexDatascan#rules}
        :param sampling_percent: The percentage of the records to be selected from the dataset for DataScan. Value can range between 0.0 and 100.0 with up to 3 significant decimal digits. Sampling is not applied if 'sampling_percent' is not specified, 0 or 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sampling_percent DataplexDatascan#sampling_percent}
        '''
        if isinstance(post_scan_actions, dict):
            post_scan_actions = DataplexDatascanDataQualitySpecPostScanActions(**post_scan_actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c98a56040ac5f9e591bba4e1a4fa0a58d92446f6282e22ad7ef9e5ead6bb80)
            check_type(argname="argument catalog_publishing_enabled", value=catalog_publishing_enabled, expected_type=type_hints["catalog_publishing_enabled"])
            check_type(argname="argument post_scan_actions", value=post_scan_actions, expected_type=type_hints["post_scan_actions"])
            check_type(argname="argument row_filter", value=row_filter, expected_type=type_hints["row_filter"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument sampling_percent", value=sampling_percent, expected_type=type_hints["sampling_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_publishing_enabled is not None:
            self._values["catalog_publishing_enabled"] = catalog_publishing_enabled
        if post_scan_actions is not None:
            self._values["post_scan_actions"] = post_scan_actions
        if row_filter is not None:
            self._values["row_filter"] = row_filter
        if rules is not None:
            self._values["rules"] = rules
        if sampling_percent is not None:
            self._values["sampling_percent"] = sampling_percent

    @builtins.property
    def catalog_publishing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, the latest DataScan job result will be published to Dataplex Catalog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#catalog_publishing_enabled DataplexDatascan#catalog_publishing_enabled}
        '''
        result = self._values.get("catalog_publishing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def post_scan_actions(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActions"]:
        '''post_scan_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#post_scan_actions DataplexDatascan#post_scan_actions}
        '''
        result = self._values.get("post_scan_actions")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActions"], result)

    @builtins.property
    def row_filter(self) -> typing.Optional[builtins.str]:
        '''A filter applied to all rows in a single DataScan job.

        The filter needs to be a valid SQL expression for a WHERE clause in BigQuery standard SQL syntax. Example: col1 >= 0 AND col2 < 10

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_filter DataplexDatascan#row_filter}
        '''
        result = self._values.get("row_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexDatascanDataQualitySpecRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#rules DataplexDatascan#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexDatascanDataQualitySpecRules"]]], result)

    @builtins.property
    def sampling_percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of the records to be selected from the dataset for DataScan.

        Value can range between 0.0 and 100.0 with up to 3 significant decimal digits.
        Sampling is not applied if 'sampling_percent' is not specified, 0 or 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sampling_percent DataplexDatascan#sampling_percent}
        '''
        result = self._values.get("sampling_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71887d414bfebf19c33160aca3d7a99a4057fb053019e41bade2100377d75079)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostScanActions")
    def put_post_scan_actions(
        self,
        *,
        bigquery_export: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_report: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActionsNotificationReport", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bigquery_export: bigquery_export block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_export DataplexDatascan#bigquery_export}
        :param notification_report: notification_report block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#notification_report DataplexDatascan#notification_report}
        '''
        value = DataplexDatascanDataQualitySpecPostScanActions(
            bigquery_export=bigquery_export, notification_report=notification_report
        )

        return typing.cast(None, jsii.invoke(self, "putPostScanActions", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataplexDatascanDataQualitySpecRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e4645c0fdd4af9c8d94abd52201f612cfbfa74e577e76ff4fbf50d84f02469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetCatalogPublishingEnabled")
    def reset_catalog_publishing_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogPublishingEnabled", []))

    @jsii.member(jsii_name="resetPostScanActions")
    def reset_post_scan_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostScanActions", []))

    @jsii.member(jsii_name="resetRowFilter")
    def reset_row_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowFilter", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="resetSamplingPercent")
    def reset_sampling_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamplingPercent", []))

    @builtins.property
    @jsii.member(jsii_name="postScanActions")
    def post_scan_actions(
        self,
    ) -> "DataplexDatascanDataQualitySpecPostScanActionsOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecPostScanActionsOutputReference", jsii.get(self, "postScanActions"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "DataplexDatascanDataQualitySpecRulesList":
        return typing.cast("DataplexDatascanDataQualitySpecRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="catalogPublishingEnabledInput")
    def catalog_publishing_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "catalogPublishingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="postScanActionsInput")
    def post_scan_actions_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActions"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActions"], jsii.get(self, "postScanActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rowFilterInput")
    def row_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rowFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexDatascanDataQualitySpecRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataplexDatascanDataQualitySpecRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingPercentInput")
    def sampling_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogPublishingEnabled")
    def catalog_publishing_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "catalogPublishingEnabled"))

    @catalog_publishing_enabled.setter
    def catalog_publishing_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6680e83acc92a17da9ddcba6145505f27ab756e059edda27694a2f0337bdb552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogPublishingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowFilter")
    def row_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rowFilter"))

    @row_filter.setter
    def row_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e684f7a223bd3b8697103319d545d5f73bca5ac008fad80de4cc4771349e5a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingPercent")
    def sampling_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingPercent"))

    @sampling_percent.setter
    def sampling_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99d588c57dd79bf1e283d4a386394ec6a940747baec8dcf253f1b84e309d0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexDatascanDataQualitySpec]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c50c625b58b82848acec8bc31b41279f7450881cce359286c40783633e1958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActions",
    jsii_struct_bases=[],
    name_mapping={
        "bigquery_export": "bigqueryExport",
        "notification_report": "notificationReport",
    },
)
class DataplexDatascanDataQualitySpecPostScanActions:
    def __init__(
        self,
        *,
        bigquery_export: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_report: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActionsNotificationReport", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bigquery_export: bigquery_export block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_export DataplexDatascan#bigquery_export}
        :param notification_report: notification_report block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#notification_report DataplexDatascan#notification_report}
        '''
        if isinstance(bigquery_export, dict):
            bigquery_export = DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport(**bigquery_export)
        if isinstance(notification_report, dict):
            notification_report = DataplexDatascanDataQualitySpecPostScanActionsNotificationReport(**notification_report)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d4c425f3b0ef2a8bf372e542b1b79e03c2b5dd24990a7772494847d9bb38ad)
            check_type(argname="argument bigquery_export", value=bigquery_export, expected_type=type_hints["bigquery_export"])
            check_type(argname="argument notification_report", value=notification_report, expected_type=type_hints["notification_report"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bigquery_export is not None:
            self._values["bigquery_export"] = bigquery_export
        if notification_report is not None:
            self._values["notification_report"] = notification_report

    @builtins.property
    def bigquery_export(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport"]:
        '''bigquery_export block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#bigquery_export DataplexDatascan#bigquery_export}
        '''
        result = self._values.get("bigquery_export")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport"], result)

    @builtins.property
    def notification_report(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReport"]:
        '''notification_report block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#notification_report DataplexDatascan#notification_report}
        '''
        result = self._values.get("notification_report")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReport"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecPostScanActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport",
    jsii_struct_bases=[],
    name_mapping={"results_table": "resultsTable"},
)
class DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport:
    def __init__(self, *, results_table: typing.Optional[builtins.str] = None) -> None:
        '''
        :param results_table: The BigQuery table to export DataQualityScan results to. Format://bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#results_table DataplexDatascan#results_table}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e32e88c2d9c7cd520d7abd11db51ab1b32ff1f7b952820017f0d4daff9d350)
            check_type(argname="argument results_table", value=results_table, expected_type=type_hints["results_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if results_table is not None:
            self._values["results_table"] = results_table

    @builtins.property
    def results_table(self) -> typing.Optional[builtins.str]:
        '''The BigQuery table to export DataQualityScan results to. Format://bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#results_table DataplexDatascan#results_table}
        '''
        result = self._values.get("results_table")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecPostScanActionsBigqueryExportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsBigqueryExportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41229a1a441415a484969f33dada1770a0fb2d61e0725348faa5589b289e36d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResultsTable")
    def reset_results_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResultsTable", []))

    @builtins.property
    @jsii.member(jsii_name="resultsTableInput")
    def results_table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resultsTableInput"))

    @builtins.property
    @jsii.member(jsii_name="resultsTable")
    def results_table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resultsTable"))

    @results_table.setter
    def results_table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7ae2abb3d11a2028b835c1fd6c58b13d7fcf533f62a55063d175fe4722b97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resultsTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f739184964e852d91eadef2fc4f35a73e0469d3c5f34f023cf0479e34316711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReport",
    jsii_struct_bases=[],
    name_mapping={
        "recipients": "recipients",
        "job_end_trigger": "jobEndTrigger",
        "job_failure_trigger": "jobFailureTrigger",
        "score_threshold_trigger": "scoreThresholdTrigger",
    },
)
class DataplexDatascanDataQualitySpecPostScanActionsNotificationReport:
    def __init__(
        self,
        *,
        recipients: typing.Union["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients", typing.Dict[builtins.str, typing.Any]],
        job_end_trigger: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        job_failure_trigger: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        score_threshold_trigger: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recipients: recipients block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#recipients DataplexDatascan#recipients}
        :param job_end_trigger: job_end_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#job_end_trigger DataplexDatascan#job_end_trigger}
        :param job_failure_trigger: job_failure_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#job_failure_trigger DataplexDatascan#job_failure_trigger}
        :param score_threshold_trigger: score_threshold_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#score_threshold_trigger DataplexDatascan#score_threshold_trigger}
        '''
        if isinstance(recipients, dict):
            recipients = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients(**recipients)
        if isinstance(job_end_trigger, dict):
            job_end_trigger = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger(**job_end_trigger)
        if isinstance(job_failure_trigger, dict):
            job_failure_trigger = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger(**job_failure_trigger)
        if isinstance(score_threshold_trigger, dict):
            score_threshold_trigger = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger(**score_threshold_trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263330631c61aa32380cfa148b6bbe38a80f342045c9c483f56bc7795e437341)
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
            check_type(argname="argument job_end_trigger", value=job_end_trigger, expected_type=type_hints["job_end_trigger"])
            check_type(argname="argument job_failure_trigger", value=job_failure_trigger, expected_type=type_hints["job_failure_trigger"])
            check_type(argname="argument score_threshold_trigger", value=score_threshold_trigger, expected_type=type_hints["score_threshold_trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recipients": recipients,
        }
        if job_end_trigger is not None:
            self._values["job_end_trigger"] = job_end_trigger
        if job_failure_trigger is not None:
            self._values["job_failure_trigger"] = job_failure_trigger
        if score_threshold_trigger is not None:
            self._values["score_threshold_trigger"] = score_threshold_trigger

    @builtins.property
    def recipients(
        self,
    ) -> "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients":
        '''recipients block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#recipients DataplexDatascan#recipients}
        '''
        result = self._values.get("recipients")
        assert result is not None, "Required property 'recipients' is missing"
        return typing.cast("DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients", result)

    @builtins.property
    def job_end_trigger(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger"]:
        '''job_end_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#job_end_trigger DataplexDatascan#job_end_trigger}
        '''
        result = self._values.get("job_end_trigger")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger"], result)

    @builtins.property
    def job_failure_trigger(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger"]:
        '''job_failure_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#job_failure_trigger DataplexDatascan#job_failure_trigger}
        '''
        result = self._values.get("job_failure_trigger")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger"], result)

    @builtins.property
    def score_threshold_trigger(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger"]:
        '''score_threshold_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#score_threshold_trigger DataplexDatascan#score_threshold_trigger}
        '''
        result = self._values.get("score_threshold_trigger")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecPostScanActionsNotificationReport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9732551621d583a343884066daefd737990c227ae0106a390d68f492015a299f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8713e6faf760580364fd9db56c4b183b51939ac2b80fad1f9d2f32c28bfc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ef48c6c04c489eb96c76ad1439c41328d683ffee803378d0e3e737f72e09fc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff50e6a06b5fa9dd42a26677ceb2e4bc20ab7a507e38a26697571dd569c41fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e207815a75a3bbf564e0f49126676b55d05aa133b34779c671087dfdfd6a7fe9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJobEndTrigger")
    def put_job_end_trigger(self) -> None:
        value = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger()

        return typing.cast(None, jsii.invoke(self, "putJobEndTrigger", [value]))

    @jsii.member(jsii_name="putJobFailureTrigger")
    def put_job_failure_trigger(self) -> None:
        value = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger()

        return typing.cast(None, jsii.invoke(self, "putJobFailureTrigger", [value]))

    @jsii.member(jsii_name="putRecipients")
    def put_recipients(
        self,
        *,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param emails: The email recipients who will receive the DataQualityScan results report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#emails DataplexDatascan#emails}
        '''
        value = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients(
            emails=emails
        )

        return typing.cast(None, jsii.invoke(self, "putRecipients", [value]))

    @jsii.member(jsii_name="putScoreThresholdTrigger")
    def put_score_threshold_trigger(
        self,
        *,
        score_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param score_threshold: The score range is in [0,100]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#score_threshold DataplexDatascan#score_threshold}
        '''
        value = DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger(
            score_threshold=score_threshold
        )

        return typing.cast(None, jsii.invoke(self, "putScoreThresholdTrigger", [value]))

    @jsii.member(jsii_name="resetJobEndTrigger")
    def reset_job_end_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobEndTrigger", []))

    @jsii.member(jsii_name="resetJobFailureTrigger")
    def reset_job_failure_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobFailureTrigger", []))

    @jsii.member(jsii_name="resetScoreThresholdTrigger")
    def reset_score_threshold_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScoreThresholdTrigger", []))

    @builtins.property
    @jsii.member(jsii_name="jobEndTrigger")
    def job_end_trigger(
        self,
    ) -> DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTriggerOutputReference:
        return typing.cast(DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTriggerOutputReference, jsii.get(self, "jobEndTrigger"))

    @builtins.property
    @jsii.member(jsii_name="jobFailureTrigger")
    def job_failure_trigger(
        self,
    ) -> DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTriggerOutputReference:
        return typing.cast(DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTriggerOutputReference, jsii.get(self, "jobFailureTrigger"))

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(
        self,
    ) -> "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipientsOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipientsOutputReference", jsii.get(self, "recipients"))

    @builtins.property
    @jsii.member(jsii_name="scoreThresholdTrigger")
    def score_threshold_trigger(
        self,
    ) -> "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTriggerOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTriggerOutputReference", jsii.get(self, "scoreThresholdTrigger"))

    @builtins.property
    @jsii.member(jsii_name="jobEndTriggerInput")
    def job_end_trigger_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger], jsii.get(self, "jobEndTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="jobFailureTriggerInput")
    def job_failure_trigger_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger], jsii.get(self, "jobFailureTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="recipientsInput")
    def recipients_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients"], jsii.get(self, "recipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="scoreThresholdTriggerInput")
    def score_threshold_trigger_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger"], jsii.get(self, "scoreThresholdTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReport]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReport],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b78b2ce38b74c416532339a685540bcf93ae6120c5f4d62d9ea2964e0f43d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients",
    jsii_struct_bases=[],
    name_mapping={"emails": "emails"},
)
class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients:
    def __init__(
        self,
        *,
        emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param emails: The email recipients who will receive the DataQualityScan results report. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#emails DataplexDatascan#emails}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43833aa201b55640cf07cbb2668906b439ba410e6ec3ac4d141924ee3f501034)
            check_type(argname="argument emails", value=emails, expected_type=type_hints["emails"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if emails is not None:
            self._values["emails"] = emails

    @builtins.property
    def emails(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The email recipients who will receive the DataQualityScan results report.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#emails DataplexDatascan#emails}
        '''
        result = self._values.get("emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipientsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipientsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0079de974cd967c3a8c3a6ce9cbd869e3ceeac821de8a017d679f063e7e8fec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmails")
    def reset_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmails", []))

    @builtins.property
    @jsii.member(jsii_name="emailsInput")
    def emails_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailsInput"))

    @builtins.property
    @jsii.member(jsii_name="emails")
    def emails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emails"))

    @emails.setter
    def emails(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80498599ea5081a45603b2ba923011de24a00eef4e91dfb8187be1097e7a219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354114ae1b91efbada122a78ad8ecad23a8269dac5e9337274701d66cb748a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger",
    jsii_struct_bases=[],
    name_mapping={"score_threshold": "scoreThreshold"},
)
class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger:
    def __init__(self, *, score_threshold: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param score_threshold: The score range is in [0,100]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#score_threshold DataplexDatascan#score_threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca71821db343b5f0d7a8116366f12948e50a962cd5a67cd1de2aa8b6a74e1e70)
            check_type(argname="argument score_threshold", value=score_threshold, expected_type=type_hints["score_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if score_threshold is not None:
            self._values["score_threshold"] = score_threshold

    @builtins.property
    def score_threshold(self) -> typing.Optional[jsii.Number]:
        '''The score range is in [0,100].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#score_threshold DataplexDatascan#score_threshold}
        '''
        result = self._values.get("score_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65b6647c5d4c113c5ec1f635ab91c89b1a9a03ed659da61a1aaaf0e6c553728b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScoreThreshold")
    def reset_score_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScoreThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="scoreThresholdInput")
    def score_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scoreThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="scoreThreshold")
    def score_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scoreThreshold"))

    @score_threshold.setter
    def score_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0679c906c8ecdd540f49d91386c073dcdd82407de3ccd88e124cbff1271e695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scoreThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ea807ddb9bb424ade304fcafe621b0c98a6b5e9288ee92541ef00d4117933b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataQualitySpecPostScanActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecPostScanActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40ec4d4f2bc1503a9faf7d8be3e8d256c28eef9a3c72260b1f154ace0564aa77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigqueryExport")
    def put_bigquery_export(
        self,
        *,
        results_table: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param results_table: The BigQuery table to export DataQualityScan results to. Format://bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#results_table DataplexDatascan#results_table}
        '''
        value = DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport(
            results_table=results_table
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryExport", [value]))

    @jsii.member(jsii_name="putNotificationReport")
    def put_notification_report(
        self,
        *,
        recipients: typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients, typing.Dict[builtins.str, typing.Any]],
        job_end_trigger: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
        job_failure_trigger: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
        score_threshold_trigger: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recipients: recipients block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#recipients DataplexDatascan#recipients}
        :param job_end_trigger: job_end_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#job_end_trigger DataplexDatascan#job_end_trigger}
        :param job_failure_trigger: job_failure_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#job_failure_trigger DataplexDatascan#job_failure_trigger}
        :param score_threshold_trigger: score_threshold_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#score_threshold_trigger DataplexDatascan#score_threshold_trigger}
        '''
        value = DataplexDatascanDataQualitySpecPostScanActionsNotificationReport(
            recipients=recipients,
            job_end_trigger=job_end_trigger,
            job_failure_trigger=job_failure_trigger,
            score_threshold_trigger=score_threshold_trigger,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationReport", [value]))

    @jsii.member(jsii_name="resetBigqueryExport")
    def reset_bigquery_export(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryExport", []))

    @jsii.member(jsii_name="resetNotificationReport")
    def reset_notification_report(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationReport", []))

    @builtins.property
    @jsii.member(jsii_name="bigqueryExport")
    def bigquery_export(
        self,
    ) -> DataplexDatascanDataQualitySpecPostScanActionsBigqueryExportOutputReference:
        return typing.cast(DataplexDatascanDataQualitySpecPostScanActionsBigqueryExportOutputReference, jsii.get(self, "bigqueryExport"))

    @builtins.property
    @jsii.member(jsii_name="notificationReport")
    def notification_report(
        self,
    ) -> DataplexDatascanDataQualitySpecPostScanActionsNotificationReportOutputReference:
        return typing.cast(DataplexDatascanDataQualitySpecPostScanActionsNotificationReportOutputReference, jsii.get(self, "notificationReport"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryExportInput")
    def bigquery_export_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport], jsii.get(self, "bigqueryExportInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationReportInput")
    def notification_report_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReport]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReport], jsii.get(self, "notificationReportInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecPostScanActions]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecPostScanActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb7c645be6acadab8d8cfd96c2cc485f3a057bf8c6fcae2bee9feb29607ccce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRules",
    jsii_struct_bases=[],
    name_mapping={
        "dimension": "dimension",
        "column": "column",
        "description": "description",
        "ignore_null": "ignoreNull",
        "name": "name",
        "non_null_expectation": "nonNullExpectation",
        "range_expectation": "rangeExpectation",
        "regex_expectation": "regexExpectation",
        "row_condition_expectation": "rowConditionExpectation",
        "set_expectation": "setExpectation",
        "sql_assertion": "sqlAssertion",
        "statistic_range_expectation": "statisticRangeExpectation",
        "suspended": "suspended",
        "table_condition_expectation": "tableConditionExpectation",
        "threshold": "threshold",
        "uniqueness_expectation": "uniquenessExpectation",
    },
)
class DataplexDatascanDataQualitySpecRules:
    def __init__(
        self,
        *,
        dimension: builtins.str,
        column: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        ignore_null: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        non_null_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesNonNullExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
        range_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesRangeExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
        regex_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesRegexExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
        row_condition_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesRowConditionExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
        set_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesSetExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_assertion: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesSqlAssertion", typing.Dict[builtins.str, typing.Any]]] = None,
        statistic_range_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        table_condition_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesTableConditionExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
        threshold: typing.Optional[jsii.Number] = None,
        uniqueness_expectation: typing.Optional[typing.Union["DataplexDatascanDataQualitySpecRulesUniquenessExpectation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dimension: The dimension name a rule belongs to. Custom dimension name is supported with all uppercase letters and maximum length of 30 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#dimension DataplexDatascan#dimension}
        :param column: The unnested column which this rule is evaluated against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#column DataplexDatascan#column}
        :param description: Description of the rule. The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#description DataplexDatascan#description}
        :param ignore_null: Rows with null values will automatically fail a rule, unless ignoreNull is true. In that case, such null rows are trivially considered passing. Only applicable to ColumnMap rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#ignore_null DataplexDatascan#ignore_null}
        :param name: A mutable name for the rule. The name must contain only letters (a-z, A-Z), numbers (0-9), or hyphens (-). The maximum length is 63 characters. Must start with a letter. Must end with a number or a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#name DataplexDatascan#name}
        :param non_null_expectation: non_null_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#non_null_expectation DataplexDatascan#non_null_expectation}
        :param range_expectation: range_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#range_expectation DataplexDatascan#range_expectation}
        :param regex_expectation: regex_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#regex_expectation DataplexDatascan#regex_expectation}
        :param row_condition_expectation: row_condition_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_condition_expectation DataplexDatascan#row_condition_expectation}
        :param set_expectation: set_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#set_expectation DataplexDatascan#set_expectation}
        :param sql_assertion: sql_assertion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_assertion DataplexDatascan#sql_assertion}
        :param statistic_range_expectation: statistic_range_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#statistic_range_expectation DataplexDatascan#statistic_range_expectation}
        :param suspended: Whether the Rule is active or suspended. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#suspended DataplexDatascan#suspended}
        :param table_condition_expectation: table_condition_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#table_condition_expectation DataplexDatascan#table_condition_expectation}
        :param threshold: The minimum ratio of passing_rows / total_rows required to pass this rule, with a range of [0.0, 1.0]. 0 indicates default value (i.e. 1.0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#threshold DataplexDatascan#threshold}
        :param uniqueness_expectation: uniqueness_expectation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#uniqueness_expectation DataplexDatascan#uniqueness_expectation}
        '''
        if isinstance(non_null_expectation, dict):
            non_null_expectation = DataplexDatascanDataQualitySpecRulesNonNullExpectation(**non_null_expectation)
        if isinstance(range_expectation, dict):
            range_expectation = DataplexDatascanDataQualitySpecRulesRangeExpectation(**range_expectation)
        if isinstance(regex_expectation, dict):
            regex_expectation = DataplexDatascanDataQualitySpecRulesRegexExpectation(**regex_expectation)
        if isinstance(row_condition_expectation, dict):
            row_condition_expectation = DataplexDatascanDataQualitySpecRulesRowConditionExpectation(**row_condition_expectation)
        if isinstance(set_expectation, dict):
            set_expectation = DataplexDatascanDataQualitySpecRulesSetExpectation(**set_expectation)
        if isinstance(sql_assertion, dict):
            sql_assertion = DataplexDatascanDataQualitySpecRulesSqlAssertion(**sql_assertion)
        if isinstance(statistic_range_expectation, dict):
            statistic_range_expectation = DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation(**statistic_range_expectation)
        if isinstance(table_condition_expectation, dict):
            table_condition_expectation = DataplexDatascanDataQualitySpecRulesTableConditionExpectation(**table_condition_expectation)
        if isinstance(uniqueness_expectation, dict):
            uniqueness_expectation = DataplexDatascanDataQualitySpecRulesUniquenessExpectation(**uniqueness_expectation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31a3525e6b316fa85e52d9d95f27722bbbbeb6ecb5187454efa713bd2be01eb)
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ignore_null", value=ignore_null, expected_type=type_hints["ignore_null"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument non_null_expectation", value=non_null_expectation, expected_type=type_hints["non_null_expectation"])
            check_type(argname="argument range_expectation", value=range_expectation, expected_type=type_hints["range_expectation"])
            check_type(argname="argument regex_expectation", value=regex_expectation, expected_type=type_hints["regex_expectation"])
            check_type(argname="argument row_condition_expectation", value=row_condition_expectation, expected_type=type_hints["row_condition_expectation"])
            check_type(argname="argument set_expectation", value=set_expectation, expected_type=type_hints["set_expectation"])
            check_type(argname="argument sql_assertion", value=sql_assertion, expected_type=type_hints["sql_assertion"])
            check_type(argname="argument statistic_range_expectation", value=statistic_range_expectation, expected_type=type_hints["statistic_range_expectation"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument table_condition_expectation", value=table_condition_expectation, expected_type=type_hints["table_condition_expectation"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument uniqueness_expectation", value=uniqueness_expectation, expected_type=type_hints["uniqueness_expectation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dimension": dimension,
        }
        if column is not None:
            self._values["column"] = column
        if description is not None:
            self._values["description"] = description
        if ignore_null is not None:
            self._values["ignore_null"] = ignore_null
        if name is not None:
            self._values["name"] = name
        if non_null_expectation is not None:
            self._values["non_null_expectation"] = non_null_expectation
        if range_expectation is not None:
            self._values["range_expectation"] = range_expectation
        if regex_expectation is not None:
            self._values["regex_expectation"] = regex_expectation
        if row_condition_expectation is not None:
            self._values["row_condition_expectation"] = row_condition_expectation
        if set_expectation is not None:
            self._values["set_expectation"] = set_expectation
        if sql_assertion is not None:
            self._values["sql_assertion"] = sql_assertion
        if statistic_range_expectation is not None:
            self._values["statistic_range_expectation"] = statistic_range_expectation
        if suspended is not None:
            self._values["suspended"] = suspended
        if table_condition_expectation is not None:
            self._values["table_condition_expectation"] = table_condition_expectation
        if threshold is not None:
            self._values["threshold"] = threshold
        if uniqueness_expectation is not None:
            self._values["uniqueness_expectation"] = uniqueness_expectation

    @builtins.property
    def dimension(self) -> builtins.str:
        '''The dimension name a rule belongs to.

        Custom dimension name is supported with all uppercase letters and maximum length of 30 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#dimension DataplexDatascan#dimension}
        '''
        result = self._values.get("dimension")
        assert result is not None, "Required property 'dimension' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''The unnested column which this rule is evaluated against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#column DataplexDatascan#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the rule. The maximum length is 1,024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#description DataplexDatascan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_null(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Rows with null values will automatically fail a rule, unless ignoreNull is true.

        In that case, such null rows are trivially considered passing. Only applicable to ColumnMap rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#ignore_null DataplexDatascan#ignore_null}
        '''
        result = self._values.get("ignore_null")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A mutable name for the rule.

        The name must contain only letters (a-z, A-Z), numbers (0-9), or hyphens (-).
        The maximum length is 63 characters.
        Must start with a letter.
        Must end with a number or a letter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#name DataplexDatascan#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_null_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesNonNullExpectation"]:
        '''non_null_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#non_null_expectation DataplexDatascan#non_null_expectation}
        '''
        result = self._values.get("non_null_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesNonNullExpectation"], result)

    @builtins.property
    def range_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesRangeExpectation"]:
        '''range_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#range_expectation DataplexDatascan#range_expectation}
        '''
        result = self._values.get("range_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesRangeExpectation"], result)

    @builtins.property
    def regex_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesRegexExpectation"]:
        '''regex_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#regex_expectation DataplexDatascan#regex_expectation}
        '''
        result = self._values.get("regex_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesRegexExpectation"], result)

    @builtins.property
    def row_condition_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesRowConditionExpectation"]:
        '''row_condition_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#row_condition_expectation DataplexDatascan#row_condition_expectation}
        '''
        result = self._values.get("row_condition_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesRowConditionExpectation"], result)

    @builtins.property
    def set_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesSetExpectation"]:
        '''set_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#set_expectation DataplexDatascan#set_expectation}
        '''
        result = self._values.get("set_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesSetExpectation"], result)

    @builtins.property
    def sql_assertion(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesSqlAssertion"]:
        '''sql_assertion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_assertion DataplexDatascan#sql_assertion}
        '''
        result = self._values.get("sql_assertion")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesSqlAssertion"], result)

    @builtins.property
    def statistic_range_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation"]:
        '''statistic_range_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#statistic_range_expectation DataplexDatascan#statistic_range_expectation}
        '''
        result = self._values.get("statistic_range_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation"], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the Rule is active or suspended. Default = false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#suspended DataplexDatascan#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def table_condition_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesTableConditionExpectation"]:
        '''table_condition_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#table_condition_expectation DataplexDatascan#table_condition_expectation}
        '''
        result = self._values.get("table_condition_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesTableConditionExpectation"], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The minimum ratio of passing_rows / total_rows required to pass this rule, with a range of [0.0, 1.0]. 0 indicates default value (i.e. 1.0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#threshold DataplexDatascan#threshold}
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uniqueness_expectation(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesUniquenessExpectation"]:
        '''uniqueness_expectation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#uniqueness_expectation DataplexDatascan#uniqueness_expectation}
        '''
        result = self._values.get("uniqueness_expectation")
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesUniquenessExpectation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6f6a501cf2ff5783ab6573f714638d827de167ccba2b5a70a7696032f776bf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataplexDatascanDataQualitySpecRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fcc45b0ed7e1e1cf1e37f592761f449a845a73c3ca5e397749e06fe0aa555a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexDatascanDataQualitySpecRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8668d815b6c8ee4e1a2eaa2532af3505c6ff1a1857d15702c367a61a0b0b62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__361e868f5fc2b28e7c42881dd07181155e351e9bf12e51f0e215207c6bbcfea2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f68d0f72f90e3e57736ddaa92ef1236e4788eb56b811ff69ff2eb95a5290559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexDatascanDataQualitySpecRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexDatascanDataQualitySpecRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexDatascanDataQualitySpecRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64df4d8637ff6193481df214baf857507ab29651b730b860fd8631e35a1dca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesNonNullExpectation",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexDatascanDataQualitySpecRulesNonNullExpectation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesNonNullExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesNonNullExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesNonNullExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3dfbe05de944fd068a47b5529354f9f73b3a6347629dd8c6b8e169870c5505f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesNonNullExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesNonNullExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesNonNullExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8849d3bf809a221ce924ebb2c0f1c6a505fa0923bbfe7c73c078b94d769a3148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanDataQualitySpecRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__760ebc6a3289ef3333f8fbe92ff7f03a37bae78f9b3d33d7b73cc72482919682)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNonNullExpectation")
    def put_non_null_expectation(self) -> None:
        value = DataplexDatascanDataQualitySpecRulesNonNullExpectation()

        return typing.cast(None, jsii.invoke(self, "putNonNullExpectation", [value]))

    @jsii.member(jsii_name="putRangeExpectation")
    def put_range_expectation(
        self,
        *,
        max_value: typing.Optional[builtins.str] = None,
        min_value: typing.Optional[builtins.str] = None,
        strict_max_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict_min_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_value: The maximum column value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#max_value DataplexDatascan#max_value}
        :param min_value: The minimum column value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#min_value DataplexDatascan#min_value}
        :param strict_max_enabled: Whether each value needs to be strictly lesser than ('<') the maximum, or if equality is allowed. Only relevant if a maxValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_max_enabled DataplexDatascan#strict_max_enabled}
        :param strict_min_enabled: Whether each value needs to be strictly greater than ('>') the minimum, or if equality is allowed. Only relevant if a minValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_min_enabled DataplexDatascan#strict_min_enabled}
        '''
        value = DataplexDatascanDataQualitySpecRulesRangeExpectation(
            max_value=max_value,
            min_value=min_value,
            strict_max_enabled=strict_max_enabled,
            strict_min_enabled=strict_min_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putRangeExpectation", [value]))

    @jsii.member(jsii_name="putRegexExpectation")
    def put_regex_expectation(self, *, regex: builtins.str) -> None:
        '''
        :param regex: A regular expression the column value is expected to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#regex DataplexDatascan#regex}
        '''
        value = DataplexDatascanDataQualitySpecRulesRegexExpectation(regex=regex)

        return typing.cast(None, jsii.invoke(self, "putRegexExpectation", [value]))

    @jsii.member(jsii_name="putRowConditionExpectation")
    def put_row_condition_expectation(self, *, sql_expression: builtins.str) -> None:
        '''
        :param sql_expression: The SQL expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_expression DataplexDatascan#sql_expression}
        '''
        value = DataplexDatascanDataQualitySpecRulesRowConditionExpectation(
            sql_expression=sql_expression
        )

        return typing.cast(None, jsii.invoke(self, "putRowConditionExpectation", [value]))

    @jsii.member(jsii_name="putSetExpectation")
    def put_set_expectation(self, *, values: typing.Sequence[builtins.str]) -> None:
        '''
        :param values: Expected values for the column value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#values DataplexDatascan#values}
        '''
        value = DataplexDatascanDataQualitySpecRulesSetExpectation(values=values)

        return typing.cast(None, jsii.invoke(self, "putSetExpectation", [value]))

    @jsii.member(jsii_name="putSqlAssertion")
    def put_sql_assertion(self, *, sql_statement: builtins.str) -> None:
        '''
        :param sql_statement: The SQL statement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_statement DataplexDatascan#sql_statement}
        '''
        value = DataplexDatascanDataQualitySpecRulesSqlAssertion(
            sql_statement=sql_statement
        )

        return typing.cast(None, jsii.invoke(self, "putSqlAssertion", [value]))

    @jsii.member(jsii_name="putStatisticRangeExpectation")
    def put_statistic_range_expectation(
        self,
        *,
        statistic: builtins.str,
        max_value: typing.Optional[builtins.str] = None,
        min_value: typing.Optional[builtins.str] = None,
        strict_max_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict_min_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param statistic: column statistics. Possible values: ["STATISTIC_UNDEFINED", "MEAN", "MIN", "MAX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#statistic DataplexDatascan#statistic}
        :param max_value: The maximum column statistic value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#max_value DataplexDatascan#max_value}
        :param min_value: The minimum column statistic value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#min_value DataplexDatascan#min_value}
        :param strict_max_enabled: Whether column statistic needs to be strictly lesser than ('<') the maximum, or if equality is allowed. Only relevant if a maxValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_max_enabled DataplexDatascan#strict_max_enabled}
        :param strict_min_enabled: Whether column statistic needs to be strictly greater than ('>') the minimum, or if equality is allowed. Only relevant if a minValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_min_enabled DataplexDatascan#strict_min_enabled}
        '''
        value = DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation(
            statistic=statistic,
            max_value=max_value,
            min_value=min_value,
            strict_max_enabled=strict_max_enabled,
            strict_min_enabled=strict_min_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putStatisticRangeExpectation", [value]))

    @jsii.member(jsii_name="putTableConditionExpectation")
    def put_table_condition_expectation(self, *, sql_expression: builtins.str) -> None:
        '''
        :param sql_expression: The SQL expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_expression DataplexDatascan#sql_expression}
        '''
        value = DataplexDatascanDataQualitySpecRulesTableConditionExpectation(
            sql_expression=sql_expression
        )

        return typing.cast(None, jsii.invoke(self, "putTableConditionExpectation", [value]))

    @jsii.member(jsii_name="putUniquenessExpectation")
    def put_uniqueness_expectation(self) -> None:
        value = DataplexDatascanDataQualitySpecRulesUniquenessExpectation()

        return typing.cast(None, jsii.invoke(self, "putUniquenessExpectation", [value]))

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetIgnoreNull")
    def reset_ignore_null(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreNull", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNonNullExpectation")
    def reset_non_null_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonNullExpectation", []))

    @jsii.member(jsii_name="resetRangeExpectation")
    def reset_range_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeExpectation", []))

    @jsii.member(jsii_name="resetRegexExpectation")
    def reset_regex_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexExpectation", []))

    @jsii.member(jsii_name="resetRowConditionExpectation")
    def reset_row_condition_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowConditionExpectation", []))

    @jsii.member(jsii_name="resetSetExpectation")
    def reset_set_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetExpectation", []))

    @jsii.member(jsii_name="resetSqlAssertion")
    def reset_sql_assertion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlAssertion", []))

    @jsii.member(jsii_name="resetStatisticRangeExpectation")
    def reset_statistic_range_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatisticRangeExpectation", []))

    @jsii.member(jsii_name="resetSuspended")
    def reset_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspended", []))

    @jsii.member(jsii_name="resetTableConditionExpectation")
    def reset_table_condition_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableConditionExpectation", []))

    @jsii.member(jsii_name="resetThreshold")
    def reset_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreshold", []))

    @jsii.member(jsii_name="resetUniquenessExpectation")
    def reset_uniqueness_expectation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniquenessExpectation", []))

    @builtins.property
    @jsii.member(jsii_name="nonNullExpectation")
    def non_null_expectation(
        self,
    ) -> DataplexDatascanDataQualitySpecRulesNonNullExpectationOutputReference:
        return typing.cast(DataplexDatascanDataQualitySpecRulesNonNullExpectationOutputReference, jsii.get(self, "nonNullExpectation"))

    @builtins.property
    @jsii.member(jsii_name="rangeExpectation")
    def range_expectation(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesRangeExpectationOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesRangeExpectationOutputReference", jsii.get(self, "rangeExpectation"))

    @builtins.property
    @jsii.member(jsii_name="regexExpectation")
    def regex_expectation(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesRegexExpectationOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesRegexExpectationOutputReference", jsii.get(self, "regexExpectation"))

    @builtins.property
    @jsii.member(jsii_name="rowConditionExpectation")
    def row_condition_expectation(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesRowConditionExpectationOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesRowConditionExpectationOutputReference", jsii.get(self, "rowConditionExpectation"))

    @builtins.property
    @jsii.member(jsii_name="setExpectation")
    def set_expectation(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesSetExpectationOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesSetExpectationOutputReference", jsii.get(self, "setExpectation"))

    @builtins.property
    @jsii.member(jsii_name="sqlAssertion")
    def sql_assertion(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesSqlAssertionOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesSqlAssertionOutputReference", jsii.get(self, "sqlAssertion"))

    @builtins.property
    @jsii.member(jsii_name="statisticRangeExpectation")
    def statistic_range_expectation(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesStatisticRangeExpectationOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesStatisticRangeExpectationOutputReference", jsii.get(self, "statisticRangeExpectation"))

    @builtins.property
    @jsii.member(jsii_name="tableConditionExpectation")
    def table_condition_expectation(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesTableConditionExpectationOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesTableConditionExpectationOutputReference", jsii.get(self, "tableConditionExpectation"))

    @builtins.property
    @jsii.member(jsii_name="uniquenessExpectation")
    def uniqueness_expectation(
        self,
    ) -> "DataplexDatascanDataQualitySpecRulesUniquenessExpectationOutputReference":
        return typing.cast("DataplexDatascanDataQualitySpecRulesUniquenessExpectationOutputReference", jsii.get(self, "uniquenessExpectation"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreNullInput")
    def ignore_null_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreNullInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nonNullExpectationInput")
    def non_null_expectation_input(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesNonNullExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesNonNullExpectation], jsii.get(self, "nonNullExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeExpectationInput")
    def range_expectation_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesRangeExpectation"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesRangeExpectation"], jsii.get(self, "rangeExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="regexExpectationInput")
    def regex_expectation_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesRegexExpectation"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesRegexExpectation"], jsii.get(self, "regexExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="rowConditionExpectationInput")
    def row_condition_expectation_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesRowConditionExpectation"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesRowConditionExpectation"], jsii.get(self, "rowConditionExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="setExpectationInput")
    def set_expectation_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesSetExpectation"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesSetExpectation"], jsii.get(self, "setExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlAssertionInput")
    def sql_assertion_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesSqlAssertion"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesSqlAssertion"], jsii.get(self, "sqlAssertionInput"))

    @builtins.property
    @jsii.member(jsii_name="statisticRangeExpectationInput")
    def statistic_range_expectation_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation"], jsii.get(self, "statisticRangeExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedInput")
    def suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="tableConditionExpectationInput")
    def table_condition_expectation_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesTableConditionExpectation"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesTableConditionExpectation"], jsii.get(self, "tableConditionExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="uniquenessExpectationInput")
    def uniqueness_expectation_input(
        self,
    ) -> typing.Optional["DataplexDatascanDataQualitySpecRulesUniquenessExpectation"]:
        return typing.cast(typing.Optional["DataplexDatascanDataQualitySpecRulesUniquenessExpectation"], jsii.get(self, "uniquenessExpectationInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52047181638f5644a574c14b17beb5bcbd317c865a247170353629e24253f4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb23ab7d88a75e61957d4e61cb08f4a0b45265454a5c7ea30046bf8ae768712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimension"))

    @dimension.setter
    def dimension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3219e0e4a1b50219d834a5a5c8c86b7f2e3bf5d1b7729947b7f2f43cc78cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreNull")
    def ignore_null(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreNull"))

    @ignore_null.setter
    def ignore_null(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0451e96f8f545004f44b04e92b7597de8201970d6739ba14f933614cc2034f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreNull", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08cfc1422780d9cbd9366c99bc1217235ed3e6d081f7d2d9f1017a784dd8856a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspended")
    def suspended(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suspended"))

    @suspended.setter
    def suspended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c0d1ad516bc6b0bda5582bc9799e4f9ae3358990562ae1202cd6776f9da670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a5aa8d2de5e9e8af1810fecb00dff022dd56eb7064e652447ac2c9bc15697a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanDataQualitySpecRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanDataQualitySpecRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanDataQualitySpecRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ec6ab48b9f4324e4e1d654a33d91db63d358c80c0187abe2e74cc03952493d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesRangeExpectation",
    jsii_struct_bases=[],
    name_mapping={
        "max_value": "maxValue",
        "min_value": "minValue",
        "strict_max_enabled": "strictMaxEnabled",
        "strict_min_enabled": "strictMinEnabled",
    },
)
class DataplexDatascanDataQualitySpecRulesRangeExpectation:
    def __init__(
        self,
        *,
        max_value: typing.Optional[builtins.str] = None,
        min_value: typing.Optional[builtins.str] = None,
        strict_max_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict_min_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_value: The maximum column value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#max_value DataplexDatascan#max_value}
        :param min_value: The minimum column value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#min_value DataplexDatascan#min_value}
        :param strict_max_enabled: Whether each value needs to be strictly lesser than ('<') the maximum, or if equality is allowed. Only relevant if a maxValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_max_enabled DataplexDatascan#strict_max_enabled}
        :param strict_min_enabled: Whether each value needs to be strictly greater than ('>') the minimum, or if equality is allowed. Only relevant if a minValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_min_enabled DataplexDatascan#strict_min_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6bc64dcf4f7f09f45fe73068b2c630074f63d470317245ba2a680d12c56c1d)
            check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
            check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
            check_type(argname="argument strict_max_enabled", value=strict_max_enabled, expected_type=type_hints["strict_max_enabled"])
            check_type(argname="argument strict_min_enabled", value=strict_min_enabled, expected_type=type_hints["strict_min_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_value is not None:
            self._values["max_value"] = max_value
        if min_value is not None:
            self._values["min_value"] = min_value
        if strict_max_enabled is not None:
            self._values["strict_max_enabled"] = strict_max_enabled
        if strict_min_enabled is not None:
            self._values["strict_min_enabled"] = strict_min_enabled

    @builtins.property
    def max_value(self) -> typing.Optional[builtins.str]:
        '''The maximum column value allowed for a row to pass this validation.

        At least one of minValue and maxValue need to be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#max_value DataplexDatascan#max_value}
        '''
        result = self._values.get("max_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_value(self) -> typing.Optional[builtins.str]:
        '''The minimum column value allowed for a row to pass this validation.

        At least one of minValue and maxValue need to be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#min_value DataplexDatascan#min_value}
        '''
        result = self._values.get("min_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict_max_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether each value needs to be strictly lesser than ('<') the maximum, or if equality is allowed.

        Only relevant if a maxValue has been defined. Default = false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_max_enabled DataplexDatascan#strict_max_enabled}
        '''
        result = self._values.get("strict_max_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def strict_min_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether each value needs to be strictly greater than ('>') the minimum, or if equality is allowed.

        Only relevant if a minValue has been defined. Default = false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_min_enabled DataplexDatascan#strict_min_enabled}
        '''
        result = self._values.get("strict_min_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesRangeExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesRangeExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesRangeExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__759703238b5b0d1a3835089c0c71204d63a6a31f39c97f57b9ced2d8536fcec5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxValue")
    def reset_max_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxValue", []))

    @jsii.member(jsii_name="resetMinValue")
    def reset_min_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinValue", []))

    @jsii.member(jsii_name="resetStrictMaxEnabled")
    def reset_strict_max_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictMaxEnabled", []))

    @jsii.member(jsii_name="resetStrictMinEnabled")
    def reset_strict_min_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictMinEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="maxValueInput")
    def max_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxValueInput"))

    @builtins.property
    @jsii.member(jsii_name="minValueInput")
    def min_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minValueInput"))

    @builtins.property
    @jsii.member(jsii_name="strictMaxEnabledInput")
    def strict_max_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictMaxEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="strictMinEnabledInput")
    def strict_min_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictMinEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxValue")
    def max_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxValue"))

    @max_value.setter
    def max_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3a9026c0215202dca02914dbdaa9cf1d2792ce6001755eb136f5a85b737005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minValue")
    def min_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minValue"))

    @min_value.setter
    def min_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12abae15248ea3615e37306659e5bf80f36d56a94fb5f11a4e5f9865a2e4fbe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictMaxEnabled")
    def strict_max_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictMaxEnabled"))

    @strict_max_enabled.setter
    def strict_max_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a607fdaebb39b605219715663624e6bb2c3d5633dfd296aa771d67393d120d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictMaxEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictMinEnabled")
    def strict_min_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictMinEnabled"))

    @strict_min_enabled.setter
    def strict_min_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e94da435a3316245418a11abcd0fbaa1ee9ae6201fcb4e8e3876ecacb7bcd8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictMinEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesRangeExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesRangeExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesRangeExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8c6819f966ceef61ffa34b5a8788e0b0d240d62390c25fb4062afd194442e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesRegexExpectation",
    jsii_struct_bases=[],
    name_mapping={"regex": "regex"},
)
class DataplexDatascanDataQualitySpecRulesRegexExpectation:
    def __init__(self, *, regex: builtins.str) -> None:
        '''
        :param regex: A regular expression the column value is expected to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#regex DataplexDatascan#regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d572b0255331e03ccc7577a2e8133353b531f411231808b1ded5ae16b165b4)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "regex": regex,
        }

    @builtins.property
    def regex(self) -> builtins.str:
        '''A regular expression the column value is expected to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#regex DataplexDatascan#regex}
        '''
        result = self._values.get("regex")
        assert result is not None, "Required property 'regex' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesRegexExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesRegexExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesRegexExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__313b8a8891714003d03503677cfc9b8524bd53fb35f1155a99087a85f8efc796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea7c94bcdcae17875c5316055b54fa0200d0acf73f6a57c123789689f8d3b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesRegexExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesRegexExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesRegexExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475a09c26a9b7d34550a970d0233670a5fa5e0e0a026dc50558962b1e466798c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesRowConditionExpectation",
    jsii_struct_bases=[],
    name_mapping={"sql_expression": "sqlExpression"},
)
class DataplexDatascanDataQualitySpecRulesRowConditionExpectation:
    def __init__(self, *, sql_expression: builtins.str) -> None:
        '''
        :param sql_expression: The SQL expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_expression DataplexDatascan#sql_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ad4aba19ee0e8a72b9600566e5aaab50eea58d6fee6f1451b2210ceb858889)
            check_type(argname="argument sql_expression", value=sql_expression, expected_type=type_hints["sql_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sql_expression": sql_expression,
        }

    @builtins.property
    def sql_expression(self) -> builtins.str:
        '''The SQL expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_expression DataplexDatascan#sql_expression}
        '''
        result = self._values.get("sql_expression")
        assert result is not None, "Required property 'sql_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesRowConditionExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesRowConditionExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesRowConditionExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3585d17a97171b4d2226f21863be39b6882b7880be852b3f36abced064cf6885)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sqlExpressionInput")
    def sql_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlExpression")
    def sql_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlExpression"))

    @sql_expression.setter
    def sql_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45d7af9028a72e0eff6f708fd474122a85a1bdf0b78cfe2b3594c326683ac34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesRowConditionExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesRowConditionExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesRowConditionExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425e669bfd65f764df50ea8c0778b1c2b453198f2008d3836d8a38bdcde536cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesSetExpectation",
    jsii_struct_bases=[],
    name_mapping={"values": "values"},
)
class DataplexDatascanDataQualitySpecRulesSetExpectation:
    def __init__(self, *, values: typing.Sequence[builtins.str]) -> None:
        '''
        :param values: Expected values for the column value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#values DataplexDatascan#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c87bedf5b64085ec94bb7706f878c3c3db008d4c783a265f2009ba8315299b5)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "values": values,
        }

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Expected values for the column value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#values DataplexDatascan#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesSetExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesSetExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesSetExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6c453804a5e391cf62b798b805cb0df27c2e26acbcc062035dfd93abe6627de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a2f911fa1c82f4b1c82be1cfd5e1d6013c3e1f95a73ba511aa8cf3756dc060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesSetExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesSetExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesSetExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2d8295163aa80ea21d497e6a6bfd05b2c03c9fa074f40dbbc0de90a8cdc1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesSqlAssertion",
    jsii_struct_bases=[],
    name_mapping={"sql_statement": "sqlStatement"},
)
class DataplexDatascanDataQualitySpecRulesSqlAssertion:
    def __init__(self, *, sql_statement: builtins.str) -> None:
        '''
        :param sql_statement: The SQL statement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_statement DataplexDatascan#sql_statement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bd6f171a68226cd104b0d34ba5b2d66637becdf96cfe795b206c7be325ff85)
            check_type(argname="argument sql_statement", value=sql_statement, expected_type=type_hints["sql_statement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sql_statement": sql_statement,
        }

    @builtins.property
    def sql_statement(self) -> builtins.str:
        '''The SQL statement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_statement DataplexDatascan#sql_statement}
        '''
        result = self._values.get("sql_statement")
        assert result is not None, "Required property 'sql_statement' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesSqlAssertion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesSqlAssertionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesSqlAssertionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d427eec99831b7fa2fee90ae42e28797a581a118f26aba4735888037508f128)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sqlStatementInput")
    def sql_statement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlStatementInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlStatement")
    def sql_statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlStatement"))

    @sql_statement.setter
    def sql_statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec36870b84fd447e196b041fdb6f366477ed3853e700e629138a6adfa56e997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlStatement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesSqlAssertion]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesSqlAssertion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesSqlAssertion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999cfa12b89a94b66f663d853074141775d5f6551afde4dcab499e11364ace6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation",
    jsii_struct_bases=[],
    name_mapping={
        "statistic": "statistic",
        "max_value": "maxValue",
        "min_value": "minValue",
        "strict_max_enabled": "strictMaxEnabled",
        "strict_min_enabled": "strictMinEnabled",
    },
)
class DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation:
    def __init__(
        self,
        *,
        statistic: builtins.str,
        max_value: typing.Optional[builtins.str] = None,
        min_value: typing.Optional[builtins.str] = None,
        strict_max_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict_min_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param statistic: column statistics. Possible values: ["STATISTIC_UNDEFINED", "MEAN", "MIN", "MAX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#statistic DataplexDatascan#statistic}
        :param max_value: The maximum column statistic value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#max_value DataplexDatascan#max_value}
        :param min_value: The minimum column statistic value allowed for a row to pass this validation. At least one of minValue and maxValue need to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#min_value DataplexDatascan#min_value}
        :param strict_max_enabled: Whether column statistic needs to be strictly lesser than ('<') the maximum, or if equality is allowed. Only relevant if a maxValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_max_enabled DataplexDatascan#strict_max_enabled}
        :param strict_min_enabled: Whether column statistic needs to be strictly greater than ('>') the minimum, or if equality is allowed. Only relevant if a minValue has been defined. Default = false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_min_enabled DataplexDatascan#strict_min_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0a5aa73adb2ee9583a2361bd732522f3b3dc6d97169e30893463bb70d70b15)
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
            check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
            check_type(argname="argument strict_max_enabled", value=strict_max_enabled, expected_type=type_hints["strict_max_enabled"])
            check_type(argname="argument strict_min_enabled", value=strict_min_enabled, expected_type=type_hints["strict_min_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "statistic": statistic,
        }
        if max_value is not None:
            self._values["max_value"] = max_value
        if min_value is not None:
            self._values["min_value"] = min_value
        if strict_max_enabled is not None:
            self._values["strict_max_enabled"] = strict_max_enabled
        if strict_min_enabled is not None:
            self._values["strict_min_enabled"] = strict_min_enabled

    @builtins.property
    def statistic(self) -> builtins.str:
        '''column statistics. Possible values: ["STATISTIC_UNDEFINED", "MEAN", "MIN", "MAX"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#statistic DataplexDatascan#statistic}
        '''
        result = self._values.get("statistic")
        assert result is not None, "Required property 'statistic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_value(self) -> typing.Optional[builtins.str]:
        '''The maximum column statistic value allowed for a row to pass this validation.

        At least one of minValue and maxValue need to be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#max_value DataplexDatascan#max_value}
        '''
        result = self._values.get("max_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_value(self) -> typing.Optional[builtins.str]:
        '''The minimum column statistic value allowed for a row to pass this validation.

        At least one of minValue and maxValue need to be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#min_value DataplexDatascan#min_value}
        '''
        result = self._values.get("min_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict_max_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether column statistic needs to be strictly lesser than ('<') the maximum, or if equality is allowed.

        Only relevant if a maxValue has been defined. Default = false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_max_enabled DataplexDatascan#strict_max_enabled}
        '''
        result = self._values.get("strict_max_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def strict_min_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether column statistic needs to be strictly greater than ('>') the minimum, or if equality is allowed.

        Only relevant if a minValue has been defined. Default = false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#strict_min_enabled DataplexDatascan#strict_min_enabled}
        '''
        result = self._values.get("strict_min_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesStatisticRangeExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesStatisticRangeExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975d32301b3563a6ee53e9ea35860ae76ed71a942de71dfa2f6539a64db59acf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxValue")
    def reset_max_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxValue", []))

    @jsii.member(jsii_name="resetMinValue")
    def reset_min_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinValue", []))

    @jsii.member(jsii_name="resetStrictMaxEnabled")
    def reset_strict_max_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictMaxEnabled", []))

    @jsii.member(jsii_name="resetStrictMinEnabled")
    def reset_strict_min_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictMinEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="maxValueInput")
    def max_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxValueInput"))

    @builtins.property
    @jsii.member(jsii_name="minValueInput")
    def min_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minValueInput"))

    @builtins.property
    @jsii.member(jsii_name="statisticInput")
    def statistic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statisticInput"))

    @builtins.property
    @jsii.member(jsii_name="strictMaxEnabledInput")
    def strict_max_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictMaxEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="strictMinEnabledInput")
    def strict_min_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictMinEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxValue")
    def max_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxValue"))

    @max_value.setter
    def max_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1b9df4f4acbe6c8c40f4e9a180a2ab96e1f5fcec945af5072b185516903aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minValue")
    def min_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minValue"))

    @min_value.setter
    def min_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd93fc38c3669a133ebb7fe4b55bc4c608e5c09ea6d4a01fab510b4abe81a5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statistic"))

    @statistic.setter
    def statistic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ba00dbd43a80b645f71245295ea4290c2b02aaee0c8cee01a0f43db50082b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statistic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictMaxEnabled")
    def strict_max_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictMaxEnabled"))

    @strict_max_enabled.setter
    def strict_max_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d8d81305355619bc8c44b1303a525b01949934c01a2dc69651734abefe3832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictMaxEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictMinEnabled")
    def strict_min_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictMinEnabled"))

    @strict_min_enabled.setter
    def strict_min_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797c434697eb4e4d61ac5116af34212ab463c6c087edf28e28e77db13e64ef3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictMinEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929fa9c246994fdaef6c453521d03b51cef32b3868bf3fbfdafe7e012a19ac75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesTableConditionExpectation",
    jsii_struct_bases=[],
    name_mapping={"sql_expression": "sqlExpression"},
)
class DataplexDatascanDataQualitySpecRulesTableConditionExpectation:
    def __init__(self, *, sql_expression: builtins.str) -> None:
        '''
        :param sql_expression: The SQL expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_expression DataplexDatascan#sql_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ef359ae5fae4724bfb144183e476594f79a5dae9d5269f2e5521757e32582a)
            check_type(argname="argument sql_expression", value=sql_expression, expected_type=type_hints["sql_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sql_expression": sql_expression,
        }

    @builtins.property
    def sql_expression(self) -> builtins.str:
        '''The SQL expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#sql_expression DataplexDatascan#sql_expression}
        '''
        result = self._values.get("sql_expression")
        assert result is not None, "Required property 'sql_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesTableConditionExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesTableConditionExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesTableConditionExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08943a8e396992a3a68166c3b89eec5abd11c659b0b2c0f9a27306d8e06d7045)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sqlExpressionInput")
    def sql_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlExpression")
    def sql_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlExpression"))

    @sql_expression.setter
    def sql_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfd3f38bb494bd76daa96d507b86916e2a785b837cbe1a229f9429e91a57c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesTableConditionExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesTableConditionExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesTableConditionExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e31bc4a5a6ae2fb8b6909bf2677b8a9dbbe5dfc9d72e326032091ffba8c647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesUniquenessExpectation",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexDatascanDataQualitySpecRulesUniquenessExpectation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanDataQualitySpecRulesUniquenessExpectation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanDataQualitySpecRulesUniquenessExpectationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanDataQualitySpecRulesUniquenessExpectationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1806639908e2ddc758362aa1e6b7f35a6ad9f71c0d825ddc17056bd3ed079e19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanDataQualitySpecRulesUniquenessExpectation]:
        return typing.cast(typing.Optional[DataplexDatascanDataQualitySpecRulesUniquenessExpectation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanDataQualitySpecRulesUniquenessExpectation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff4cf9f9fe5e2387d40e51e7f1aac3f3b985dc5b2583111a77deeb60b231af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpec",
    jsii_struct_bases=[],
    name_mapping={"trigger": "trigger", "field": "field"},
)
class DataplexDatascanExecutionSpec:
    def __init__(
        self,
        *,
        trigger: typing.Union["DataplexDatascanExecutionSpecTrigger", typing.Dict[builtins.str, typing.Any]],
        field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#trigger DataplexDatascan#trigger}
        :param field: The unnested field (of type Date or Timestamp) that contains values which monotonically increase over time. If not specified, a data scan will run for all data in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field DataplexDatascan#field}
        '''
        if isinstance(trigger, dict):
            trigger = DataplexDatascanExecutionSpecTrigger(**trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8cc75270233134533a2ebea3761c0c9afbb2d5df361fc03ffa6e43a7424dbd)
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger": trigger,
        }
        if field is not None:
            self._values["field"] = field

    @builtins.property
    def trigger(self) -> "DataplexDatascanExecutionSpecTrigger":
        '''trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#trigger DataplexDatascan#trigger}
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast("DataplexDatascanExecutionSpecTrigger", result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''The unnested field (of type Date or Timestamp) that contains values which monotonically increase over time.

        If not specified, a data scan will run for all data in the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#field DataplexDatascan#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanExecutionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanExecutionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b46009e0440d7a7f337ba02f1c1aeda149ef4674d2c0c6cba5eb415cd9b33213)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        *,
        on_demand: typing.Optional[typing.Union["DataplexDatascanExecutionSpecTriggerOnDemand", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["DataplexDatascanExecutionSpecTriggerSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_demand: on_demand block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#on_demand DataplexDatascan#on_demand}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#schedule DataplexDatascan#schedule}
        '''
        value = DataplexDatascanExecutionSpecTrigger(
            on_demand=on_demand, schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> "DataplexDatascanExecutionSpecTriggerOutputReference":
        return typing.cast("DataplexDatascanExecutionSpecTriggerOutputReference", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(self) -> typing.Optional["DataplexDatascanExecutionSpecTrigger"]:
        return typing.cast(typing.Optional["DataplexDatascanExecutionSpecTrigger"], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e92371b04ff583d035d6fb435a3214c481e4f7b1ae8902310ca5ba4db9bb033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexDatascanExecutionSpec]:
        return typing.cast(typing.Optional[DataplexDatascanExecutionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanExecutionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40fcbea972db179740b8bbc2b444e7b2522f997b90d8da3644ae0cd870bab1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpecTrigger",
    jsii_struct_bases=[],
    name_mapping={"on_demand": "onDemand", "schedule": "schedule"},
)
class DataplexDatascanExecutionSpecTrigger:
    def __init__(
        self,
        *,
        on_demand: typing.Optional[typing.Union["DataplexDatascanExecutionSpecTriggerOnDemand", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["DataplexDatascanExecutionSpecTriggerSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_demand: on_demand block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#on_demand DataplexDatascan#on_demand}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#schedule DataplexDatascan#schedule}
        '''
        if isinstance(on_demand, dict):
            on_demand = DataplexDatascanExecutionSpecTriggerOnDemand(**on_demand)
        if isinstance(schedule, dict):
            schedule = DataplexDatascanExecutionSpecTriggerSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c326eb32426671157f23411fe7d5d60e206383138a9d0609e6b56135a5c8f47)
            check_type(argname="argument on_demand", value=on_demand, expected_type=type_hints["on_demand"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_demand is not None:
            self._values["on_demand"] = on_demand
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def on_demand(
        self,
    ) -> typing.Optional["DataplexDatascanExecutionSpecTriggerOnDemand"]:
        '''on_demand block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#on_demand DataplexDatascan#on_demand}
        '''
        result = self._values.get("on_demand")
        return typing.cast(typing.Optional["DataplexDatascanExecutionSpecTriggerOnDemand"], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional["DataplexDatascanExecutionSpecTriggerSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#schedule DataplexDatascan#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["DataplexDatascanExecutionSpecTriggerSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanExecutionSpecTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpecTriggerOnDemand",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexDatascanExecutionSpecTriggerOnDemand:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanExecutionSpecTriggerOnDemand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanExecutionSpecTriggerOnDemandOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpecTriggerOnDemandOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e79b2992d91166f552b247e99d167026617ab696a992286451173260fe7d8474)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanExecutionSpecTriggerOnDemand]:
        return typing.cast(typing.Optional[DataplexDatascanExecutionSpecTriggerOnDemand], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanExecutionSpecTriggerOnDemand],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac2dd2832e47bbd25099eab7c46c2998bc0dc3b1ee32223be731361b5edf70f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanExecutionSpecTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpecTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af631a52da0b6f9c9527a1b4b147459b15214714a82a7fe79c65d4471218fc3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOnDemand")
    def put_on_demand(self) -> None:
        value = DataplexDatascanExecutionSpecTriggerOnDemand()

        return typing.cast(None, jsii.invoke(self, "putOnDemand", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(self, *, cron: builtins.str) -> None:
        '''
        :param cron: Cron schedule for running scans periodically. This field is required for Schedule scans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#cron DataplexDatascan#cron}
        '''
        value = DataplexDatascanExecutionSpecTriggerSchedule(cron=cron)

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetOnDemand")
    def reset_on_demand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDemand", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="onDemand")
    def on_demand(self) -> DataplexDatascanExecutionSpecTriggerOnDemandOutputReference:
        return typing.cast(DataplexDatascanExecutionSpecTriggerOnDemandOutputReference, jsii.get(self, "onDemand"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "DataplexDatascanExecutionSpecTriggerScheduleOutputReference":
        return typing.cast("DataplexDatascanExecutionSpecTriggerScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="onDemandInput")
    def on_demand_input(
        self,
    ) -> typing.Optional[DataplexDatascanExecutionSpecTriggerOnDemand]:
        return typing.cast(typing.Optional[DataplexDatascanExecutionSpecTriggerOnDemand], jsii.get(self, "onDemandInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["DataplexDatascanExecutionSpecTriggerSchedule"]:
        return typing.cast(typing.Optional["DataplexDatascanExecutionSpecTriggerSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexDatascanExecutionSpecTrigger]:
        return typing.cast(typing.Optional[DataplexDatascanExecutionSpecTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanExecutionSpecTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf68f8ce2d89be025bfa54077b2ff8e615d4e89bb13858f171ab866b8344e0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpecTriggerSchedule",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class DataplexDatascanExecutionSpecTriggerSchedule:
    def __init__(self, *, cron: builtins.str) -> None:
        '''
        :param cron: Cron schedule for running scans periodically. This field is required for Schedule scans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#cron DataplexDatascan#cron}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67af15409251f4fe8b14154bb5d82fdb50d31d9078d511db381dcf238b8fa15)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cron": cron,
        }

    @builtins.property
    def cron(self) -> builtins.str:
        '''Cron schedule for running scans periodically. This field is required for Schedule scans.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#cron DataplexDatascan#cron}
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanExecutionSpecTriggerSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanExecutionSpecTriggerScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionSpecTriggerScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76342835417c2ba3b6449ce682bbebb8a2bf2f1e3c01282eb313f49e2063f2b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cronInput")
    def cron_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronInput"))

    @builtins.property
    @jsii.member(jsii_name="cron")
    def cron(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cron"))

    @cron.setter
    def cron(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0560f70824c04198cb1c6efe514a1edcc969529b4c7285ac0b6408ad207e74ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexDatascanExecutionSpecTriggerSchedule]:
        return typing.cast(typing.Optional[DataplexDatascanExecutionSpecTriggerSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanExecutionSpecTriggerSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5a250d239b798f9e07fc500c4cff6fdc847eb63081f3fed168948a965eb84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexDatascanExecutionStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanExecutionStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanExecutionStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18f4fbf3a2ab3da0c905c4e58173fc4aced91b7399146dfe3b5367bbea675f0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataplexDatascanExecutionStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85987651862b400eaca66b701c273e12846f41884c31ab1a05b6f8c18b676cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexDatascanExecutionStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf2820c64604b40cc3bede32da2b19364b4e5c3ba5617ad55fb7926fc5c3f67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61ffac7a646f442a9ab8409e62881bd3b8ea38b79aeb4db8cd3003391e9b37cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ec82fea6381ea48ecc94c1532c1f83b291ec95209592f4f3bcbcf7d128cfca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexDatascanExecutionStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanExecutionStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__908b95b79615cb54c32444bd58ba85e978ba45d0b741ea925d37c6a1dec91b6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="latestJobEndTime")
    def latest_job_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestJobEndTime"))

    @builtins.property
    @jsii.member(jsii_name="latestJobStartTime")
    def latest_job_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestJobStartTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexDatascanExecutionStatus]:
        return typing.cast(typing.Optional[DataplexDatascanExecutionStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexDatascanExecutionStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f44f24f13e6510f286786aee0fb68c01f6252572210f6ee6e372508451dc349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataplexDatascanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#create DataplexDatascan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#delete DataplexDatascan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#update DataplexDatascan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9e767d17707360c1f5acec92641a1b9725c17bdddb5bfad21942bfaa7be421)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#create DataplexDatascan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#delete DataplexDatascan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_datascan#update DataplexDatascan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexDatascanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexDatascanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexDatascan.DataplexDatascanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27eac39fe10f76a66c07edab1599b9046c39a7d5462689d4ec4f346fa3a2785f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05e92ea2645f7fa6de5fe8cd3bd752a775b1a082f40ef49810a63b50b2bad12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e692111a9603c4e81b1372ce4c8f4cd634021ee01e658a668b2dd253e5390d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810f491654b4a796e2f9b5140e9ea1fe070ade83544bd5eea65c50a34babf380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeace9f1ee313460a947488670405a304c37c3925c7e0d8985b31cd695c84412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataplexDatascan",
    "DataplexDatascanConfig",
    "DataplexDatascanData",
    "DataplexDatascanDataDiscoverySpec",
    "DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig",
    "DataplexDatascanDataDiscoverySpecBigqueryPublishingConfigOutputReference",
    "DataplexDatascanDataDiscoverySpecOutputReference",
    "DataplexDatascanDataDiscoverySpecStorageConfig",
    "DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions",
    "DataplexDatascanDataDiscoverySpecStorageConfigCsvOptionsOutputReference",
    "DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions",
    "DataplexDatascanDataDiscoverySpecStorageConfigJsonOptionsOutputReference",
    "DataplexDatascanDataDiscoverySpecStorageConfigOutputReference",
    "DataplexDatascanDataOutputReference",
    "DataplexDatascanDataProfileSpec",
    "DataplexDatascanDataProfileSpecExcludeFields",
    "DataplexDatascanDataProfileSpecExcludeFieldsOutputReference",
    "DataplexDatascanDataProfileSpecIncludeFields",
    "DataplexDatascanDataProfileSpecIncludeFieldsOutputReference",
    "DataplexDatascanDataProfileSpecOutputReference",
    "DataplexDatascanDataProfileSpecPostScanActions",
    "DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport",
    "DataplexDatascanDataProfileSpecPostScanActionsBigqueryExportOutputReference",
    "DataplexDatascanDataProfileSpecPostScanActionsOutputReference",
    "DataplexDatascanDataQualitySpec",
    "DataplexDatascanDataQualitySpecOutputReference",
    "DataplexDatascanDataQualitySpecPostScanActions",
    "DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport",
    "DataplexDatascanDataQualitySpecPostScanActionsBigqueryExportOutputReference",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReport",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTriggerOutputReference",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTriggerOutputReference",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportOutputReference",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipientsOutputReference",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger",
    "DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTriggerOutputReference",
    "DataplexDatascanDataQualitySpecPostScanActionsOutputReference",
    "DataplexDatascanDataQualitySpecRules",
    "DataplexDatascanDataQualitySpecRulesList",
    "DataplexDatascanDataQualitySpecRulesNonNullExpectation",
    "DataplexDatascanDataQualitySpecRulesNonNullExpectationOutputReference",
    "DataplexDatascanDataQualitySpecRulesOutputReference",
    "DataplexDatascanDataQualitySpecRulesRangeExpectation",
    "DataplexDatascanDataQualitySpecRulesRangeExpectationOutputReference",
    "DataplexDatascanDataQualitySpecRulesRegexExpectation",
    "DataplexDatascanDataQualitySpecRulesRegexExpectationOutputReference",
    "DataplexDatascanDataQualitySpecRulesRowConditionExpectation",
    "DataplexDatascanDataQualitySpecRulesRowConditionExpectationOutputReference",
    "DataplexDatascanDataQualitySpecRulesSetExpectation",
    "DataplexDatascanDataQualitySpecRulesSetExpectationOutputReference",
    "DataplexDatascanDataQualitySpecRulesSqlAssertion",
    "DataplexDatascanDataQualitySpecRulesSqlAssertionOutputReference",
    "DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation",
    "DataplexDatascanDataQualitySpecRulesStatisticRangeExpectationOutputReference",
    "DataplexDatascanDataQualitySpecRulesTableConditionExpectation",
    "DataplexDatascanDataQualitySpecRulesTableConditionExpectationOutputReference",
    "DataplexDatascanDataQualitySpecRulesUniquenessExpectation",
    "DataplexDatascanDataQualitySpecRulesUniquenessExpectationOutputReference",
    "DataplexDatascanExecutionSpec",
    "DataplexDatascanExecutionSpecOutputReference",
    "DataplexDatascanExecutionSpecTrigger",
    "DataplexDatascanExecutionSpecTriggerOnDemand",
    "DataplexDatascanExecutionSpecTriggerOnDemandOutputReference",
    "DataplexDatascanExecutionSpecTriggerOutputReference",
    "DataplexDatascanExecutionSpecTriggerSchedule",
    "DataplexDatascanExecutionSpecTriggerScheduleOutputReference",
    "DataplexDatascanExecutionStatus",
    "DataplexDatascanExecutionStatusList",
    "DataplexDatascanExecutionStatusOutputReference",
    "DataplexDatascanTimeouts",
    "DataplexDatascanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f7d978d3a14103b3ef12c1f35fc9a0641f3a0e983ba57bcdb6a7dd8fa7392d37(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data: typing.Union[DataplexDatascanData, typing.Dict[builtins.str, typing.Any]],
    data_scan_id: builtins.str,
    execution_spec: typing.Union[DataplexDatascanExecutionSpec, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    data_discovery_spec: typing.Optional[typing.Union[DataplexDatascanDataDiscoverySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    data_profile_spec: typing.Optional[typing.Union[DataplexDatascanDataProfileSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    data_quality_spec: typing.Optional[typing.Union[DataplexDatascanDataQualitySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexDatascanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__79426be3928dab88c96febb41f5a5cf41f97167357d7fd4c1ff34fc7df5d0c90(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e599fb759e13751ed4e9d77184f41e10d6c3e05dc3490fedfd53a40515ed90d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9177039bf399af0070309fe327788cbf0f4a3ba85ca45b30ca264e3821ebe69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acddc10756adbd43ebd70f29476a8202acf88a6d91e235c4ceb847ca2e99d1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01402634ddabb6c346b4cb2c18c6624021a009b09431401735ca8c1d779f9d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f3d64f33812a62d780f892003e5f8802daa4860abf27562a4a358eb53e212c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8453c5d69cbc241fd463cde478b1c8b4320b9f09468b4be2f475d7f47adcc2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6e3f10a1999fb9aa8f39e401feeeb6b48be2e9b7d28ede14ab07b3a7571f19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59b584f3c2ab4707c1e0552da13804a76b02aef972499ba94c6adac30ad061a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data: typing.Union[DataplexDatascanData, typing.Dict[builtins.str, typing.Any]],
    data_scan_id: builtins.str,
    execution_spec: typing.Union[DataplexDatascanExecutionSpec, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    data_discovery_spec: typing.Optional[typing.Union[DataplexDatascanDataDiscoverySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    data_profile_spec: typing.Optional[typing.Union[DataplexDatascanDataProfileSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    data_quality_spec: typing.Optional[typing.Union[DataplexDatascanDataQualitySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexDatascanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887b51eb9dc74c5797b8b0d833c1f65c3c1c65e4e91004ea510fa663bde76d5d(
    *,
    entity: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a941c0030179ccbc60700b68120ec74c77aab2dfa6e4864727b01225fb639c15(
    *,
    bigquery_publishing_config: typing.Optional[typing.Union[DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_config: typing.Optional[typing.Union[DataplexDatascanDataDiscoverySpecStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536b9cfd09a6268ad88ae10e29aaf044d866cd2e80160e1588a8bb1ab33e728f(
    *,
    connection: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    table_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803774bfad0a4bc28839bbd88c07261e9e19a6069bc88286c8a0f3c923090d49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d773a76393b1e670bb8dba04fe66b8d269935ebde00da0f8823ddca69475f30b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3e0c2e32ce9f6a72f0a5d103157e9af243f4a66edb22484abcf0f23f665982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53fe3ad89fb88260be8b7cbc2d5d13cb3e80f9d2835d84ee1de8965e545d73b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249ae6b737fbf6f8346ba709f7e2ef1c5cf2c0b4714bcabeef397a3cdea83853(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8a617005d9dcff9f732e58114a23820e6d0b7f3018077e846f8b9503d563b4(
    value: typing.Optional[DataplexDatascanDataDiscoverySpecBigqueryPublishingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4f845937cc2789fe26b104a37067ac447c2bd83113daf3f2badf5ea4944bf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6972dc10e679f84106050b855fc71fe1e37d799bcf8ecf4f1838cb0c8f4248e(
    value: typing.Optional[DataplexDatascanDataDiscoverySpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0fdc670747f0bc0893fbf643e659bf559fd9c0237b856286b0d90e7da25aae(
    *,
    csv_options: typing.Optional[typing.Union[DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_options: typing.Optional[typing.Union[DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2718cb44b7122d0b4191c453c2cfc2d7f47e1d4f1eb2472307e703cee78c79(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[builtins.str] = None,
    header_rows: typing.Optional[jsii.Number] = None,
    quote: typing.Optional[builtins.str] = None,
    type_inference_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb023934ba7711d76022197021c85d06614b5da3bcc2d7c34b699d7656586fae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3885bab5067f5700c9639dc06f15fd582f7049784ff53b4a98639f34a53de5f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5fe1cf9734c37af90c6c172860c19940d636bbbcfafb30a964432ff9d76071(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67424a1680eedabc8bdaa6bc2abef4e1807166e1f837124cc4b7c23ab33941f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c26ff7b2b1ddaaccfdc1b5fb5b750dd06e39e40ef9474cf341f1e6d047df449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965d24242984ce0a96e27587751a1a12d918d9f00061075b126cf78e37c96f87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc029051bed29523ac2fbc611f63560483f7a1b4087450cf9a1fe7676a4af042(
    value: typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigCsvOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6d83a25a17a2a2bc50d5c5aa6696013f9f6c2cb474e72eec88c4be20f75ee9(
    *,
    encoding: typing.Optional[builtins.str] = None,
    type_inference_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4452c32dcc21475c8eb94d5fcfc78e65571cfbb8a129e82012e8786bc556d13d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40abab90cd182f29c5912232d099a40a2586a36952f2e83a474b3c6bc4bc356f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7427aac116f15901bd921c62a5cfaa0c07ddbdaee89564a4433d35307829a037(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66020970399977943c6fb8ec63da0db1978a7397886da70a1de153fb622a4764(
    value: typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfigJsonOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91418feb6e952ba20e3661b3ba2b497372e4bb56bec2f237ccfd25e1611ebd56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b582a869c6693ed5d8c5f5747594bfc0b4503f2e653c8cd95e0beacede91aacb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7019cd9b411c1c00ec2baa5471e65abb57db72b0aacbbb0de0abc7b904f1fac7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20e9f97ba110b68631183bf473ed0fc78d0a808269d4b356eb0474adfa3f319(
    value: typing.Optional[DataplexDatascanDataDiscoverySpecStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d07a3087d95dce1b616a931956230cfd53d601f3db40f9da601a820db8924c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8b1ee53c0d22ea8df64f3ec598e967dc156a10fed885a0f729cf7f651bdf06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d02c9fc495878cbebd90c932cc5aeefd43e50d9834c4799b71ac8a184cf05d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecfe3da18a82a79c7d4e90e51f374b6340929ff8062d6c77258151ec9f7f51a(
    value: typing.Optional[DataplexDatascanData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97359cc1586f9deb4de9c7e12f4682dac9e7dd4d4fca628be49da0ff075b12f8(
    *,
    exclude_fields: typing.Optional[typing.Union[DataplexDatascanDataProfileSpecExcludeFields, typing.Dict[builtins.str, typing.Any]]] = None,
    include_fields: typing.Optional[typing.Union[DataplexDatascanDataProfileSpecIncludeFields, typing.Dict[builtins.str, typing.Any]]] = None,
    post_scan_actions: typing.Optional[typing.Union[DataplexDatascanDataProfileSpecPostScanActions, typing.Dict[builtins.str, typing.Any]]] = None,
    row_filter: typing.Optional[builtins.str] = None,
    sampling_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317b91e781a70d6fad6013a374886068dda8ff121929bec9c8d0657b1c3d5c9d(
    *,
    field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab82f93c5b430d1788ef410438ff3eab940d106ffbb978fe7152cc4d80febe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdcac021b9965491bda49fa6b9d1406131d6d600cb12123b8c19c44c5395a09(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514fe3bbc8323bba64096b62898c41318dc3be0ce5781178f037e79d6403a6cc(
    value: typing.Optional[DataplexDatascanDataProfileSpecExcludeFields],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cc9d674cdfa8f3c1724cafe1f5a3fb480acc9c68cd6b5ddd424cfed9fa399f(
    *,
    field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d1fb585271177c44c468dd93dcad4ad5389daaec077cbe2bbb1992aaa20e28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90af2e7104018dd67faba658bf81aa1f23ddf543605d7aae58e7263e7ce1311a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4137798a894c7cadf23b6e98b2ce6982be340029ba4d8aac394476d64d9cc3(
    value: typing.Optional[DataplexDatascanDataProfileSpecIncludeFields],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249c1b17060819390364350da4fc04f801484cad1eea5c334ddd06a25e947453(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7258d6e996ed8fc69dfd98fa4ea5915f2f62b8f0221713857a361f4c50a1f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3d642e4e66f780a58eed116cc3f089bd8e13713e1e836c1f427d6ea4b8edd6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ebfe7dbf82ace6f2dc587fc4a14e5eef3cdbe8a0d7af1cf282b0ec0e78fdba(
    value: typing.Optional[DataplexDatascanDataProfileSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2420faf9c7d516a166319fa522692d6f12166431d6e6c3d20dc893e930b081(
    *,
    bigquery_export: typing.Optional[typing.Union[DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ff25a7f34bc05f1c2964df3baba773c1bd7f5fd73c27abde8ff1d63ca483a1(
    *,
    results_table: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f2d719ea688fb37587f352bdc503c8570b92b2b73b01633d9c4fb5bd1238ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0523fdb60e6c58d72823452f982496b52d9bd851de801ee582959968a2ccb189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1376163de2a44cd1f2ea700e708602a69aabb542d6697dd07af9f3842980d19f(
    value: typing.Optional[DataplexDatascanDataProfileSpecPostScanActionsBigqueryExport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7e37c13b20d42c56e72f6294c14dd314bb931cf25dd59bfa022a8a963d77ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d8b9c26ad5ee444d69a6d0d5affdaa135f0cd75916453d317c13c29d7e23a7(
    value: typing.Optional[DataplexDatascanDataProfileSpecPostScanActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c98a56040ac5f9e591bba4e1a4fa0a58d92446f6282e22ad7ef9e5ead6bb80(
    *,
    catalog_publishing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    post_scan_actions: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActions, typing.Dict[builtins.str, typing.Any]]] = None,
    row_filter: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexDatascanDataQualitySpecRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sampling_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71887d414bfebf19c33160aca3d7a99a4057fb053019e41bade2100377d75079(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e4645c0fdd4af9c8d94abd52201f612cfbfa74e577e76ff4fbf50d84f02469(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataplexDatascanDataQualitySpecRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6680e83acc92a17da9ddcba6145505f27ab756e059edda27694a2f0337bdb552(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e684f7a223bd3b8697103319d545d5f73bca5ac008fad80de4cc4771349e5a07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99d588c57dd79bf1e283d4a386394ec6a940747baec8dcf253f1b84e309d0f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c50c625b58b82848acec8bc31b41279f7450881cce359286c40783633e1958(
    value: typing.Optional[DataplexDatascanDataQualitySpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d4c425f3b0ef2a8bf372e542b1b79e03c2b5dd24990a7772494847d9bb38ad(
    *,
    bigquery_export: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_report: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReport, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e32e88c2d9c7cd520d7abd11db51ab1b32ff1f7b952820017f0d4daff9d350(
    *,
    results_table: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41229a1a441415a484969f33dada1770a0fb2d61e0725348faa5589b289e36d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7ae2abb3d11a2028b835c1fd6c58b13d7fcf533f62a55063d175fe4722b97d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f739184964e852d91eadef2fc4f35a73e0469d3c5f34f023cf0479e34316711(
    value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsBigqueryExport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263330631c61aa32380cfa148b6bbe38a80f342045c9c483f56bc7795e437341(
    *,
    recipients: typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients, typing.Dict[builtins.str, typing.Any]],
    job_end_trigger: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    job_failure_trigger: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    score_threshold_trigger: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9732551621d583a343884066daefd737990c227ae0106a390d68f492015a299f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8713e6faf760580364fd9db56c4b183b51939ac2b80fad1f9d2f32c28bfc6a(
    value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobEndTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef48c6c04c489eb96c76ad1439c41328d683ffee803378d0e3e737f72e09fc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff50e6a06b5fa9dd42a26677ceb2e4bc20ab7a507e38a26697571dd569c41fb0(
    value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportJobFailureTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e207815a75a3bbf564e0f49126676b55d05aa133b34779c671087dfdfd6a7fe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b78b2ce38b74c416532339a685540bcf93ae6120c5f4d62d9ea2964e0f43d75(
    value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43833aa201b55640cf07cbb2668906b439ba410e6ec3ac4d141924ee3f501034(
    *,
    emails: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0079de974cd967c3a8c3a6ce9cbd869e3ceeac821de8a017d679f063e7e8fec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80498599ea5081a45603b2ba923011de24a00eef4e91dfb8187be1097e7a219(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354114ae1b91efbada122a78ad8ecad23a8269dac5e9337274701d66cb748a14(
    value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportRecipients],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca71821db343b5f0d7a8116366f12948e50a962cd5a67cd1de2aa8b6a74e1e70(
    *,
    score_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b6647c5d4c113c5ec1f635ab91c89b1a9a03ed659da61a1aaaf0e6c553728b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0679c906c8ecdd540f49d91386c073dcdd82407de3ccd88e124cbff1271e695(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ea807ddb9bb424ade304fcafe621b0c98a6b5e9288ee92541ef00d4117933b(
    value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActionsNotificationReportScoreThresholdTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ec4d4f2bc1503a9faf7d8be3e8d256c28eef9a3c72260b1f154ace0564aa77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb7c645be6acadab8d8cfd96c2cc485f3a057bf8c6fcae2bee9feb29607ccce(
    value: typing.Optional[DataplexDatascanDataQualitySpecPostScanActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31a3525e6b316fa85e52d9d95f27722bbbbeb6ecb5187454efa713bd2be01eb(
    *,
    dimension: builtins.str,
    column: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    ignore_null: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    non_null_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesNonNullExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
    range_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesRangeExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
    regex_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesRegexExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
    row_condition_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesRowConditionExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
    set_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesSetExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_assertion: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesSqlAssertion, typing.Dict[builtins.str, typing.Any]]] = None,
    statistic_range_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    table_condition_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesTableConditionExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
    uniqueness_expectation: typing.Optional[typing.Union[DataplexDatascanDataQualitySpecRulesUniquenessExpectation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f6a501cf2ff5783ab6573f714638d827de167ccba2b5a70a7696032f776bf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fcc45b0ed7e1e1cf1e37f592761f449a845a73c3ca5e397749e06fe0aa555a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8668d815b6c8ee4e1a2eaa2532af3505c6ff1a1857d15702c367a61a0b0b62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361e868f5fc2b28e7c42881dd07181155e351e9bf12e51f0e215207c6bbcfea2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f68d0f72f90e3e57736ddaa92ef1236e4788eb56b811ff69ff2eb95a5290559(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64df4d8637ff6193481df214baf857507ab29651b730b860fd8631e35a1dca8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataplexDatascanDataQualitySpecRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dfbe05de944fd068a47b5529354f9f73b3a6347629dd8c6b8e169870c5505f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8849d3bf809a221ce924ebb2c0f1c6a505fa0923bbfe7c73c078b94d769a3148(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesNonNullExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760ebc6a3289ef3333f8fbe92ff7f03a37bae78f9b3d33d7b73cc72482919682(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52047181638f5644a574c14b17beb5bcbd317c865a247170353629e24253f4db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb23ab7d88a75e61957d4e61cb08f4a0b45265454a5c7ea30046bf8ae768712(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3219e0e4a1b50219d834a5a5c8c86b7f2e3bf5d1b7729947b7f2f43cc78cbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0451e96f8f545004f44b04e92b7597de8201970d6739ba14f933614cc2034f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cfc1422780d9cbd9366c99bc1217235ed3e6d081f7d2d9f1017a784dd8856a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c0d1ad516bc6b0bda5582bc9799e4f9ae3358990562ae1202cd6776f9da670(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a5aa8d2de5e9e8af1810fecb00dff022dd56eb7064e652447ac2c9bc15697a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ec6ab48b9f4324e4e1d654a33d91db63d358c80c0187abe2e74cc03952493d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanDataQualitySpecRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6bc64dcf4f7f09f45fe73068b2c630074f63d470317245ba2a680d12c56c1d(
    *,
    max_value: typing.Optional[builtins.str] = None,
    min_value: typing.Optional[builtins.str] = None,
    strict_max_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strict_min_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759703238b5b0d1a3835089c0c71204d63a6a31f39c97f57b9ced2d8536fcec5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3a9026c0215202dca02914dbdaa9cf1d2792ce6001755eb136f5a85b737005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12abae15248ea3615e37306659e5bf80f36d56a94fb5f11a4e5f9865a2e4fbe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a607fdaebb39b605219715663624e6bb2c3d5633dfd296aa771d67393d120d26(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e94da435a3316245418a11abcd0fbaa1ee9ae6201fcb4e8e3876ecacb7bcd8b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8c6819f966ceef61ffa34b5a8788e0b0d240d62390c25fb4062afd194442e1(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesRangeExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d572b0255331e03ccc7577a2e8133353b531f411231808b1ded5ae16b165b4(
    *,
    regex: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313b8a8891714003d03503677cfc9b8524bd53fb35f1155a99087a85f8efc796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea7c94bcdcae17875c5316055b54fa0200d0acf73f6a57c123789689f8d3b15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475a09c26a9b7d34550a970d0233670a5fa5e0e0a026dc50558962b1e466798c(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesRegexExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ad4aba19ee0e8a72b9600566e5aaab50eea58d6fee6f1451b2210ceb858889(
    *,
    sql_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3585d17a97171b4d2226f21863be39b6882b7880be852b3f36abced064cf6885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45d7af9028a72e0eff6f708fd474122a85a1bdf0b78cfe2b3594c326683ac34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425e669bfd65f764df50ea8c0778b1c2b453198f2008d3836d8a38bdcde536cd(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesRowConditionExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c87bedf5b64085ec94bb7706f878c3c3db008d4c783a265f2009ba8315299b5(
    *,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c453804a5e391cf62b798b805cb0df27c2e26acbcc062035dfd93abe6627de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a2f911fa1c82f4b1c82be1cfd5e1d6013c3e1f95a73ba511aa8cf3756dc060(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2d8295163aa80ea21d497e6a6bfd05b2c03c9fa074f40dbbc0de90a8cdc1c7(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesSetExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bd6f171a68226cd104b0d34ba5b2d66637becdf96cfe795b206c7be325ff85(
    *,
    sql_statement: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d427eec99831b7fa2fee90ae42e28797a581a118f26aba4735888037508f128(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec36870b84fd447e196b041fdb6f366477ed3853e700e629138a6adfa56e997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999cfa12b89a94b66f663d853074141775d5f6551afde4dcab499e11364ace6f(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesSqlAssertion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0a5aa73adb2ee9583a2361bd732522f3b3dc6d97169e30893463bb70d70b15(
    *,
    statistic: builtins.str,
    max_value: typing.Optional[builtins.str] = None,
    min_value: typing.Optional[builtins.str] = None,
    strict_max_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strict_min_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975d32301b3563a6ee53e9ea35860ae76ed71a942de71dfa2f6539a64db59acf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1b9df4f4acbe6c8c40f4e9a180a2ab96e1f5fcec945af5072b185516903aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd93fc38c3669a133ebb7fe4b55bc4c608e5c09ea6d4a01fab510b4abe81a5d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ba00dbd43a80b645f71245295ea4290c2b02aaee0c8cee01a0f43db50082b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d8d81305355619bc8c44b1303a525b01949934c01a2dc69651734abefe3832(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797c434697eb4e4d61ac5116af34212ab463c6c087edf28e28e77db13e64ef3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929fa9c246994fdaef6c453521d03b51cef32b3868bf3fbfdafe7e012a19ac75(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesStatisticRangeExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ef359ae5fae4724bfb144183e476594f79a5dae9d5269f2e5521757e32582a(
    *,
    sql_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08943a8e396992a3a68166c3b89eec5abd11c659b0b2c0f9a27306d8e06d7045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfd3f38bb494bd76daa96d507b86916e2a785b837cbe1a229f9429e91a57c4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e31bc4a5a6ae2fb8b6909bf2677b8a9dbbe5dfc9d72e326032091ffba8c647(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesTableConditionExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1806639908e2ddc758362aa1e6b7f35a6ad9f71c0d825ddc17056bd3ed079e19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff4cf9f9fe5e2387d40e51e7f1aac3f3b985dc5b2583111a77deeb60b231af4(
    value: typing.Optional[DataplexDatascanDataQualitySpecRulesUniquenessExpectation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8cc75270233134533a2ebea3761c0c9afbb2d5df361fc03ffa6e43a7424dbd(
    *,
    trigger: typing.Union[DataplexDatascanExecutionSpecTrigger, typing.Dict[builtins.str, typing.Any]],
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46009e0440d7a7f337ba02f1c1aeda149ef4674d2c0c6cba5eb415cd9b33213(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e92371b04ff583d035d6fb435a3214c481e4f7b1ae8902310ca5ba4db9bb033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40fcbea972db179740b8bbc2b444e7b2522f997b90d8da3644ae0cd870bab1e(
    value: typing.Optional[DataplexDatascanExecutionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c326eb32426671157f23411fe7d5d60e206383138a9d0609e6b56135a5c8f47(
    *,
    on_demand: typing.Optional[typing.Union[DataplexDatascanExecutionSpecTriggerOnDemand, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[DataplexDatascanExecutionSpecTriggerSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79b2992d91166f552b247e99d167026617ab696a992286451173260fe7d8474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac2dd2832e47bbd25099eab7c46c2998bc0dc3b1ee32223be731361b5edf70f(
    value: typing.Optional[DataplexDatascanExecutionSpecTriggerOnDemand],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af631a52da0b6f9c9527a1b4b147459b15214714a82a7fe79c65d4471218fc3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf68f8ce2d89be025bfa54077b2ff8e615d4e89bb13858f171ab866b8344e0bc(
    value: typing.Optional[DataplexDatascanExecutionSpecTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67af15409251f4fe8b14154bb5d82fdb50d31d9078d511db381dcf238b8fa15(
    *,
    cron: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76342835417c2ba3b6449ce682bbebb8a2bf2f1e3c01282eb313f49e2063f2b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0560f70824c04198cb1c6efe514a1edcc969529b4c7285ac0b6408ad207e74ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5a250d239b798f9e07fc500c4cff6fdc847eb63081f3fed168948a965eb84d(
    value: typing.Optional[DataplexDatascanExecutionSpecTriggerSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f4fbf3a2ab3da0c905c4e58173fc4aced91b7399146dfe3b5367bbea675f0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85987651862b400eaca66b701c273e12846f41884c31ab1a05b6f8c18b676cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf2820c64604b40cc3bede32da2b19364b4e5c3ba5617ad55fb7926fc5c3f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ffac7a646f442a9ab8409e62881bd3b8ea38b79aeb4db8cd3003391e9b37cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec82fea6381ea48ecc94c1532c1f83b291ec95209592f4f3bcbcf7d128cfca4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908b95b79615cb54c32444bd58ba85e978ba45d0b741ea925d37c6a1dec91b6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f44f24f13e6510f286786aee0fb68c01f6252572210f6ee6e372508451dc349(
    value: typing.Optional[DataplexDatascanExecutionStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9e767d17707360c1f5acec92641a1b9725c17bdddb5bfad21942bfaa7be421(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27eac39fe10f76a66c07edab1599b9046c39a7d5462689d4ec4f346fa3a2785f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e92ea2645f7fa6de5fe8cd3bd752a775b1a082f40ef49810a63b50b2bad12a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e692111a9603c4e81b1372ce4c8f4cd634021ee01e658a668b2dd253e5390d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810f491654b4a796e2f9b5140e9ea1fe070ade83544bd5eea65c50a34babf380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeace9f1ee313460a947488670405a304c37c3925c7e0d8985b31cd695c84412(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexDatascanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
