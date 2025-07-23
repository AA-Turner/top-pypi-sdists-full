r'''
# `google_healthcare_pipeline_job`

Refer to the Terraform Registry for docs: [`google_healthcare_pipeline_job`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job).
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


class HealthcarePipelineJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job google_healthcare_pipeline_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset: builtins.str,
        location: builtins.str,
        name: builtins.str,
        backfill_pipeline_job: typing.Optional[typing.Union["HealthcarePipelineJobBackfillPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mapping_pipeline_job: typing.Optional[typing.Union["HealthcarePipelineJobMappingPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_pipeline_job: typing.Optional[typing.Union["HealthcarePipelineJobReconciliationPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["HealthcarePipelineJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job google_healthcare_pipeline_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset: Healthcare Dataset under which the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#dataset HealthcarePipelineJob#dataset}
        :param location: Location where the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#location HealthcarePipelineJob#location}
        :param name: Specifies the name of the pipeline job. This field is user-assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#name HealthcarePipelineJob#name}
        :param backfill_pipeline_job: backfill_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#backfill_pipeline_job HealthcarePipelineJob#backfill_pipeline_job}
        :param disable_lineage: If true, disables writing lineage for the pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#disable_lineage HealthcarePipelineJob#disable_lineage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#id HealthcarePipelineJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize Pipeline Jobs. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}*-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}*-]{0,63} No more than 64 labels can be associated with a given pipeline. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#labels HealthcarePipelineJob#labels}
        :param mapping_pipeline_job: mapping_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_pipeline_job HealthcarePipelineJob#mapping_pipeline_job}
        :param reconciliation_pipeline_job: reconciliation_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#reconciliation_pipeline_job HealthcarePipelineJob#reconciliation_pipeline_job}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#timeouts HealthcarePipelineJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52924e48fb240fc57c185ade8e7e706356247a4b5205c6149a7561acf56c7296)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HealthcarePipelineJobConfig(
            dataset=dataset,
            location=location,
            name=name,
            backfill_pipeline_job=backfill_pipeline_job,
            disable_lineage=disable_lineage,
            id=id,
            labels=labels,
            mapping_pipeline_job=mapping_pipeline_job,
            reconciliation_pipeline_job=reconciliation_pipeline_job,
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
        '''Generates CDKTF code for importing a HealthcarePipelineJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HealthcarePipelineJob to import.
        :param import_from_id: The id of the existing HealthcarePipelineJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HealthcarePipelineJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1764e222ffca9bfa5a655ba1737dd749483128b986aba9abd47eac74183d6a92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackfillPipelineJob")
    def put_backfill_pipeline_job(
        self,
        *,
        mapping_pipeline_job: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mapping_pipeline_job: Specifies the mapping pipeline job to backfill, the name format should follow: projects/{projectId}/locations/{locationId}/datasets/{datasetId}/pipelineJobs/{pipelineJobId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_pipeline_job HealthcarePipelineJob#mapping_pipeline_job}
        '''
        value = HealthcarePipelineJobBackfillPipelineJob(
            mapping_pipeline_job=mapping_pipeline_job
        )

        return typing.cast(None, jsii.invoke(self, "putBackfillPipelineJob", [value]))

    @jsii.member(jsii_name="putMappingPipelineJob")
    def put_mapping_pipeline_job(
        self,
        *,
        mapping_config: typing.Union["HealthcarePipelineJobMappingPipelineJobMappingConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
        fhir_streaming_source: typing.Optional[typing.Union["HealthcarePipelineJobMappingPipelineJobFhirStreamingSource", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param mapping_config: mapping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_config HealthcarePipelineJob#mapping_config}
        :param fhir_store_destination: If set, the mapping pipeline will write snapshots to this FHIR store without assigning stable IDs. You must grant your pipeline project's Cloud Healthcare Service Agent serviceaccount healthcare.fhirResources.executeBundle and healthcare.fhirResources.create permissions on the destination store. The destination store must set [disableReferentialIntegrity][FhirStore.disable_referential_integrity] to true. The destination store must use FHIR version R4. Format: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{fhirStoreID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store_destination HealthcarePipelineJob#fhir_store_destination}
        :param fhir_streaming_source: fhir_streaming_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_streaming_source HealthcarePipelineJob#fhir_streaming_source}
        :param reconciliation_destination: If set to true, a mapping pipeline will send output snapshots to the reconciliation pipeline in its dataset. A reconciliation pipeline must exist in this dataset before a mapping pipeline with a reconciliation destination can be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#reconciliation_destination HealthcarePipelineJob#reconciliation_destination}
        '''
        value = HealthcarePipelineJobMappingPipelineJob(
            mapping_config=mapping_config,
            fhir_store_destination=fhir_store_destination,
            fhir_streaming_source=fhir_streaming_source,
            reconciliation_destination=reconciliation_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putMappingPipelineJob", [value]))

    @jsii.member(jsii_name="putReconciliationPipelineJob")
    def put_reconciliation_pipeline_job(
        self,
        *,
        matching_uri_prefix: builtins.str,
        merge_config: typing.Union["HealthcarePipelineJobReconciliationPipelineJobMergeConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param matching_uri_prefix: Specifies the top level directory of the matching configs used in all mapping pipelines, which extract properties for resources to be matched on. Example: gs://{bucket-id}/{path/to/matching/configs} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#matching_uri_prefix HealthcarePipelineJob#matching_uri_prefix}
        :param merge_config: merge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#merge_config HealthcarePipelineJob#merge_config}
        :param fhir_store_destination: The harmonized FHIR store to write harmonized FHIR resources to, in the format of: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store_destination HealthcarePipelineJob#fhir_store_destination}
        '''
        value = HealthcarePipelineJobReconciliationPipelineJob(
            matching_uri_prefix=matching_uri_prefix,
            merge_config=merge_config,
            fhir_store_destination=fhir_store_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putReconciliationPipelineJob", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#create HealthcarePipelineJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#delete HealthcarePipelineJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#update HealthcarePipelineJob#update}.
        '''
        value = HealthcarePipelineJobTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackfillPipelineJob")
    def reset_backfill_pipeline_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackfillPipelineJob", []))

    @jsii.member(jsii_name="resetDisableLineage")
    def reset_disable_lineage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableLineage", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMappingPipelineJob")
    def reset_mapping_pipeline_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingPipelineJob", []))

    @jsii.member(jsii_name="resetReconciliationPipelineJob")
    def reset_reconciliation_pipeline_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReconciliationPipelineJob", []))

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
    @jsii.member(jsii_name="backfillPipelineJob")
    def backfill_pipeline_job(
        self,
    ) -> "HealthcarePipelineJobBackfillPipelineJobOutputReference":
        return typing.cast("HealthcarePipelineJobBackfillPipelineJobOutputReference", jsii.get(self, "backfillPipelineJob"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="mappingPipelineJob")
    def mapping_pipeline_job(
        self,
    ) -> "HealthcarePipelineJobMappingPipelineJobOutputReference":
        return typing.cast("HealthcarePipelineJobMappingPipelineJobOutputReference", jsii.get(self, "mappingPipelineJob"))

    @builtins.property
    @jsii.member(jsii_name="reconciliationPipelineJob")
    def reconciliation_pipeline_job(
        self,
    ) -> "HealthcarePipelineJobReconciliationPipelineJobOutputReference":
        return typing.cast("HealthcarePipelineJobReconciliationPipelineJobOutputReference", jsii.get(self, "reconciliationPipelineJob"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HealthcarePipelineJobTimeoutsOutputReference":
        return typing.cast("HealthcarePipelineJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backfillPipelineJobInput")
    def backfill_pipeline_job_input(
        self,
    ) -> typing.Optional["HealthcarePipelineJobBackfillPipelineJob"]:
        return typing.cast(typing.Optional["HealthcarePipelineJobBackfillPipelineJob"], jsii.get(self, "backfillPipelineJobInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="disableLineageInput")
    def disable_lineage_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableLineageInput"))

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
    @jsii.member(jsii_name="mappingPipelineJobInput")
    def mapping_pipeline_job_input(
        self,
    ) -> typing.Optional["HealthcarePipelineJobMappingPipelineJob"]:
        return typing.cast(typing.Optional["HealthcarePipelineJobMappingPipelineJob"], jsii.get(self, "mappingPipelineJobInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="reconciliationPipelineJobInput")
    def reconciliation_pipeline_job_input(
        self,
    ) -> typing.Optional["HealthcarePipelineJobReconciliationPipelineJob"]:
        return typing.cast(typing.Optional["HealthcarePipelineJobReconciliationPipelineJob"], jsii.get(self, "reconciliationPipelineJobInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HealthcarePipelineJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HealthcarePipelineJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed39eddc8c223310e873db89bcb573863a7308db9647ca107a14cb8a6bbd9d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableLineage")
    def disable_lineage(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableLineage"))

    @disable_lineage.setter
    def disable_lineage(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8858d8652cefc6ecc7162a530f8c845f2472fa5631b28fe7f1cc2fa446e2876a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableLineage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9210f1b304b223fa8fef0eb432e771ad1abe6bd13a4b58e0793af85a3d043b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3947a9f8b44efe02de9922417be9d38c124bd3bfcc8ccbc48b93004e888c3ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f6c353cf4f57b81e0e35b326b79132ab6197d0f513a001381fb1ee4a9af144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3ebb69782137fb6cc2b731fc80d38a6f2a8e23c01c67556cd067a06c454ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobBackfillPipelineJob",
    jsii_struct_bases=[],
    name_mapping={"mapping_pipeline_job": "mappingPipelineJob"},
)
class HealthcarePipelineJobBackfillPipelineJob:
    def __init__(
        self,
        *,
        mapping_pipeline_job: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mapping_pipeline_job: Specifies the mapping pipeline job to backfill, the name format should follow: projects/{projectId}/locations/{locationId}/datasets/{datasetId}/pipelineJobs/{pipelineJobId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_pipeline_job HealthcarePipelineJob#mapping_pipeline_job}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b4be80a16786c8e444693e8bd8eb8b01aa78dc95c310acce7608ca95ddc73a)
            check_type(argname="argument mapping_pipeline_job", value=mapping_pipeline_job, expected_type=type_hints["mapping_pipeline_job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mapping_pipeline_job is not None:
            self._values["mapping_pipeline_job"] = mapping_pipeline_job

    @builtins.property
    def mapping_pipeline_job(self) -> typing.Optional[builtins.str]:
        '''Specifies the mapping pipeline job to backfill, the name format should follow: projects/{projectId}/locations/{locationId}/datasets/{datasetId}/pipelineJobs/{pipelineJobId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_pipeline_job HealthcarePipelineJob#mapping_pipeline_job}
        '''
        result = self._values.get("mapping_pipeline_job")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobBackfillPipelineJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcarePipelineJobBackfillPipelineJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobBackfillPipelineJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f63d9c5cd526b865e1e0330b1e52c4149b020d40b2e1e0884965975b6ff108fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMappingPipelineJob")
    def reset_mapping_pipeline_job(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingPipelineJob", []))

    @builtins.property
    @jsii.member(jsii_name="mappingPipelineJobInput")
    def mapping_pipeline_job_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingPipelineJobInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingPipelineJob")
    def mapping_pipeline_job(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mappingPipelineJob"))

    @mapping_pipeline_job.setter
    def mapping_pipeline_job(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e388e9d464fe7cc7fdc30b80d81f62ff0c4250f95f1403062b48e492561d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingPipelineJob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobBackfillPipelineJob]:
        return typing.cast(typing.Optional[HealthcarePipelineJobBackfillPipelineJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobBackfillPipelineJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e196bea724e98a6b817a1571ec1d89518acba63183827003367acf0de0f0dad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset": "dataset",
        "location": "location",
        "name": "name",
        "backfill_pipeline_job": "backfillPipelineJob",
        "disable_lineage": "disableLineage",
        "id": "id",
        "labels": "labels",
        "mapping_pipeline_job": "mappingPipelineJob",
        "reconciliation_pipeline_job": "reconciliationPipelineJob",
        "timeouts": "timeouts",
    },
)
class HealthcarePipelineJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset: builtins.str,
        location: builtins.str,
        name: builtins.str,
        backfill_pipeline_job: typing.Optional[typing.Union[HealthcarePipelineJobBackfillPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
        disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mapping_pipeline_job: typing.Optional[typing.Union["HealthcarePipelineJobMappingPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_pipeline_job: typing.Optional[typing.Union["HealthcarePipelineJobReconciliationPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["HealthcarePipelineJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset: Healthcare Dataset under which the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#dataset HealthcarePipelineJob#dataset}
        :param location: Location where the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#location HealthcarePipelineJob#location}
        :param name: Specifies the name of the pipeline job. This field is user-assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#name HealthcarePipelineJob#name}
        :param backfill_pipeline_job: backfill_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#backfill_pipeline_job HealthcarePipelineJob#backfill_pipeline_job}
        :param disable_lineage: If true, disables writing lineage for the pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#disable_lineage HealthcarePipelineJob#disable_lineage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#id HealthcarePipelineJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize Pipeline Jobs. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}*-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}*-]{0,63} No more than 64 labels can be associated with a given pipeline. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#labels HealthcarePipelineJob#labels}
        :param mapping_pipeline_job: mapping_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_pipeline_job HealthcarePipelineJob#mapping_pipeline_job}
        :param reconciliation_pipeline_job: reconciliation_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#reconciliation_pipeline_job HealthcarePipelineJob#reconciliation_pipeline_job}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#timeouts HealthcarePipelineJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backfill_pipeline_job, dict):
            backfill_pipeline_job = HealthcarePipelineJobBackfillPipelineJob(**backfill_pipeline_job)
        if isinstance(mapping_pipeline_job, dict):
            mapping_pipeline_job = HealthcarePipelineJobMappingPipelineJob(**mapping_pipeline_job)
        if isinstance(reconciliation_pipeline_job, dict):
            reconciliation_pipeline_job = HealthcarePipelineJobReconciliationPipelineJob(**reconciliation_pipeline_job)
        if isinstance(timeouts, dict):
            timeouts = HealthcarePipelineJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c699606eced548201ab1dad222d8773a7114d91fd58ff4fe57de2029e88d9e4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument backfill_pipeline_job", value=backfill_pipeline_job, expected_type=type_hints["backfill_pipeline_job"])
            check_type(argname="argument disable_lineage", value=disable_lineage, expected_type=type_hints["disable_lineage"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mapping_pipeline_job", value=mapping_pipeline_job, expected_type=type_hints["mapping_pipeline_job"])
            check_type(argname="argument reconciliation_pipeline_job", value=reconciliation_pipeline_job, expected_type=type_hints["reconciliation_pipeline_job"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
            "location": location,
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
        if backfill_pipeline_job is not None:
            self._values["backfill_pipeline_job"] = backfill_pipeline_job
        if disable_lineage is not None:
            self._values["disable_lineage"] = disable_lineage
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if mapping_pipeline_job is not None:
            self._values["mapping_pipeline_job"] = mapping_pipeline_job
        if reconciliation_pipeline_job is not None:
            self._values["reconciliation_pipeline_job"] = reconciliation_pipeline_job
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
    def dataset(self) -> builtins.str:
        '''Healthcare Dataset under which the Pipeline Job is to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#dataset HealthcarePipelineJob#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location where the Pipeline Job is to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#location HealthcarePipelineJob#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the pipeline job. This field is user-assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#name HealthcarePipelineJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backfill_pipeline_job(
        self,
    ) -> typing.Optional[HealthcarePipelineJobBackfillPipelineJob]:
        '''backfill_pipeline_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#backfill_pipeline_job HealthcarePipelineJob#backfill_pipeline_job}
        '''
        result = self._values.get("backfill_pipeline_job")
        return typing.cast(typing.Optional[HealthcarePipelineJobBackfillPipelineJob], result)

    @builtins.property
    def disable_lineage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, disables writing lineage for the pipeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#disable_lineage HealthcarePipelineJob#disable_lineage}
        '''
        result = self._values.get("disable_lineage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#id HealthcarePipelineJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-supplied key-value pairs used to organize Pipeline Jobs.

        Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of
        maximum 128 bytes, and must conform to the following PCRE regular expression:
        [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}*-]{0,62}
        Label values are optional, must be between 1 and 63 characters long, have a
        UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE
        regular expression: [\\p{Ll}\\p{Lo}\\p{N}*-]{0,63}
        No more than 64 labels can be associated with a given pipeline.
        An object containing a list of "key": value pairs.
        Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#labels HealthcarePipelineJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mapping_pipeline_job(
        self,
    ) -> typing.Optional["HealthcarePipelineJobMappingPipelineJob"]:
        '''mapping_pipeline_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_pipeline_job HealthcarePipelineJob#mapping_pipeline_job}
        '''
        result = self._values.get("mapping_pipeline_job")
        return typing.cast(typing.Optional["HealthcarePipelineJobMappingPipelineJob"], result)

    @builtins.property
    def reconciliation_pipeline_job(
        self,
    ) -> typing.Optional["HealthcarePipelineJobReconciliationPipelineJob"]:
        '''reconciliation_pipeline_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#reconciliation_pipeline_job HealthcarePipelineJob#reconciliation_pipeline_job}
        '''
        result = self._values.get("reconciliation_pipeline_job")
        return typing.cast(typing.Optional["HealthcarePipelineJobReconciliationPipelineJob"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HealthcarePipelineJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#timeouts HealthcarePipelineJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HealthcarePipelineJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJob",
    jsii_struct_bases=[],
    name_mapping={
        "mapping_config": "mappingConfig",
        "fhir_store_destination": "fhirStoreDestination",
        "fhir_streaming_source": "fhirStreamingSource",
        "reconciliation_destination": "reconciliationDestination",
    },
)
class HealthcarePipelineJobMappingPipelineJob:
    def __init__(
        self,
        *,
        mapping_config: typing.Union["HealthcarePipelineJobMappingPipelineJobMappingConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
        fhir_streaming_source: typing.Optional[typing.Union["HealthcarePipelineJobMappingPipelineJobFhirStreamingSource", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param mapping_config: mapping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_config HealthcarePipelineJob#mapping_config}
        :param fhir_store_destination: If set, the mapping pipeline will write snapshots to this FHIR store without assigning stable IDs. You must grant your pipeline project's Cloud Healthcare Service Agent serviceaccount healthcare.fhirResources.executeBundle and healthcare.fhirResources.create permissions on the destination store. The destination store must set [disableReferentialIntegrity][FhirStore.disable_referential_integrity] to true. The destination store must use FHIR version R4. Format: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{fhirStoreID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store_destination HealthcarePipelineJob#fhir_store_destination}
        :param fhir_streaming_source: fhir_streaming_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_streaming_source HealthcarePipelineJob#fhir_streaming_source}
        :param reconciliation_destination: If set to true, a mapping pipeline will send output snapshots to the reconciliation pipeline in its dataset. A reconciliation pipeline must exist in this dataset before a mapping pipeline with a reconciliation destination can be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#reconciliation_destination HealthcarePipelineJob#reconciliation_destination}
        '''
        if isinstance(mapping_config, dict):
            mapping_config = HealthcarePipelineJobMappingPipelineJobMappingConfig(**mapping_config)
        if isinstance(fhir_streaming_source, dict):
            fhir_streaming_source = HealthcarePipelineJobMappingPipelineJobFhirStreamingSource(**fhir_streaming_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3bf3ed54cd4917f25f3bd81c8742352415a2b85a38db84896b1297b115ad35)
            check_type(argname="argument mapping_config", value=mapping_config, expected_type=type_hints["mapping_config"])
            check_type(argname="argument fhir_store_destination", value=fhir_store_destination, expected_type=type_hints["fhir_store_destination"])
            check_type(argname="argument fhir_streaming_source", value=fhir_streaming_source, expected_type=type_hints["fhir_streaming_source"])
            check_type(argname="argument reconciliation_destination", value=reconciliation_destination, expected_type=type_hints["reconciliation_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mapping_config": mapping_config,
        }
        if fhir_store_destination is not None:
            self._values["fhir_store_destination"] = fhir_store_destination
        if fhir_streaming_source is not None:
            self._values["fhir_streaming_source"] = fhir_streaming_source
        if reconciliation_destination is not None:
            self._values["reconciliation_destination"] = reconciliation_destination

    @builtins.property
    def mapping_config(self) -> "HealthcarePipelineJobMappingPipelineJobMappingConfig":
        '''mapping_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#mapping_config HealthcarePipelineJob#mapping_config}
        '''
        result = self._values.get("mapping_config")
        assert result is not None, "Required property 'mapping_config' is missing"
        return typing.cast("HealthcarePipelineJobMappingPipelineJobMappingConfig", result)

    @builtins.property
    def fhir_store_destination(self) -> typing.Optional[builtins.str]:
        '''If set, the mapping pipeline will write snapshots to this FHIR store without assigning stable IDs.

        You must
        grant your pipeline project's Cloud Healthcare Service
        Agent serviceaccount healthcare.fhirResources.executeBundle
        and healthcare.fhirResources.create permissions on the
        destination store. The destination store must set
        [disableReferentialIntegrity][FhirStore.disable_referential_integrity]
        to true. The destination store must use FHIR version R4.
        Format: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{fhirStoreID}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store_destination HealthcarePipelineJob#fhir_store_destination}
        '''
        result = self._values.get("fhir_store_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fhir_streaming_source(
        self,
    ) -> typing.Optional["HealthcarePipelineJobMappingPipelineJobFhirStreamingSource"]:
        '''fhir_streaming_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_streaming_source HealthcarePipelineJob#fhir_streaming_source}
        '''
        result = self._values.get("fhir_streaming_source")
        return typing.cast(typing.Optional["HealthcarePipelineJobMappingPipelineJobFhirStreamingSource"], result)

    @builtins.property
    def reconciliation_destination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, a mapping pipeline will send output snapshots to the reconciliation pipeline in its dataset.

        A reconciliation
        pipeline must exist in this dataset before a mapping pipeline
        with a reconciliation destination can be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#reconciliation_destination HealthcarePipelineJob#reconciliation_destination}
        '''
        result = self._values.get("reconciliation_destination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobMappingPipelineJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJobFhirStreamingSource",
    jsii_struct_bases=[],
    name_mapping={"fhir_store": "fhirStore", "description": "description"},
)
class HealthcarePipelineJobMappingPipelineJobFhirStreamingSource:
    def __init__(
        self,
        *,
        fhir_store: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fhir_store: The path to the FHIR store in the format projects/{projectId}/locations/{locationId}/datasets/{datasetId}/fhirStores/{fhirStoreId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store HealthcarePipelineJob#fhir_store}
        :param description: Describes the streaming FHIR data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6897743733845ebc17b05b026f645bb9d0b52612f0c5f377e68f628c35315fa7)
            check_type(argname="argument fhir_store", value=fhir_store, expected_type=type_hints["fhir_store"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fhir_store": fhir_store,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def fhir_store(self) -> builtins.str:
        '''The path to the FHIR store in the format projects/{projectId}/locations/{locationId}/datasets/{datasetId}/fhirStores/{fhirStoreId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store HealthcarePipelineJob#fhir_store}
        '''
        result = self._values.get("fhir_store")
        assert result is not None, "Required property 'fhir_store' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the streaming FHIR data source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobMappingPipelineJobFhirStreamingSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a13eef469fa4805c93509ea54ad8804ef6164169e7af96d145c6b7a0b2010cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fhirStoreInput")
    def fhir_store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fhirStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b7e79414ccb35e0d8598b1b3c45edc25953c5db6aa165253d941ea12f16fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fhirStore")
    def fhir_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fhirStore"))

    @fhir_store.setter
    def fhir_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c35a3f650b842c6818e1a145bfac15b372cb73b10597f891ad866aba723e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fhirStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobMappingPipelineJobFhirStreamingSource]:
        return typing.cast(typing.Optional[HealthcarePipelineJobMappingPipelineJobFhirStreamingSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobMappingPipelineJobFhirStreamingSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddf2de260bad090b112b8d31083ad713399909b549ace52e8fa2c9073e43a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJobMappingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "whistle_config_source": "whistleConfigSource",
    },
)
class HealthcarePipelineJobMappingPipelineJobMappingConfig:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        whistle_config_source: typing.Optional[typing.Union["HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#whistle_config_source HealthcarePipelineJob#whistle_config_source}
        '''
        if isinstance(whistle_config_source, dict):
            whistle_config_source = HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource(**whistle_config_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fcbc9efbd4f899ab58f98fadf6bfe6c30509975ea6d9113e0d2f085aac3b533)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument whistle_config_source", value=whistle_config_source, expected_type=type_hints["whistle_config_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if whistle_config_source is not None:
            self._values["whistle_config_source"] = whistle_config_source

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the mapping configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def whistle_config_source(
        self,
    ) -> typing.Optional["HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"]:
        '''whistle_config_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#whistle_config_source HealthcarePipelineJob#whistle_config_source}
        '''
        result = self._values.get("whistle_config_source")
        return typing.cast(typing.Optional["HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobMappingPipelineJobMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c62e68169a7e01f359adb6803bb9d818bee5c61d72e4610f22bdad3dc2e7b650)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWhistleConfigSource")
    def put_whistle_config_source(
        self,
        *,
        import_uri_prefix: builtins.str,
        uri: builtins.str,
    ) -> None:
        '''
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#import_uri_prefix HealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#uri HealthcarePipelineJob#uri}
        '''
        value = HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource(
            import_uri_prefix=import_uri_prefix, uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putWhistleConfigSource", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetWhistleConfigSource")
    def reset_whistle_config_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhistleConfigSource", []))

    @builtins.property
    @jsii.member(jsii_name="whistleConfigSource")
    def whistle_config_source(
        self,
    ) -> "HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference":
        return typing.cast("HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference", jsii.get(self, "whistleConfigSource"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="whistleConfigSourceInput")
    def whistle_config_source_input(
        self,
    ) -> typing.Optional["HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"]:
        return typing.cast(typing.Optional["HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"], jsii.get(self, "whistleConfigSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a162b7ac23e76278e163c3fd489e7290338e68334698a057360028350959910e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfig]:
        return typing.cast(typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196fdd797a175cbcea5554af4c2fb497a53f628868b98e66f227b7fb6e717dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource",
    jsii_struct_bases=[],
    name_mapping={"import_uri_prefix": "importUriPrefix", "uri": "uri"},
)
class HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource:
    def __init__(self, *, import_uri_prefix: builtins.str, uri: builtins.str) -> None:
        '''
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#import_uri_prefix HealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#uri HealthcarePipelineJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d884660ce6f2a67dd353eee22840344ba0f34523cadf836418688c8832b704)
            check_type(argname="argument import_uri_prefix", value=import_uri_prefix, expected_type=type_hints["import_uri_prefix"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "import_uri_prefix": import_uri_prefix,
            "uri": uri,
        }

    @builtins.property
    def import_uri_prefix(self) -> builtins.str:
        '''Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#import_uri_prefix HealthcarePipelineJob#import_uri_prefix}
        '''
        result = self._values.get("import_uri_prefix")
        assert result is not None, "Required property 'import_uri_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#uri HealthcarePipelineJob#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__595dfa558c9cb31a66cbf3a9c71b157f44f4549931c71bc6d3cceb49dffcf068)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="importUriPrefixInput")
    def import_uri_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importUriPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="importUriPrefix")
    def import_uri_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importUriPrefix"))

    @import_uri_prefix.setter
    def import_uri_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79935589663b3412a6dbecc1891c67d75d03256d6ee384a09d5e00599f742f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importUriPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad5eafea5aaab0218fa1080b3ca9060bcd1aa9a17dd6e8f3a3b3332c188eead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource]:
        return typing.cast(typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae7e591c3aa0765904c9cf4ab015d9a8836adb4f80f1f7b6cf5dadf837bfbce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HealthcarePipelineJobMappingPipelineJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobMappingPipelineJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b2c2be3ba1f4a388fb38486ebfb1c8b505f2ab0d2a39bfcb34398c80f23aa0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFhirStreamingSource")
    def put_fhir_streaming_source(
        self,
        *,
        fhir_store: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fhir_store: The path to the FHIR store in the format projects/{projectId}/locations/{locationId}/datasets/{datasetId}/fhirStores/{fhirStoreId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store HealthcarePipelineJob#fhir_store}
        :param description: Describes the streaming FHIR data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        '''
        value = HealthcarePipelineJobMappingPipelineJobFhirStreamingSource(
            fhir_store=fhir_store, description=description
        )

        return typing.cast(None, jsii.invoke(self, "putFhirStreamingSource", [value]))

    @jsii.member(jsii_name="putMappingConfig")
    def put_mapping_config(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        whistle_config_source: typing.Optional[typing.Union[HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#whistle_config_source HealthcarePipelineJob#whistle_config_source}
        '''
        value = HealthcarePipelineJobMappingPipelineJobMappingConfig(
            description=description, whistle_config_source=whistle_config_source
        )

        return typing.cast(None, jsii.invoke(self, "putMappingConfig", [value]))

    @jsii.member(jsii_name="resetFhirStoreDestination")
    def reset_fhir_store_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFhirStoreDestination", []))

    @jsii.member(jsii_name="resetFhirStreamingSource")
    def reset_fhir_streaming_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFhirStreamingSource", []))

    @jsii.member(jsii_name="resetReconciliationDestination")
    def reset_reconciliation_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReconciliationDestination", []))

    @builtins.property
    @jsii.member(jsii_name="fhirStreamingSource")
    def fhir_streaming_source(
        self,
    ) -> HealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference:
        return typing.cast(HealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference, jsii.get(self, "fhirStreamingSource"))

    @builtins.property
    @jsii.member(jsii_name="mappingConfig")
    def mapping_config(
        self,
    ) -> HealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference:
        return typing.cast(HealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference, jsii.get(self, "mappingConfig"))

    @builtins.property
    @jsii.member(jsii_name="fhirStoreDestinationInput")
    def fhir_store_destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fhirStoreDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="fhirStreamingSourceInput")
    def fhir_streaming_source_input(
        self,
    ) -> typing.Optional[HealthcarePipelineJobMappingPipelineJobFhirStreamingSource]:
        return typing.cast(typing.Optional[HealthcarePipelineJobMappingPipelineJobFhirStreamingSource], jsii.get(self, "fhirStreamingSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingConfigInput")
    def mapping_config_input(
        self,
    ) -> typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfig]:
        return typing.cast(typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfig], jsii.get(self, "mappingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="reconciliationDestinationInput")
    def reconciliation_destination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reconciliationDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="fhirStoreDestination")
    def fhir_store_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fhirStoreDestination"))

    @fhir_store_destination.setter
    def fhir_store_destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c6e04cfda557df3bab88b7f92addea1691b2c5cf47a749a8757710eee56ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fhirStoreDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reconciliationDestination")
    def reconciliation_destination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reconciliationDestination"))

    @reconciliation_destination.setter
    def reconciliation_destination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c9ff176d4d19fdc50db41ca6def0a33aea2e3f61bb4c105b1d73539e4e8488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reconciliationDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobMappingPipelineJob]:
        return typing.cast(typing.Optional[HealthcarePipelineJobMappingPipelineJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobMappingPipelineJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37623e2d29125e708c58879221903f54133837004749e7707fe6a00260ec6f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobReconciliationPipelineJob",
    jsii_struct_bases=[],
    name_mapping={
        "matching_uri_prefix": "matchingUriPrefix",
        "merge_config": "mergeConfig",
        "fhir_store_destination": "fhirStoreDestination",
    },
)
class HealthcarePipelineJobReconciliationPipelineJob:
    def __init__(
        self,
        *,
        matching_uri_prefix: builtins.str,
        merge_config: typing.Union["HealthcarePipelineJobReconciliationPipelineJobMergeConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param matching_uri_prefix: Specifies the top level directory of the matching configs used in all mapping pipelines, which extract properties for resources to be matched on. Example: gs://{bucket-id}/{path/to/matching/configs} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#matching_uri_prefix HealthcarePipelineJob#matching_uri_prefix}
        :param merge_config: merge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#merge_config HealthcarePipelineJob#merge_config}
        :param fhir_store_destination: The harmonized FHIR store to write harmonized FHIR resources to, in the format of: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store_destination HealthcarePipelineJob#fhir_store_destination}
        '''
        if isinstance(merge_config, dict):
            merge_config = HealthcarePipelineJobReconciliationPipelineJobMergeConfig(**merge_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa63511d6e269bf31b08e1a24204018fa098774eaa0a7f198757e31b29b1eb1)
            check_type(argname="argument matching_uri_prefix", value=matching_uri_prefix, expected_type=type_hints["matching_uri_prefix"])
            check_type(argname="argument merge_config", value=merge_config, expected_type=type_hints["merge_config"])
            check_type(argname="argument fhir_store_destination", value=fhir_store_destination, expected_type=type_hints["fhir_store_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matching_uri_prefix": matching_uri_prefix,
            "merge_config": merge_config,
        }
        if fhir_store_destination is not None:
            self._values["fhir_store_destination"] = fhir_store_destination

    @builtins.property
    def matching_uri_prefix(self) -> builtins.str:
        '''Specifies the top level directory of the matching configs used in all mapping pipelines, which extract properties for resources to be matched on.

        Example: gs://{bucket-id}/{path/to/matching/configs}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#matching_uri_prefix HealthcarePipelineJob#matching_uri_prefix}
        '''
        result = self._values.get("matching_uri_prefix")
        assert result is not None, "Required property 'matching_uri_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def merge_config(
        self,
    ) -> "HealthcarePipelineJobReconciliationPipelineJobMergeConfig":
        '''merge_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#merge_config HealthcarePipelineJob#merge_config}
        '''
        result = self._values.get("merge_config")
        assert result is not None, "Required property 'merge_config' is missing"
        return typing.cast("HealthcarePipelineJobReconciliationPipelineJobMergeConfig", result)

    @builtins.property
    def fhir_store_destination(self) -> typing.Optional[builtins.str]:
        '''The harmonized FHIR store to write harmonized FHIR resources to, in the format of: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#fhir_store_destination HealthcarePipelineJob#fhir_store_destination}
        '''
        result = self._values.get("fhir_store_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobReconciliationPipelineJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobReconciliationPipelineJobMergeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "whistle_config_source": "whistleConfigSource",
        "description": "description",
    },
)
class HealthcarePipelineJobReconciliationPipelineJobMergeConfig:
    def __init__(
        self,
        *,
        whistle_config_source: typing.Union["HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#whistle_config_source HealthcarePipelineJob#whistle_config_source}
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        '''
        if isinstance(whistle_config_source, dict):
            whistle_config_source = HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource(**whistle_config_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649384fb409d1346708edbf3c36aae53a86ac5ce60569de6269eba86ca061171)
            check_type(argname="argument whistle_config_source", value=whistle_config_source, expected_type=type_hints["whistle_config_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "whistle_config_source": whistle_config_source,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def whistle_config_source(
        self,
    ) -> "HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource":
        '''whistle_config_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#whistle_config_source HealthcarePipelineJob#whistle_config_source}
        '''
        result = self._values.get("whistle_config_source")
        assert result is not None, "Required property 'whistle_config_source' is missing"
        return typing.cast("HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the mapping configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobReconciliationPipelineJobMergeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3012fb536bc1a7714628665f67bbb6ed8031b6b241555abd08b77474624b1deb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWhistleConfigSource")
    def put_whistle_config_source(
        self,
        *,
        import_uri_prefix: builtins.str,
        uri: builtins.str,
    ) -> None:
        '''
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#import_uri_prefix HealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#uri HealthcarePipelineJob#uri}
        '''
        value = HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource(
            import_uri_prefix=import_uri_prefix, uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putWhistleConfigSource", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="whistleConfigSource")
    def whistle_config_source(
        self,
    ) -> "HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference":
        return typing.cast("HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference", jsii.get(self, "whistleConfigSource"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="whistleConfigSourceInput")
    def whistle_config_source_input(
        self,
    ) -> typing.Optional["HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource"]:
        return typing.cast(typing.Optional["HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource"], jsii.get(self, "whistleConfigSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26e1d02d726fe2ea4e1c1c2f7e67c3e3c14a791987838b35e5e5fb1437cf016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfig]:
        return typing.cast(typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36038a821f37e04a29260456f3d522230793a14781a84762a822a1e31e5cef16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource",
    jsii_struct_bases=[],
    name_mapping={"import_uri_prefix": "importUriPrefix", "uri": "uri"},
)
class HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource:
    def __init__(self, *, import_uri_prefix: builtins.str, uri: builtins.str) -> None:
        '''
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#import_uri_prefix HealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#uri HealthcarePipelineJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce2010ef04015218a6f65399121aade11151ddd678a63e97d3ac005243e3647)
            check_type(argname="argument import_uri_prefix", value=import_uri_prefix, expected_type=type_hints["import_uri_prefix"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "import_uri_prefix": import_uri_prefix,
            "uri": uri,
        }

    @builtins.property
    def import_uri_prefix(self) -> builtins.str:
        '''Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#import_uri_prefix HealthcarePipelineJob#import_uri_prefix}
        '''
        result = self._values.get("import_uri_prefix")
        assert result is not None, "Required property 'import_uri_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#uri HealthcarePipelineJob#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90ef814b4de9976322a1086cf567a971e9fbcc74f9aa52b9fa7fcba80f49c214)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="importUriPrefixInput")
    def import_uri_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importUriPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="importUriPrefix")
    def import_uri_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importUriPrefix"))

    @import_uri_prefix.setter
    def import_uri_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f26101ca62183f5790b4973df24cb0fc3c2ae8808c78630781a5dd00e6001b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importUriPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db80a6c8aa591480caa337f031858392f9619a61d729172a1c6de6115097ef0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource]:
        return typing.cast(typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05cf17c30b460a0dda57805c0887074989a94ce033bf181106d1500b19a06397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HealthcarePipelineJobReconciliationPipelineJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobReconciliationPipelineJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f20fd74eca0b3699d35d6a5b9df9e9cabc6342bb88b13cebfc2b09cd1d3c7a1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMergeConfig")
    def put_merge_config(
        self,
        *,
        whistle_config_source: typing.Union[HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#whistle_config_source HealthcarePipelineJob#whistle_config_source}
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#description HealthcarePipelineJob#description}
        '''
        value = HealthcarePipelineJobReconciliationPipelineJobMergeConfig(
            whistle_config_source=whistle_config_source, description=description
        )

        return typing.cast(None, jsii.invoke(self, "putMergeConfig", [value]))

    @jsii.member(jsii_name="resetFhirStoreDestination")
    def reset_fhir_store_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFhirStoreDestination", []))

    @builtins.property
    @jsii.member(jsii_name="mergeConfig")
    def merge_config(
        self,
    ) -> HealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference:
        return typing.cast(HealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference, jsii.get(self, "mergeConfig"))

    @builtins.property
    @jsii.member(jsii_name="fhirStoreDestinationInput")
    def fhir_store_destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fhirStoreDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingUriPrefixInput")
    def matching_uri_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchingUriPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeConfigInput")
    def merge_config_input(
        self,
    ) -> typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfig]:
        return typing.cast(typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfig], jsii.get(self, "mergeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fhirStoreDestination")
    def fhir_store_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fhirStoreDestination"))

    @fhir_store_destination.setter
    def fhir_store_destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f1bd33ee3529fcc852e5a9942e6cad01648e77c179789c0e5a8f46db1f71b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fhirStoreDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchingUriPrefix")
    def matching_uri_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchingUriPrefix"))

    @matching_uri_prefix.setter
    def matching_uri_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d016ee825d02123e7e8c5459c9aa6c511df322a3200891b9bdbdc97681adb104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingUriPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HealthcarePipelineJobReconciliationPipelineJob]:
        return typing.cast(typing.Optional[HealthcarePipelineJobReconciliationPipelineJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HealthcarePipelineJobReconciliationPipelineJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a325d8b1697e0ff454c9da4a09aeefc5efbafa262ac78368f77652b5cf6416a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class HealthcarePipelineJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#create HealthcarePipelineJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#delete HealthcarePipelineJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#update HealthcarePipelineJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b33739aba83c43023647abaf188319c70867c1369f9780a1f6fa5ae75304bba)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#create HealthcarePipelineJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#delete HealthcarePipelineJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/healthcare_pipeline_job#update HealthcarePipelineJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthcarePipelineJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthcarePipelineJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.healthcarePipelineJob.HealthcarePipelineJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efa197f654b8aa093f1dbbd5cc16e3ce533d7e49d4f3307420452ba150437777)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56c59f8043d6d85f001bd9262b5aea53ca01605940c4b516e72b910016301390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b799c4be40f9584701a91c28245819583443aae6c20cb4f83c9a8ba0674e56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a4a254fcbf707d48f7affa8fb7f2b41c2f5ec74704831868ecdbe33a2de620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcarePipelineJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcarePipelineJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcarePipelineJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f795595d96da0785ed9d4241b81ec59cfae2cbc45987610042c36276c066bd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HealthcarePipelineJob",
    "HealthcarePipelineJobBackfillPipelineJob",
    "HealthcarePipelineJobBackfillPipelineJobOutputReference",
    "HealthcarePipelineJobConfig",
    "HealthcarePipelineJobMappingPipelineJob",
    "HealthcarePipelineJobMappingPipelineJobFhirStreamingSource",
    "HealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference",
    "HealthcarePipelineJobMappingPipelineJobMappingConfig",
    "HealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference",
    "HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource",
    "HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference",
    "HealthcarePipelineJobMappingPipelineJobOutputReference",
    "HealthcarePipelineJobReconciliationPipelineJob",
    "HealthcarePipelineJobReconciliationPipelineJobMergeConfig",
    "HealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference",
    "HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource",
    "HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference",
    "HealthcarePipelineJobReconciliationPipelineJobOutputReference",
    "HealthcarePipelineJobTimeouts",
    "HealthcarePipelineJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__52924e48fb240fc57c185ade8e7e706356247a4b5205c6149a7561acf56c7296(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset: builtins.str,
    location: builtins.str,
    name: builtins.str,
    backfill_pipeline_job: typing.Optional[typing.Union[HealthcarePipelineJobBackfillPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mapping_pipeline_job: typing.Optional[typing.Union[HealthcarePipelineJobMappingPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    reconciliation_pipeline_job: typing.Optional[typing.Union[HealthcarePipelineJobReconciliationPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[HealthcarePipelineJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1764e222ffca9bfa5a655ba1737dd749483128b986aba9abd47eac74183d6a92(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed39eddc8c223310e873db89bcb573863a7308db9647ca107a14cb8a6bbd9d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8858d8652cefc6ecc7162a530f8c845f2472fa5631b28fe7f1cc2fa446e2876a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9210f1b304b223fa8fef0eb432e771ad1abe6bd13a4b58e0793af85a3d043b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3947a9f8b44efe02de9922417be9d38c124bd3bfcc8ccbc48b93004e888c3ca4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f6c353cf4f57b81e0e35b326b79132ab6197d0f513a001381fb1ee4a9af144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3ebb69782137fb6cc2b731fc80d38a6f2a8e23c01c67556cd067a06c454ef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b4be80a16786c8e444693e8bd8eb8b01aa78dc95c310acce7608ca95ddc73a(
    *,
    mapping_pipeline_job: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63d9c5cd526b865e1e0330b1e52c4149b020d40b2e1e0884965975b6ff108fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e388e9d464fe7cc7fdc30b80d81f62ff0c4250f95f1403062b48e492561d7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e196bea724e98a6b817a1571ec1d89518acba63183827003367acf0de0f0dad7(
    value: typing.Optional[HealthcarePipelineJobBackfillPipelineJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c699606eced548201ab1dad222d8773a7114d91fd58ff4fe57de2029e88d9e4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset: builtins.str,
    location: builtins.str,
    name: builtins.str,
    backfill_pipeline_job: typing.Optional[typing.Union[HealthcarePipelineJobBackfillPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mapping_pipeline_job: typing.Optional[typing.Union[HealthcarePipelineJobMappingPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    reconciliation_pipeline_job: typing.Optional[typing.Union[HealthcarePipelineJobReconciliationPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[HealthcarePipelineJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3bf3ed54cd4917f25f3bd81c8742352415a2b85a38db84896b1297b115ad35(
    *,
    mapping_config: typing.Union[HealthcarePipelineJobMappingPipelineJobMappingConfig, typing.Dict[builtins.str, typing.Any]],
    fhir_store_destination: typing.Optional[builtins.str] = None,
    fhir_streaming_source: typing.Optional[typing.Union[HealthcarePipelineJobMappingPipelineJobFhirStreamingSource, typing.Dict[builtins.str, typing.Any]]] = None,
    reconciliation_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6897743733845ebc17b05b026f645bb9d0b52612f0c5f377e68f628c35315fa7(
    *,
    fhir_store: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a13eef469fa4805c93509ea54ad8804ef6164169e7af96d145c6b7a0b2010cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b7e79414ccb35e0d8598b1b3c45edc25953c5db6aa165253d941ea12f16fbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c35a3f650b842c6818e1a145bfac15b372cb73b10597f891ad866aba723e5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddf2de260bad090b112b8d31083ad713399909b549ace52e8fa2c9073e43a82(
    value: typing.Optional[HealthcarePipelineJobMappingPipelineJobFhirStreamingSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcbc9efbd4f899ab58f98fadf6bfe6c30509975ea6d9113e0d2f085aac3b533(
    *,
    description: typing.Optional[builtins.str] = None,
    whistle_config_source: typing.Optional[typing.Union[HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62e68169a7e01f359adb6803bb9d818bee5c61d72e4610f22bdad3dc2e7b650(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a162b7ac23e76278e163c3fd489e7290338e68334698a057360028350959910e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196fdd797a175cbcea5554af4c2fb497a53f628868b98e66f227b7fb6e717dc8(
    value: typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d884660ce6f2a67dd353eee22840344ba0f34523cadf836418688c8832b704(
    *,
    import_uri_prefix: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595dfa558c9cb31a66cbf3a9c71b157f44f4549931c71bc6d3cceb49dffcf068(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79935589663b3412a6dbecc1891c67d75d03256d6ee384a09d5e00599f742f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad5eafea5aaab0218fa1080b3ca9060bcd1aa9a17dd6e8f3a3b3332c188eead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae7e591c3aa0765904c9cf4ab015d9a8836adb4f80f1f7b6cf5dadf837bfbce(
    value: typing.Optional[HealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2c2be3ba1f4a388fb38486ebfb1c8b505f2ab0d2a39bfcb34398c80f23aa0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c6e04cfda557df3bab88b7f92addea1691b2c5cf47a749a8757710eee56ed9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c9ff176d4d19fdc50db41ca6def0a33aea2e3f61bb4c105b1d73539e4e8488(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37623e2d29125e708c58879221903f54133837004749e7707fe6a00260ec6f8c(
    value: typing.Optional[HealthcarePipelineJobMappingPipelineJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa63511d6e269bf31b08e1a24204018fa098774eaa0a7f198757e31b29b1eb1(
    *,
    matching_uri_prefix: builtins.str,
    merge_config: typing.Union[HealthcarePipelineJobReconciliationPipelineJobMergeConfig, typing.Dict[builtins.str, typing.Any]],
    fhir_store_destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649384fb409d1346708edbf3c36aae53a86ac5ce60569de6269eba86ca061171(
    *,
    whistle_config_source: typing.Union[HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3012fb536bc1a7714628665f67bbb6ed8031b6b241555abd08b77474624b1deb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26e1d02d726fe2ea4e1c1c2f7e67c3e3c14a791987838b35e5e5fb1437cf016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36038a821f37e04a29260456f3d522230793a14781a84762a822a1e31e5cef16(
    value: typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce2010ef04015218a6f65399121aade11151ddd678a63e97d3ac005243e3647(
    *,
    import_uri_prefix: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ef814b4de9976322a1086cf567a971e9fbcc74f9aa52b9fa7fcba80f49c214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f26101ca62183f5790b4973df24cb0fc3c2ae8808c78630781a5dd00e6001b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db80a6c8aa591480caa337f031858392f9619a61d729172a1c6de6115097ef0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05cf17c30b460a0dda57805c0887074989a94ce033bf181106d1500b19a06397(
    value: typing.Optional[HealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20fd74eca0b3699d35d6a5b9df9e9cabc6342bb88b13cebfc2b09cd1d3c7a1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f1bd33ee3529fcc852e5a9942e6cad01648e77c179789c0e5a8f46db1f71b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d016ee825d02123e7e8c5459c9aa6c511df322a3200891b9bdbdc97681adb104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a325d8b1697e0ff454c9da4a09aeefc5efbafa262ac78368f77652b5cf6416a(
    value: typing.Optional[HealthcarePipelineJobReconciliationPipelineJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b33739aba83c43023647abaf188319c70867c1369f9780a1f6fa5ae75304bba(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa197f654b8aa093f1dbbd5cc16e3ce533d7e49d4f3307420452ba150437777(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c59f8043d6d85f001bd9262b5aea53ca01605940c4b516e72b910016301390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b799c4be40f9584701a91c28245819583443aae6c20cb4f83c9a8ba0674e56e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a4a254fcbf707d48f7affa8fb7f2b41c2f5ec74704831868ecdbe33a2de620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f795595d96da0785ed9d4241b81ec59cfae2cbc45987610042c36276c066bd45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HealthcarePipelineJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
