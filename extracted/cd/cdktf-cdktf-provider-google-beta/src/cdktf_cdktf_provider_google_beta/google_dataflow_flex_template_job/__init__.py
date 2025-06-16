r'''
# `google_dataflow_flex_template_job`

Refer to the Terraform Registry for docs: [`google_dataflow_flex_template_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job).
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


class GoogleDataflowFlexTemplateJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataflowFlexTemplateJob.GoogleDataflowFlexTemplateJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job google_dataflow_flex_template_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container_spec_gcs_path: builtins.str,
        name: builtins.str,
        additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_pipeline_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        autoscaling_algorithm: typing.Optional[builtins.str] = None,
        enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_configuration: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launcher_machine_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        on_delete: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sdk_container_image: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        skip_wait_on_job_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        staging_location: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        temp_location: typing.Optional[builtins.str] = None,
        transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job google_dataflow_flex_template_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container_spec_gcs_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#container_spec_gcs_path GoogleDataflowFlexTemplateJob#container_spec_gcs_path}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#name GoogleDataflowFlexTemplateJob#name}.
        :param additional_experiments: List of experiments that should be used by the job. An example value is ["enable_stackdriver_agent_metrics"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#additional_experiments GoogleDataflowFlexTemplateJob#additional_experiments}
        :param additional_pipeline_options: List of pipeline options that should be used by the job. An example value is ["numberOfWorkerHarnessThreads=20"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#additional_pipeline_options GoogleDataflowFlexTemplateJob#additional_pipeline_options}
        :param autoscaling_algorithm: The algorithm to use for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#autoscaling_algorithm GoogleDataflowFlexTemplateJob#autoscaling_algorithm}
        :param enable_streaming_engine: Indicates if the job should use the streaming engine feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#enable_streaming_engine GoogleDataflowFlexTemplateJob#enable_streaming_engine}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#id GoogleDataflowFlexTemplateJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_configuration: The configuration for VM IPs. Options are "WORKER_IP_PUBLIC" or "WORKER_IP_PRIVATE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#ip_configuration GoogleDataflowFlexTemplateJob#ip_configuration}
        :param kms_key_name: The name for the Cloud KMS key for the job. Key format is: projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#kms_key_name GoogleDataflowFlexTemplateJob#kms_key_name}
        :param labels: User labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. NOTE: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#labels GoogleDataflowFlexTemplateJob#labels}
        :param launcher_machine_type: The machine type to use for launching the job. The default is n1-standard-1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#launcher_machine_type GoogleDataflowFlexTemplateJob#launcher_machine_type}
        :param machine_type: The machine type to use for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#machine_type GoogleDataflowFlexTemplateJob#machine_type}
        :param max_workers: The maximum number of Google Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#max_workers GoogleDataflowFlexTemplateJob#max_workers}
        :param network: The network to which VMs will be assigned. If it is not provided, "default" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#network GoogleDataflowFlexTemplateJob#network}
        :param num_workers: The initial number of Google Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#num_workers GoogleDataflowFlexTemplateJob#num_workers}
        :param on_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#on_delete GoogleDataflowFlexTemplateJob#on_delete}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#parameters GoogleDataflowFlexTemplateJob#parameters}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#project GoogleDataflowFlexTemplateJob#project}.
        :param region: The region in which the created job should run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#region GoogleDataflowFlexTemplateJob#region}
        :param sdk_container_image: Docker registry location of container image to use for the 'worker harness. Default is the container for the version of the SDK. Note this field is only valid for portable pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#sdk_container_image GoogleDataflowFlexTemplateJob#sdk_container_image}
        :param service_account_email: The Service Account email used to create the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#service_account_email GoogleDataflowFlexTemplateJob#service_account_email}
        :param skip_wait_on_job_termination: If true, treat DRAINING and CANCELLING as terminal job states and do not wait for further changes before removing from terraform state and moving on. WARNING: this will lead to job name conflicts if you do not ensure that the job names are different, e.g. by embedding a release ID or by using a random_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#skip_wait_on_job_termination GoogleDataflowFlexTemplateJob#skip_wait_on_job_termination}
        :param staging_location: The Cloud Storage path to use for staging files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#staging_location GoogleDataflowFlexTemplateJob#staging_location}
        :param subnetwork: The subnetwork to which VMs will be assigned. Should be of the form "regions/REGION/subnetworks/SUBNETWORK". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#subnetwork GoogleDataflowFlexTemplateJob#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#temp_location GoogleDataflowFlexTemplateJob#temp_location}
        :param transform_name_mapping: Only applicable when updating a pipeline. Map of transform name prefixes of the job to be replaced with the corresponding name prefixes of the new job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#transform_name_mapping GoogleDataflowFlexTemplateJob#transform_name_mapping}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013e09be6a774a88845af984bf9e30a636c685203d324d91ee99f699b472fdee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataflowFlexTemplateJobConfig(
            container_spec_gcs_path=container_spec_gcs_path,
            name=name,
            additional_experiments=additional_experiments,
            additional_pipeline_options=additional_pipeline_options,
            autoscaling_algorithm=autoscaling_algorithm,
            enable_streaming_engine=enable_streaming_engine,
            id=id,
            ip_configuration=ip_configuration,
            kms_key_name=kms_key_name,
            labels=labels,
            launcher_machine_type=launcher_machine_type,
            machine_type=machine_type,
            max_workers=max_workers,
            network=network,
            num_workers=num_workers,
            on_delete=on_delete,
            parameters=parameters,
            project=project,
            region=region,
            sdk_container_image=sdk_container_image,
            service_account_email=service_account_email,
            skip_wait_on_job_termination=skip_wait_on_job_termination,
            staging_location=staging_location,
            subnetwork=subnetwork,
            temp_location=temp_location,
            transform_name_mapping=transform_name_mapping,
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
        '''Generates CDKTF code for importing a GoogleDataflowFlexTemplateJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataflowFlexTemplateJob to import.
        :param import_from_id: The id of the existing GoogleDataflowFlexTemplateJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataflowFlexTemplateJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0886dcdd8d4bead5cd6b2a75516b775150079b8c21077ea4587b31f7ab0a4d37)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAdditionalExperiments")
    def reset_additional_experiments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExperiments", []))

    @jsii.member(jsii_name="resetAdditionalPipelineOptions")
    def reset_additional_pipeline_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalPipelineOptions", []))

    @jsii.member(jsii_name="resetAutoscalingAlgorithm")
    def reset_autoscaling_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingAlgorithm", []))

    @jsii.member(jsii_name="resetEnableStreamingEngine")
    def reset_enable_streaming_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStreamingEngine", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpConfiguration")
    def reset_ip_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpConfiguration", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLauncherMachineType")
    def reset_launcher_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLauncherMachineType", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMaxWorkers")
    def reset_max_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWorkers", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNumWorkers")
    def reset_num_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumWorkers", []))

    @jsii.member(jsii_name="resetOnDelete")
    def reset_on_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDelete", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSdkContainerImage")
    def reset_sdk_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSdkContainerImage", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @jsii.member(jsii_name="resetSkipWaitOnJobTermination")
    def reset_skip_wait_on_job_termination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipWaitOnJobTermination", []))

    @jsii.member(jsii_name="resetStagingLocation")
    def reset_staging_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingLocation", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTempLocation")
    def reset_temp_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTempLocation", []))

    @jsii.member(jsii_name="resetTransformNameMapping")
    def reset_transform_name_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformNameMapping", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="additionalExperimentsInput")
    def additional_experiments_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalExperimentsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalPipelineOptionsInput")
    def additional_pipeline_options_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalPipelineOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingAlgorithmInput")
    def autoscaling_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoscalingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="containerSpecGcsPathInput")
    def container_spec_gcs_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerSpecGcsPathInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStreamingEngineInput")
    def enable_streaming_engine_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStreamingEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="launcherMachineTypeInput")
    def launcher_machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launcherMachineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkersInput")
    def max_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="numWorkersInput")
    def num_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="onDeleteInput")
    def on_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sdkContainerImageInput")
    def sdk_container_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sdkContainerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="skipWaitOnJobTerminationInput")
    def skip_wait_on_job_termination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipWaitOnJobTerminationInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingLocationInput")
    def staging_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tempLocationInput")
    def temp_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tempLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="transformNameMappingInput")
    def transform_name_mapping_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "transformNameMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalExperiments")
    def additional_experiments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalExperiments"))

    @additional_experiments.setter
    def additional_experiments(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67170bdf764c33767d6e2766219635750540e8926a84efd6f2d1b0863e8953e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalExperiments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="additionalPipelineOptions")
    def additional_pipeline_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalPipelineOptions"))

    @additional_pipeline_options.setter
    def additional_pipeline_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7d1cfbd5d94642178cca29cdb6504599a20c682b849d3227c102a007ad5296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalPipelineOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoscalingAlgorithm")
    def autoscaling_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoscalingAlgorithm"))

    @autoscaling_algorithm.setter
    def autoscaling_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532a35eda53f0d8fcd09f3afee1db3a4ae5826be2472130e5e73e81f2a759f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerSpecGcsPath")
    def container_spec_gcs_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerSpecGcsPath"))

    @container_spec_gcs_path.setter
    def container_spec_gcs_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e817f92e5dca948168c452e8698f62cad3d3afe0be7b55e32dfc404f3880e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerSpecGcsPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableStreamingEngine")
    def enable_streaming_engine(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableStreamingEngine"))

    @enable_streaming_engine.setter
    def enable_streaming_engine(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90058f03955066b58f553c6e46cacccf14f34c80065f5eb9005e7e617294d7d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStreamingEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a97b1a2af4a30e5ed3b2cf2bcf892c52662f47e2ca974ffe0674527cfc68a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipConfiguration"))

    @ip_configuration.setter
    def ip_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc788960ceeecba9a7fd998e0d52a31261237cae9061921e321e8ee16fce5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8d6f3b17ba4232e6a8a7034d38663e8954659d784f62e34c8093a5e307ca97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4893141cdde28ae7b65dc1b0d18127a37c53e0338b9283bef41ed7f33b95656b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launcherMachineType")
    def launcher_machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launcherMachineType"))

    @launcher_machine_type.setter
    def launcher_machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a200c2667d1e08ac1c27287c6a138e5d9c8f6314092f775c1c46afe5d2130aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launcherMachineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac41c89b9041c852cee2a29eccb43451eebf442953a0d559ddb87f11c98ead6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f91e06b104ddda3c7b1df0495d6b621015775bf450a449be865f790878fb37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc11dc7347e73bd66125b222ed73e9e11ba8e526628b055a48f992c45d93a81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9873876b758bc04575930cf01d2cd731b4e107baa4d656d07a1bd63bfb8e6dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numWorkers")
    def num_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numWorkers"))

    @num_workers.setter
    def num_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd32e2cdc418dc699d85c5f49967f7c8784211aa6e0de0fc3817fa3e52c8b833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onDelete")
    def on_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onDelete"))

    @on_delete.setter
    def on_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6977704fe6666d37197ac75b55b3fcc47f278cec5283398d650d5888a89643cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d6c658051af9762136cd9467f1b93f2abe6a27678cf81832769342d6659884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605f35dcac0e805dbbaa32919798a4ecb8980b8c50e406969052bee5faf1c209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cdc39671f5e046b7f3bda98d48ca83903f13d76aa7176979c6797ff3e6497c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sdkContainerImage")
    def sdk_container_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sdkContainerImage"))

    @sdk_container_image.setter
    def sdk_container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211ed1ae4703e75c70e77dc76339ff4cfb2734e55610ab6956bde383998ecd9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sdkContainerImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a71be9a0682f03c8fb032765885e7895883cc3a80af3f9638f39803fc11709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipWaitOnJobTermination")
    def skip_wait_on_job_termination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipWaitOnJobTermination"))

    @skip_wait_on_job_termination.setter
    def skip_wait_on_job_termination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5915a46969b18ea718200d24e4b345bb7418bb15485e4ee81b0b553cbed317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipWaitOnJobTermination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingLocation")
    def staging_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingLocation"))

    @staging_location.setter
    def staging_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e267b01a1fff0c6298469e2507fff6a6b04b0d82cee755ce9e3cbfa0e03992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2798934d63820bbb20aac484db7b7915ec85eb60b335efd7e34cc7075b833c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tempLocation")
    def temp_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempLocation"))

    @temp_location.setter
    def temp_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f251664c56a9e8a6f169d012400a1ed8e5c870aba6b4c83ba49481e3b58f1ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transformNameMapping")
    def transform_name_mapping(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "transformNameMapping"))

    @transform_name_mapping.setter
    def transform_name_mapping(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e5c4a8e5b9f6d02d091d07e88d080e5e65d6d13dac8f87e36f83abbcbe7d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformNameMapping", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataflowFlexTemplateJob.GoogleDataflowFlexTemplateJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "container_spec_gcs_path": "containerSpecGcsPath",
        "name": "name",
        "additional_experiments": "additionalExperiments",
        "additional_pipeline_options": "additionalPipelineOptions",
        "autoscaling_algorithm": "autoscalingAlgorithm",
        "enable_streaming_engine": "enableStreamingEngine",
        "id": "id",
        "ip_configuration": "ipConfiguration",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "launcher_machine_type": "launcherMachineType",
        "machine_type": "machineType",
        "max_workers": "maxWorkers",
        "network": "network",
        "num_workers": "numWorkers",
        "on_delete": "onDelete",
        "parameters": "parameters",
        "project": "project",
        "region": "region",
        "sdk_container_image": "sdkContainerImage",
        "service_account_email": "serviceAccountEmail",
        "skip_wait_on_job_termination": "skipWaitOnJobTermination",
        "staging_location": "stagingLocation",
        "subnetwork": "subnetwork",
        "temp_location": "tempLocation",
        "transform_name_mapping": "transformNameMapping",
    },
)
class GoogleDataflowFlexTemplateJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container_spec_gcs_path: builtins.str,
        name: builtins.str,
        additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_pipeline_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        autoscaling_algorithm: typing.Optional[builtins.str] = None,
        enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_configuration: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launcher_machine_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        on_delete: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sdk_container_image: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        skip_wait_on_job_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        staging_location: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        temp_location: typing.Optional[builtins.str] = None,
        transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param container_spec_gcs_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#container_spec_gcs_path GoogleDataflowFlexTemplateJob#container_spec_gcs_path}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#name GoogleDataflowFlexTemplateJob#name}.
        :param additional_experiments: List of experiments that should be used by the job. An example value is ["enable_stackdriver_agent_metrics"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#additional_experiments GoogleDataflowFlexTemplateJob#additional_experiments}
        :param additional_pipeline_options: List of pipeline options that should be used by the job. An example value is ["numberOfWorkerHarnessThreads=20"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#additional_pipeline_options GoogleDataflowFlexTemplateJob#additional_pipeline_options}
        :param autoscaling_algorithm: The algorithm to use for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#autoscaling_algorithm GoogleDataflowFlexTemplateJob#autoscaling_algorithm}
        :param enable_streaming_engine: Indicates if the job should use the streaming engine feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#enable_streaming_engine GoogleDataflowFlexTemplateJob#enable_streaming_engine}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#id GoogleDataflowFlexTemplateJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_configuration: The configuration for VM IPs. Options are "WORKER_IP_PUBLIC" or "WORKER_IP_PRIVATE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#ip_configuration GoogleDataflowFlexTemplateJob#ip_configuration}
        :param kms_key_name: The name for the Cloud KMS key for the job. Key format is: projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#kms_key_name GoogleDataflowFlexTemplateJob#kms_key_name}
        :param labels: User labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. NOTE: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#labels GoogleDataflowFlexTemplateJob#labels}
        :param launcher_machine_type: The machine type to use for launching the job. The default is n1-standard-1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#launcher_machine_type GoogleDataflowFlexTemplateJob#launcher_machine_type}
        :param machine_type: The machine type to use for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#machine_type GoogleDataflowFlexTemplateJob#machine_type}
        :param max_workers: The maximum number of Google Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#max_workers GoogleDataflowFlexTemplateJob#max_workers}
        :param network: The network to which VMs will be assigned. If it is not provided, "default" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#network GoogleDataflowFlexTemplateJob#network}
        :param num_workers: The initial number of Google Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#num_workers GoogleDataflowFlexTemplateJob#num_workers}
        :param on_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#on_delete GoogleDataflowFlexTemplateJob#on_delete}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#parameters GoogleDataflowFlexTemplateJob#parameters}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#project GoogleDataflowFlexTemplateJob#project}.
        :param region: The region in which the created job should run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#region GoogleDataflowFlexTemplateJob#region}
        :param sdk_container_image: Docker registry location of container image to use for the 'worker harness. Default is the container for the version of the SDK. Note this field is only valid for portable pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#sdk_container_image GoogleDataflowFlexTemplateJob#sdk_container_image}
        :param service_account_email: The Service Account email used to create the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#service_account_email GoogleDataflowFlexTemplateJob#service_account_email}
        :param skip_wait_on_job_termination: If true, treat DRAINING and CANCELLING as terminal job states and do not wait for further changes before removing from terraform state and moving on. WARNING: this will lead to job name conflicts if you do not ensure that the job names are different, e.g. by embedding a release ID or by using a random_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#skip_wait_on_job_termination GoogleDataflowFlexTemplateJob#skip_wait_on_job_termination}
        :param staging_location: The Cloud Storage path to use for staging files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#staging_location GoogleDataflowFlexTemplateJob#staging_location}
        :param subnetwork: The subnetwork to which VMs will be assigned. Should be of the form "regions/REGION/subnetworks/SUBNETWORK". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#subnetwork GoogleDataflowFlexTemplateJob#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#temp_location GoogleDataflowFlexTemplateJob#temp_location}
        :param transform_name_mapping: Only applicable when updating a pipeline. Map of transform name prefixes of the job to be replaced with the corresponding name prefixes of the new job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#transform_name_mapping GoogleDataflowFlexTemplateJob#transform_name_mapping}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de023addd99a52594a5a29a6dc457e88db74f737f253395920b5d7a5b38da68)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container_spec_gcs_path", value=container_spec_gcs_path, expected_type=type_hints["container_spec_gcs_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_experiments", value=additional_experiments, expected_type=type_hints["additional_experiments"])
            check_type(argname="argument additional_pipeline_options", value=additional_pipeline_options, expected_type=type_hints["additional_pipeline_options"])
            check_type(argname="argument autoscaling_algorithm", value=autoscaling_algorithm, expected_type=type_hints["autoscaling_algorithm"])
            check_type(argname="argument enable_streaming_engine", value=enable_streaming_engine, expected_type=type_hints["enable_streaming_engine"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launcher_machine_type", value=launcher_machine_type, expected_type=type_hints["launcher_machine_type"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument num_workers", value=num_workers, expected_type=type_hints["num_workers"])
            check_type(argname="argument on_delete", value=on_delete, expected_type=type_hints["on_delete"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument sdk_container_image", value=sdk_container_image, expected_type=type_hints["sdk_container_image"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument skip_wait_on_job_termination", value=skip_wait_on_job_termination, expected_type=type_hints["skip_wait_on_job_termination"])
            check_type(argname="argument staging_location", value=staging_location, expected_type=type_hints["staging_location"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument temp_location", value=temp_location, expected_type=type_hints["temp_location"])
            check_type(argname="argument transform_name_mapping", value=transform_name_mapping, expected_type=type_hints["transform_name_mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_spec_gcs_path": container_spec_gcs_path,
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
        if additional_experiments is not None:
            self._values["additional_experiments"] = additional_experiments
        if additional_pipeline_options is not None:
            self._values["additional_pipeline_options"] = additional_pipeline_options
        if autoscaling_algorithm is not None:
            self._values["autoscaling_algorithm"] = autoscaling_algorithm
        if enable_streaming_engine is not None:
            self._values["enable_streaming_engine"] = enable_streaming_engine
        if id is not None:
            self._values["id"] = id
        if ip_configuration is not None:
            self._values["ip_configuration"] = ip_configuration
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if launcher_machine_type is not None:
            self._values["launcher_machine_type"] = launcher_machine_type
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if network is not None:
            self._values["network"] = network
        if num_workers is not None:
            self._values["num_workers"] = num_workers
        if on_delete is not None:
            self._values["on_delete"] = on_delete
        if parameters is not None:
            self._values["parameters"] = parameters
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if sdk_container_image is not None:
            self._values["sdk_container_image"] = sdk_container_image
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email
        if skip_wait_on_job_termination is not None:
            self._values["skip_wait_on_job_termination"] = skip_wait_on_job_termination
        if staging_location is not None:
            self._values["staging_location"] = staging_location
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if temp_location is not None:
            self._values["temp_location"] = temp_location
        if transform_name_mapping is not None:
            self._values["transform_name_mapping"] = transform_name_mapping

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
    def container_spec_gcs_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#container_spec_gcs_path GoogleDataflowFlexTemplateJob#container_spec_gcs_path}.'''
        result = self._values.get("container_spec_gcs_path")
        assert result is not None, "Required property 'container_spec_gcs_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#name GoogleDataflowFlexTemplateJob#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_experiments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of experiments that should be used by the job. An example value is ["enable_stackdriver_agent_metrics"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#additional_experiments GoogleDataflowFlexTemplateJob#additional_experiments}
        '''
        result = self._values.get("additional_experiments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def additional_pipeline_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of pipeline options that should be used by the job. An example value is ["numberOfWorkerHarnessThreads=20"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#additional_pipeline_options GoogleDataflowFlexTemplateJob#additional_pipeline_options}
        '''
        result = self._values.get("additional_pipeline_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def autoscaling_algorithm(self) -> typing.Optional[builtins.str]:
        '''The algorithm to use for autoscaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#autoscaling_algorithm GoogleDataflowFlexTemplateJob#autoscaling_algorithm}
        '''
        result = self._values.get("autoscaling_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_streaming_engine(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if the job should use the streaming engine feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#enable_streaming_engine GoogleDataflowFlexTemplateJob#enable_streaming_engine}
        '''
        result = self._values.get("enable_streaming_engine")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#id GoogleDataflowFlexTemplateJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_configuration(self) -> typing.Optional[builtins.str]:
        '''The configuration for VM IPs. Options are "WORKER_IP_PUBLIC" or "WORKER_IP_PRIVATE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#ip_configuration GoogleDataflowFlexTemplateJob#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The name for the Cloud KMS key for the job. Key format is: projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#kms_key_name GoogleDataflowFlexTemplateJob#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User labels to be specified for the job.

        Keys and values should follow the restrictions specified in the labeling restrictions page. NOTE: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#labels GoogleDataflowFlexTemplateJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def launcher_machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type to use for launching the job. The default is n1-standard-1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#launcher_machine_type GoogleDataflowFlexTemplateJob#launcher_machine_type}
        '''
        result = self._values.get("launcher_machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type to use for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#machine_type GoogleDataflowFlexTemplateJob#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of Google Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#max_workers GoogleDataflowFlexTemplateJob#max_workers}
        '''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The network to which VMs will be assigned. If it is not provided, "default" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#network GoogleDataflowFlexTemplateJob#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''The initial number of Google Compute Engine instances for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#num_workers GoogleDataflowFlexTemplateJob#num_workers}
        '''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#on_delete GoogleDataflowFlexTemplateJob#on_delete}.'''
        result = self._values.get("on_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#parameters GoogleDataflowFlexTemplateJob#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#project GoogleDataflowFlexTemplateJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region in which the created job should run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#region GoogleDataflowFlexTemplateJob#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sdk_container_image(self) -> typing.Optional[builtins.str]:
        '''Docker registry location of container image to use for the 'worker harness.

        Default is the container for the version of the SDK. Note this field is only valid for portable pipelines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#sdk_container_image GoogleDataflowFlexTemplateJob#sdk_container_image}
        '''
        result = self._values.get("sdk_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Service Account email used to create the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#service_account_email GoogleDataflowFlexTemplateJob#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_wait_on_job_termination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, treat DRAINING and CANCELLING as terminal job states and do not wait for further changes before removing from terraform state and moving on.

        WARNING: this will lead to job name conflicts if you do not ensure that the job names are different, e.g. by embedding a release ID or by using a random_id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#skip_wait_on_job_termination GoogleDataflowFlexTemplateJob#skip_wait_on_job_termination}
        '''
        result = self._values.get("skip_wait_on_job_termination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def staging_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage path to use for staging files. Must be a valid Cloud Storage URL, beginning with gs://.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#staging_location GoogleDataflowFlexTemplateJob#staging_location}
        '''
        result = self._values.get("staging_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The subnetwork to which VMs will be assigned. Should be of the form "regions/REGION/subnetworks/SUBNETWORK".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#subnetwork GoogleDataflowFlexTemplateJob#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#temp_location GoogleDataflowFlexTemplateJob#temp_location}
        '''
        result = self._values.get("temp_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transform_name_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Only applicable when updating a pipeline.

        Map of transform name prefixes of the job to be replaced with the corresponding name prefixes of the new job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataflow_flex_template_job#transform_name_mapping GoogleDataflowFlexTemplateJob#transform_name_mapping}
        '''
        result = self._values.get("transform_name_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataflowFlexTemplateJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GoogleDataflowFlexTemplateJob",
    "GoogleDataflowFlexTemplateJobConfig",
]

publication.publish()

def _typecheckingstub__013e09be6a774a88845af984bf9e30a636c685203d324d91ee99f699b472fdee(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container_spec_gcs_path: builtins.str,
    name: builtins.str,
    additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_pipeline_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    autoscaling_algorithm: typing.Optional[builtins.str] = None,
    enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_configuration: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launcher_machine_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_workers: typing.Optional[jsii.Number] = None,
    network: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    on_delete: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sdk_container_image: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    skip_wait_on_job_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    staging_location: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    temp_location: typing.Optional[builtins.str] = None,
    transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__0886dcdd8d4bead5cd6b2a75516b775150079b8c21077ea4587b31f7ab0a4d37(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67170bdf764c33767d6e2766219635750540e8926a84efd6f2d1b0863e8953e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7d1cfbd5d94642178cca29cdb6504599a20c682b849d3227c102a007ad5296(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532a35eda53f0d8fcd09f3afee1db3a4ae5826be2472130e5e73e81f2a759f5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e817f92e5dca948168c452e8698f62cad3d3afe0be7b55e32dfc404f3880e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90058f03955066b58f553c6e46cacccf14f34c80065f5eb9005e7e617294d7d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a97b1a2af4a30e5ed3b2cf2bcf892c52662f47e2ca974ffe0674527cfc68a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc788960ceeecba9a7fd998e0d52a31261237cae9061921e321e8ee16fce5b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8d6f3b17ba4232e6a8a7034d38663e8954659d784f62e34c8093a5e307ca97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4893141cdde28ae7b65dc1b0d18127a37c53e0338b9283bef41ed7f33b95656b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a200c2667d1e08ac1c27287c6a138e5d9c8f6314092f775c1c46afe5d2130aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac41c89b9041c852cee2a29eccb43451eebf442953a0d559ddb87f11c98ead6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f91e06b104ddda3c7b1df0495d6b621015775bf450a449be865f790878fb37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc11dc7347e73bd66125b222ed73e9e11ba8e526628b055a48f992c45d93a81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9873876b758bc04575930cf01d2cd731b4e107baa4d656d07a1bd63bfb8e6dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd32e2cdc418dc699d85c5f49967f7c8784211aa6e0de0fc3817fa3e52c8b833(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6977704fe6666d37197ac75b55b3fcc47f278cec5283398d650d5888a89643cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d6c658051af9762136cd9467f1b93f2abe6a27678cf81832769342d6659884(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605f35dcac0e805dbbaa32919798a4ecb8980b8c50e406969052bee5faf1c209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cdc39671f5e046b7f3bda98d48ca83903f13d76aa7176979c6797ff3e6497c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211ed1ae4703e75c70e77dc76339ff4cfb2734e55610ab6956bde383998ecd9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a71be9a0682f03c8fb032765885e7895883cc3a80af3f9638f39803fc11709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5915a46969b18ea718200d24e4b345bb7418bb15485e4ee81b0b553cbed317(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e267b01a1fff0c6298469e2507fff6a6b04b0d82cee755ce9e3cbfa0e03992(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2798934d63820bbb20aac484db7b7915ec85eb60b335efd7e34cc7075b833c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f251664c56a9e8a6f169d012400a1ed8e5c870aba6b4c83ba49481e3b58f1ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e5c4a8e5b9f6d02d091d07e88d080e5e65d6d13dac8f87e36f83abbcbe7d52(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de023addd99a52594a5a29a6dc457e88db74f737f253395920b5d7a5b38da68(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_spec_gcs_path: builtins.str,
    name: builtins.str,
    additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_pipeline_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    autoscaling_algorithm: typing.Optional[builtins.str] = None,
    enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_configuration: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launcher_machine_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_workers: typing.Optional[jsii.Number] = None,
    network: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    on_delete: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sdk_container_image: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    skip_wait_on_job_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    staging_location: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    temp_location: typing.Optional[builtins.str] = None,
    transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
