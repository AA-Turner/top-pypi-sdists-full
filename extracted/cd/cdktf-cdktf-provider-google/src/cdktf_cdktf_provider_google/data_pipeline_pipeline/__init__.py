r'''
# `google_data_pipeline_pipeline`

Refer to the Terraform Registry for docs: [`google_data_pipeline_pipeline`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline).
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


class DataPipelinePipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline google_data_pipeline_pipeline}.'''

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
        schedule_info: typing.Optional[typing.Union["DataPipelinePipelineScheduleInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler_service_account_email: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataPipelinePipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload: typing.Optional[typing.Union["DataPipelinePipelineWorkload", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline google_data_pipeline_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: "The pipeline name. For example': 'projects/PROJECT_ID/locations/LOCATION_ID/pipelines/PIPELINE_ID." "- PROJECT_ID can contain letters ([A-Za-z]), numbers ([0-9]), hyphens (-), colons (:), and periods (.). For more information, see Identifying projects." "LOCATION_ID is the canonical ID for the pipeline's location. The list of available locations can be obtained by calling google.cloud.location.Locations.ListLocations. Note that the Data Pipelines service is not available in all regions. It depends on Cloud Scheduler, an App Engine application, so it's only available in App Engine regions." "PIPELINE_ID is the ID of the pipeline. Must be unique for the selected project and location." Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#name DataPipelinePipeline#name}
        :param state: The state of the pipeline. When the pipeline is created, the state is set to 'PIPELINE_STATE_ACTIVE' by default. State changes can be requested by setting the state to stopping, paused, or resuming. State cannot be changed through pipelines.patch requests. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#state Possible values: ["STATE_UNSPECIFIED", "STATE_RESUMING", "STATE_ACTIVE", "STATE_STOPPING", "STATE_ARCHIVED", "STATE_PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#state DataPipelinePipeline#state}
        :param type: The type of the pipeline. This field affects the scheduling of the pipeline and the type of metrics to show for the pipeline. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#pipelinetype Possible values: ["PIPELINE_TYPE_UNSPECIFIED", "PIPELINE_TYPE_BATCH", "PIPELINE_TYPE_STREAMING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#type DataPipelinePipeline#type}
        :param display_name: The display name of the pipeline. It can contain only letters ([A-Za-z]), numbers ([0-9]), hyphens (-), and underscores (_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#display_name DataPipelinePipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#id DataPipelinePipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pipeline_sources: The sources of the pipeline (for example, Dataplex). The keys and values are set by the corresponding sources during pipeline creation. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#pipeline_sources DataPipelinePipeline#pipeline_sources}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project DataPipelinePipeline#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#region DataPipelinePipeline#region}
        :param schedule_info: schedule_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#schedule_info DataPipelinePipeline#schedule_info}
        :param scheduler_service_account_email: Optional. A service account email to be used with the Cloud Scheduler job. If not specified, the default compute engine service account will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#scheduler_service_account_email DataPipelinePipeline#scheduler_service_account_email}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#timeouts DataPipelinePipeline#timeouts}
        :param workload: workload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#workload DataPipelinePipeline#workload}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ba1b660da86533f1c613affbdc1e2807d3131eb62b01354b1adae2ae58fd13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataPipelinePipelineConfig(
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
        '''Generates CDKTF code for importing a DataPipelinePipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataPipelinePipeline to import.
        :param import_from_id: The id of the existing DataPipelinePipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataPipelinePipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecadb79b9ab9dfec6c63939199d0ff38bd1f45dc1c5d7d8b319cb35c5937ce0b)
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
        :param schedule: Unix-cron format of the schedule. This information is retrieved from the linked Cloud Scheduler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#schedule DataPipelinePipeline#schedule}
        :param time_zone: Timezone ID. This matches the timezone IDs used by the Cloud Scheduler API. If empty, UTC time is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#time_zone DataPipelinePipeline#time_zone}
        '''
        value = DataPipelinePipelineScheduleInfo(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#create DataPipelinePipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#delete DataPipelinePipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}.
        '''
        value = DataPipelinePipelineTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkload")
    def put_workload(
        self,
        *,
        dataflow_flex_template_request: typing.Optional[typing.Union["DataPipelinePipelineWorkloadDataflowFlexTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        dataflow_launch_template_request: typing.Optional[typing.Union["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dataflow_flex_template_request: dataflow_flex_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#dataflow_flex_template_request DataPipelinePipeline#dataflow_flex_template_request}
        :param dataflow_launch_template_request: dataflow_launch_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#dataflow_launch_template_request DataPipelinePipeline#dataflow_launch_template_request}
        '''
        value = DataPipelinePipelineWorkload(
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
    def schedule_info(self) -> "DataPipelinePipelineScheduleInfoOutputReference":
        return typing.cast("DataPipelinePipelineScheduleInfoOutputReference", jsii.get(self, "scheduleInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataPipelinePipelineTimeoutsOutputReference":
        return typing.cast("DataPipelinePipelineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workload")
    def workload(self) -> "DataPipelinePipelineWorkloadOutputReference":
        return typing.cast("DataPipelinePipelineWorkloadOutputReference", jsii.get(self, "workload"))

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
    ) -> typing.Optional["DataPipelinePipelineScheduleInfo"]:
        return typing.cast(typing.Optional["DataPipelinePipelineScheduleInfo"], jsii.get(self, "scheduleInfoInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataPipelinePipelineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataPipelinePipelineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadInput")
    def workload_input(self) -> typing.Optional["DataPipelinePipelineWorkload"]:
        return typing.cast(typing.Optional["DataPipelinePipelineWorkload"], jsii.get(self, "workloadInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b53704f5e5ae529596fa97712a9bf9cb7df1d88068e4ecc90eff539221fad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f2e0374fcba914f19f500bff6403c8bd2fec4dbc814c2a0f9f5a5a5e203632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fefb93e0b855c56ef0845f245274683b03a33b807648c1f19e2770f03daa9659)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59c06e59f3d26e6ffe0be34043b33f537df263dd381a41cfb42b1d38b993125d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineSources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099b97d9001eb8a94ff5780c9841a9c8d2b501f85fa06d9dec589f8f7039c18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31bae024f42aff828c586dc363a15b05863e1bf566933f5d1b2e7c025950b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedulerServiceAccountEmail")
    def scheduler_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedulerServiceAccountEmail"))

    @scheduler_service_account_email.setter
    def scheduler_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d57e9d857312217cc63f0789cf8a048ccf2969eada6d06da3d09168820670b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulerServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e515063fc181cf1ba37627692cebd3b2670b5d02902d34fa6864668b3515b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05e739d526a34a1425028521efdb65db09516bae0c3780fd16a677196d44d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineConfig",
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
class DataPipelinePipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        schedule_info: typing.Optional[typing.Union["DataPipelinePipelineScheduleInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler_service_account_email: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataPipelinePipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload: typing.Optional[typing.Union["DataPipelinePipelineWorkload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: "The pipeline name. For example': 'projects/PROJECT_ID/locations/LOCATION_ID/pipelines/PIPELINE_ID." "- PROJECT_ID can contain letters ([A-Za-z]), numbers ([0-9]), hyphens (-), colons (:), and periods (.). For more information, see Identifying projects." "LOCATION_ID is the canonical ID for the pipeline's location. The list of available locations can be obtained by calling google.cloud.location.Locations.ListLocations. Note that the Data Pipelines service is not available in all regions. It depends on Cloud Scheduler, an App Engine application, so it's only available in App Engine regions." "PIPELINE_ID is the ID of the pipeline. Must be unique for the selected project and location." Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#name DataPipelinePipeline#name}
        :param state: The state of the pipeline. When the pipeline is created, the state is set to 'PIPELINE_STATE_ACTIVE' by default. State changes can be requested by setting the state to stopping, paused, or resuming. State cannot be changed through pipelines.patch requests. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#state Possible values: ["STATE_UNSPECIFIED", "STATE_RESUMING", "STATE_ACTIVE", "STATE_STOPPING", "STATE_ARCHIVED", "STATE_PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#state DataPipelinePipeline#state}
        :param type: The type of the pipeline. This field affects the scheduling of the pipeline and the type of metrics to show for the pipeline. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#pipelinetype Possible values: ["PIPELINE_TYPE_UNSPECIFIED", "PIPELINE_TYPE_BATCH", "PIPELINE_TYPE_STREAMING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#type DataPipelinePipeline#type}
        :param display_name: The display name of the pipeline. It can contain only letters ([A-Za-z]), numbers ([0-9]), hyphens (-), and underscores (_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#display_name DataPipelinePipeline#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#id DataPipelinePipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pipeline_sources: The sources of the pipeline (for example, Dataplex). The keys and values are set by the corresponding sources during pipeline creation. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#pipeline_sources DataPipelinePipeline#pipeline_sources}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project DataPipelinePipeline#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#region DataPipelinePipeline#region}
        :param schedule_info: schedule_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#schedule_info DataPipelinePipeline#schedule_info}
        :param scheduler_service_account_email: Optional. A service account email to be used with the Cloud Scheduler job. If not specified, the default compute engine service account will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#scheduler_service_account_email DataPipelinePipeline#scheduler_service_account_email}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#timeouts DataPipelinePipeline#timeouts}
        :param workload: workload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#workload DataPipelinePipeline#workload}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(schedule_info, dict):
            schedule_info = DataPipelinePipelineScheduleInfo(**schedule_info)
        if isinstance(timeouts, dict):
            timeouts = DataPipelinePipelineTimeouts(**timeouts)
        if isinstance(workload, dict):
            workload = DataPipelinePipelineWorkload(**workload)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d10ecc13f4a11bccd59b1f59e4fa32b1d784df6962ece194edfbc780b9aab5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#name DataPipelinePipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''The state of the pipeline.

        When the pipeline is created, the state is set to 'PIPELINE_STATE_ACTIVE' by default. State changes can be requested by setting the state to stopping, paused, or resuming. State cannot be changed through pipelines.patch requests.
        https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#state Possible values: ["STATE_UNSPECIFIED", "STATE_RESUMING", "STATE_ACTIVE", "STATE_STOPPING", "STATE_ARCHIVED", "STATE_PAUSED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#state DataPipelinePipeline#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the pipeline.

        This field affects the scheduling of the pipeline and the type of metrics to show for the pipeline.
        https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#pipelinetype Possible values: ["PIPELINE_TYPE_UNSPECIFIED", "PIPELINE_TYPE_BATCH", "PIPELINE_TYPE_STREAMING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#type DataPipelinePipeline#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the pipeline. It can contain only letters ([A-Za-z]), numbers ([0-9]), hyphens (-), and underscores (_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#display_name DataPipelinePipeline#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#id DataPipelinePipeline#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#pipeline_sources DataPipelinePipeline#pipeline_sources}
        '''
        result = self._values.get("pipeline_sources")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project DataPipelinePipeline#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#region DataPipelinePipeline#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_info(self) -> typing.Optional["DataPipelinePipelineScheduleInfo"]:
        '''schedule_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#schedule_info DataPipelinePipeline#schedule_info}
        '''
        result = self._values.get("schedule_info")
        return typing.cast(typing.Optional["DataPipelinePipelineScheduleInfo"], result)

    @builtins.property
    def scheduler_service_account_email(self) -> typing.Optional[builtins.str]:
        '''Optional.

        A service account email to be used with the Cloud Scheduler job. If not specified, the default compute engine service account will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#scheduler_service_account_email DataPipelinePipeline#scheduler_service_account_email}
        '''
        result = self._values.get("scheduler_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataPipelinePipelineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#timeouts DataPipelinePipeline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataPipelinePipelineTimeouts"], result)

    @builtins.property
    def workload(self) -> typing.Optional["DataPipelinePipelineWorkload"]:
        '''workload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#workload DataPipelinePipeline#workload}
        '''
        result = self._values.get("workload")
        return typing.cast(typing.Optional["DataPipelinePipelineWorkload"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineScheduleInfo",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule", "time_zone": "timeZone"},
)
class DataPipelinePipelineScheduleInfo:
    def __init__(
        self,
        *,
        schedule: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule: Unix-cron format of the schedule. This information is retrieved from the linked Cloud Scheduler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#schedule DataPipelinePipeline#schedule}
        :param time_zone: Timezone ID. This matches the timezone IDs used by the Cloud Scheduler API. If empty, UTC time is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#time_zone DataPipelinePipeline#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8069f7028865dce8719ae78ee0a6806f7e5ce0054249d3c69f3a8b6ef89d78c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#schedule DataPipelinePipeline#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Timezone ID. This matches the timezone IDs used by the Cloud Scheduler API. If empty, UTC time is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#time_zone DataPipelinePipeline#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineScheduleInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataPipelinePipelineScheduleInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineScheduleInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3052550ee6a9ac020083989f17ce1a9c6ced39ac404ca57d94af79e0e066c0ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a4dbd84f7cef2e4b4a1985f7082b55dc271f17f830520e2670367f5c9e2729c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e38a44ab2a623d4f23fe5084ae9acec0fa074053d818cdbc3ecbbdbacd4e4c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataPipelinePipelineScheduleInfo]:
        return typing.cast(typing.Optional[DataPipelinePipelineScheduleInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineScheduleInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14be513be1ded29f723cbd88931172c89120972972808138bb7b1d005961b104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataPipelinePipelineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#create DataPipelinePipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#delete DataPipelinePipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f417b3509aacf985e03fb83fda05ab98ed47fb4c00d913c9d975c86d370d4bb7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#create DataPipelinePipeline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#delete DataPipelinePipeline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataPipelinePipelineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6674380134364a8d3733ad515ac9d185cab1ccab514da10fa928de1787415a22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c29550c477927fed6e330491864fde9896635bbf4eeaf1cd295320402f20ea98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345f2a7b6e599f9e6feebfdbf864c8ca840f8e7901ab70294ac819448d335b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412c5fe154fc1f3b636b0e74b4ee2c3c04f0771b63ebcbd3798fd9fe507a279f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataPipelinePipelineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataPipelinePipelineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataPipelinePipelineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65ddadc165d2a205400a433c404b1f0270887487b1621287e3ddb2937263ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkload",
    jsii_struct_bases=[],
    name_mapping={
        "dataflow_flex_template_request": "dataflowFlexTemplateRequest",
        "dataflow_launch_template_request": "dataflowLaunchTemplateRequest",
    },
)
class DataPipelinePipelineWorkload:
    def __init__(
        self,
        *,
        dataflow_flex_template_request: typing.Optional[typing.Union["DataPipelinePipelineWorkloadDataflowFlexTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        dataflow_launch_template_request: typing.Optional[typing.Union["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dataflow_flex_template_request: dataflow_flex_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#dataflow_flex_template_request DataPipelinePipeline#dataflow_flex_template_request}
        :param dataflow_launch_template_request: dataflow_launch_template_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#dataflow_launch_template_request DataPipelinePipeline#dataflow_launch_template_request}
        '''
        if isinstance(dataflow_flex_template_request, dict):
            dataflow_flex_template_request = DataPipelinePipelineWorkloadDataflowFlexTemplateRequest(**dataflow_flex_template_request)
        if isinstance(dataflow_launch_template_request, dict):
            dataflow_launch_template_request = DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest(**dataflow_launch_template_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2305d72e616dcf4889588adab9439080d6d94d11e2bee228246b597965ce4fb)
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
    ) -> typing.Optional["DataPipelinePipelineWorkloadDataflowFlexTemplateRequest"]:
        '''dataflow_flex_template_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#dataflow_flex_template_request DataPipelinePipeline#dataflow_flex_template_request}
        '''
        result = self._values.get("dataflow_flex_template_request")
        return typing.cast(typing.Optional["DataPipelinePipelineWorkloadDataflowFlexTemplateRequest"], result)

    @builtins.property
    def dataflow_launch_template_request(
        self,
    ) -> typing.Optional["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest"]:
        '''dataflow_launch_template_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#dataflow_launch_template_request DataPipelinePipeline#dataflow_launch_template_request}
        '''
        result = self._values.get("dataflow_launch_template_request")
        return typing.cast(typing.Optional["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineWorkload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowFlexTemplateRequest",
    jsii_struct_bases=[],
    name_mapping={
        "launch_parameter": "launchParameter",
        "location": "location",
        "project_id": "projectId",
        "validate_only": "validateOnly",
    },
)
class DataPipelinePipelineWorkloadDataflowFlexTemplateRequest:
    def __init__(
        self,
        *,
        launch_parameter: typing.Union["DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        project_id: builtins.str,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param launch_parameter: launch_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_parameter DataPipelinePipeline#launch_parameter}
        :param location: The regional endpoint to which to direct the request. For example, us-central1, us-west1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#location DataPipelinePipeline#location}
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project_id DataPipelinePipeline#project_id}
        :param validate_only: If true, the request is validated but not actually executed. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#validate_only DataPipelinePipeline#validate_only}
        '''
        if isinstance(launch_parameter, dict):
            launch_parameter = DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter(**launch_parameter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946cabbb80d0d7659fec41f759dc4cb2e1ff905c44eeb516d0b935e2475f7574)
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
    ) -> "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter":
        '''launch_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_parameter DataPipelinePipeline#launch_parameter}
        '''
        result = self._values.get("launch_parameter")
        assert result is not None, "Required property 'launch_parameter' is missing"
        return typing.cast("DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The regional endpoint to which to direct the request. For example, us-central1, us-west1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#location DataPipelinePipeline#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the Cloud Platform project that the job belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project_id DataPipelinePipeline#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validate_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the request is validated but not actually executed. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#validate_only DataPipelinePipeline#validate_only}
        '''
        result = self._values.get("validate_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineWorkloadDataflowFlexTemplateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter",
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
class DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter:
    def __init__(
        self,
        *,
        job_name: builtins.str,
        container_spec_gcs_path: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union["DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        launch_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. For an update job request, the job name should be the same as the existing running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#job_name DataPipelinePipeline#job_name}
        :param container_spec_gcs_path: Cloud Storage path to a file with a JSON-serialized ContainerSpec as content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#container_spec_gcs_path DataPipelinePipeline#container_spec_gcs_path}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#environment DataPipelinePipeline#environment}
        :param launch_options: Launch options for this Flex Template job. This is a common set of options across languages and templates. This should not be used to pass job parameters. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_options DataPipelinePipeline#launch_options}
        :param parameters: 'The parameters for the Flex Template. Example: {"numWorkers":"5"}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#parameters DataPipelinePipeline#parameters}
        :param transform_name_mappings: 'Use this to pass transform name mappings for streaming update jobs. Example: {"oldTransformName":"newTransformName",...}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#transform_name_mappings DataPipelinePipeline#transform_name_mappings}
        :param update: Set this to true if you are sending a request to update a running streaming job. When set, the job name should be the same as the running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}
        '''
        if isinstance(environment, dict):
            environment = DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment(**environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94ad0390a51330e9cd93df5ab608a38f35b6eec29320d4720267b7576aa278c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#job_name DataPipelinePipeline#job_name}
        '''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_spec_gcs_path(self) -> typing.Optional[builtins.str]:
        '''Cloud Storage path to a file with a JSON-serialized ContainerSpec as content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#container_spec_gcs_path DataPipelinePipeline#container_spec_gcs_path}
        '''
        result = self._values.get("container_spec_gcs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional["DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment"]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#environment DataPipelinePipeline#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional["DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment"], result)

    @builtins.property
    def launch_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Launch options for this Flex Template job.

        This is a common set of options across languages and templates. This should not be used to pass job parameters.
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_options DataPipelinePipeline#launch_options}
        '''
        result = self._values.get("launch_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ''''The parameters for the Flex Template.

        Example: {"numWorkers":"5"}'
        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#parameters DataPipelinePipeline#parameters}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#transform_name_mappings DataPipelinePipeline#transform_name_mappings}
        '''
        result = self._values.get("transform_name_mappings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set this to true if you are sending a request to update a running streaming job.

        When set, the job name should be the same as the running job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment",
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
class DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment:
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
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_experiments DataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_user_labels DataPipelinePipeline#additional_user_labels}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#enable_streaming_engine DataPipelinePipeline#enable_streaming_engine}
        :param flexrs_goal: Set FlexRS goal for the job. https://cloud.google.com/dataflow/docs/guides/flexrs https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#FlexResourceSchedulingGoal Possible values: ["FLEXRS_UNSPECIFIED", "FLEXRS_SPEED_OPTIMIZED", "FLEXRS_COST_OPTIMIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#flexrs_goal DataPipelinePipeline#flexrs_goal}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#ip_configuration DataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#kms_key_name DataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#machine_type DataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#max_workers DataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#network DataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#num_workers DataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#service_account_email DataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#subnetwork DataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#temp_location DataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_region DataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_zone DataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#zone DataPipelinePipeline#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4d323756ef4418284bb108cbe1ae717394ee09f270343b121884fe67378f38)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_experiments DataPipelinePipeline#additional_experiments}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_user_labels DataPipelinePipeline#additional_user_labels}
        '''
        result = self._values.get("additional_user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def enable_streaming_engine(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable Streaming Engine for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#enable_streaming_engine DataPipelinePipeline#enable_streaming_engine}
        '''
        result = self._values.get("enable_streaming_engine")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def flexrs_goal(self) -> typing.Optional[builtins.str]:
        '''Set FlexRS goal for the job. https://cloud.google.com/dataflow/docs/guides/flexrs https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#FlexResourceSchedulingGoal Possible values: ["FLEXRS_UNSPECIFIED", "FLEXRS_SPEED_OPTIMIZED", "FLEXRS_COST_OPTIMIZED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#flexrs_goal DataPipelinePipeline#flexrs_goal}
        '''
        result = self._values.get("flexrs_goal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_configuration(self) -> typing.Optional[builtins.str]:
        '''Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#ip_configuration DataPipelinePipeline#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        ''''Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#kms_key_name DataPipelinePipeline#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type to use for the job. Defaults to the value from the template if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#machine_type DataPipelinePipeline#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#max_workers DataPipelinePipeline#max_workers}
        '''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#network DataPipelinePipeline#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''The initial number of Compute Engine instances for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#num_workers DataPipelinePipeline#num_workers}
        '''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The email address of the service account to run the job as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#service_account_email DataPipelinePipeline#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Subnetwork to which VMs will be assigned, if desired.

        You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#subnetwork DataPipelinePipeline#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#temp_location DataPipelinePipeline#temp_location}
        '''
        result = self._values.get("temp_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_region(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_region DataPipelinePipeline#worker_region}
        '''
        result = self._values.get("worker_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_zone DataPipelinePipeline#worker_zone}
        '''
        result = self._values.get("worker_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine availability zone for launching worker instances to run your pipeline.

        In the future, workerZone will take precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#zone DataPipelinePipeline#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7b670c415b85a389ea0b9eb79187a6c9628dfe992cff8d1e899e0800da8e76c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4696843e889eab87fd2d2bb85f7291cd39fd17b4f355139748da4225857e0f68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72f156bf5b3be9087403bc3b2f9954bdfb138a0562f3ca8255d90bbb1835cd91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9301f7d0893c6c0795ab78d8d5fa9748de04e3335a412d55aee5485eeb3833ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStreamingEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flexrsGoal")
    def flexrs_goal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flexrsGoal"))

    @flexrs_goal.setter
    def flexrs_goal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a580e6bc4fc2bfbc728c6d8cf12b1500e3e39d20c4d64eee81c18176adc35d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexrsGoal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipConfiguration"))

    @ip_configuration.setter
    def ip_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f0b993b41ad8b7413fb2812750a06100d16465ba57a9bc2cb416f052978b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39c3928fd7a9bd12eb0c6e329dd03a9504f7e71e353237357b1a9db89b7888d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fea9594d0bc9ab0a555d650cfc01420982852cf937f63905a06fb3a0e4291d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6703dec3e7c527a41733dfbb3a367f0c9e86506851464844fbac75d06d9fc3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7252a066f0f6a07c8e87e968d29314760db4e98955faeb52d2dc3335f5b3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numWorkers")
    def num_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numWorkers"))

    @num_workers.setter
    def num_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0dd1efb7606e2d9f0fea8f6c044fac9b6becb84f0d7cc8de6a960cc48c5309e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532ca91a03dd1d67d9a90e662a7ff0f51bdf67f0c6528bece34964151886ae95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704db88339c536aaa9de97d4b705da18299c0e627fbf6b43e1f37c46c5488919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tempLocation")
    def temp_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempLocation"))

    @temp_location.setter
    def temp_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd14a919456ed81e268072d2a8a360fa32147bb2c1c0b20826e7640ea7e182b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerRegion")
    def worker_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerRegion"))

    @worker_region.setter
    def worker_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386900e014ae8116183d33a3ed10047d9a11b2cbf2d1f2625c5a1499c10c13a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerZone")
    def worker_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerZone"))

    @worker_zone.setter
    def worker_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845f373d58c03eab79fe7cc6b812b3e1e7d4b6ed713c0e08203020b526218d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ac43d42bdd6d430b20b8ab73be7f09a57057c9470ab23563350102dfd787d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d5b9c44107cdb683bcca2e73bb5e4fb12605d86b65d94c2718c321037c6838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a9e6e8e261105fc3cd91fac2bd528613cc8ce3853090ffcd5415e9579d20831)
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
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_experiments DataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_user_labels DataPipelinePipeline#additional_user_labels}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#enable_streaming_engine DataPipelinePipeline#enable_streaming_engine}
        :param flexrs_goal: Set FlexRS goal for the job. https://cloud.google.com/dataflow/docs/guides/flexrs https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#FlexResourceSchedulingGoal Possible values: ["FLEXRS_UNSPECIFIED", "FLEXRS_SPEED_OPTIMIZED", "FLEXRS_COST_OPTIMIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#flexrs_goal DataPipelinePipeline#flexrs_goal}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#ip_configuration DataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#kms_key_name DataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#machine_type DataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#max_workers DataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#network DataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#num_workers DataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#service_account_email DataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#subnetwork DataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#temp_location DataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_region DataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_zone DataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#zone DataPipelinePipeline#zone}
        '''
        value = DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment(
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
    ) -> DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference:
        return typing.cast(DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="containerSpecGcsPathInput")
    def container_spec_gcs_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerSpecGcsPathInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment], jsii.get(self, "environmentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ad3b34c647d0cc3efa5d3dcb70d1812a7e3e4df11ea19b785707e6a9f34634b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerSpecGcsPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d305997e972d9e0720b8f8b1cac64f3bf49b4eabddc09ce102ec6851456ab690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchOptions")
    def launch_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "launchOptions"))

    @launch_options.setter
    def launch_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0f25d45438fedc0c5905ba57cc5d5c86d79a1520cb76d7752650d224d87cb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea90910b11552904e8c1a71441d85ba9193b39d66cf05cb03a818506897fa72b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2a0c3b6097accf987570db811b8a438186b3e2068bc2c00c5c871847c4e7f87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3f3c3657629a4d7af6e0c1005b1cc46274d5ac3343c9b6b97bab625b5846682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ae9f912eb60ec175452f9f1c7673ffae625cda4f369e8d6a9e070c7553f4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb29f5ad6effff22fed86ed0c5f714f038678391d92da645816ae07b0cbf540d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLaunchParameter")
    def put_launch_parameter(
        self,
        *,
        job_name: builtins.str,
        container_spec_gcs_path: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        launch_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. For an update job request, the job name should be the same as the existing running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#job_name DataPipelinePipeline#job_name}
        :param container_spec_gcs_path: Cloud Storage path to a file with a JSON-serialized ContainerSpec as content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#container_spec_gcs_path DataPipelinePipeline#container_spec_gcs_path}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#environment DataPipelinePipeline#environment}
        :param launch_options: Launch options for this Flex Template job. This is a common set of options across languages and templates. This should not be used to pass job parameters. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_options DataPipelinePipeline#launch_options}
        :param parameters: 'The parameters for the Flex Template. Example: {"numWorkers":"5"}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#parameters DataPipelinePipeline#parameters}
        :param transform_name_mappings: 'Use this to pass transform name mappings for streaming update jobs. Example: {"oldTransformName":"newTransformName",...}' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#transform_name_mappings DataPipelinePipeline#transform_name_mappings}
        :param update: Set this to true if you are sending a request to update a running streaming job. When set, the job name should be the same as the running job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}
        '''
        value = DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter(
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
    ) -> DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference:
        return typing.cast(DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference, jsii.get(self, "launchParameter"))

    @builtins.property
    @jsii.member(jsii_name="launchParameterInput")
    def launch_parameter_input(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter], jsii.get(self, "launchParameterInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__acf34229fd2bab0c3f0bf7c384bca0b78bc0fe09a7a494b0652f18e31b2642af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fbf82db2b799d78514970509577600d4c4584068d0940e9df0151f57833ca86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__118b818e4d2dd358852855b31a5fb6d2b6324af91701732f6cc1ba48f284251f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequest]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__addad0051033a93373a714e0e6fe4800d7c631c64f65171683463c8b6c430684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest",
    jsii_struct_bases=[],
    name_mapping={
        "project_id": "projectId",
        "gcs_path": "gcsPath",
        "launch_parameters": "launchParameters",
        "location": "location",
        "validate_only": "validateOnly",
    },
)
class DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest:
    def __init__(
        self,
        *,
        project_id: builtins.str,
        gcs_path: typing.Optional[builtins.str] = None,
        launch_parameters: typing.Optional[typing.Union["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project_id DataPipelinePipeline#project_id}
        :param gcs_path: A Cloud Storage path to the template from which to create the job. Must be a valid Cloud Storage URL, beginning with 'gs://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#gcs_path DataPipelinePipeline#gcs_path}
        :param launch_parameters: launch_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_parameters DataPipelinePipeline#launch_parameters}
        :param location: The regional endpoint to which to direct the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#location DataPipelinePipeline#location}
        :param validate_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#validate_only DataPipelinePipeline#validate_only}.
        '''
        if isinstance(launch_parameters, dict):
            launch_parameters = DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters(**launch_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faca2f85861020a527783f2a2f9d8abdd3cd3cd290aba78bfe4acb1ece643b72)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project_id DataPipelinePipeline#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcs_path(self) -> typing.Optional[builtins.str]:
        '''A Cloud Storage path to the template from which to create the job.

        Must be a valid Cloud Storage URL, beginning with 'gs://'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#gcs_path DataPipelinePipeline#gcs_path}
        '''
        result = self._values.get("gcs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_parameters(
        self,
    ) -> typing.Optional["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters"]:
        '''launch_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_parameters DataPipelinePipeline#launch_parameters}
        '''
        result = self._values.get("launch_parameters")
        return typing.cast(typing.Optional["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters"], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The regional endpoint to which to direct the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#location DataPipelinePipeline#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#validate_only DataPipelinePipeline#validate_only}.'''
        result = self._values.get("validate_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "environment": "environment",
        "parameters": "parameters",
        "transform_name_mapping": "transformNameMapping",
        "update": "update",
    },
)
class DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters:
    def __init__(
        self,
        *,
        job_name: builtins.str,
        environment: typing.Optional[typing.Union["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#job_name DataPipelinePipeline#job_name}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#environment DataPipelinePipeline#environment}
        :param parameters: The runtime parameters to pass to the job. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#parameters DataPipelinePipeline#parameters}
        :param transform_name_mapping: Map of transform name prefixes of the job to be replaced to the corresponding name prefixes of the new job. Only applicable when updating a pipeline. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#transform_name_mapping DataPipelinePipeline#transform_name_mapping}
        :param update: If set, replace the existing pipeline with the name specified by jobName with this pipeline, preserving state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}
        '''
        if isinstance(environment, dict):
            environment = DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment(**environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8e2718e9039c70abcac1397bd9f9a957dd376a8cfb49f6fad780b790cc0b7e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#job_name DataPipelinePipeline#job_name}
        '''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment"]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#environment DataPipelinePipeline#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional["DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment"], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The runtime parameters to pass to the job.

        'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#parameters DataPipelinePipeline#parameters}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#transform_name_mapping DataPipelinePipeline#transform_name_mapping}
        '''
        result = self._values.get("transform_name_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, replace the existing pipeline with the name specified by jobName with this pipeline, preserving state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment",
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
class DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment:
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
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_experiments DataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_user_labels DataPipelinePipeline#additional_user_labels}
        :param bypass_temp_dir_validation: Whether to bypass the safety checks for the job's temporary directory. Use with caution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#bypass_temp_dir_validation DataPipelinePipeline#bypass_temp_dir_validation}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#enable_streaming_engine DataPipelinePipeline#enable_streaming_engine}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#ip_configuration DataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#kms_key_name DataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#machine_type DataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#max_workers DataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#network DataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#num_workers DataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#service_account_email DataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#subnetwork DataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#temp_location DataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_region DataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_zone DataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#zone DataPipelinePipeline#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20c28ba32690095bcc6f7c5f7d44dd27e2ced5c8ad5a49bfad0c823689efe41)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_experiments DataPipelinePipeline#additional_experiments}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_user_labels DataPipelinePipeline#additional_user_labels}
        '''
        result = self._values.get("additional_user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bypass_temp_dir_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to bypass the safety checks for the job's temporary directory. Use with caution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#bypass_temp_dir_validation DataPipelinePipeline#bypass_temp_dir_validation}
        '''
        result = self._values.get("bypass_temp_dir_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_streaming_engine(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable Streaming Engine for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#enable_streaming_engine DataPipelinePipeline#enable_streaming_engine}
        '''
        result = self._values.get("enable_streaming_engine")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_configuration(self) -> typing.Optional[builtins.str]:
        '''Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#ip_configuration DataPipelinePipeline#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        ''''Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#kms_key_name DataPipelinePipeline#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type to use for the job. Defaults to the value from the template if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#machine_type DataPipelinePipeline#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#max_workers DataPipelinePipeline#max_workers}
        '''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#network DataPipelinePipeline#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''The initial number of Compute Engine instances for the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#num_workers DataPipelinePipeline#num_workers}
        '''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The email address of the service account to run the job as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#service_account_email DataPipelinePipeline#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Subnetwork to which VMs will be assigned, if desired.

        You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#subnetwork DataPipelinePipeline#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#temp_location DataPipelinePipeline#temp_location}
        '''
        result = self._values.get("temp_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_region(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_region DataPipelinePipeline#worker_region}
        '''
        result = self._values.get("worker_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_zone DataPipelinePipeline#worker_zone}
        '''
        result = self._values.get("worker_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine availability zone for launching worker instances to run your pipeline.

        In the future, workerZone will take precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#zone DataPipelinePipeline#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e40fe578b0dbccd8e1e84b4928a9bfdf7f06aeb5b0bbab90c8579ecf18722f77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97eeca6fd502f557b3807d0c72982f4ac88c98f7ac397623298004c729e0a96a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc10f98ecaca2ada55a4405c62811dfb07d8d768acd3fa3fb539ef4518394c1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88a572538aabf9c477656fdeb81526c22a1583f87881011df414da1e57c398e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39ffa96044623d7d3f1b6e954d9ccd70d9527da97e1e2709c6d0142a18ac1c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStreamingEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipConfiguration"))

    @ip_configuration.setter
    def ip_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f1c4aeec4b0b996fdfb43fe8493f034af29e02a615d2d9ea8379ea440801c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917378e0541f2b086dce1ed07bae47284dfe2631a04dd684cf56609a3d80d661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be606c596f1eb5c7f07c9529c2affba8e260e0eab160556d4194d8be0f0f2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edee7fd9a645ad86301bb32137ff7b65beb71a69015021a675e80e5936e89aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c14d5f924bc09044f657ea8fa624d9333bc129040b71fe9c1a719687ddcc14f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numWorkers")
    def num_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numWorkers"))

    @num_workers.setter
    def num_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf994dc4ffac520909e61a40418b54ecb98ae74578e62dc13bdea682e2f7485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770697d5c5725e734b51859a17b0c63516e5bc98ee8ae2b95e8a3d1dc85efb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a7e5d48232ac14e3c3f73e99927135d406ec8131492b2a5e69880fa39c1bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tempLocation")
    def temp_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempLocation"))

    @temp_location.setter
    def temp_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8180e3462be6337c3e7790e199e9578e76a7d64001994c9a93d89367588c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerRegion")
    def worker_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerRegion"))

    @worker_region.setter
    def worker_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74563f4433e432959922b1f3602d8fb2bb31e8b78481394598d61eb509fb543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerZone")
    def worker_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerZone"))

    @worker_zone.setter
    def worker_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5185ea8a21b458f9195cbdd14826cf6c4185bfd19e0ae794a3fce6fbe6741eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d466d580554031241b9e309aafa2f657651ca0692e86949e829a7b3c805c777c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e254613c304ea908816e5961805a1095fb25db9b44d1432d254f143346eaee82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70309469e88f56cddc951210e575cbda50e54a1664b742204e2d0a6c71126095)
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
        :param additional_experiments: Additional experiment flags for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_experiments DataPipelinePipeline#additional_experiments}
        :param additional_user_labels: Additional user labels to be specified for the job. Keys and values should follow the restrictions specified in the labeling restrictions page. An object containing a list of key/value pairs. 'Example: { "name": "wrench", "mass": "1kg", "count": "3" }.' 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#additional_user_labels DataPipelinePipeline#additional_user_labels}
        :param bypass_temp_dir_validation: Whether to bypass the safety checks for the job's temporary directory. Use with caution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#bypass_temp_dir_validation DataPipelinePipeline#bypass_temp_dir_validation}
        :param enable_streaming_engine: Whether to enable Streaming Engine for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#enable_streaming_engine DataPipelinePipeline#enable_streaming_engine}
        :param ip_configuration: Configuration for VM IPs. https://cloud.google.com/dataflow/docs/reference/data-pipelines/rest/v1/projects.locations.pipelines#WorkerIPAddressConfiguration Possible values: ["WORKER_IP_UNSPECIFIED", "WORKER_IP_PUBLIC", "WORKER_IP_PRIVATE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#ip_configuration DataPipelinePipeline#ip_configuration}
        :param kms_key_name: 'Name for the Cloud KMS key for the job. The key format is: projects//locations//keyRings//cryptoKeys/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#kms_key_name DataPipelinePipeline#kms_key_name}
        :param machine_type: The machine type to use for the job. Defaults to the value from the template if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#machine_type DataPipelinePipeline#machine_type}
        :param max_workers: The maximum number of Compute Engine instances to be made available to your pipeline during execution, from 1 to 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#max_workers DataPipelinePipeline#max_workers}
        :param network: Network to which VMs will be assigned. If empty or unspecified, the service will use the network "default". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#network DataPipelinePipeline#network}
        :param num_workers: The initial number of Compute Engine instances for the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#num_workers DataPipelinePipeline#num_workers}
        :param service_account_email: The email address of the service account to run the job as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#service_account_email DataPipelinePipeline#service_account_email}
        :param subnetwork: Subnetwork to which VMs will be assigned, if desired. You can specify a subnetwork using either a complete URL or an abbreviated path. Expected to be of the form "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK" or "regions/REGION/subnetworks/SUBNETWORK". If the subnetwork is located in a Shared VPC network, you must use the complete URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#subnetwork DataPipelinePipeline#subnetwork}
        :param temp_location: The Cloud Storage path to use for temporary files. Must be a valid Cloud Storage URL, beginning with gs://. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#temp_location DataPipelinePipeline#temp_location}
        :param worker_region: The Compute Engine region (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1". Mutually exclusive with workerZone. If neither workerRegion nor workerZone is specified, default to the control plane's region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_region DataPipelinePipeline#worker_region}
        :param worker_zone: The Compute Engine zone (https://cloud.google.com/compute/docs/regions-zones/regions-zones) in which worker processing should occur, e.g. "us-west1-a". Mutually exclusive with workerRegion. If neither workerRegion nor workerZone is specified, a zone in the control plane's region is chosen based on available capacity. If both workerZone and zone are set, workerZone takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#worker_zone DataPipelinePipeline#worker_zone}
        :param zone: The Compute Engine availability zone for launching worker instances to run your pipeline. In the future, workerZone will take precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#zone DataPipelinePipeline#zone}
        '''
        value = DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment(
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
    ) -> DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference:
        return typing.cast(DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment], jsii.get(self, "environmentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd70c231d6d067080e851a0c510726af9e48ddfb0d65ce4a4acb614b3846f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06dedd14a36ef932d146df211d1e450279f448eba979b26d9c6be76e384ec155)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d56c3c3edecd1b8b1278746a875243804d243b155e9e2d09bf1d3a9bc0321356)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbeefe0db053fe0eb0f19db765e53fef320ec9501cbd8b50262633d07854eb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77401b5df3343385b735af0425de8d9d710faf35921e0d1efba4c7586e848e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02688af336752ee63322651672bed29e9d35dbbcd219bfa2353c12b87cad9378)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLaunchParameters")
    def put_launch_parameters(
        self,
        *,
        job_name: builtins.str,
        environment: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param job_name: The job name to use for the created job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#job_name DataPipelinePipeline#job_name}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#environment DataPipelinePipeline#environment}
        :param parameters: The runtime parameters to pass to the job. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#parameters DataPipelinePipeline#parameters}
        :param transform_name_mapping: Map of transform name prefixes of the job to be replaced to the corresponding name prefixes of the new job. Only applicable when updating a pipeline. 'An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#transform_name_mapping DataPipelinePipeline#transform_name_mapping}
        :param update: If set, replace the existing pipeline with the name specified by jobName with this pipeline, preserving state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#update DataPipelinePipeline#update}
        '''
        value = DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters(
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
    ) -> DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference:
        return typing.cast(DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference, jsii.get(self, "launchParameters"))

    @builtins.property
    @jsii.member(jsii_name="gcsPathInput")
    def gcs_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcsPathInput"))

    @builtins.property
    @jsii.member(jsii_name="launchParametersInput")
    def launch_parameters_input(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters], jsii.get(self, "launchParametersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d9aaafaf043baea7ec17c667891dade2dbb60cee81b35b87126ce59cc6a6784a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3563a1b185c71fec20236d8fa8492b62f97f0a7401de509caf5db02a3c208fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af61641d115a4b233d5ba06aad996da552e68b68743dcea5200cfe733e01902)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44c1f7c24ca34c36a2dac0450d6903caace27452f475483f19cdfaa995d102d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26f6dd68f2537c7824c3e04ffdd60b7e9783dd8c8aa8815ef995c9c26fc974f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataPipelinePipelineWorkloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataPipelinePipeline.DataPipelinePipelineWorkloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72866c74e93df4fc56bfb15ce2e5481348f5a7fccab7d91356067d66e036a9b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataflowFlexTemplateRequest")
    def put_dataflow_flex_template_request(
        self,
        *,
        launch_parameter: typing.Union[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter, typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        project_id: builtins.str,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param launch_parameter: launch_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_parameter DataPipelinePipeline#launch_parameter}
        :param location: The regional endpoint to which to direct the request. For example, us-central1, us-west1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#location DataPipelinePipeline#location}
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project_id DataPipelinePipeline#project_id}
        :param validate_only: If true, the request is validated but not actually executed. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#validate_only DataPipelinePipeline#validate_only}
        '''
        value = DataPipelinePipelineWorkloadDataflowFlexTemplateRequest(
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
        launch_parameters: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters, typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param project_id: The ID of the Cloud Platform project that the job belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#project_id DataPipelinePipeline#project_id}
        :param gcs_path: A Cloud Storage path to the template from which to create the job. Must be a valid Cloud Storage URL, beginning with 'gs://'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#gcs_path DataPipelinePipeline#gcs_path}
        :param launch_parameters: launch_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#launch_parameters DataPipelinePipeline#launch_parameters}
        :param location: The regional endpoint to which to direct the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#location DataPipelinePipeline#location}
        :param validate_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_pipeline_pipeline#validate_only DataPipelinePipeline#validate_only}.
        '''
        value = DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest(
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
    ) -> DataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference:
        return typing.cast(DataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference, jsii.get(self, "dataflowFlexTemplateRequest"))

    @builtins.property
    @jsii.member(jsii_name="dataflowLaunchTemplateRequest")
    def dataflow_launch_template_request(
        self,
    ) -> DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference:
        return typing.cast(DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference, jsii.get(self, "dataflowLaunchTemplateRequest"))

    @builtins.property
    @jsii.member(jsii_name="dataflowFlexTemplateRequestInput")
    def dataflow_flex_template_request_input(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequest]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequest], jsii.get(self, "dataflowFlexTemplateRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="dataflowLaunchTemplateRequestInput")
    def dataflow_launch_template_request_input(
        self,
    ) -> typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest], jsii.get(self, "dataflowLaunchTemplateRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataPipelinePipelineWorkload]:
        return typing.cast(typing.Optional[DataPipelinePipelineWorkload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPipelinePipelineWorkload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08eec69ae21c2f1aa64011231b21ca31fde52449391410e80c04021303278263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataPipelinePipeline",
    "DataPipelinePipelineConfig",
    "DataPipelinePipelineScheduleInfo",
    "DataPipelinePipelineScheduleInfoOutputReference",
    "DataPipelinePipelineTimeouts",
    "DataPipelinePipelineTimeoutsOutputReference",
    "DataPipelinePipelineWorkload",
    "DataPipelinePipelineWorkloadDataflowFlexTemplateRequest",
    "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter",
    "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment",
    "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironmentOutputReference",
    "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterOutputReference",
    "DataPipelinePipelineWorkloadDataflowFlexTemplateRequestOutputReference",
    "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest",
    "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters",
    "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment",
    "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironmentOutputReference",
    "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersOutputReference",
    "DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestOutputReference",
    "DataPipelinePipelineWorkloadOutputReference",
]

publication.publish()

def _typecheckingstub__16ba1b660da86533f1c613affbdc1e2807d3131eb62b01354b1adae2ae58fd13(
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
    schedule_info: typing.Optional[typing.Union[DataPipelinePipelineScheduleInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler_service_account_email: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataPipelinePipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload: typing.Optional[typing.Union[DataPipelinePipelineWorkload, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ecadb79b9ab9dfec6c63939199d0ff38bd1f45dc1c5d7d8b319cb35c5937ce0b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b53704f5e5ae529596fa97712a9bf9cb7df1d88068e4ecc90eff539221fad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f2e0374fcba914f19f500bff6403c8bd2fec4dbc814c2a0f9f5a5a5e203632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefb93e0b855c56ef0845f245274683b03a33b807648c1f19e2770f03daa9659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c06e59f3d26e6ffe0be34043b33f537df263dd381a41cfb42b1d38b993125d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099b97d9001eb8a94ff5780c9841a9c8d2b501f85fa06d9dec589f8f7039c18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31bae024f42aff828c586dc363a15b05863e1bf566933f5d1b2e7c025950b20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d57e9d857312217cc63f0789cf8a048ccf2969eada6d06da3d09168820670b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e515063fc181cf1ba37627692cebd3b2670b5d02902d34fa6864668b3515b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05e739d526a34a1425028521efdb65db09516bae0c3780fd16a677196d44d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d10ecc13f4a11bccd59b1f59e4fa32b1d784df6962ece194edfbc780b9aab5(
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
    schedule_info: typing.Optional[typing.Union[DataPipelinePipelineScheduleInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler_service_account_email: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataPipelinePipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload: typing.Optional[typing.Union[DataPipelinePipelineWorkload, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8069f7028865dce8719ae78ee0a6806f7e5ce0054249d3c69f3a8b6ef89d78c(
    *,
    schedule: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3052550ee6a9ac020083989f17ce1a9c6ced39ac404ca57d94af79e0e066c0ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4dbd84f7cef2e4b4a1985f7082b55dc271f17f830520e2670367f5c9e2729c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e38a44ab2a623d4f23fe5084ae9acec0fa074053d818cdbc3ecbbdbacd4e4c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14be513be1ded29f723cbd88931172c89120972972808138bb7b1d005961b104(
    value: typing.Optional[DataPipelinePipelineScheduleInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f417b3509aacf985e03fb83fda05ab98ed47fb4c00d913c9d975c86d370d4bb7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6674380134364a8d3733ad515ac9d185cab1ccab514da10fa928de1787415a22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29550c477927fed6e330491864fde9896635bbf4eeaf1cd295320402f20ea98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345f2a7b6e599f9e6feebfdbf864c8ca840f8e7901ab70294ac819448d335b62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412c5fe154fc1f3b636b0e74b4ee2c3c04f0771b63ebcbd3798fd9fe507a279f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65ddadc165d2a205400a433c404b1f0270887487b1621287e3ddb2937263ef6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataPipelinePipelineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2305d72e616dcf4889588adab9439080d6d94d11e2bee228246b597965ce4fb(
    *,
    dataflow_flex_template_request: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowFlexTemplateRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    dataflow_launch_template_request: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946cabbb80d0d7659fec41f759dc4cb2e1ff905c44eeb516d0b935e2475f7574(
    *,
    launch_parameter: typing.Union[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    project_id: builtins.str,
    validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94ad0390a51330e9cd93df5ab608a38f35b6eec29320d4720267b7576aa278c(
    *,
    job_name: builtins.str,
    container_spec_gcs_path: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    launch_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transform_name_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4d323756ef4418284bb108cbe1ae717394ee09f270343b121884fe67378f38(
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

def _typecheckingstub__d7b670c415b85a389ea0b9eb79187a6c9628dfe992cff8d1e899e0800da8e76c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4696843e889eab87fd2d2bb85f7291cd39fd17b4f355139748da4225857e0f68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f156bf5b3be9087403bc3b2f9954bdfb138a0562f3ca8255d90bbb1835cd91(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9301f7d0893c6c0795ab78d8d5fa9748de04e3335a412d55aee5485eeb3833ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a580e6bc4fc2bfbc728c6d8cf12b1500e3e39d20c4d64eee81c18176adc35d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f0b993b41ad8b7413fb2812750a06100d16465ba57a9bc2cb416f052978b68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39c3928fd7a9bd12eb0c6e329dd03a9504f7e71e353237357b1a9db89b7888d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fea9594d0bc9ab0a555d650cfc01420982852cf937f63905a06fb3a0e4291d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6703dec3e7c527a41733dfbb3a367f0c9e86506851464844fbac75d06d9fc3ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7252a066f0f6a07c8e87e968d29314760db4e98955faeb52d2dc3335f5b3be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dd1efb7606e2d9f0fea8f6c044fac9b6becb84f0d7cc8de6a960cc48c5309e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532ca91a03dd1d67d9a90e662a7ff0f51bdf67f0c6528bece34964151886ae95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704db88339c536aaa9de97d4b705da18299c0e627fbf6b43e1f37c46c5488919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd14a919456ed81e268072d2a8a360fa32147bb2c1c0b20826e7640ea7e182b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386900e014ae8116183d33a3ed10047d9a11b2cbf2d1f2625c5a1499c10c13a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845f373d58c03eab79fe7cc6b812b3e1e7d4b6ed713c0e08203020b526218d0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ac43d42bdd6d430b20b8ab73be7f09a57057c9470ab23563350102dfd787d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d5b9c44107cdb683bcca2e73bb5e4fb12605d86b65d94c2718c321037c6838(
    value: typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameterEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9e6e8e261105fc3cd91fac2bd528613cc8ce3853090ffcd5415e9579d20831(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3b34c647d0cc3efa5d3dcb70d1812a7e3e4df11ea19b785707e6a9f34634b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d305997e972d9e0720b8f8b1cac64f3bf49b4eabddc09ce102ec6851456ab690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0f25d45438fedc0c5905ba57cc5d5c86d79a1520cb76d7752650d224d87cb0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea90910b11552904e8c1a71441d85ba9193b39d66cf05cb03a818506897fa72b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a0c3b6097accf987570db811b8a438186b3e2068bc2c00c5c871847c4e7f87(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f3c3657629a4d7af6e0c1005b1cc46274d5ac3343c9b6b97bab625b5846682(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ae9f912eb60ec175452f9f1c7673ffae625cda4f369e8d6a9e070c7553f4ae(
    value: typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequestLaunchParameter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb29f5ad6effff22fed86ed0c5f714f038678391d92da645816ae07b0cbf540d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf34229fd2bab0c3f0bf7c384bca0b78bc0fe09a7a494b0652f18e31b2642af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbf82db2b799d78514970509577600d4c4584068d0940e9df0151f57833ca86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118b818e4d2dd358852855b31a5fb6d2b6324af91701732f6cc1ba48f284251f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addad0051033a93373a714e0e6fe4800d7c631c64f65171683463c8b6c430684(
    value: typing.Optional[DataPipelinePipelineWorkloadDataflowFlexTemplateRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faca2f85861020a527783f2a2f9d8abdd3cd3cd290aba78bfe4acb1ece643b72(
    *,
    project_id: builtins.str,
    gcs_path: typing.Optional[builtins.str] = None,
    launch_parameters: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    validate_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8e2718e9039c70abcac1397bd9f9a957dd376a8cfb49f6fad780b790cc0b7e(
    *,
    job_name: builtins.str,
    environment: typing.Optional[typing.Union[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transform_name_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20c28ba32690095bcc6f7c5f7d44dd27e2ced5c8ad5a49bfad0c823689efe41(
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

def _typecheckingstub__e40fe578b0dbccd8e1e84b4928a9bfdf7f06aeb5b0bbab90c8579ecf18722f77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97eeca6fd502f557b3807d0c72982f4ac88c98f7ac397623298004c729e0a96a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc10f98ecaca2ada55a4405c62811dfb07d8d768acd3fa3fb539ef4518394c1d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a572538aabf9c477656fdeb81526c22a1583f87881011df414da1e57c398e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ffa96044623d7d3f1b6e954d9ccd70d9527da97e1e2709c6d0142a18ac1c16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f1c4aeec4b0b996fdfb43fe8493f034af29e02a615d2d9ea8379ea440801c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917378e0541f2b086dce1ed07bae47284dfe2631a04dd684cf56609a3d80d661(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be606c596f1eb5c7f07c9529c2affba8e260e0eab160556d4194d8be0f0f2e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edee7fd9a645ad86301bb32137ff7b65beb71a69015021a675e80e5936e89aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c14d5f924bc09044f657ea8fa624d9333bc129040b71fe9c1a719687ddcc14f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf994dc4ffac520909e61a40418b54ecb98ae74578e62dc13bdea682e2f7485(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770697d5c5725e734b51859a17b0c63516e5bc98ee8ae2b95e8a3d1dc85efb3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a7e5d48232ac14e3c3f73e99927135d406ec8131492b2a5e69880fa39c1bf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8180e3462be6337c3e7790e199e9578e76a7d64001994c9a93d89367588c3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74563f4433e432959922b1f3602d8fb2bb31e8b78481394598d61eb509fb543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5185ea8a21b458f9195cbdd14826cf6c4185bfd19e0ae794a3fce6fbe6741eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d466d580554031241b9e309aafa2f657651ca0692e86949e829a7b3c805c777c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e254613c304ea908816e5961805a1095fb25db9b44d1432d254f143346eaee82(
    value: typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParametersEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70309469e88f56cddc951210e575cbda50e54a1664b742204e2d0a6c71126095(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd70c231d6d067080e851a0c510726af9e48ddfb0d65ce4a4acb614b3846f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06dedd14a36ef932d146df211d1e450279f448eba979b26d9c6be76e384ec155(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56c3c3edecd1b8b1278746a875243804d243b155e9e2d09bf1d3a9bc0321356(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbeefe0db053fe0eb0f19db765e53fef320ec9501cbd8b50262633d07854eb71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77401b5df3343385b735af0425de8d9d710faf35921e0d1efba4c7586e848e47(
    value: typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequestLaunchParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02688af336752ee63322651672bed29e9d35dbbcd219bfa2353c12b87cad9378(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9aaafaf043baea7ec17c667891dade2dbb60cee81b35b87126ce59cc6a6784a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3563a1b185c71fec20236d8fa8492b62f97f0a7401de509caf5db02a3c208fb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af61641d115a4b233d5ba06aad996da552e68b68743dcea5200cfe733e01902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c1f7c24ca34c36a2dac0450d6903caace27452f475483f19cdfaa995d102d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26f6dd68f2537c7824c3e04ffdd60b7e9783dd8c8aa8815ef995c9c26fc974f(
    value: typing.Optional[DataPipelinePipelineWorkloadDataflowLaunchTemplateRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72866c74e93df4fc56bfb15ce2e5481348f5a7fccab7d91356067d66e036a9b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08eec69ae21c2f1aa64011231b21ca31fde52449391410e80c04021303278263(
    value: typing.Optional[DataPipelinePipelineWorkload],
) -> None:
    """Type checking stubs"""
    pass
