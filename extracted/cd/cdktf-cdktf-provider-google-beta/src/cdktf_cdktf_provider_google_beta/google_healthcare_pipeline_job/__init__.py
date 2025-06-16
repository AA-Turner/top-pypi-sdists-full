r'''
# `google_healthcare_pipeline_job`

Refer to the Terraform Registry for docs: [`google_healthcare_pipeline_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job).
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


class GoogleHealthcarePipelineJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job google_healthcare_pipeline_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset: builtins.str,
        location: builtins.str,
        name: builtins.str,
        backfill_pipeline_job: typing.Optional[typing.Union["GoogleHealthcarePipelineJobBackfillPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mapping_pipeline_job: typing.Optional[typing.Union["GoogleHealthcarePipelineJobMappingPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_pipeline_job: typing.Optional[typing.Union["GoogleHealthcarePipelineJobReconciliationPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleHealthcarePipelineJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job google_healthcare_pipeline_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset: Healthcare Dataset under which the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#dataset GoogleHealthcarePipelineJob#dataset}
        :param location: Location where the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#location GoogleHealthcarePipelineJob#location}
        :param name: Specifies the name of the pipeline job. This field is user-assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#name GoogleHealthcarePipelineJob#name}
        :param backfill_pipeline_job: backfill_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#backfill_pipeline_job GoogleHealthcarePipelineJob#backfill_pipeline_job}
        :param disable_lineage: If true, disables writing lineage for the pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#disable_lineage GoogleHealthcarePipelineJob#disable_lineage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#id GoogleHealthcarePipelineJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize Pipeline Jobs. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}*-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}*-]{0,63} No more than 64 labels can be associated with a given pipeline. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#labels GoogleHealthcarePipelineJob#labels}
        :param mapping_pipeline_job: mapping_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_pipeline_job GoogleHealthcarePipelineJob#mapping_pipeline_job}
        :param reconciliation_pipeline_job: reconciliation_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#reconciliation_pipeline_job GoogleHealthcarePipelineJob#reconciliation_pipeline_job}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#timeouts GoogleHealthcarePipelineJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ef5337d0b16180d66835ceb50e93bbd0310c75ff921def824521697a11eab0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleHealthcarePipelineJobConfig(
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
        '''Generates CDKTF code for importing a GoogleHealthcarePipelineJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleHealthcarePipelineJob to import.
        :param import_from_id: The id of the existing GoogleHealthcarePipelineJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleHealthcarePipelineJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b46dd4602aca499beeff2229b071d1fa429d28d0a48fad7140d24fde2a5e0d)
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
        :param mapping_pipeline_job: Specifies the mapping pipeline job to backfill, the name format should follow: projects/{projectId}/locations/{locationId}/datasets/{datasetId}/pipelineJobs/{pipelineJobId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_pipeline_job GoogleHealthcarePipelineJob#mapping_pipeline_job}
        '''
        value = GoogleHealthcarePipelineJobBackfillPipelineJob(
            mapping_pipeline_job=mapping_pipeline_job
        )

        return typing.cast(None, jsii.invoke(self, "putBackfillPipelineJob", [value]))

    @jsii.member(jsii_name="putMappingPipelineJob")
    def put_mapping_pipeline_job(
        self,
        *,
        mapping_config: typing.Union["GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
        fhir_streaming_source: typing.Optional[typing.Union["GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param mapping_config: mapping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_config GoogleHealthcarePipelineJob#mapping_config}
        :param fhir_store_destination: If set, the mapping pipeline will write snapshots to this FHIR store without assigning stable IDs. You must grant your pipeline project's Cloud Healthcare Service Agent serviceaccount healthcare.fhirResources.executeBundle and healthcare.fhirResources.create permissions on the destination store. The destination store must set [disableReferentialIntegrity][FhirStore.disable_referential_integrity] to true. The destination store must use FHIR version R4. Format: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{fhirStoreID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store_destination GoogleHealthcarePipelineJob#fhir_store_destination}
        :param fhir_streaming_source: fhir_streaming_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_streaming_source GoogleHealthcarePipelineJob#fhir_streaming_source}
        :param reconciliation_destination: If set to true, a mapping pipeline will send output snapshots to the reconciliation pipeline in its dataset. A reconciliation pipeline must exist in this dataset before a mapping pipeline with a reconciliation destination can be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#reconciliation_destination GoogleHealthcarePipelineJob#reconciliation_destination}
        '''
        value = GoogleHealthcarePipelineJobMappingPipelineJob(
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
        merge_config: typing.Union["GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param matching_uri_prefix: Specifies the top level directory of the matching configs used in all mapping pipelines, which extract properties for resources to be matched on. Example: gs://{bucket-id}/{path/to/matching/configs} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#matching_uri_prefix GoogleHealthcarePipelineJob#matching_uri_prefix}
        :param merge_config: merge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#merge_config GoogleHealthcarePipelineJob#merge_config}
        :param fhir_store_destination: The harmonized FHIR store to write harmonized FHIR resources to, in the format of: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store_destination GoogleHealthcarePipelineJob#fhir_store_destination}
        '''
        value = GoogleHealthcarePipelineJobReconciliationPipelineJob(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#create GoogleHealthcarePipelineJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#delete GoogleHealthcarePipelineJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#update GoogleHealthcarePipelineJob#update}.
        '''
        value = GoogleHealthcarePipelineJobTimeouts(
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
    ) -> "GoogleHealthcarePipelineJobBackfillPipelineJobOutputReference":
        return typing.cast("GoogleHealthcarePipelineJobBackfillPipelineJobOutputReference", jsii.get(self, "backfillPipelineJob"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="mappingPipelineJob")
    def mapping_pipeline_job(
        self,
    ) -> "GoogleHealthcarePipelineJobMappingPipelineJobOutputReference":
        return typing.cast("GoogleHealthcarePipelineJobMappingPipelineJobOutputReference", jsii.get(self, "mappingPipelineJob"))

    @builtins.property
    @jsii.member(jsii_name="reconciliationPipelineJob")
    def reconciliation_pipeline_job(
        self,
    ) -> "GoogleHealthcarePipelineJobReconciliationPipelineJobOutputReference":
        return typing.cast("GoogleHealthcarePipelineJobReconciliationPipelineJobOutputReference", jsii.get(self, "reconciliationPipelineJob"))

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
    def timeouts(self) -> "GoogleHealthcarePipelineJobTimeoutsOutputReference":
        return typing.cast("GoogleHealthcarePipelineJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backfillPipelineJobInput")
    def backfill_pipeline_job_input(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobBackfillPipelineJob"]:
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobBackfillPipelineJob"], jsii.get(self, "backfillPipelineJobInput"))

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
    ) -> typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJob"]:
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJob"], jsii.get(self, "mappingPipelineJobInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="reconciliationPipelineJobInput")
    def reconciliation_pipeline_job_input(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobReconciliationPipelineJob"]:
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobReconciliationPipelineJob"], jsii.get(self, "reconciliationPipelineJobInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleHealthcarePipelineJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleHealthcarePipelineJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d47143ce1edcca0e2eca640012817dbd10d28a4f9e2b1006c49fc93b96923a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__633516e924938fb0a815f129819b87edee4e2882573caef1fc8afe1c112fd6b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableLineage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8770435b849883733129112fa4f89f4aa841c59892703df7aa66e18c0fa7b321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bee44e3c91edcdbe77b019c73a68eef481dc843fda19c0842f52eec1f70c819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc85e13e9b49d88a95dfb7f236f45a3a59901165134bb5b96448dbfc6d39dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4feb6ec3f9c81eeced95543c46d3d101d4a474e54d7c98a22ac554cc8862252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobBackfillPipelineJob",
    jsii_struct_bases=[],
    name_mapping={"mapping_pipeline_job": "mappingPipelineJob"},
)
class GoogleHealthcarePipelineJobBackfillPipelineJob:
    def __init__(
        self,
        *,
        mapping_pipeline_job: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mapping_pipeline_job: Specifies the mapping pipeline job to backfill, the name format should follow: projects/{projectId}/locations/{locationId}/datasets/{datasetId}/pipelineJobs/{pipelineJobId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_pipeline_job GoogleHealthcarePipelineJob#mapping_pipeline_job}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16518a9be6c6cb6bf6e54cb63444dca7c82e056db4926180fdd9c50014c2358)
            check_type(argname="argument mapping_pipeline_job", value=mapping_pipeline_job, expected_type=type_hints["mapping_pipeline_job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mapping_pipeline_job is not None:
            self._values["mapping_pipeline_job"] = mapping_pipeline_job

    @builtins.property
    def mapping_pipeline_job(self) -> typing.Optional[builtins.str]:
        '''Specifies the mapping pipeline job to backfill, the name format should follow: projects/{projectId}/locations/{locationId}/datasets/{datasetId}/pipelineJobs/{pipelineJobId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_pipeline_job GoogleHealthcarePipelineJob#mapping_pipeline_job}
        '''
        result = self._values.get("mapping_pipeline_job")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobBackfillPipelineJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcarePipelineJobBackfillPipelineJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobBackfillPipelineJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa78d24dc02ec288a35bda53c29b9b77bc2f68264a39909305b4c0d175730a22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__744ff60654ece9e1d64c8b8071dd3544ac6520dfd5f0062bf5050a236377890c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingPipelineJob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobBackfillPipelineJob]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobBackfillPipelineJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobBackfillPipelineJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cdda7e92ff4b33acec2ae9dff34e29fa054a2def940be387ca9ee20912d826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobConfig",
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
class GoogleHealthcarePipelineJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backfill_pipeline_job: typing.Optional[typing.Union[GoogleHealthcarePipelineJobBackfillPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
        disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mapping_pipeline_job: typing.Optional[typing.Union["GoogleHealthcarePipelineJobMappingPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_pipeline_job: typing.Optional[typing.Union["GoogleHealthcarePipelineJobReconciliationPipelineJob", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleHealthcarePipelineJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset: Healthcare Dataset under which the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#dataset GoogleHealthcarePipelineJob#dataset}
        :param location: Location where the Pipeline Job is to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#location GoogleHealthcarePipelineJob#location}
        :param name: Specifies the name of the pipeline job. This field is user-assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#name GoogleHealthcarePipelineJob#name}
        :param backfill_pipeline_job: backfill_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#backfill_pipeline_job GoogleHealthcarePipelineJob#backfill_pipeline_job}
        :param disable_lineage: If true, disables writing lineage for the pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#disable_lineage GoogleHealthcarePipelineJob#disable_lineage}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#id GoogleHealthcarePipelineJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-supplied key-value pairs used to organize Pipeline Jobs. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}*-]{0,62} Label values are optional, must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}*-]{0,63} No more than 64 labels can be associated with a given pipeline. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#labels GoogleHealthcarePipelineJob#labels}
        :param mapping_pipeline_job: mapping_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_pipeline_job GoogleHealthcarePipelineJob#mapping_pipeline_job}
        :param reconciliation_pipeline_job: reconciliation_pipeline_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#reconciliation_pipeline_job GoogleHealthcarePipelineJob#reconciliation_pipeline_job}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#timeouts GoogleHealthcarePipelineJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backfill_pipeline_job, dict):
            backfill_pipeline_job = GoogleHealthcarePipelineJobBackfillPipelineJob(**backfill_pipeline_job)
        if isinstance(mapping_pipeline_job, dict):
            mapping_pipeline_job = GoogleHealthcarePipelineJobMappingPipelineJob(**mapping_pipeline_job)
        if isinstance(reconciliation_pipeline_job, dict):
            reconciliation_pipeline_job = GoogleHealthcarePipelineJobReconciliationPipelineJob(**reconciliation_pipeline_job)
        if isinstance(timeouts, dict):
            timeouts = GoogleHealthcarePipelineJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c94b648304cfa6aac58f4d52da79377b30d1eaa48e2cdb87ccf356314103a7f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#dataset GoogleHealthcarePipelineJob#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location where the Pipeline Job is to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#location GoogleHealthcarePipelineJob#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the pipeline job. This field is user-assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#name GoogleHealthcarePipelineJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backfill_pipeline_job(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobBackfillPipelineJob]:
        '''backfill_pipeline_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#backfill_pipeline_job GoogleHealthcarePipelineJob#backfill_pipeline_job}
        '''
        result = self._values.get("backfill_pipeline_job")
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobBackfillPipelineJob], result)

    @builtins.property
    def disable_lineage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, disables writing lineage for the pipeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#disable_lineage GoogleHealthcarePipelineJob#disable_lineage}
        '''
        result = self._values.get("disable_lineage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#id GoogleHealthcarePipelineJob#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#labels GoogleHealthcarePipelineJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mapping_pipeline_job(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJob"]:
        '''mapping_pipeline_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_pipeline_job GoogleHealthcarePipelineJob#mapping_pipeline_job}
        '''
        result = self._values.get("mapping_pipeline_job")
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJob"], result)

    @builtins.property
    def reconciliation_pipeline_job(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobReconciliationPipelineJob"]:
        '''reconciliation_pipeline_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#reconciliation_pipeline_job GoogleHealthcarePipelineJob#reconciliation_pipeline_job}
        '''
        result = self._values.get("reconciliation_pipeline_job")
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobReconciliationPipelineJob"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleHealthcarePipelineJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#timeouts GoogleHealthcarePipelineJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJob",
    jsii_struct_bases=[],
    name_mapping={
        "mapping_config": "mappingConfig",
        "fhir_store_destination": "fhirStoreDestination",
        "fhir_streaming_source": "fhirStreamingSource",
        "reconciliation_destination": "reconciliationDestination",
    },
)
class GoogleHealthcarePipelineJobMappingPipelineJob:
    def __init__(
        self,
        *,
        mapping_config: typing.Union["GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
        fhir_streaming_source: typing.Optional[typing.Union["GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource", typing.Dict[builtins.str, typing.Any]]] = None,
        reconciliation_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param mapping_config: mapping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_config GoogleHealthcarePipelineJob#mapping_config}
        :param fhir_store_destination: If set, the mapping pipeline will write snapshots to this FHIR store without assigning stable IDs. You must grant your pipeline project's Cloud Healthcare Service Agent serviceaccount healthcare.fhirResources.executeBundle and healthcare.fhirResources.create permissions on the destination store. The destination store must set [disableReferentialIntegrity][FhirStore.disable_referential_integrity] to true. The destination store must use FHIR version R4. Format: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{fhirStoreID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store_destination GoogleHealthcarePipelineJob#fhir_store_destination}
        :param fhir_streaming_source: fhir_streaming_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_streaming_source GoogleHealthcarePipelineJob#fhir_streaming_source}
        :param reconciliation_destination: If set to true, a mapping pipeline will send output snapshots to the reconciliation pipeline in its dataset. A reconciliation pipeline must exist in this dataset before a mapping pipeline with a reconciliation destination can be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#reconciliation_destination GoogleHealthcarePipelineJob#reconciliation_destination}
        '''
        if isinstance(mapping_config, dict):
            mapping_config = GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig(**mapping_config)
        if isinstance(fhir_streaming_source, dict):
            fhir_streaming_source = GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource(**fhir_streaming_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262f1c00778ce0b464981303687456e4063113f9f67af6098158870daa3907b4)
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
    def mapping_config(
        self,
    ) -> "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig":
        '''mapping_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#mapping_config GoogleHealthcarePipelineJob#mapping_config}
        '''
        result = self._values.get("mapping_config")
        assert result is not None, "Required property 'mapping_config' is missing"
        return typing.cast("GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig", result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store_destination GoogleHealthcarePipelineJob#fhir_store_destination}
        '''
        result = self._values.get("fhir_store_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fhir_streaming_source(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource"]:
        '''fhir_streaming_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_streaming_source GoogleHealthcarePipelineJob#fhir_streaming_source}
        '''
        result = self._values.get("fhir_streaming_source")
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource"], result)

    @builtins.property
    def reconciliation_destination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, a mapping pipeline will send output snapshots to the reconciliation pipeline in its dataset.

        A reconciliation
        pipeline must exist in this dataset before a mapping pipeline
        with a reconciliation destination can be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#reconciliation_destination GoogleHealthcarePipelineJob#reconciliation_destination}
        '''
        result = self._values.get("reconciliation_destination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobMappingPipelineJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource",
    jsii_struct_bases=[],
    name_mapping={"fhir_store": "fhirStore", "description": "description"},
)
class GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource:
    def __init__(
        self,
        *,
        fhir_store: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fhir_store: The path to the FHIR store in the format projects/{projectId}/locations/{locationId}/datasets/{datasetId}/fhirStores/{fhirStoreId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store GoogleHealthcarePipelineJob#fhir_store}
        :param description: Describes the streaming FHIR data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcab80674de146c6c937de13083fc26417c7178ae1b1afd05840af6f7584c706)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store GoogleHealthcarePipelineJob#fhir_store}
        '''
        result = self._values.get("fhir_store")
        assert result is not None, "Required property 'fhir_store' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the streaming FHIR data source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eea1b99e74e80d75ba4f1c4a7e51677583aa464598dd7cfd09b80596f33d4002)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b455326c12caa700f0a3ddaf895c1f89884137931469e9d3411ab920b9498aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fhirStore")
    def fhir_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fhirStore"))

    @fhir_store.setter
    def fhir_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fefb94e635261e6a28f4c95d88e8c97b21451860c99acfc5d190bf673921676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fhirStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa5b496425a48da585e76b76a26a80ce976fd94eda5f43ce9a413cf104fb84b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "whistle_config_source": "whistleConfigSource",
    },
)
class GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        whistle_config_source: typing.Optional[typing.Union["GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#whistle_config_source GoogleHealthcarePipelineJob#whistle_config_source}
        '''
        if isinstance(whistle_config_source, dict):
            whistle_config_source = GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource(**whistle_config_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a608ae4115429130f907f0e0963d22d627bff034e998249049b5197a0c5bb6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def whistle_config_source(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"]:
        '''whistle_config_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#whistle_config_source GoogleHealthcarePipelineJob#whistle_config_source}
        '''
        result = self._values.get("whistle_config_source")
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3dd30bf1938f9e123c86537683aa7133c33a0b9cc22b21881cc2f299a93ab14)
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
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#import_uri_prefix GoogleHealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#uri GoogleHealthcarePipelineJob#uri}
        '''
        value = GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource(
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
    ) -> "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference":
        return typing.cast("GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference", jsii.get(self, "whistleConfigSource"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="whistleConfigSourceInput")
    def whistle_config_source_input(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"]:
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource"], jsii.get(self, "whistleConfigSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c9e2db173c147fe71e684728207ca12c3fbe2b7f2006ddeacd1bf8ad960395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304844b4b666b47e138c97466c744c2b102a186385124110d37cd84268b642bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource",
    jsii_struct_bases=[],
    name_mapping={"import_uri_prefix": "importUriPrefix", "uri": "uri"},
)
class GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource:
    def __init__(self, *, import_uri_prefix: builtins.str, uri: builtins.str) -> None:
        '''
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#import_uri_prefix GoogleHealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#uri GoogleHealthcarePipelineJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087f000f27833837fafd5931563d1a34ffbffff9c61dc1ce67d1c47266a16583)
            check_type(argname="argument import_uri_prefix", value=import_uri_prefix, expected_type=type_hints["import_uri_prefix"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "import_uri_prefix": import_uri_prefix,
            "uri": uri,
        }

    @builtins.property
    def import_uri_prefix(self) -> builtins.str:
        '''Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#import_uri_prefix GoogleHealthcarePipelineJob#import_uri_prefix}
        '''
        result = self._values.get("import_uri_prefix")
        assert result is not None, "Required property 'import_uri_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#uri GoogleHealthcarePipelineJob#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf8a62cb84dab79928f9d4aae514f28aa8491fc1ef9921e2d974ce28eaa5249f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3efe6097c0db156fc701da6de55026d6d470a30971935be790658c484060326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importUriPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac01574bc8ca55e95adc7f147faf1eb26b19051c230bd02afa59b206e25b6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed6446eabee7e7dc00be00299dab15c80baf4ad9785fd0f98fbcfe812e9816a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleHealthcarePipelineJobMappingPipelineJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobMappingPipelineJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cd5f7deae41352d10bad2448392d63ed23bd789354957a292c712e94881f8ef)
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
        :param fhir_store: The path to the FHIR store in the format projects/{projectId}/locations/{locationId}/datasets/{datasetId}/fhirStores/{fhirStoreId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store GoogleHealthcarePipelineJob#fhir_store}
        :param description: Describes the streaming FHIR data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        '''
        value = GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource(
            fhir_store=fhir_store, description=description
        )

        return typing.cast(None, jsii.invoke(self, "putFhirStreamingSource", [value]))

    @jsii.member(jsii_name="putMappingConfig")
    def put_mapping_config(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        whistle_config_source: typing.Optional[typing.Union[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#whistle_config_source GoogleHealthcarePipelineJob#whistle_config_source}
        '''
        value = GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig(
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
    ) -> GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference:
        return typing.cast(GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference, jsii.get(self, "fhirStreamingSource"))

    @builtins.property
    @jsii.member(jsii_name="mappingConfig")
    def mapping_config(
        self,
    ) -> GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference:
        return typing.cast(GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference, jsii.get(self, "mappingConfig"))

    @builtins.property
    @jsii.member(jsii_name="fhirStoreDestinationInput")
    def fhir_store_destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fhirStoreDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="fhirStreamingSourceInput")
    def fhir_streaming_source_input(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource], jsii.get(self, "fhirStreamingSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingConfigInput")
    def mapping_config_input(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig], jsii.get(self, "mappingConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0ada752113c2c031a32a9ab1c59bba16c1728e26721538bd7a02d73664b9b861)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c96ff60c7cae8c43498a73d34cf8a9de3fd145e3046ae721bd0bb961817d9bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reconciliationDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJob]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fac50ce20efcde3adfe2cec6a70e6c5aba3d6164d868ff83a6a2944c4237fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobReconciliationPipelineJob",
    jsii_struct_bases=[],
    name_mapping={
        "matching_uri_prefix": "matchingUriPrefix",
        "merge_config": "mergeConfig",
        "fhir_store_destination": "fhirStoreDestination",
    },
)
class GoogleHealthcarePipelineJobReconciliationPipelineJob:
    def __init__(
        self,
        *,
        matching_uri_prefix: builtins.str,
        merge_config: typing.Union["GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig", typing.Dict[builtins.str, typing.Any]],
        fhir_store_destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param matching_uri_prefix: Specifies the top level directory of the matching configs used in all mapping pipelines, which extract properties for resources to be matched on. Example: gs://{bucket-id}/{path/to/matching/configs} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#matching_uri_prefix GoogleHealthcarePipelineJob#matching_uri_prefix}
        :param merge_config: merge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#merge_config GoogleHealthcarePipelineJob#merge_config}
        :param fhir_store_destination: The harmonized FHIR store to write harmonized FHIR resources to, in the format of: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store_destination GoogleHealthcarePipelineJob#fhir_store_destination}
        '''
        if isinstance(merge_config, dict):
            merge_config = GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig(**merge_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc90a9649e324cba2724feac15eda1d4add5cb2729f98ec4e652f8688af0957)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#matching_uri_prefix GoogleHealthcarePipelineJob#matching_uri_prefix}
        '''
        result = self._values.get("matching_uri_prefix")
        assert result is not None, "Required property 'matching_uri_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def merge_config(
        self,
    ) -> "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig":
        '''merge_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#merge_config GoogleHealthcarePipelineJob#merge_config}
        '''
        result = self._values.get("merge_config")
        assert result is not None, "Required property 'merge_config' is missing"
        return typing.cast("GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig", result)

    @builtins.property
    def fhir_store_destination(self) -> typing.Optional[builtins.str]:
        '''The harmonized FHIR store to write harmonized FHIR resources to, in the format of: project/{projectID}/locations/{locationID}/datasets/{datasetName}/fhirStores/{id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#fhir_store_destination GoogleHealthcarePipelineJob#fhir_store_destination}
        '''
        result = self._values.get("fhir_store_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobReconciliationPipelineJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "whistle_config_source": "whistleConfigSource",
        "description": "description",
    },
)
class GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig:
    def __init__(
        self,
        *,
        whistle_config_source: typing.Union["GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#whistle_config_source GoogleHealthcarePipelineJob#whistle_config_source}
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        '''
        if isinstance(whistle_config_source, dict):
            whistle_config_source = GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource(**whistle_config_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53528d8023206dda951d6ec39cac6cd89bd265c152848801e0dfb09cd2db448)
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
    ) -> "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource":
        '''whistle_config_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#whistle_config_source GoogleHealthcarePipelineJob#whistle_config_source}
        '''
        result = self._values.get("whistle_config_source")
        assert result is not None, "Required property 'whistle_config_source' is missing"
        return typing.cast("GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the mapping configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28fc50921b88cdfc013f56555e388302bf1714334b62f861974389657578c03a)
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
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#import_uri_prefix GoogleHealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#uri GoogleHealthcarePipelineJob#uri}
        '''
        value = GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource(
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
    ) -> "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference":
        return typing.cast("GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference", jsii.get(self, "whistleConfigSource"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="whistleConfigSourceInput")
    def whistle_config_source_input(
        self,
    ) -> typing.Optional["GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource"]:
        return typing.cast(typing.Optional["GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource"], jsii.get(self, "whistleConfigSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ec2cf5427ff1ff7434c073139ed98c6695fa590d19569f09646ba6d039710b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7008d58a71c4e621d3d66de049620f761fb36602f1cd4cbe8bf963f762f3451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource",
    jsii_struct_bases=[],
    name_mapping={"import_uri_prefix": "importUriPrefix", "uri": "uri"},
)
class GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource:
    def __init__(self, *, import_uri_prefix: builtins.str, uri: builtins.str) -> None:
        '''
        :param import_uri_prefix: Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#import_uri_prefix GoogleHealthcarePipelineJob#import_uri_prefix}
        :param uri: Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#uri GoogleHealthcarePipelineJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2609e5a6ec9efb127acdb9183d15a19eb1a227f39a557218e2b159f015de33)
            check_type(argname="argument import_uri_prefix", value=import_uri_prefix, expected_type=type_hints["import_uri_prefix"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "import_uri_prefix": import_uri_prefix,
            "uri": uri,
        }

    @builtins.property
    def import_uri_prefix(self) -> builtins.str:
        '''Directory path where all the Whistle files are located. Example: gs://{bucket-id}/{path/to/import-root/dir}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#import_uri_prefix GoogleHealthcarePipelineJob#import_uri_prefix}
        '''
        result = self._values.get("import_uri_prefix")
        assert result is not None, "Required property 'import_uri_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Main configuration file which has the entrypoint or the root function. Example: gs://{bucket-id}/{path/to/import-root/dir}/entrypoint-file-name.wstl.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#uri GoogleHealthcarePipelineJob#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2a2809d00955fbd624b4ed7e6ce7008c497843653d0ef3159a2f50d2c2bd4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28595f762b510b54ec9c212511b384608531436c3a23f6078cd4176ccd5c3a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importUriPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8cc01f5cf73e288566421c68945b70315e2455f0459737b16c1b831b869ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f583a68f08baee00814543132716435fb267438cbc193d07a1930b607eb17f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleHealthcarePipelineJobReconciliationPipelineJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobReconciliationPipelineJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebac6b82b62fa9b7fbc724b3d44794c6d824f98bd6e33c02cfad55dfcebd38e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMergeConfig")
    def put_merge_config(
        self,
        *,
        whistle_config_source: typing.Union[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param whistle_config_source: whistle_config_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#whistle_config_source GoogleHealthcarePipelineJob#whistle_config_source}
        :param description: Describes the mapping configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#description GoogleHealthcarePipelineJob#description}
        '''
        value = GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig(
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
    ) -> GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference:
        return typing.cast(GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference, jsii.get(self, "mergeConfig"))

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
    ) -> typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig], jsii.get(self, "mergeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fhirStoreDestination")
    def fhir_store_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fhirStoreDestination"))

    @fhir_store_destination.setter
    def fhir_store_destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a71490a5637f9692377b88e5a5d957b94a3272c2f893e68320b2ffba53da7a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fhirStoreDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchingUriPrefix")
    def matching_uri_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchingUriPrefix"))

    @matching_uri_prefix.setter
    def matching_uri_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f13956267af12aacfae50bd794033ff08c5c06bbf8e0617e25ab80862b79883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingUriPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJob]:
        return typing.cast(typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6609f72cbb51808645a6a40b61a3623bef19b6f20b4b72309afa1a53aa6daf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleHealthcarePipelineJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#create GoogleHealthcarePipelineJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#delete GoogleHealthcarePipelineJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#update GoogleHealthcarePipelineJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe8f1ed9e85981fd5e8e7ff009c8f96fd020ff873dd67a1e87efc60f5da101f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#create GoogleHealthcarePipelineJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#delete GoogleHealthcarePipelineJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_healthcare_pipeline_job#update GoogleHealthcarePipelineJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleHealthcarePipelineJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleHealthcarePipelineJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleHealthcarePipelineJob.GoogleHealthcarePipelineJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__872fbfa08edd01101a161daac3993d823bc9790239e3b37f5ddb59e8b64c8fdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fed3c95fedb6e1f847f6432083a7e715c3b34a2963fae1453f8e9be64ad9a5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6502529809c4af6474b075b6a0d068a7de4882fea9a65b9e03d9b1b23fcdec7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217d41fdfff20c88fe6ab88165b399f18563d6e2a0f0b2c5a3f576e8ee831973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcarePipelineJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcarePipelineJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcarePipelineJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54405161a8d633ea8f6a5bfe6fdb69db86f71f3baad88270fd4d4bfecca001b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleHealthcarePipelineJob",
    "GoogleHealthcarePipelineJobBackfillPipelineJob",
    "GoogleHealthcarePipelineJobBackfillPipelineJobOutputReference",
    "GoogleHealthcarePipelineJobConfig",
    "GoogleHealthcarePipelineJobMappingPipelineJob",
    "GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource",
    "GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSourceOutputReference",
    "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig",
    "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigOutputReference",
    "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource",
    "GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSourceOutputReference",
    "GoogleHealthcarePipelineJobMappingPipelineJobOutputReference",
    "GoogleHealthcarePipelineJobReconciliationPipelineJob",
    "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig",
    "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigOutputReference",
    "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource",
    "GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSourceOutputReference",
    "GoogleHealthcarePipelineJobReconciliationPipelineJobOutputReference",
    "GoogleHealthcarePipelineJobTimeouts",
    "GoogleHealthcarePipelineJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__24ef5337d0b16180d66835ceb50e93bbd0310c75ff921def824521697a11eab0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset: builtins.str,
    location: builtins.str,
    name: builtins.str,
    backfill_pipeline_job: typing.Optional[typing.Union[GoogleHealthcarePipelineJobBackfillPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mapping_pipeline_job: typing.Optional[typing.Union[GoogleHealthcarePipelineJobMappingPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    reconciliation_pipeline_job: typing.Optional[typing.Union[GoogleHealthcarePipelineJobReconciliationPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleHealthcarePipelineJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e4b46dd4602aca499beeff2229b071d1fa429d28d0a48fad7140d24fde2a5e0d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d47143ce1edcca0e2eca640012817dbd10d28a4f9e2b1006c49fc93b96923a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633516e924938fb0a815f129819b87edee4e2882573caef1fc8afe1c112fd6b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8770435b849883733129112fa4f89f4aa841c59892703df7aa66e18c0fa7b321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bee44e3c91edcdbe77b019c73a68eef481dc843fda19c0842f52eec1f70c819(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc85e13e9b49d88a95dfb7f236f45a3a59901165134bb5b96448dbfc6d39dd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4feb6ec3f9c81eeced95543c46d3d101d4a474e54d7c98a22ac554cc8862252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16518a9be6c6cb6bf6e54cb63444dca7c82e056db4926180fdd9c50014c2358(
    *,
    mapping_pipeline_job: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa78d24dc02ec288a35bda53c29b9b77bc2f68264a39909305b4c0d175730a22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744ff60654ece9e1d64c8b8071dd3544ac6520dfd5f0062bf5050a236377890c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cdda7e92ff4b33acec2ae9dff34e29fa054a2def940be387ca9ee20912d826(
    value: typing.Optional[GoogleHealthcarePipelineJobBackfillPipelineJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c94b648304cfa6aac58f4d52da79377b30d1eaa48e2cdb87ccf356314103a7f(
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
    backfill_pipeline_job: typing.Optional[typing.Union[GoogleHealthcarePipelineJobBackfillPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_lineage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mapping_pipeline_job: typing.Optional[typing.Union[GoogleHealthcarePipelineJobMappingPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    reconciliation_pipeline_job: typing.Optional[typing.Union[GoogleHealthcarePipelineJobReconciliationPipelineJob, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleHealthcarePipelineJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262f1c00778ce0b464981303687456e4063113f9f67af6098158870daa3907b4(
    *,
    mapping_config: typing.Union[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig, typing.Dict[builtins.str, typing.Any]],
    fhir_store_destination: typing.Optional[builtins.str] = None,
    fhir_streaming_source: typing.Optional[typing.Union[GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource, typing.Dict[builtins.str, typing.Any]]] = None,
    reconciliation_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcab80674de146c6c937de13083fc26417c7178ae1b1afd05840af6f7584c706(
    *,
    fhir_store: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea1b99e74e80d75ba4f1c4a7e51677583aa464598dd7cfd09b80596f33d4002(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b455326c12caa700f0a3ddaf895c1f89884137931469e9d3411ab920b9498aaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fefb94e635261e6a28f4c95d88e8c97b21451860c99acfc5d190bf673921676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa5b496425a48da585e76b76a26a80ce976fd94eda5f43ce9a413cf104fb84b(
    value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobFhirStreamingSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a608ae4115429130f907f0e0963d22d627bff034e998249049b5197a0c5bb6(
    *,
    description: typing.Optional[builtins.str] = None,
    whistle_config_source: typing.Optional[typing.Union[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3dd30bf1938f9e123c86537683aa7133c33a0b9cc22b21881cc2f299a93ab14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c9e2db173c147fe71e684728207ca12c3fbe2b7f2006ddeacd1bf8ad960395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304844b4b666b47e138c97466c744c2b102a186385124110d37cd84268b642bd(
    value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087f000f27833837fafd5931563d1a34ffbffff9c61dc1ce67d1c47266a16583(
    *,
    import_uri_prefix: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8a62cb84dab79928f9d4aae514f28aa8491fc1ef9921e2d974ce28eaa5249f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3efe6097c0db156fc701da6de55026d6d470a30971935be790658c484060326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac01574bc8ca55e95adc7f147faf1eb26b19051c230bd02afa59b206e25b6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed6446eabee7e7dc00be00299dab15c80baf4ad9785fd0f98fbcfe812e9816a(
    value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJobMappingConfigWhistleConfigSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd5f7deae41352d10bad2448392d63ed23bd789354957a292c712e94881f8ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ada752113c2c031a32a9ab1c59bba16c1728e26721538bd7a02d73664b9b861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96ff60c7cae8c43498a73d34cf8a9de3fd145e3046ae721bd0bb961817d9bee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fac50ce20efcde3adfe2cec6a70e6c5aba3d6164d868ff83a6a2944c4237fc(
    value: typing.Optional[GoogleHealthcarePipelineJobMappingPipelineJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc90a9649e324cba2724feac15eda1d4add5cb2729f98ec4e652f8688af0957(
    *,
    matching_uri_prefix: builtins.str,
    merge_config: typing.Union[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig, typing.Dict[builtins.str, typing.Any]],
    fhir_store_destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53528d8023206dda951d6ec39cac6cd89bd265c152848801e0dfb09cd2db448(
    *,
    whistle_config_source: typing.Union[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fc50921b88cdfc013f56555e388302bf1714334b62f861974389657578c03a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ec2cf5427ff1ff7434c073139ed98c6695fa590d19569f09646ba6d039710b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7008d58a71c4e621d3d66de049620f761fb36602f1cd4cbe8bf963f762f3451(
    value: typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2609e5a6ec9efb127acdb9183d15a19eb1a227f39a557218e2b159f015de33(
    *,
    import_uri_prefix: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2a2809d00955fbd624b4ed7e6ce7008c497843653d0ef3159a2f50d2c2bd4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28595f762b510b54ec9c212511b384608531436c3a23f6078cd4176ccd5c3a1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8cc01f5cf73e288566421c68945b70315e2455f0459737b16c1b831b869ebc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f583a68f08baee00814543132716435fb267438cbc193d07a1930b607eb17f9c(
    value: typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJobMergeConfigWhistleConfigSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebac6b82b62fa9b7fbc724b3d44794c6d824f98bd6e33c02cfad55dfcebd38e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a71490a5637f9692377b88e5a5d957b94a3272c2f893e68320b2ffba53da7a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f13956267af12aacfae50bd794033ff08c5c06bbf8e0617e25ab80862b79883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6609f72cbb51808645a6a40b61a3623bef19b6f20b4b72309afa1a53aa6daf6(
    value: typing.Optional[GoogleHealthcarePipelineJobReconciliationPipelineJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe8f1ed9e85981fd5e8e7ff009c8f96fd020ff873dd67a1e87efc60f5da101f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872fbfa08edd01101a161daac3993d823bc9790239e3b37f5ddb59e8b64c8fdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed3c95fedb6e1f847f6432083a7e715c3b34a2963fae1453f8e9be64ad9a5d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6502529809c4af6474b075b6a0d068a7de4882fea9a65b9e03d9b1b23fcdec7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217d41fdfff20c88fe6ab88165b399f18563d6e2a0f0b2c5a3f576e8ee831973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54405161a8d633ea8f6a5bfe6fdb69db86f71f3baad88270fd4d4bfecca001b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleHealthcarePipelineJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
