r'''
# `google_data_pipeline_pipeline`

Refer to the Terraform Registry for docs: [`google_data_pipeline_pipeline`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline).
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


class GoogleDataPipelinePipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline google_data_pipeline_pipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        state: builtins.str,
        type: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pipeline_sources: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        schedule_info: typing.Optional[typing.Union["GoogleDataPipelinePipelineScheduleInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler_service_account_email: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataPipelinePipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkload", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline google_data_pipeline_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: "The pipeline name. For example': 'projects/PROJECT_ID/locations/LOCATION_ID/pipelines/PIPELINE_ID." "- PROJECT_ID can contain letters ([A-Za-z]), numbers ([0-9]), hyphens (-), colons (:), and periods (.). For more information, see Identifying projects." "LOCATION_ID is the canonical ID for the pipeline's location. The list of available locations can be obtained by calling google.cloud.location.Locations.ListLocations. Note that the Data Pipelines service is not available in all regions. It depends on Cloud Scheduler, an App Engine application, so it's only available in App Engine regions." "PIPELINE_ID is the ID of the pipeline. Must be unique for the selected project and location." Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#name GoogleDataPipelinePipeline#name}
        :param state: The state of the pipeline. When the pipeline is created, the state is set to 'PIPELINE_STATE_ACTIVE' by default. State changes can be requested by setting the state to stopping, paused, or resuming. State cannot be changed through pipelines.patch requests. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#state Possible values: ["STATE_UNSPECIFIED", "STATE_RESUMING", "STATE_ACTIVE", "STATE_STOPPING", "STATE_ARCHIVED", "STATE_PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#state GoogleDataPipelinePipeline#state}
        :param type: The type of the pipeline. This field affects the scheduling of the pipeline and the type of metrics to show for the pipeline. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#pipelinetype Possible values: ["PIPELINE_TYPE_UNSPECIFIED", "PIPELINE_TYPE_BATCH", "PIPELINE_TYPE_STREAMING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#type GoogleDataPipelinePipeline#type}
        :param display_name: The display name of the pipeline. It can contain only letters ([A-Za-z]), numbers ([0-9]), hyphens (-), and underscores (_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#display_name GoogleDataPipelinePipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#id GoogleDataPipelinePipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pipeline_sources: The sources of the pipeline (for example, Dataplex). The keys and values are set by the corresponding sources during pipeline creation. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#pipeline_sources GoogleDataPipelinePipeline#pipeline_sources}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project GoogleDataPipelinePipeline#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#region GoogleDataPipelinePipeline#region}
        :param schedule_info: schedule_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#schedule_info GoogleDataPipelinePipeline#schedule_info}
        :param scheduler_service_account_email: Optional. A service account email to be used with the Cloud Scheduler job. If not specified, the default compute engine service account will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#scheduler_service_account_email GoogleDataPipelinePipeline#scheduler_service_account_email}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#timeouts GoogleDataPipelinePipeline#timeouts}
        :param workload: workload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#workload GoogleDataPipelinePipeline#workload}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1164e51cf8c3d968b7015a47366e1d59e4f917f5c7288200cdb7872fac6b4f45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataPipelinePipelineConfig(
            name=name,
            state=state,
            type=type,
            display_name=display_name,
            id=id,
            pipeline_sources=pipeline_sources,
            project=project,
            region=region,
            schedule_info=schedule_info,
            scheduler_service_account_email=scheduler_service_account_email,
            timeouts=timeouts,
            workload=workload,
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
        '''Generates CDKTF code for importing a GoogleDataPipelinePipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataPipelinePipeline to import.
        :param import_from_id: The id of the existing GoogleDataPipelinePipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataPipelinePipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423318e4b60da69d6f71479753a29696a5a6aa31b9d107116fcf41939f62c421)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putScheduleInfo")
    def put_schedule_info(
        self,
        *,
        schedule: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule: Unix-cron format of the schedule. This information is retrieved from the linked Cloud Scheduler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#schedule GoogleDataPipelinePipeline#schedule}
        :param time_zone: Timezone ID. This matches the timezone IDs used by the Cloud Scheduler API. If empty, UTC time is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#time_zone GoogleDataPipelinePipeline#time_zone}
        '''
        value = GoogleDataPipelinePipelineScheduleInfo(
            schedule=schedule, time_zone=time_zone
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleInfo", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#create GoogleDataPipelinePipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#delete GoogleDataPipelinePipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}.
        '''
        value = GoogleDataPipelinePipelineTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkload")
    def put_workload(
        self,
        *,
        dataflow_flex_template_request: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        dataflow_launch_template_request: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dataflow_flex_template_request: dataflow_flex_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#dataflow_flex_template_request GoogleDataPipelinePipeline#dataflow_flex_template_request}
        :param dataflow_launch_template_request: dataflow_launch_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#dataflow_launch_template_request GoogleDataPipelinePipeline#dataflow_launch_template_request}
        '''
        value = GoogleDataPipelinePipelineWorkload(
            dataflow_flex_template_request=dataflow_flex_template_request,
            dataflow_launch_template_request=dataflow_launch_template_request,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkload", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPipelineSources")
    def reset_pipeline_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineSources", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScheduleInfo")
    def reset_schedule_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleInfo", []))

    @jsii.member(jsii_name="resetSchedulerServiceAccountEmail")
    def reset_scheduler_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulerServiceAccountEmail", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkload")
    def reset_workload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkload", []))

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
    @jsii.member(jsii_name="jobCount")
    def job_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jobCount"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdateTime")
    def last_update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInfo")
    def schedule_info(self) -> "GoogleDataPipelinePipelineScheduleInfoOutputReference":
        return typing.cast("GoogleDataPipelinePipelineScheduleInfoOutputReference", jsii.get(self, "scheduleInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataPipelinePipelineTimeoutsOutputReference":
        return typing.cast("GoogleDataPipelinePipelineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workload")
    def workload(self) -> "GoogleDataPipelinePipelineWorkloadOutputReference":
        return typing.cast("GoogleDataPipelinePipelineWorkloadOutputReference", jsii.get(self, "workload"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineSourcesInput")
    def pipeline_sources_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "pipelineSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInfoInput")
    def schedule_info_input(
        self,
    ) -> typing.Optional["GoogleDataPipelinePipelineScheduleInfo"]:
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineScheduleInfo"], jsii.get(self, "scheduleInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerServiceAccountEmailInput")
    def scheduler_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schedulerServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataPipelinePipelineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataPipelinePipelineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadInput")
    def workload_input(self) -> typing.Optional["GoogleDataPipelinePipelineWorkload"]:
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineWorkload"], jsii.get(self, "workloadInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9de8e38c040c80a9841d8ff353d8528d55632a96f534bec8c90b90ba89cb87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd91f4f2ef53948dd66c343e1063a4ad2157ba4ea4ace2b631eb95c6a3d62d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a0af60dcbdd68cedde1b029416d662d3b8a2f449a3cca23aab95c896d3bc3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipelineSources")
    def pipeline_sources(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "pipelineSources"))

    @pipeline_sources.setter
    def pipeline_sources(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4b94df1169ffca65f51fec100681576590988d79452c2562f6528b6be13cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineSources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8948c275ea24e012e80340793b5a75fe7088c0e5b404f16c3a87dbb1e093da42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0830ef81cc7ea9b8780dbf93d9a1b08a94e51f101508379715cb9c4f4fcab9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedulerServiceAccountEmail")
    def scheduler_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedulerServiceAccountEmail"))

    @scheduler_service_account_email.setter
    def scheduler_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ff49f15e870293194cc3f2ce62e6764327a7d76cd39b8063372cee2b247726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulerServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3047c7603269b18627d065ad517a19d19cd1e1567ef8bb267ee09cbb079374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5c07fd34ce848d4fdfb47469ffc9ee500cbe764c3d6bf0d1e7c7ab059031f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "state": "state",
        "type": "type",
        "display_name": "displayName",
        "id": "id",
        "pipeline_sources": "pipelineSources",
        "project": "project",
        "region": "region",
        "schedule_info": "scheduleInfo",
        "scheduler_service_account_email": "schedulerServiceAccountEmail",
        "timeouts": "timeouts",
        "workload": "workload",
    },
)
class GoogleDataPipelinePipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        state: builtins.str,
        type: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pipeline_sources: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        schedule_info: typing.Optional[typing.Union["GoogleDataPipelinePipelineScheduleInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler_service_account_email: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataPipelinePipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: "The pipeline name. For example': 'projects/PROJECT_ID/locations/LOCATION_ID/pipelines/PIPELINE_ID." "- PROJECT_ID can contain letters ([A-Za-z]), numbers ([0-9]), hyphens (-), colons (:), and periods (.). For more information, see Identifying projects." "LOCATION_ID is the canonical ID for the pipeline's location. The list of available locations can be obtained by calling google.cloud.location.Locations.ListLocations. Note that the Data Pipelines service is not available in all regions. It depends on Cloud Scheduler, an App Engine application, so it's only available in App Engine regions." "PIPELINE_ID is the ID of the pipeline. Must be unique for the selected project and location." Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#name GoogleDataPipelinePipeline#name}
        :param state: The state of the pipeline. When the pipeline is created, the state is set to 'PIPELINE_STATE_ACTIVE' by default. State changes can be requested by setting the state to stopping, paused, or resuming. State cannot be changed through pipelines.patch requests. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#state Possible values: ["STATE_UNSPECIFIED", "STATE_RESUMING", "STATE_ACTIVE", "STATE_STOPPING", "STATE_ARCHIVED", "STATE_PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#state GoogleDataPipelinePipeline#state}
        :param type: The type of the pipeline. This field affects the scheduling of the pipeline and the type of metrics to show for the pipeline. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#pipelinetype Possible values: ["PIPELINE_TYPE_UNSPECIFIED", "PIPELINE_TYPE_BATCH", "PIPELINE_TYPE_STREAMING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#type GoogleDataPipelinePipeline#type}
        :param display_name: The display name of the pipeline. It can contain only letters ([A-Za-z]), numbers ([0-9]), hyphens (-), and underscores (_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#display_name GoogleDataPipelinePipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#id GoogleDataPipelinePipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pipeline_sources: The sources of the pipeline (for example, Dataplex). The keys and values are set by the corresponding sources during pipeline creation. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#pipeline_sources GoogleDataPipelinePipeline#pipeline_sources}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project GoogleDataPipelinePipeline#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#region GoogleDataPipelinePipeline#region}
        :param schedule_info: schedule_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#schedule_info GoogleDataPipelinePipeline#schedule_info}
        :param scheduler_service_account_email: Optional. A service account email to be used with the Cloud Scheduler job. If not specified, the default compute engine service account will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#scheduler_service_account_email GoogleDataPipelinePipeline#scheduler_service_account_email}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#timeouts GoogleDataPipelinePipeline#timeouts}
        :param workload: workload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#workload GoogleDataPipelinePipeline#workload}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(schedule_info, dict):
            schedule_info = GoogleDataPipelinePipelineScheduleInfo(**schedule_info)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataPipelinePipelineTimeouts(**timeouts)
        if isinstance(workload, dict):
            workload = GoogleDataPipelinePipelineWorkload(**workload)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6828e8e3eeb3d89de1be4bfe322e68bfcd0bbc93129baf0f330de93494905a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pipeline_sources", value=pipeline_sources, expected_type=type_hints["pipeline_sources"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument schedule_info", value=schedule_info, expected_type=type_hints["schedule_info"])
            check_type(argname="argument scheduler_service_account_email", value=scheduler_service_account_email, expected_type=type_hints["scheduler_service_account_email"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workload", value=workload, expected_type=type_hints["workload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "state": state,
            "type": type,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if pipeline_sources is not None:
            self._values["pipeline_sources"] = pipeline_sources
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if schedule_info is not None:
            self._values["schedule_info"] = schedule_info
        if scheduler_service_account_email is not None:
            self._values["scheduler_service_account_email"] = scheduler_service_account_email
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workload is not None:
            self._values["workload"] = workload

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
    def name(self) -> builtins.str:
        '''"The pipeline name.

        For example': 'projects/PROJECT_ID/locations/LOCATION_ID/pipelines/PIPELINE_ID."
        "- PROJECT_ID can contain letters ([A-Za-z]), numbers ([0-9]), hyphens (-), colons (:), and periods (.). For more information, see Identifying projects."
        "LOCATION_ID is the canonical ID for the pipeline's location. The list of available locations can be obtained by calling google.cloud.location.Locations.ListLocations. Note that the Data Pipelines service is not available in all regions. It depends on Cloud Scheduler, an App Engine application, so it's only available in App Engine regions."
        "PIPELINE_ID is the ID of the pipeline. Must be unique for the selected project and location."

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#name GoogleDataPipelinePipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''The state of the pipeline.

        When the pipeline is created, the state is set to 'PIPELINE_STATE_ACTIVE' by default. State changes can be requested by setting the state to stopping, paused, or resuming. State cannot be changed through pipelines.patch requests.
        https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#state Possible values: ["STATE_UNSPECIFIED", "STATE_RESUMING", "STATE_ACTIVE", "STATE_STOPPING", "STATE_ARCHIVED", "STATE_PAUSED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#state GoogleDataPipelinePipeline#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the pipeline.

        This field affects the scheduling of the pipeline and the type of metrics to show for the pipeline.
        https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#pipelinetype Possible values: ["PIPELINE_TYPE_UNSPECIFIED", "PIPELINE_TYPE_BATCH", "PIPELINE_TYPE_STREAMING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#type GoogleDataPipelinePipeline#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the pipeline. It can contain only letters ([A-Za-z]), numbers ([0-9]), hyphens (-), and underscores (_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#display_name GoogleDataPipelinePipeline#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#id GoogleDataPipelinePipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_sources(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The sources of the pipeline (for example, Dataplex).

        The keys and values are set by the corresponding sources during pipeline creation.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#pipeline_sources GoogleDataPipelinePipeline#pipeline_sources}
        '''
        result = self._values.get("pipeline_sources")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project GoogleDataPipelinePipeline#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#region GoogleDataPipelinePipeline#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_info(
        self,
    ) -> typing.Optional["GoogleDataPipelinePipelineScheduleInfo"]:
        '''schedule_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#schedule_info GoogleDataPipelinePipeline#schedule_info}
        '''
        result = self._values.get("schedule_info")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineScheduleInfo"], result)

    @builtins.property
    def scheduler_service_account_email(self) -> typing.Optional[builtins.str]:
        '''Optional.

        A service account email to be used with the Cloud Scheduler job. If not specified, the default compute engine service account will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#scheduler_service_account_email GoogleDataPipelinePipeline#scheduler_service_account_email}
        '''
        result = self._values.get("scheduler_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataPipelinePipelineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#timeouts GoogleDataPipelinePipeline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineTimeouts"], result)

    @builtins.property
    def workload(self) -> typing.Optional["GoogleDataPipelinePipelineWorkload"]:
        '''workload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#workload GoogleDataPipelinePipeline#workload}
        '''
        result = self._values.get("workload")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineWorkload"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineScheduleInfo",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule", "time_zone": "timeZone"},
)
class GoogleDataPipelinePipelineScheduleInfo:
    def __init__(
        self,
        *,
        schedule: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule: Unix-cron format of the schedule. This information is retrieved from the linked Cloud Scheduler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#schedule GoogleDataPipelinePipeline#schedule}
        :param time_zone: Timezone ID. This matches the timezone IDs used by the Cloud Scheduler API. If empty, UTC time is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#time_zone GoogleDataPipelinePipeline#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4953af14f4c95547a350b4811e783ce182c5edcc898a4898ffd76153b43bf929)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schedule is not None:
            self._values["schedule"] = schedule
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Unix-cron format of the schedule. This information is retrieved from the linked Cloud Scheduler.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#schedule GoogleDataPipelinePipeline#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Timezone ID. This matches the timezone IDs used by the Cloud Scheduler API. If empty, UTC time is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#time_zone GoogleDataPipelinePipeline#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineScheduleInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataPipelinePipelineScheduleInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineScheduleInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__769a135e21520b27a50af7ce56c0d629b9903fd13ef3c4a886357cf168b87e77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="nextJobTime")
    def next_job_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextJobTime"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0a7ffd2b7bef1dfab13d3c07f84efbcf2d671d4ad91d4f982c9e3c6f2c0dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee4ad12e58f44e83f6474fb94efc9408df4d00c9bcff0507bd6469bf41a722e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataPipelinePipelineScheduleInfo]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineScheduleInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineScheduleInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f60705c4a7c062e090cca05240121e1f80f6099738955360a9a651cbf6e7aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataPipelinePipelineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#create GoogleDataPipelinePipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#delete GoogleDataPipelinePipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc4e2ecd669f6990e0d1679c98998d483343b282279cc7fa89bd03398df3ab1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#create GoogleDataPipelinePipeline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#delete GoogleDataPipelinePipeline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataPipelinePipelineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae605514fff7bf887b46d18e9a55e5f0bca4941c0b9733e057dcc032f27af5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e496e92c16640f6bc7618f75b4531168178d05b36603c245f0b66cc5a6273e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afcebf5216e0def11c86c5cc6bc3205352eab9cce5fea6f32ff6abfc6daa4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec58e0f8f59f8e0399e6c55d8f52a914bbe9a745b673d7594707bad44866b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataPipelinePipelineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataPipelinePipelineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataPipelinePipelineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a67741167973142027e043d0b4d61334b88c1e03cf015b8d4a7b152db77bbfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkload",
    jsii_struct_bases=[],
    name_mapping={
        "dataflow_flex_template_request": "dataflowFlexTemplateRequest",
        "dataflow_launch_template_request": "dataflowLaunchTemplateRequest",
    },
)
class GoogleDataPipelinePipelineWorkload:
    def __init__(
        self,
        *,
        dataflow_flex_template_request: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        dataflow_launch_template_request: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dataflow_flex_template_request: dataflow_flex_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#dataflow_flex_template_request GoogleDataPipelinePipeline#dataflow_flex_template_request}
        :param dataflow_launch_template_request: dataflow_launch_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#dataflow_launch_template_request GoogleDataPipelinePipeline#dataflow_launch_template_request}
        '''
        if isinstance(dataflow_flex_template_request, dict):
            dataflow_flex_template_request = GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest(**dataflow_flex_template_request)
        if isinstance(dataflow_launch_template_request, dict):
            dataflow_launch_template_request = GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest(**dataflow_launch_template_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c4025d3ed7c401ccacecea15694c534f8390e6ce735c178b8e413b25977515)
            check_type(argname="argument dataflow_flex_template_request", value=dataflow_flex_template_request, expected_type=type_hints["dataflow_flex_template_request"])
            check_type(argname="argument dataflow_launch_template_request", value=dataflow_launch_template_request, expected_type=type_hints["dataflow_launch_template_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataflow_flex_template_request is not None:
            self._values["dataflow_flex_template_request"] = dataflow_flex_template_request
        if dataflow_launch_template_request is not None:
            self._values["dataflow_launch_template_request"] = dataflow_launch_template_request

    @builtins.property
    def dataflow_flex_template_request(
        self,
    ) -> typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest"]:
        '''dataflow_flex_template_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#dataflow_flex_template_request GoogleDataPipelinePipeline#dataflow_flex_template_request}
        '''
        result = self._values.get("dataflow_flex_template_request")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest"], result)

    @builtins.property
    def dataflow_launch_template_request(
        self,
    ) -> typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest"]:
        '''dataflow_launch_template_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#dataflow_launch_template_request GoogleDataPipelinePipeline#dataflow_launch_template_request}
        '''
        result = self._values.get("dataflow_launch_template_request")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineWorkload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest",
    jsii_struct_bases=[],
    name_mapping={
        "launch_parameter": "launchParameter",
        "location": "location",
        "project_id": "projectId",
        "validate_only": "validateOnly",
    },
)
class GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest:
    def __init__(
        self,
        *,
        launch_parameter: typing.Union["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        project_id: builtins.str,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param launch_parameter: launch_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_parameter GoogleDataPipelinePipeline#launch_parameter}
        :param location: The regional endpoint to which to direct the request. For example, us-central1, us-west1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#location GoogleDataPipelinePipeline#location}
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project_id GoogleDataPipelinePipeline#project_id}
        :param validate_only: If true, the request is validated but not actually executed. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#validate_only GoogleDataPipelinePipeline#validate_only}
        '''
        if isinstance(launch_parameter, dict):
            launch_parameter = GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter(**launch_parameter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dd1aac391f426a8f01c2da155460d157fadde5eae4a4008e854f58318fdcc8)
            check_type(argname="argument launch_parameter", value=launch_parameter, expected_type=type_hints["launch_parameter"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument validate_only", value=validate_only, expected_type=type_hints["validate_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "launch_parameter": launch_parameter,
            "location": location,
            "project_id": project_id,
        }
        if validate_only is not None:
            self._values["validate_only"] = validate_only

    @builtins.property
    def launch_parameter(
        self,
    ) -> "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter":
        '''launch_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_parameter GoogleDataPipelinePipeline#launch_parameter}
        '''
        result = self._values.get("launch_parameter")
        assert result is not None, "Required property 'launch_parameter' is missing"
        return typing.cast("GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The regional endpoint to which to direct the request. For example, us-central1, us-west1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#location GoogleDataPipelinePipeline#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the Cloud Platform project that the job belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project_id GoogleDataPipelinePipeline#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validate_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the request is validated but not actually executed. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#validate_only GoogleDataPipelinePipeline#validate_only}
        '''
        result = self._values.get("validate_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "container_spec_gcs_path": "containerSpecGcsPath",
        "environment": "environment",
        "launch_options": "launchOptions",
        "parameters": "parameters",
        "transform_name_mappings": "transformNameMappings",
        "update": "update",
    },
)
class GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter:
    def __init__(
        self,
        *,
        job_name: builtins.str,
        container_spec_gcs_path: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        launch_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. For an update job request, the job name should be the same as the existing running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#job_name GoogleDataPipelinePipeline#job_name}
        :param container_spec_gcs_path: Cloud Storage path to a file with a JSON-serialized ContainerSpec as content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#container_spec_gcs_path GoogleDataPipelinePipeline#container_spec_gcs_path}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#environment GoogleDataPipelinePipeline#environment}
        :param launch_options: Launch options for this Flex Template job. This is a common set of options across languages and templates. This should not be used to pass job parameters. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_options GoogleDataPipelinePipeline#launch_options}
        :param parameters: 'The parameters for the Flex Template. Example: {"numWorkers":"5"}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#parameters GoogleDataPipelinePipeline#parameters}
        :param transform_name_mappings: 'Use this to pass transform name mappings for streaming update jobs. Example: {"oldTransformName":"newTransformName",...}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#transform_name_mappings GoogleDataPipelinePipeline#transform_name_mappings}
        :param update: Set this to true if you are sending a request to update a running streaming job. When set, the job name should be the same as the running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}
        '''
        if isinstance(environment, dict):
            environment = GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment(**environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f318685a21dec14c71ceeb1c7fa387d000edd893185d85f1fa9f74a718f0db27)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument container_spec_gcs_path", value=container_spec_gcs_path, expected_type=type_hints["container_spec_gcs_path"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument launch_options", value=launch_options, expected_type=type_hints["launch_options"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument transform_name_mappings", value=transform_name_mappings, expected_type=type_hints["transform_name_mappings"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_name": job_name,
        }
        if container_spec_gcs_path is not None:
            self._values["container_spec_gcs_path"] = container_spec_gcs_path
        if environment is not None:
            self._values["environment"] = environment
        if launch_options is not None:
            self._values["launch_options"] = launch_options
        if parameters is not None:
            self._values["parameters"] = parameters
        if transform_name_mappings is not None:
            self._values["transform_name_mappings"] = transform_name_mappings
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def job_name(self) -> builtins.str:
        '''The job name to use for the created job.

        For an update job request, the job name should be the same as the existing running job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#job_name GoogleDataPipelinePipeline#job_name}
        '''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_spec_gcs_path(self) -> typing.Optional[builtins.str]:
        '''Cloud Storage path to a file with a JSON-serialized ContainerSpec as content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#container_spec_gcs_path GoogleDataPipelinePipeline#container_spec_gcs_path}
        '''
        result = self._values.get("container_spec_gcs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment"]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#environment GoogleDataPipelinePipeline#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment"], result)

    @builtins.property
    def launch_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Launch options for this Flex Template job.

        This is a common set of options across languages and templates. This should not be used to pass job parameters.
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_options GoogleDataPipelinePipeline#launch_options}
        '''
        result = self._values.get("launch_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ''''The parameters for the Flex Template.

        Example: {"numWorkers":"5"}'
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#parameters GoogleDataPipelinePipeline#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def transform_name_mappings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ''''Use this to pass transform name mappings for streaming update jobs.

        Example: {"oldTransformName":"newTransformName",...}'
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#transform_name_mappings GoogleDataPipelinePipeline#transform_name_mappings}
        '''
        result = self._values.get("transform_name_mappings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set this to true if you are sending a request to update a running streaming job.

        When set, the job name should be the same as the running job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment",
    jsii_struct_bases=[],
    name_mapping={
        "additional_experiments": "additionalExperiments",
        "additional_user_labels": "additionalUserLabels",
        "enable_streaming_engine": "enableStreamingEngine",
        "flexrs_goal": "flexrsGoal",
        "ip_configuration": "ipConfiguration",
        "kms_key_name": "kmsKeyName",
        "machine_type": "machineType",
        "max_workers": "maxWorkers",
        "network": "network",
        "num_workers": "numWorkers",
        "service_account_email": "serviceAccountEmail",
        "subnetwork": "subnetwork",
        "temp_location": "tempLocation",
        "worker_region": "workerRegion",
        "worker_zone": "workerZone",
        "zone": "zone",
    },
)
class GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment:
    def __init__(
        self,
        *,
        additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        flexrs_goal: typing.Optional[builtins.str] = None,
        ip_configuration: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        temp_location: typing.Optional[builtins.str] = None,
        worker_region: typing.Optional[builtins.str] = None,
        worker_zone: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_experiments GoogleDataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_user_labels GoogleDataPipelinePipeline#additional_user_labels}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#enable_streaming_engine GoogleDataPipelinePipeline#enable_streaming_engine}
        :param flexrs_goal: Set FlexRS goal for the job. https://cloud.google.com/dataflow/docs/guides/flexrs https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#FlexResourceSchedulingGoal Possible values: ["FLEXRS_UNSPECIFIED", "FLEXRS_SPEED_OPTIMIZED", "FLEXRS_COST_OPTIMIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#flexrs_goal GoogleDataPipelinePipeline#flexrs_goal}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#ip_configuration GoogleDataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#kms_key_name GoogleDataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#machine_type GoogleDataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#max_workers GoogleDataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#network GoogleDataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#num_workers GoogleDataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#service_account_email GoogleDataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#subnetwork GoogleDataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#temp_location GoogleDataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_region GoogleDataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_zone GoogleDataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#zone GoogleDataPipelinePipeline#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e2deaaf2739d827b22c16442a2afe134e899e4c149686b20ead8d65bfb1e3e)
            check_type(argname="argument additional_experiments", value=additional_experiments, expected_type=type_hints["additional_experiments"])
            check_type(argname="argument additional_user_labels", value=additional_user_labels, expected_type=type_hints["additional_user_labels"])
            check_type(argname="argument enable_streaming_engine", value=enable_streaming_engine, expected_type=type_hints["enable_streaming_engine"])
            check_type(argname="argument flexrs_goal", value=flexrs_goal, expected_type=type_hints["flexrs_goal"])
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument num_workers", value=num_workers, expected_type=type_hints["num_workers"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument temp_location", value=temp_location, expected_type=type_hints["temp_location"])
            check_type(argname="argument worker_region", value=worker_region, expected_type=type_hints["worker_region"])
            check_type(argname="argument worker_zone", value=worker_zone, expected_type=type_hints["worker_zone"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_experiments is not None:
            self._values["additional_experiments"] = additional_experiments
        if additional_user_labels is not None:
            self._values["additional_user_labels"] = additional_user_labels
        if enable_streaming_engine is not None:
            self._values["enable_streaming_engine"] = enable_streaming_engine
        if flexrs_goal is not None:
            self._values["flexrs_goal"] = flexrs_goal
        if ip_configuration is not None:
            self._values["ip_configuration"] = ip_configuration
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if network is not None:
            self._values["network"] = network
        if num_workers is not None:
            self._values["num_workers"] = num_workers
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if temp_location is not None:
            self._values["temp_location"] = temp_location
        if worker_region is not None:
            self._values["worker_region"] = worker_region
        if worker_zone is not None:
            self._values["worker_zone"] = worker_zone
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def additional_experiments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional experiment flags for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_experiments GoogleDataPipelinePipeline#additional_experiments}
        '''
        result = self._values.get("additional_experiments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def additional_user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional user labels to be specified for the job.

        Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs.
        'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.'
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_user_labels GoogleDataPipelinePipeline#additional_user_labels}
        '''
        result = self._values.get("additional_user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def enable_streaming_engine(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable Streaming Engine for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#enable_streaming_engine GoogleDataPipelinePipeline#enable_streaming_engine}
        '''
        result = self._values.get("enable_streaming_engine")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def flexrs_goal(self) -> typing.Optional[builtins.str]:
        '''Set FlexRS goal for the job. https://cloud.google.com/dataflow/docs/guides/flexrs https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#FlexResourceSchedulingGoal Possible values: ["FLEXRS_UNSPECIFIED", "FLEXRS_SPEED_OPTIMIZED", "FLEXRS_COST_OPTIMIZED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#flexrs_goal GoogleDataPipelinePipeline#flexrs_goal}
        '''
        result = self._values.get("flexrs_goal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_configuration(self) -> typing.Optional[builtins.str]:
        '''Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#ip_configuration GoogleDataPipelinePipeline#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        ''''Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#kms_key_name GoogleDataPipelinePipeline#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type to use for the job. Defaults to the value from the template if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#machine_type GoogleDataPipelinePipeline#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#max_workers GoogleDataPipelinePipeline#max_workers}
        '''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#network GoogleDataPipelinePipeline#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''The initial number of Compute Engine instances for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#num_workers GoogleDataPipelinePipeline#num_workers}
        '''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The email address of the service account to run the job as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#service_account_email GoogleDataPipelinePipeline#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Subnetwork to which VMs will be assigned, if desired.

        You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#subnetwork GoogleDataPipelinePipeline#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#temp_location GoogleDataPipelinePipeline#temp_location}
        '''
        result = self._values.get("temp_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_region(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_region GoogleDataPipelinePipeline#worker_region}
        '''
        result = self._values.get("worker_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_zone GoogleDataPipelinePipeline#worker_zone}
        '''
        result = self._values.get("worker_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine availability zone for launching worker instances to run your pipeline.

        In the future, workerZone will take precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#zone GoogleDataPipelinePipeline#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__833ad64f3bf83fb001734229ad08c66a8195619c727713b01ed72e7fdb4a2a6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalExperiments")
    def reset_additional_experiments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExperiments", []))

    @jsii.member(jsii_name="resetAdditionalUserLabels")
    def reset_additional_user_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalUserLabels", []))

    @jsii.member(jsii_name="resetEnableStreamingEngine")
    def reset_enable_streaming_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStreamingEngine", []))

    @jsii.member(jsii_name="resetFlexrsGoal")
    def reset_flexrs_goal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlexrsGoal", []))

    @jsii.member(jsii_name="resetIpConfiguration")
    def reset_ip_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpConfiguration", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

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

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTempLocation")
    def reset_temp_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTempLocation", []))

    @jsii.member(jsii_name="resetWorkerRegion")
    def reset_worker_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerRegion", []))

    @jsii.member(jsii_name="resetWorkerZone")
    def reset_worker_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerZone", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="additionalExperimentsInput")
    def additional_experiments_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalExperimentsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalUserLabelsInput")
    def additional_user_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalUserLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStreamingEngineInput")
    def enable_streaming_engine_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStreamingEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="flexrsGoalInput")
    def flexrs_goal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flexrsGoalInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkersInput")
    def max_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="numWorkersInput")
    def num_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tempLocationInput")
    def temp_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tempLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="workerRegionInput")
    def worker_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="workerZoneInput")
    def worker_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalExperiments")
    def additional_experiments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalExperiments"))

    @additional_experiments.setter
    def additional_experiments(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b3161f84b2ad725c7998a9b0038efe9bb6ab1a26a6bbe3da89a76641dcacab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalExperiments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="additionalUserLabels")
    def additional_user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalUserLabels"))

    @additional_user_labels.setter
    def additional_user_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f85ab0a6b1090c43697eeb44c4ceab46c0124b9e0e1d9d0dab9600a75f69c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalUserLabels", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9e80322dfb28a9f8d87daef6eef03167922e3550322e4946e4957951006d7905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStreamingEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flexrsGoal")
    def flexrs_goal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flexrsGoal"))

    @flexrs_goal.setter
    def flexrs_goal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f5378e5c358d0829663834513c21edf8fabd60d3a5059c36d71625b90965b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexrsGoal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipConfiguration"))

    @ip_configuration.setter
    def ip_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__403ff74e36efcfc95372889ebe18b90e0fde2b2408bcdf3f3ca805d2e55c2be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12a095a9778ce6f011fb41016b56522f1308144c50db4dfefdc27abc2070feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a71b3439336ec3e8a6b8ffd968f89297ddad23df50940b6dd0667935dcab7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc91f49db06cc03f6c0c950f36ba17598424a12f576fde7c4e31a1f972172fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42257479e2469709f0052073e67fc55d7a986fb0e2144cf49b3362e8c0f0666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numWorkers")
    def num_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numWorkers"))

    @num_workers.setter
    def num_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1a3f63cd36eb7a288eeb1ce57f4da72ff446b097e1997057bbbabbf81bcd6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd6f16a0a8751407e6bae46d1ab23beb0dae882dca01bb3a711086c110f18be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861afb7fafd4746f519a0f19e2bce6c29d6b0ecbac9f938597100aa1cea412c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tempLocation")
    def temp_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempLocation"))

    @temp_location.setter
    def temp_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba86b6ebfa59d8a19ca86510a18b491ff89ba55811393f1a6373b0946c82f60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerRegion")
    def worker_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerRegion"))

    @worker_region.setter
    def worker_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee27fd6197f651e078924866ae6aa3b746815bbd6cf5d954b499950b55c5201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerZone")
    def worker_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerZone"))

    @worker_zone.setter
    def worker_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebcddff94a9abbcb111fe36ab30f023b162e35bb7d25cdcf7fe480b8a38ce66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e928c8ef1d97dc8044639054b85d5768dcbd03ea601e9b5ed4d4e8621b61e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d097ecff779a83ad3d639ae0a716c7c4511c36ca13f73dbeb32193d0d3cf1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c608ae4f0250d8f80a01d25d1f4860f4a84881613366218f7cbb1b0f02e44f15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        *,
        additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        flexrs_goal: typing.Optional[builtins.str] = None,
        ip_configuration: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        temp_location: typing.Optional[builtins.str] = None,
        worker_region: typing.Optional[builtins.str] = None,
        worker_zone: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_experiments GoogleDataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_user_labels GoogleDataPipelinePipeline#additional_user_labels}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#enable_streaming_engine GoogleDataPipelinePipeline#enable_streaming_engine}
        :param flexrs_goal: Set FlexRS goal for the job. https://cloud.google.com/dataflow/docs/guides/flexrs https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#FlexResourceSchedulingGoal Possible values: ["FLEXRS_UNSPECIFIED", "FLEXRS_SPEED_OPTIMIZED", "FLEXRS_COST_OPTIMIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#flexrs_goal GoogleDataPipelinePipeline#flexrs_goal}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#ip_configuration GoogleDataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#kms_key_name GoogleDataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#machine_type GoogleDataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#max_workers GoogleDataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#network GoogleDataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#num_workers GoogleDataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#service_account_email GoogleDataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#subnetwork GoogleDataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#temp_location GoogleDataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_region GoogleDataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_zone GoogleDataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#zone GoogleDataPipelinePipeline#zone}
        '''
        value = GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment(
            additional_experiments=additional_experiments,
            additional_user_labels=additional_user_labels,
            enable_streaming_engine=enable_streaming_engine,
            flexrs_goal=flexrs_goal,
            ip_configuration=ip_configuration,
            kms_key_name=kms_key_name,
            machine_type=machine_type,
            max_workers=max_workers,
            network=network,
            num_workers=num_workers,
            service_account_email=service_account_email,
            subnetwork=subnetwork,
            temp_location=temp_location,
            worker_region=worker_region,
            worker_zone=worker_zone,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="resetContainerSpecGcsPath")
    def reset_container_spec_gcs_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerSpecGcsPath", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetLaunchOptions")
    def reset_launch_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchOptions", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetTransformNameMappings")
    def reset_transform_name_mappings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformNameMappings", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference:
        return typing.cast(GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="containerSpecGcsPathInput")
    def container_spec_gcs_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerSpecGcsPathInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="jobNameInput")
    def job_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobNameInput"))

    @builtins.property
    @jsii.member(jsii_name="launchOptionsInput")
    def launch_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "launchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="transformNameMappingsInput")
    def transform_name_mappings_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "transformNameMappingsInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="containerSpecGcsPath")
    def container_spec_gcs_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerSpecGcsPath"))

    @container_spec_gcs_path.setter
    def container_spec_gcs_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df9a38f89d49fd70ed411e28f9a09cf4769fe0d2c0c6585fddd6a44079474e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerSpecGcsPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374fefa4e9f47eb61619ef0449beaa42e7c253e16635465ed89687fa57f6f997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchOptions")
    def launch_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "launchOptions"))

    @launch_options.setter
    def launch_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7514ff0112510de5aad6ae56ffa4de531e8815ac8f03c6addeed59fbe7869e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd353a12956824a6cb35b02610ff072801ab60f7283945c2fa76b1babe30ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transformNameMappings")
    def transform_name_mappings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "transformNameMappings"))

    @transform_name_mappings.setter
    def transform_name_mappings(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8851b76d452940b7d6843ff2d0609c39597892cd2cf2693044d0d4c5c5b705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformNameMappings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "update"))

    @update.setter
    def update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360494143666e0bfe38d0c9a4144a04b738381a5ff0e48e5febc489a43324935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43c672e9462acdb26074500d07eb9ad81ed1f9a823a4263490438dccb77052f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72bc21713f7eea4aaf568fd2001910edb10569d6d8ddd73e9370133525b1d26a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLaunchParameter")
    def put_launch_parameter(
        self,
        *,
        job_name: builtins.str,
        container_spec_gcs_path: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        launch_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. For an update job request, the job name should be the same as the existing running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#job_name GoogleDataPipelinePipeline#job_name}
        :param container_spec_gcs_path: Cloud Storage path to a file with a JSON-serialized ContainerSpec as content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#container_spec_gcs_path GoogleDataPipelinePipeline#container_spec_gcs_path}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#environment GoogleDataPipelinePipeline#environment}
        :param launch_options: Launch options for this Flex Template job. This is a common set of options across languages and templates. This should not be used to pass job parameters. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_options GoogleDataPipelinePipeline#launch_options}
        :param parameters: 'The parameters for the Flex Template. Example: {"numWorkers":"5"}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#parameters GoogleDataPipelinePipeline#parameters}
        :param transform_name_mappings: 'Use this to pass transform name mappings for streaming update jobs. Example: {"oldTransformName":"newTransformName",...}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#transform_name_mappings GoogleDataPipelinePipeline#transform_name_mappings}
        :param update: Set this to true if you are sending a request to update a running streaming job. When set, the job name should be the same as the running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}
        '''
        value = GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter(
            job_name=job_name,
            container_spec_gcs_path=container_spec_gcs_path,
            environment=environment,
            launch_options=launch_options,
            parameters=parameters,
            transform_name_mappings=transform_name_mappings,
            update=update,
        )

        return typing.cast(None, jsii.invoke(self, "putLaunchParameter", [value]))

    @jsii.member(jsii_name="resetValidateOnly")
    def reset_validate_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateOnly", []))

    @builtins.property
    @jsii.member(jsii_name="launchParameter")
    def launch_parameter(
        self,
    ) -> GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference:
        return typing.cast(GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference, jsii.get(self, "launchParameter"))

    @builtins.property
    @jsii.member(jsii_name="launchParameterInput")
    def launch_parameter_input(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter], jsii.get(self, "launchParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="validateOnlyInput")
    def validate_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b2205813cd4319642577d30e32ba3a423ccf76a088deda21e54d7f70f7f980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015ec47d6c0231a045cb02d60676514e905c471f825015424ada7866a3a4ab85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateOnly")
    def validate_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validateOnly"))

    @validate_only.setter
    def validate_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff2ce683bbce20b905e6fd5f36b36d904476129191e3d8b777805979ec51257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f850a07f3ffd5b14b4893326cac43e25feed07856821217195f494dee2895f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest",
    jsii_struct_bases=[],
    name_mapping={
        "project_id": "projectId",
        "gcs_path": "gcsPath",
        "launch_parameters": "launchParameters",
        "location": "location",
        "validate_only": "validateOnly",
    },
)
class GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest:
    def __init__(
        self,
        *,
        project_id: builtins.str,
        gcs_path: typing.Optional[builtins.str] = None,
        launch_parameters: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project_id GoogleDataPipelinePipeline#project_id}
        :param gcs_path: A Cloud Storage path to the template from which to create the job. Must be a valid Cloud Storage URL, beginning with 'gs://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#gcs_path GoogleDataPipelinePipeline#gcs_path}
        :param launch_parameters: launch_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_parameters GoogleDataPipelinePipeline#launch_parameters}
        :param location: The regional endpoint to which to direct the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#location GoogleDataPipelinePipeline#location}
        :param validate_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#validate_only GoogleDataPipelinePipeline#validate_only}.
        '''
        if isinstance(launch_parameters, dict):
            launch_parameters = GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters(**launch_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7147c2314c14009649e9f4a8f8f9fa6a84e7e2bb26ca6c1b3a8451338149d585)
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument gcs_path", value=gcs_path, expected_type=type_hints["gcs_path"])
            check_type(argname="argument launch_parameters", value=launch_parameters, expected_type=type_hints["launch_parameters"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument validate_only", value=validate_only, expected_type=type_hints["validate_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_id": project_id,
        }
        if gcs_path is not None:
            self._values["gcs_path"] = gcs_path
        if launch_parameters is not None:
            self._values["launch_parameters"] = launch_parameters
        if location is not None:
            self._values["location"] = location
        if validate_only is not None:
            self._values["validate_only"] = validate_only

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the Cloud Platform project that the job belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project_id GoogleDataPipelinePipeline#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcs_path(self) -> typing.Optional[builtins.str]:
        '''A Cloud Storage path to the template from which to create the job.

        Must be a valid Cloud Storage URL, beginning with 'gs://'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#gcs_path GoogleDataPipelinePipeline#gcs_path}
        '''
        result = self._values.get("gcs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_parameters(
        self,
    ) -> typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters"]:
        '''launch_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_parameters GoogleDataPipelinePipeline#launch_parameters}
        '''
        result = self._values.get("launch_parameters")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters"], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The regional endpoint to which to direct the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#location GoogleDataPipelinePipeline#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#validate_only GoogleDataPipelinePipeline#validate_only}.'''
        result = self._values.get("validate_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "environment": "environment",
        "parameters": "parameters",
        "transform_name_mapping": "transformNameMapping",
        "update": "update",
    },
)
class GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters:
    def __init__(
        self,
        *,
        job_name: builtins.str,
        environment: typing.Optional[typing.Union["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#job_name GoogleDataPipelinePipeline#job_name}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#environment GoogleDataPipelinePipeline#environment}
        :param parameters: The runtime parameters to pass to the job. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#parameters GoogleDataPipelinePipeline#parameters}
        :param transform_name_mapping: Map of transform name prefixes of the job to be replaced to the corresponding name prefixes of the new job. Only applicable when updating a pipeline. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#transform_name_mapping GoogleDataPipelinePipeline#transform_name_mapping}
        :param update: If set, replace the existing pipeline with the name specified by jobName with this pipeline, preserving state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}
        '''
        if isinstance(environment, dict):
            environment = GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment(**environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e614a10374dad1c1e76548feb7f62edba4ec619fefd081af82dfca74488be62b)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument transform_name_mapping", value=transform_name_mapping, expected_type=type_hints["transform_name_mapping"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_name": job_name,
        }
        if environment is not None:
            self._values["environment"] = environment
        if parameters is not None:
            self._values["parameters"] = parameters
        if transform_name_mapping is not None:
            self._values["transform_name_mapping"] = transform_name_mapping
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def job_name(self) -> builtins.str:
        '''The job name to use for the created job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#job_name GoogleDataPipelinePipeline#job_name}
        '''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment"]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#environment GoogleDataPipelinePipeline#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional["GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment"], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The runtime parameters to pass to the job.

        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#parameters GoogleDataPipelinePipeline#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def transform_name_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of transform name prefixes of the job to be replaced to the corresponding name prefixes of the new job.

        Only applicable when updating a pipeline.
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#transform_name_mapping GoogleDataPipelinePipeline#transform_name_mapping}
        '''
        result = self._values.get("transform_name_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, replace the existing pipeline with the name specified by jobName with this pipeline, preserving state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment",
    jsii_struct_bases=[],
    name_mapping={
        "additional_experiments": "additionalExperiments",
        "additional_user_labels": "additionalUserLabels",
        "bypass_temp_dir_validation": "bypassTempDirValidation",
        "enable_streaming_engine": "enableStreamingEngine",
        "ip_configuration": "ipConfiguration",
        "kms_key_name": "kmsKeyName",
        "machine_type": "machineType",
        "max_workers": "maxWorkers",
        "network": "network",
        "num_workers": "numWorkers",
        "service_account_email": "serviceAccountEmail",
        "subnetwork": "subnetwork",
        "temp_location": "tempLocation",
        "worker_region": "workerRegion",
        "worker_zone": "workerZone",
        "zone": "zone",
    },
)
class GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment:
    def __init__(
        self,
        *,
        additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bypass_temp_dir_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_configuration: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        temp_location: typing.Optional[builtins.str] = None,
        worker_region: typing.Optional[builtins.str] = None,
        worker_zone: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_experiments GoogleDataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_user_labels GoogleDataPipelinePipeline#additional_user_labels}
        :param bypass_temp_dir_validation: Whether to bypass the safety checks for the job's temporary directory. Use with caution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#bypass_temp_dir_validation GoogleDataPipelinePipeline#bypass_temp_dir_validation}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#enable_streaming_engine GoogleDataPipelinePipeline#enable_streaming_engine}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#ip_configuration GoogleDataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#kms_key_name GoogleDataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#machine_type GoogleDataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#max_workers GoogleDataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#network GoogleDataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#num_workers GoogleDataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#service_account_email GoogleDataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#subnetwork GoogleDataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#temp_location GoogleDataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_region GoogleDataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_zone GoogleDataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#zone GoogleDataPipelinePipeline#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dc6c15597ce05579dd4c633e638d80a1869e952a126654f4a814940a171b03)
            check_type(argname="argument additional_experiments", value=additional_experiments, expected_type=type_hints["additional_experiments"])
            check_type(argname="argument additional_user_labels", value=additional_user_labels, expected_type=type_hints["additional_user_labels"])
            check_type(argname="argument bypass_temp_dir_validation", value=bypass_temp_dir_validation, expected_type=type_hints["bypass_temp_dir_validation"])
            check_type(argname="argument enable_streaming_engine", value=enable_streaming_engine, expected_type=type_hints["enable_streaming_engine"])
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument num_workers", value=num_workers, expected_type=type_hints["num_workers"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument temp_location", value=temp_location, expected_type=type_hints["temp_location"])
            check_type(argname="argument worker_region", value=worker_region, expected_type=type_hints["worker_region"])
            check_type(argname="argument worker_zone", value=worker_zone, expected_type=type_hints["worker_zone"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_experiments is not None:
            self._values["additional_experiments"] = additional_experiments
        if additional_user_labels is not None:
            self._values["additional_user_labels"] = additional_user_labels
        if bypass_temp_dir_validation is not None:
            self._values["bypass_temp_dir_validation"] = bypass_temp_dir_validation
        if enable_streaming_engine is not None:
            self._values["enable_streaming_engine"] = enable_streaming_engine
        if ip_configuration is not None:
            self._values["ip_configuration"] = ip_configuration
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if network is not None:
            self._values["network"] = network
        if num_workers is not None:
            self._values["num_workers"] = num_workers
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if temp_location is not None:
            self._values["temp_location"] = temp_location
        if worker_region is not None:
            self._values["worker_region"] = worker_region
        if worker_zone is not None:
            self._values["worker_zone"] = worker_zone
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def additional_experiments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional experiment flags for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_experiments GoogleDataPipelinePipeline#additional_experiments}
        '''
        result = self._values.get("additional_experiments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def additional_user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional user labels to be specified for the job.

        Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs.
        'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.'
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_user_labels GoogleDataPipelinePipeline#additional_user_labels}
        '''
        result = self._values.get("additional_user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bypass_temp_dir_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to bypass the safety checks for the job's temporary directory. Use with caution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#bypass_temp_dir_validation GoogleDataPipelinePipeline#bypass_temp_dir_validation}
        '''
        result = self._values.get("bypass_temp_dir_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_streaming_engine(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable Streaming Engine for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#enable_streaming_engine GoogleDataPipelinePipeline#enable_streaming_engine}
        '''
        result = self._values.get("enable_streaming_engine")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_configuration(self) -> typing.Optional[builtins.str]:
        '''Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#ip_configuration GoogleDataPipelinePipeline#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        ''''Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#kms_key_name GoogleDataPipelinePipeline#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type to use for the job. Defaults to the value from the template if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#machine_type GoogleDataPipelinePipeline#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#max_workers GoogleDataPipelinePipeline#max_workers}
        '''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#network GoogleDataPipelinePipeline#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''The initial number of Compute Engine instances for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#num_workers GoogleDataPipelinePipeline#num_workers}
        '''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The email address of the service account to run the job as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#service_account_email GoogleDataPipelinePipeline#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Subnetwork to which VMs will be assigned, if desired.

        You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#subnetwork GoogleDataPipelinePipeline#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#temp_location GoogleDataPipelinePipeline#temp_location}
        '''
        result = self._values.get("temp_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_region(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_region GoogleDataPipelinePipeline#worker_region}
        '''
        result = self._values.get("worker_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_zone GoogleDataPipelinePipeline#worker_zone}
        '''
        result = self._values.get("worker_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine availability zone for launching worker instances to run your pipeline.

        In the future, workerZone will take precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#zone GoogleDataPipelinePipeline#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71346d675ea1f79aa430e927413ede33aea0633ae80adee9c395ab7c6e93f2bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalExperiments")
    def reset_additional_experiments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExperiments", []))

    @jsii.member(jsii_name="resetAdditionalUserLabels")
    def reset_additional_user_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalUserLabels", []))

    @jsii.member(jsii_name="resetBypassTempDirValidation")
    def reset_bypass_temp_dir_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassTempDirValidation", []))

    @jsii.member(jsii_name="resetEnableStreamingEngine")
    def reset_enable_streaming_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStreamingEngine", []))

    @jsii.member(jsii_name="resetIpConfiguration")
    def reset_ip_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpConfiguration", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

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

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTempLocation")
    def reset_temp_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTempLocation", []))

    @jsii.member(jsii_name="resetWorkerRegion")
    def reset_worker_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerRegion", []))

    @jsii.member(jsii_name="resetWorkerZone")
    def reset_worker_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerZone", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="additionalExperimentsInput")
    def additional_experiments_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalExperimentsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalUserLabelsInput")
    def additional_user_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalUserLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="bypassTempDirValidationInput")
    def bypass_temp_dir_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bypassTempDirValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStreamingEngineInput")
    def enable_streaming_engine_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStreamingEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkersInput")
    def max_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="numWorkersInput")
    def num_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tempLocationInput")
    def temp_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tempLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="workerRegionInput")
    def worker_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="workerZoneInput")
    def worker_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalExperiments")
    def additional_experiments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalExperiments"))

    @additional_experiments.setter
    def additional_experiments(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f896a546fb8c43b85d4aa21eddeb57a9049342b7132bdee7e6e9b794567b2cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalExperiments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="additionalUserLabels")
    def additional_user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalUserLabels"))

    @additional_user_labels.setter
    def additional_user_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21520835361f43511dcce36e3ae2598c2963bdc786e0872f1ce5f18ec881d418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalUserLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bypassTempDirValidation")
    def bypass_temp_dir_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bypassTempDirValidation"))

    @bypass_temp_dir_validation.setter
    def bypass_temp_dir_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68872cded551542129eda83327f4d7a8824490a0cac45a47acdb9f4e731856c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassTempDirValidation", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__5842102e946a4cff12bf46fc52456e5fa134628dbca6e39111fff89e8856d6ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStreamingEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipConfiguration"))

    @ip_configuration.setter
    def ip_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e08b73aed84defa81afddd397f0eb824b719fcdbeb2f98e3cde71a70ac0ec65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdd9be1a59d8c06e61f8c91f9c90b562abe21e7c809ef1842a2f24b5d403bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0917502fb667630963bae8402cf5afa69f3491ed6a69dfb48252eb8894eb8df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8620a6ff85a6e07c5164339e8e37ff46172a7901b70e5849cefb39027ae6bb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e56848bb49a41b3213df13b700897c602782b242a4edd09eb40bcc2dc0226f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numWorkers")
    def num_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numWorkers"))

    @num_workers.setter
    def num_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431be3c7f785c3c79d36db2acc60cf3892a9d2358c0b38a839fc0c8c54e912d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e845ebea2c0920b8835b2fb3361dfd2c0a4099068fc532e1442436e831bddb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be41f3b7f105a3f43e1b8078f54209af4373c806205450ee9ec9e63eee660065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tempLocation")
    def temp_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempLocation"))

    @temp_location.setter
    def temp_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0b39d9e1a965eba948385588e5fca226192c2e290fbe539b8a50e35f5bae45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerRegion")
    def worker_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerRegion"))

    @worker_region.setter
    def worker_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bd61a8a636a3c5ef0ca48fa3a4160cfd9bd193c472fb7a94345d2a1583d9fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerZone")
    def worker_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerZone"))

    @worker_zone.setter
    def worker_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec67817f83dd574900e37127c3f3196fbe786517320de8942365e1ef1cbb0155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f1e7550f575602a3971094b6aacd69286415a42e2bce9950415b82224991f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5da6cf20727ca4673f2d7a16acb2ca081c23e87a29e36768e16906bd82542c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a9394bf9eb05aae52f68ce339c3972ab7de1b5ab39905d0fd6c313a724f113)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        *,
        additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
        additional_user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bypass_temp_dir_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_configuration: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        temp_location: typing.Optional[builtins.str] = None,
        worker_region: typing.Optional[builtins.str] = None,
        worker_zone: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_experiments GoogleDataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#additional_user_labels GoogleDataPipelinePipeline#additional_user_labels}
        :param bypass_temp_dir_validation: Whether to bypass the safety checks for the job's temporary directory. Use with caution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#bypass_temp_dir_validation GoogleDataPipelinePipeline#bypass_temp_dir_validation}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#enable_streaming_engine GoogleDataPipelinePipeline#enable_streaming_engine}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#ip_configuration GoogleDataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#kms_key_name GoogleDataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#machine_type GoogleDataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#max_workers GoogleDataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#network GoogleDataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#num_workers GoogleDataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#service_account_email GoogleDataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#subnetwork GoogleDataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#temp_location GoogleDataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_region GoogleDataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#worker_zone GoogleDataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#zone GoogleDataPipelinePipeline#zone}
        '''
        value = GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment(
            additional_experiments=additional_experiments,
            additional_user_labels=additional_user_labels,
            bypass_temp_dir_validation=bypass_temp_dir_validation,
            enable_streaming_engine=enable_streaming_engine,
            ip_configuration=ip_configuration,
            kms_key_name=kms_key_name,
            machine_type=machine_type,
            max_workers=max_workers,
            network=network,
            num_workers=num_workers,
            service_account_email=service_account_email,
            subnetwork=subnetwork,
            temp_location=temp_location,
            worker_region=worker_region,
            worker_zone=worker_zone,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetTransformNameMapping")
    def reset_transform_name_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformNameMapping", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference:
        return typing.cast(GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="jobNameInput")
    def job_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="transformNameMappingInput")
    def transform_name_mapping_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "transformNameMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b38cce8f324236b174f4ceaa26b30594f011c7250cdd76927f70cbfc49f9083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8b5496fe4edb50aa9a2b43c9429618d87ad8cf3199e91f0192b8ff3325413f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b068ea346fe9c5a19c3261ca190e5048ebdecf15ed400e7d7a8bc5bc45079780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformNameMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "update"))

    @update.setter
    def update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7185caa9726cab024ac8c5977c09cc36989c0244a61f5524002e6c4496bc3dc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb119990c17a79e796a33267d83f28636ff2e1ae58eb7a17a40eab990552a871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56899307e7d1efefac79966670b7720fc9b8ee7820002534b9c16741d0c1c07e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLaunchParameters")
    def put_launch_parameters(
        self,
        *,
        job_name: builtins.str,
        environment: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#job_name GoogleDataPipelinePipeline#job_name}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#environment GoogleDataPipelinePipeline#environment}
        :param parameters: The runtime parameters to pass to the job. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#parameters GoogleDataPipelinePipeline#parameters}
        :param transform_name_mapping: Map of transform name prefixes of the job to be replaced to the corresponding name prefixes of the new job. Only applicable when updating a pipeline. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#transform_name_mapping GoogleDataPipelinePipeline#transform_name_mapping}
        :param update: If set, replace the existing pipeline with the name specified by jobName with this pipeline, preserving state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#update GoogleDataPipelinePipeline#update}
        '''
        value = GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters(
            job_name=job_name,
            environment=environment,
            parameters=parameters,
            transform_name_mapping=transform_name_mapping,
            update=update,
        )

        return typing.cast(None, jsii.invoke(self, "putLaunchParameters", [value]))

    @jsii.member(jsii_name="resetGcsPath")
    def reset_gcs_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsPath", []))

    @jsii.member(jsii_name="resetLaunchParameters")
    def reset_launch_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchParameters", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetValidateOnly")
    def reset_validate_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateOnly", []))

    @builtins.property
    @jsii.member(jsii_name="launchParameters")
    def launch_parameters(
        self,
    ) -> GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference:
        return typing.cast(GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference, jsii.get(self, "launchParameters"))

    @builtins.property
    @jsii.member(jsii_name="gcsPathInput")
    def gcs_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcsPathInput"))

    @builtins.property
    @jsii.member(jsii_name="launchParametersInput")
    def launch_parameters_input(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters], jsii.get(self, "launchParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="validateOnlyInput")
    def validate_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsPath")
    def gcs_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsPath"))

    @gcs_path.setter
    def gcs_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7551bbbc6bc27ef5ddcc9d1588c456bdbede65a3c3135f5f0c71ea150e2556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b1c223b8fff7d65261e940702543b8ba6192bbc1c377841ac86b097aff47c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7218dc4fa1ff74a7f3d1b9de10c3a34049322427284de4031ab28db7314eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateOnly")
    def validate_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validateOnly"))

    @validate_only.setter
    def validate_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f18a9e47e042deaabe2feb74033c9acf4e232af7466460b9a0af57694f76cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432659c91b3dd448b897a81e13f17ead8089d1a23fa99168053e779a0ef21dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataPipelinePipelineWorkloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataPipelinePipeline.GoogleDataPipelinePipelineWorkloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad9cbcf0dbc1b61244d372a6cf3e0520b5b32e70715d07f73ab0db2520ff75ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataflowFlexTemplateRequest")
    def put_dataflow_flex_template_request(
        self,
        *,
        launch_parameter: typing.Union[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter, typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        project_id: builtins.str,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param launch_parameter: launch_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_parameter GoogleDataPipelinePipeline#launch_parameter}
        :param location: The regional endpoint to which to direct the request. For example, us-central1, us-west1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#location GoogleDataPipelinePipeline#location}
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project_id GoogleDataPipelinePipeline#project_id}
        :param validate_only: If true, the request is validated but not actually executed. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#validate_only GoogleDataPipelinePipeline#validate_only}
        '''
        value = GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest(
            launch_parameter=launch_parameter,
            location=location,
            project_id=project_id,
            validate_only=validate_only,
        )

        return typing.cast(None, jsii.invoke(self, "putDataflowFlexTemplateRequest", [value]))

    @jsii.member(jsii_name="putDataflowLaunchTemplateRequest")
    def put_dataflow_launch_template_request(
        self,
        *,
        project_id: builtins.str,
        gcs_path: typing.Optional[builtins.str] = None,
        launch_parameters: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters, typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#project_id GoogleDataPipelinePipeline#project_id}
        :param gcs_path: A Cloud Storage path to the template from which to create the job. Must be a valid Cloud Storage URL, beginning with 'gs://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#gcs_path GoogleDataPipelinePipeline#gcs_path}
        :param launch_parameters: launch_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#launch_parameters GoogleDataPipelinePipeline#launch_parameters}
        :param location: The regional endpoint to which to direct the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#location GoogleDataPipelinePipeline#location}
        :param validate_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_pipeline_pipeline#validate_only GoogleDataPipelinePipeline#validate_only}.
        '''
        value = GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest(
            project_id=project_id,
            gcs_path=gcs_path,
            launch_parameters=launch_parameters,
            location=location,
            validate_only=validate_only,
        )

        return typing.cast(None, jsii.invoke(self, "putDataflowLaunchTemplateRequest", [value]))

    @jsii.member(jsii_name="resetDataflowFlexTemplateRequest")
    def reset_dataflow_flex_template_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataflowFlexTemplateRequest", []))

    @jsii.member(jsii_name="resetDataflowLaunchTemplateRequest")
    def reset_dataflow_launch_template_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataflowLaunchTemplateRequest", []))

    @builtins.property
    @jsii.member(jsii_name="dataflowFlexTemplateRequest")
    def dataflow_flex_template_request(
        self,
    ) -> GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference:
        return typing.cast(GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference, jsii.get(self, "dataflowFlexTemplateRequest"))

    @builtins.property
    @jsii.member(jsii_name="dataflowLaunchTemplateRequest")
    def dataflow_launch_template_request(
        self,
    ) -> GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference:
        return typing.cast(GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference, jsii.get(self, "dataflowLaunchTemplateRequest"))

    @builtins.property
    @jsii.member(jsii_name="dataflowFlexTemplateRequestInput")
    def dataflow_flex_template_request_input(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest], jsii.get(self, "dataflowFlexTemplateRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="dataflowLaunchTemplateRequestInput")
    def dataflow_launch_template_request_input(
        self,
    ) -> typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest], jsii.get(self, "dataflowLaunchTemplateRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataPipelinePipelineWorkload]:
        return typing.cast(typing.Optional[GoogleDataPipelinePipelineWorkload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataPipelinePipelineWorkload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552dd057d6f8ffb7fe00265005501a3ae56f78248ee0c3672fd26b8f7962efc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataPipelinePipeline",
    "GoogleDataPipelinePipelineConfig",
    "GoogleDataPipelinePipelineScheduleInfo",
    "GoogleDataPipelinePipelineScheduleInfoOutputReference",
    "GoogleDataPipelinePipelineTimeouts",
    "GoogleDataPipelinePipelineTimeoutsOutputReference",
    "GoogleDataPipelinePipelineWorkload",
    "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest",
    "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter",
    "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment",
    "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference",
    "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference",
    "GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference",
    "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest",
    "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters",
    "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment",
    "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference",
    "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference",
    "GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference",
    "GoogleDataPipelinePipelineWorkloadOutputReference",
]

publication.publish()

def _typecheckingstub__1164e51cf8c3d968b7015a47366e1d59e4f917f5c7288200cdb7872fac6b4f45(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    state: builtins.str,
    type: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pipeline_sources: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    schedule_info: typing.Optional[typing.Union[GoogleDataPipelinePipelineScheduleInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler_service_account_email: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataPipelinePipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkload, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__423318e4b60da69d6f71479753a29696a5a6aa31b9d107116fcf41939f62c421(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9de8e38c040c80a9841d8ff353d8528d55632a96f534bec8c90b90ba89cb87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd91f4f2ef53948dd66c343e1063a4ad2157ba4ea4ace2b631eb95c6a3d62d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a0af60dcbdd68cedde1b029416d662d3b8a2f449a3cca23aab95c896d3bc3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4b94df1169ffca65f51fec100681576590988d79452c2562f6528b6be13cd8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8948c275ea24e012e80340793b5a75fe7088c0e5b404f16c3a87dbb1e093da42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0830ef81cc7ea9b8780dbf93d9a1b08a94e51f101508379715cb9c4f4fcab9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ff49f15e870293194cc3f2ce62e6764327a7d76cd39b8063372cee2b247726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3047c7603269b18627d065ad517a19d19cd1e1567ef8bb267ee09cbb079374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5c07fd34ce848d4fdfb47469ffc9ee500cbe764c3d6bf0d1e7c7ab059031f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6828e8e3eeb3d89de1be4bfe322e68bfcd0bbc93129baf0f330de93494905a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    state: builtins.str,
    type: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pipeline_sources: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    schedule_info: typing.Optional[typing.Union[GoogleDataPipelinePipelineScheduleInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler_service_account_email: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataPipelinePipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkload, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4953af14f4c95547a350b4811e783ce182c5edcc898a4898ffd76153b43bf929(
    *,
    schedule: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769a135e21520b27a50af7ce56c0d629b9903fd13ef3c4a886357cf168b87e77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0a7ffd2b7bef1dfab13d3c07f84efbcf2d671d4ad91d4f982c9e3c6f2c0dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee4ad12e58f44e83f6474fb94efc9408df4d00c9bcff0507bd6469bf41a722e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f60705c4a7c062e090cca05240121e1f80f6099738955360a9a651cbf6e7aa(
    value: typing.Optional[GoogleDataPipelinePipelineScheduleInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc4e2ecd669f6990e0d1679c98998d483343b282279cc7fa89bd03398df3ab1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae605514fff7bf887b46d18e9a55e5f0bca4941c0b9733e057dcc032f27af5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e496e92c16640f6bc7618f75b4531168178d05b36603c245f0b66cc5a6273e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afcebf5216e0def11c86c5cc6bc3205352eab9cce5fea6f32ff6abfc6daa4cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec58e0f8f59f8e0399e6c55d8f52a914bbe9a745b673d7594707bad44866b6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a67741167973142027e043d0b4d61334b88c1e03cf015b8d4a7b152db77bbfc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataPipelinePipelineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c4025d3ed7c401ccacecea15694c534f8390e6ce735c178b8e413b25977515(
    *,
    dataflow_flex_template_request: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    dataflow_launch_template_request: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dd1aac391f426a8f01c2da155460d157fadde5eae4a4008e854f58318fdcc8(
    *,
    launch_parameter: typing.Union[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    project_id: builtins.str,
    validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f318685a21dec14c71ceeb1c7fa387d000edd893185d85f1fa9f74a718f0db27(
    *,
    job_name: builtins.str,
    container_spec_gcs_path: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    launch_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transform_name_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e2deaaf2739d827b22c16442a2afe134e899e4c149686b20ead8d65bfb1e3e(
    *,
    additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    flexrs_goal: typing.Optional[builtins.str] = None,
    ip_configuration: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_workers: typing.Optional[jsii.Number] = None,
    network: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    temp_location: typing.Optional[builtins.str] = None,
    worker_region: typing.Optional[builtins.str] = None,
    worker_zone: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833ad64f3bf83fb001734229ad08c66a8195619c727713b01ed72e7fdb4a2a6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b3161f84b2ad725c7998a9b0038efe9bb6ab1a26a6bbe3da89a76641dcacab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f85ab0a6b1090c43697eeb44c4ceab46c0124b9e0e1d9d0dab9600a75f69c3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e80322dfb28a9f8d87daef6eef03167922e3550322e4946e4957951006d7905(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f5378e5c358d0829663834513c21edf8fabd60d3a5059c36d71625b90965b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403ff74e36efcfc95372889ebe18b90e0fde2b2408bcdf3f3ca805d2e55c2be2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12a095a9778ce6f011fb41016b56522f1308144c50db4dfefdc27abc2070feb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a71b3439336ec3e8a6b8ffd968f89297ddad23df50940b6dd0667935dcab7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc91f49db06cc03f6c0c950f36ba17598424a12f576fde7c4e31a1f972172fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42257479e2469709f0052073e67fc55d7a986fb0e2144cf49b3362e8c0f0666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1a3f63cd36eb7a288eeb1ce57f4da72ff446b097e1997057bbbabbf81bcd6d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd6f16a0a8751407e6bae46d1ab23beb0dae882dca01bb3a711086c110f18be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861afb7fafd4746f519a0f19e2bce6c29d6b0ecbac9f938597100aa1cea412c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba86b6ebfa59d8a19ca86510a18b491ff89ba55811393f1a6373b0946c82f60d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee27fd6197f651e078924866ae6aa3b746815bbd6cf5d954b499950b55c5201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebcddff94a9abbcb111fe36ab30f023b162e35bb7d25cdcf7fe480b8a38ce66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e928c8ef1d97dc8044639054b85d5768dcbd03ea601e9b5ed4d4e8621b61e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d097ecff779a83ad3d639ae0a716c7c4511c36ca13f73dbeb32193d0d3cf1a(
    value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c608ae4f0250d8f80a01d25d1f4860f4a84881613366218f7cbb1b0f02e44f15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df9a38f89d49fd70ed411e28f9a09cf4769fe0d2c0c6585fddd6a44079474e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374fefa4e9f47eb61619ef0449beaa42e7c253e16635465ed89687fa57f6f997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7514ff0112510de5aad6ae56ffa4de531e8815ac8f03c6addeed59fbe7869e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd353a12956824a6cb35b02610ff072801ab60f7283945c2fa76b1babe30ac4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8851b76d452940b7d6843ff2d0609c39597892cd2cf2693044d0d4c5c5b705(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360494143666e0bfe38d0c9a4144a04b738381a5ff0e48e5febc489a43324935(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43c672e9462acdb26074500d07eb9ad81ed1f9a823a4263490438dccb77052f(
    value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bc21713f7eea4aaf568fd2001910edb10569d6d8ddd73e9370133525b1d26a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b2205813cd4319642577d30e32ba3a423ccf76a088deda21e54d7f70f7f980(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015ec47d6c0231a045cb02d60676514e905c471f825015424ada7866a3a4ab85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff2ce683bbce20b905e6fd5f36b36d904476129191e3d8b777805979ec51257(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f850a07f3ffd5b14b4893326cac43e25feed07856821217195f494dee2895f66(
    value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowFlexTemplateRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7147c2314c14009649e9f4a8f8f9fa6a84e7e2bb26ca6c1b3a8451338149d585(
    *,
    project_id: builtins.str,
    gcs_path: typing.Optional[builtins.str] = None,
    launch_parameters: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e614a10374dad1c1e76548feb7f62edba4ec619fefd081af82dfca74488be62b(
    *,
    job_name: builtins.str,
    environment: typing.Optional[typing.Union[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dc6c15597ce05579dd4c633e638d80a1869e952a126654f4a814940a171b03(
    *,
    additional_experiments: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bypass_temp_dir_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_streaming_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_configuration: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_workers: typing.Optional[jsii.Number] = None,
    network: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    temp_location: typing.Optional[builtins.str] = None,
    worker_region: typing.Optional[builtins.str] = None,
    worker_zone: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71346d675ea1f79aa430e927413ede33aea0633ae80adee9c395ab7c6e93f2bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f896a546fb8c43b85d4aa21eddeb57a9049342b7132bdee7e6e9b794567b2cd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21520835361f43511dcce36e3ae2598c2963bdc786e0872f1ce5f18ec881d418(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68872cded551542129eda83327f4d7a8824490a0cac45a47acdb9f4e731856c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5842102e946a4cff12bf46fc52456e5fa134628dbca6e39111fff89e8856d6ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e08b73aed84defa81afddd397f0eb824b719fcdbeb2f98e3cde71a70ac0ec65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdd9be1a59d8c06e61f8c91f9c90b562abe21e7c809ef1842a2f24b5d403bbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0917502fb667630963bae8402cf5afa69f3491ed6a69dfb48252eb8894eb8df7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8620a6ff85a6e07c5164339e8e37ff46172a7901b70e5849cefb39027ae6bb72(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e56848bb49a41b3213df13b700897c602782b242a4edd09eb40bcc2dc0226f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431be3c7f785c3c79d36db2acc60cf3892a9d2358c0b38a839fc0c8c54e912d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e845ebea2c0920b8835b2fb3361dfd2c0a4099068fc532e1442436e831bddb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be41f3b7f105a3f43e1b8078f54209af4373c806205450ee9ec9e63eee660065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0b39d9e1a965eba948385588e5fca226192c2e290fbe539b8a50e35f5bae45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bd61a8a636a3c5ef0ca48fa3a4160cfd9bd193c472fb7a94345d2a1583d9fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec67817f83dd574900e37127c3f3196fbe786517320de8942365e1ef1cbb0155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f1e7550f575602a3971094b6aacd69286415a42e2bce9950415b82224991f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5da6cf20727ca4673f2d7a16acb2ca081c23e87a29e36768e16906bd82542c(
    value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a9394bf9eb05aae52f68ce339c3972ab7de1b5ab39905d0fd6c313a724f113(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b38cce8f324236b174f4ceaa26b30594f011c7250cdd76927f70cbfc49f9083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8b5496fe4edb50aa9a2b43c9429618d87ad8cf3199e91f0192b8ff3325413f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b068ea346fe9c5a19c3261ca190e5048ebdecf15ed400e7d7a8bc5bc45079780(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7185caa9726cab024ac8c5977c09cc36989c0244a61f5524002e6c4496bc3dc1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb119990c17a79e796a33267d83f28636ff2e1ae58eb7a17a40eab990552a871(
    value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56899307e7d1efefac79966670b7720fc9b8ee7820002534b9c16741d0c1c07e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7551bbbc6bc27ef5ddcc9d1588c456bdbede65a3c3135f5f0c71ea150e2556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b1c223b8fff7d65261e940702543b8ba6192bbc1c377841ac86b097aff47c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7218dc4fa1ff74a7f3d1b9de10c3a34049322427284de4031ab28db7314eb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f18a9e47e042deaabe2feb74033c9acf4e232af7466460b9a0af57694f76cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432659c91b3dd448b897a81e13f17ead8089d1a23fa99168053e779a0ef21dfe(
    value: typing.Optional[GoogleDataPipelinePipelineWorkloadDataflowLaunchTemplateRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9cbcf0dbc1b61244d372a6cf3e0520b5b32e70715d07f73ab0db2520ff75ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552dd057d6f8ffb7fe00265005501a3ae56f78248ee0c3672fd26b8f7962efc5(
    value: typing.Optional[GoogleDataPipelinePipelineWorkload],
) -> None:
    """Type checking stubs"""
    pass
