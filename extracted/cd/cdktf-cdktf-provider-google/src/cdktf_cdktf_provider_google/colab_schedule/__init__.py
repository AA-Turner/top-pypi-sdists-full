r'''
# `google_colab_schedule`

Refer to the Terraform Registry for docs: [`google_colab_schedule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule).
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


class ColabSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabSchedule.ColabSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule google_colab_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        create_notebook_execution_job_request: typing.Union["ColabScheduleCreateNotebookExecutionJobRequest", typing.Dict[builtins.str, typing.Any]],
        cron: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        max_concurrent_run_count: builtins.str,
        allow_queueing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_state: typing.Optional[builtins.str] = None,
        end_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_run_count: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ColabScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule google_colab_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param create_notebook_execution_job_request: create_notebook_execution_job_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#create_notebook_execution_job_request ColabSchedule#create_notebook_execution_job_request}
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#cron ColabSchedule#cron}
        :param display_name: Required. The display name of the Schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#display_name ColabSchedule#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#location ColabSchedule#location}
        :param max_concurrent_run_count: Maximum number of runs that can be started concurrently for this Schedule. This is the limit for starting the scheduled requests and not the execution of the notebook execution jobs created by the requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#max_concurrent_run_count ColabSchedule#max_concurrent_run_count}
        :param allow_queueing: Whether new scheduled runs can be queued when max_concurrent_runs limit is reached. If set to true, new runs will be queued instead of skipped. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#allow_queueing ColabSchedule#allow_queueing}
        :param desired_state: Desired state of the Colab Schedule. Set this field to 'ACTIVE' to start/resume the schedule, and 'PAUSED' to pause the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#desired_state ColabSchedule#desired_state}
        :param end_time: Timestamp after which no new runs can be scheduled. If specified, the schedule will be completed when either end_time is reached or when scheduled_run_count >= max_run_count. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#end_time ColabSchedule#end_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#id ColabSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_run_count: Maximum run count of the schedule. If specified, The schedule will be completed when either startedRunCount >= maxRunCount or when endTime is reached. If not specified, new runs will keep getting scheduled until this Schedule is paused or deleted. Already scheduled runs will be allowed to complete. Unset if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#max_run_count ColabSchedule#max_run_count}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#project ColabSchedule#project}.
        :param start_time: The timestamp after which the first run can be scheduled. Defaults to the schedule creation time. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#start_time ColabSchedule#start_time}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#timeouts ColabSchedule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f25c4c7d9202254adff00d98f2862135c5556c30a95066a3ca70fcd2477a8b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ColabScheduleConfig(
            create_notebook_execution_job_request=create_notebook_execution_job_request,
            cron=cron,
            display_name=display_name,
            location=location,
            max_concurrent_run_count=max_concurrent_run_count,
            allow_queueing=allow_queueing,
            desired_state=desired_state,
            end_time=end_time,
            id=id,
            max_run_count=max_run_count,
            project=project,
            start_time=start_time,
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
        '''Generates CDKTF code for importing a ColabSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ColabSchedule to import.
        :param import_from_id: The id of the existing ColabSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ColabSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b40d1f652605f7c180f60217566a7e7e89171be4c01f1c810e4025c2f08a84)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCreateNotebookExecutionJobRequest")
    def put_create_notebook_execution_job_request(
        self,
        *,
        notebook_execution_job: typing.Union["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param notebook_execution_job: notebook_execution_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#notebook_execution_job ColabSchedule#notebook_execution_job}
        '''
        value = ColabScheduleCreateNotebookExecutionJobRequest(
            notebook_execution_job=notebook_execution_job
        )

        return typing.cast(None, jsii.invoke(self, "putCreateNotebookExecutionJobRequest", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#create ColabSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#delete ColabSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#update ColabSchedule#update}.
        '''
        value = ColabScheduleTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowQueueing")
    def reset_allow_queueing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowQueueing", []))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxRunCount")
    def reset_max_run_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRunCount", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

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
    @jsii.member(jsii_name="createNotebookExecutionJobRequest")
    def create_notebook_execution_job_request(
        self,
    ) -> "ColabScheduleCreateNotebookExecutionJobRequestOutputReference":
        return typing.cast("ColabScheduleCreateNotebookExecutionJobRequestOutputReference", jsii.get(self, "createNotebookExecutionJobRequest"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ColabScheduleTimeoutsOutputReference":
        return typing.cast("ColabScheduleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowQueueingInput")
    def allow_queueing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowQueueingInput"))

    @builtins.property
    @jsii.member(jsii_name="createNotebookExecutionJobRequestInput")
    def create_notebook_execution_job_request_input(
        self,
    ) -> typing.Optional["ColabScheduleCreateNotebookExecutionJobRequest"]:
        return typing.cast(typing.Optional["ColabScheduleCreateNotebookExecutionJobRequest"], jsii.get(self, "createNotebookExecutionJobRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="cronInput")
    def cron_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRunCountInput")
    def max_concurrent_run_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxConcurrentRunCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRunCountInput")
    def max_run_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxRunCountInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ColabScheduleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ColabScheduleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowQueueing")
    def allow_queueing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowQueueing"))

    @allow_queueing.setter
    def allow_queueing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29456610995a1b3abb79ddd26fa5ba5b2d09d47fe65b62a685f6397d9c30f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowQueueing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cron")
    def cron(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cron"))

    @cron.setter
    def cron(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9acae823ad2c436ec769d05b801f14770b6728caedad6cafa06e5aefc34230ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314ef2d4e29c976c5d1077cf267a0a17e95f965b24584fd71c2e05c42bf1b33e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a57862412b1ac4cead8f906fe8840042ae560dbb86c39d608a6641be05e1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b6ab9c0a50129485a06639e5570ac2bc1bdc40464c838e91eef0c97586016a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd751d7d4c8aff75066c953eb81b0cf027f0259c3cad867683e7a045ee58723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc8b81e755872bfa955e7e9949cd31c32197e845ae43ab6a3e573defcfdba24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRunCount")
    def max_concurrent_run_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxConcurrentRunCount"))

    @max_concurrent_run_count.setter
    def max_concurrent_run_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733058d7992eca88f1dc4afe9d1ca1e36f94158f2cac9312bb6b1c4cbf7054d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRunCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRunCount")
    def max_run_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRunCount"))

    @max_run_count.setter
    def max_run_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b5e8275aed850ee13b98c195611ad6a7da37e04ada43789b5315a1ee6d0d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRunCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50420a9b44ce010e21049700ce93965a6664d379810c458a8db02498dc0e060d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269f170273dc086560a9567f78e4da850bb646f568ac0389b3ab9b95a96ddd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "create_notebook_execution_job_request": "createNotebookExecutionJobRequest",
        "cron": "cron",
        "display_name": "displayName",
        "location": "location",
        "max_concurrent_run_count": "maxConcurrentRunCount",
        "allow_queueing": "allowQueueing",
        "desired_state": "desiredState",
        "end_time": "endTime",
        "id": "id",
        "max_run_count": "maxRunCount",
        "project": "project",
        "start_time": "startTime",
        "timeouts": "timeouts",
    },
)
class ColabScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        create_notebook_execution_job_request: typing.Union["ColabScheduleCreateNotebookExecutionJobRequest", typing.Dict[builtins.str, typing.Any]],
        cron: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        max_concurrent_run_count: builtins.str,
        allow_queueing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_state: typing.Optional[builtins.str] = None,
        end_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_run_count: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ColabScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param create_notebook_execution_job_request: create_notebook_execution_job_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#create_notebook_execution_job_request ColabSchedule#create_notebook_execution_job_request}
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#cron ColabSchedule#cron}
        :param display_name: Required. The display name of the Schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#display_name ColabSchedule#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#location ColabSchedule#location}
        :param max_concurrent_run_count: Maximum number of runs that can be started concurrently for this Schedule. This is the limit for starting the scheduled requests and not the execution of the notebook execution jobs created by the requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#max_concurrent_run_count ColabSchedule#max_concurrent_run_count}
        :param allow_queueing: Whether new scheduled runs can be queued when max_concurrent_runs limit is reached. If set to true, new runs will be queued instead of skipped. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#allow_queueing ColabSchedule#allow_queueing}
        :param desired_state: Desired state of the Colab Schedule. Set this field to 'ACTIVE' to start/resume the schedule, and 'PAUSED' to pause the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#desired_state ColabSchedule#desired_state}
        :param end_time: Timestamp after which no new runs can be scheduled. If specified, the schedule will be completed when either end_time is reached or when scheduled_run_count >= max_run_count. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#end_time ColabSchedule#end_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#id ColabSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_run_count: Maximum run count of the schedule. If specified, The schedule will be completed when either startedRunCount >= maxRunCount or when endTime is reached. If not specified, new runs will keep getting scheduled until this Schedule is paused or deleted. Already scheduled runs will be allowed to complete. Unset if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#max_run_count ColabSchedule#max_run_count}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#project ColabSchedule#project}.
        :param start_time: The timestamp after which the first run can be scheduled. Defaults to the schedule creation time. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#start_time ColabSchedule#start_time}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#timeouts ColabSchedule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(create_notebook_execution_job_request, dict):
            create_notebook_execution_job_request = ColabScheduleCreateNotebookExecutionJobRequest(**create_notebook_execution_job_request)
        if isinstance(timeouts, dict):
            timeouts = ColabScheduleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5fe38e812aa703c7df537f6367200afc570fac3c8a44d9277656742d77e795)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument create_notebook_execution_job_request", value=create_notebook_execution_job_request, expected_type=type_hints["create_notebook_execution_job_request"])
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument max_concurrent_run_count", value=max_concurrent_run_count, expected_type=type_hints["max_concurrent_run_count"])
            check_type(argname="argument allow_queueing", value=allow_queueing, expected_type=type_hints["allow_queueing"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_run_count", value=max_run_count, expected_type=type_hints["max_run_count"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_notebook_execution_job_request": create_notebook_execution_job_request,
            "cron": cron,
            "display_name": display_name,
            "location": location,
            "max_concurrent_run_count": max_concurrent_run_count,
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
        if allow_queueing is not None:
            self._values["allow_queueing"] = allow_queueing
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if end_time is not None:
            self._values["end_time"] = end_time
        if id is not None:
            self._values["id"] = id
        if max_run_count is not None:
            self._values["max_run_count"] = max_run_count
        if project is not None:
            self._values["project"] = project
        if start_time is not None:
            self._values["start_time"] = start_time
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
    def create_notebook_execution_job_request(
        self,
    ) -> "ColabScheduleCreateNotebookExecutionJobRequest":
        '''create_notebook_execution_job_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#create_notebook_execution_job_request ColabSchedule#create_notebook_execution_job_request}
        '''
        result = self._values.get("create_notebook_execution_job_request")
        assert result is not None, "Required property 'create_notebook_execution_job_request' is missing"
        return typing.cast("ColabScheduleCreateNotebookExecutionJobRequest", result)

    @builtins.property
    def cron(self) -> builtins.str:
        '''Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#cron ColabSchedule#cron}
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required. The display name of the Schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#display_name ColabSchedule#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource: https://cloud.google.com/colab/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#location ColabSchedule#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_concurrent_run_count(self) -> builtins.str:
        '''Maximum number of runs that can be started concurrently for this Schedule.

        This is the limit for starting the scheduled requests and not the execution of the notebook execution jobs created by the requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#max_concurrent_run_count ColabSchedule#max_concurrent_run_count}
        '''
        result = self._values.get("max_concurrent_run_count")
        assert result is not None, "Required property 'max_concurrent_run_count' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_queueing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether new scheduled runs can be queued when max_concurrent_runs limit is reached.

        If set to true, new runs will be queued instead of skipped. Default to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#allow_queueing ColabSchedule#allow_queueing}
        '''
        result = self._values.get("allow_queueing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Desired state of the Colab Schedule.

        Set this field to 'ACTIVE' to start/resume the schedule, and 'PAUSED' to pause the schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#desired_state ColabSchedule#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Timestamp after which no new runs can be scheduled.

        If specified, the schedule will be completed when either end_time is reached or when scheduled_run_count >= max_run_count. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#end_time ColabSchedule#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#id ColabSchedule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_run_count(self) -> typing.Optional[builtins.str]:
        '''Maximum run count of the schedule.

        If specified, The schedule will be completed when either startedRunCount >= maxRunCount or when endTime is reached. If not specified, new runs will keep getting scheduled until this Schedule is paused or deleted. Already scheduled runs will be allowed to complete. Unset if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#max_run_count ColabSchedule#max_run_count}
        '''
        result = self._values.get("max_run_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#project ColabSchedule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The timestamp after which the first run can be scheduled.

        Defaults to the schedule creation time. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#start_time ColabSchedule#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ColabScheduleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#timeouts ColabSchedule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ColabScheduleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequest",
    jsii_struct_bases=[],
    name_mapping={"notebook_execution_job": "notebookExecutionJob"},
)
class ColabScheduleCreateNotebookExecutionJobRequest:
    def __init__(
        self,
        *,
        notebook_execution_job: typing.Union["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param notebook_execution_job: notebook_execution_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#notebook_execution_job ColabSchedule#notebook_execution_job}
        '''
        if isinstance(notebook_execution_job, dict):
            notebook_execution_job = ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob(**notebook_execution_job)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad5ae578e86f54d512c67779886f011803cb0447c0f64db57e8ada5df4d912c)
            check_type(argname="argument notebook_execution_job", value=notebook_execution_job, expected_type=type_hints["notebook_execution_job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notebook_execution_job": notebook_execution_job,
        }

    @builtins.property
    def notebook_execution_job(
        self,
    ) -> "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob":
        '''notebook_execution_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#notebook_execution_job ColabSchedule#notebook_execution_job}
        '''
        result = self._values.get("notebook_execution_job")
        assert result is not None, "Required property 'notebook_execution_job' is missing"
        return typing.cast("ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabScheduleCreateNotebookExecutionJobRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "gcs_output_uri": "gcsOutputUri",
        "notebook_runtime_template_resource_name": "notebookRuntimeTemplateResourceName",
        "dataform_repository_source": "dataformRepositorySource",
        "execution_timeout": "executionTimeout",
        "execution_user": "executionUser",
        "gcs_notebook_source": "gcsNotebookSource",
        "service_account": "serviceAccount",
    },
)
class ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        gcs_output_uri: builtins.str,
        notebook_runtime_template_resource_name: builtins.str,
        dataform_repository_source: typing.Optional[typing.Union["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#display_name ColabSchedule#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#gcs_output_uri ColabSchedule#gcs_output_uri}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#notebook_runtime_template_resource_name ColabSchedule#notebook_runtime_template_resource_name}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#dataform_repository_source ColabSchedule#dataform_repository_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). A duration in seconds with up to nine fractional digits, ending with "s". Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#execution_timeout ColabSchedule#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#execution_user ColabSchedule#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#gcs_notebook_source ColabSchedule#gcs_notebook_source}
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#service_account ColabSchedule#service_account}
        '''
        if isinstance(dataform_repository_source, dict):
            dataform_repository_source = ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource(**dataform_repository_source)
        if isinstance(gcs_notebook_source, dict):
            gcs_notebook_source = ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource(**gcs_notebook_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf39db6d5d09fabd5b7998031c2d8139cf006a218b410755800dc8b9d4984b36)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gcs_output_uri", value=gcs_output_uri, expected_type=type_hints["gcs_output_uri"])
            check_type(argname="argument notebook_runtime_template_resource_name", value=notebook_runtime_template_resource_name, expected_type=type_hints["notebook_runtime_template_resource_name"])
            check_type(argname="argument dataform_repository_source", value=dataform_repository_source, expected_type=type_hints["dataform_repository_source"])
            check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
            check_type(argname="argument execution_user", value=execution_user, expected_type=type_hints["execution_user"])
            check_type(argname="argument gcs_notebook_source", value=gcs_notebook_source, expected_type=type_hints["gcs_notebook_source"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "gcs_output_uri": gcs_output_uri,
            "notebook_runtime_template_resource_name": notebook_runtime_template_resource_name,
        }
        if dataform_repository_source is not None:
            self._values["dataform_repository_source"] = dataform_repository_source
        if execution_timeout is not None:
            self._values["execution_timeout"] = execution_timeout
        if execution_user is not None:
            self._values["execution_user"] = execution_user
        if gcs_notebook_source is not None:
            self._values["gcs_notebook_source"] = gcs_notebook_source
        if service_account is not None:
            self._values["service_account"] = service_account

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required. The display name of the Notebook Execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#display_name ColabSchedule#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcs_output_uri(self) -> builtins.str:
        '''The Cloud Storage location to upload the result to. Format:'gs://bucket-name'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#gcs_output_uri ColabSchedule#gcs_output_uri}
        '''
        result = self._values.get("gcs_output_uri")
        assert result is not None, "Required property 'gcs_output_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notebook_runtime_template_resource_name(self) -> builtins.str:
        '''The NotebookRuntimeTemplate to source compute configuration from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#notebook_runtime_template_resource_name ColabSchedule#notebook_runtime_template_resource_name}
        '''
        result = self._values.get("notebook_runtime_template_resource_name")
        assert result is not None, "Required property 'notebook_runtime_template_resource_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataform_repository_source(
        self,
    ) -> typing.Optional["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource"]:
        '''dataform_repository_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#dataform_repository_source ColabSchedule#dataform_repository_source}
        '''
        result = self._values.get("dataform_repository_source")
        return typing.cast(typing.Optional["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource"], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[builtins.str]:
        '''Max running time of the execution job in seconds (default 86400s / 24 hrs).

        A duration in seconds with up to nine fractional digits, ending with "s". Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#execution_timeout ColabSchedule#execution_timeout}
        '''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_user(self) -> typing.Optional[builtins.str]:
        '''The user email to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#execution_user ColabSchedule#execution_user}
        '''
        result = self._values.get("execution_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_notebook_source(
        self,
    ) -> typing.Optional["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource"]:
        '''gcs_notebook_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#gcs_notebook_source ColabSchedule#gcs_notebook_source}
        '''
        result = self._values.get("gcs_notebook_source")
        return typing.cast(typing.Optional["ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#service_account ColabSchedule#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource",
    jsii_struct_bases=[],
    name_mapping={
        "dataform_repository_resource_name": "dataformRepositoryResourceName",
        "commit_sha": "commitSha",
    },
)
class ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource:
    def __init__(
        self,
        *,
        dataform_repository_resource_name: builtins.str,
        commit_sha: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#dataform_repository_resource_name ColabSchedule#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#commit_sha ColabSchedule#commit_sha}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df6e98f559b9fa9a941cc3312f4d3f1b7d234c4436fee34a07a4d4165c08860)
            check_type(argname="argument dataform_repository_resource_name", value=dataform_repository_resource_name, expected_type=type_hints["dataform_repository_resource_name"])
            check_type(argname="argument commit_sha", value=commit_sha, expected_type=type_hints["commit_sha"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataform_repository_resource_name": dataform_repository_resource_name,
        }
        if commit_sha is not None:
            self._values["commit_sha"] = commit_sha

    @builtins.property
    def dataform_repository_resource_name(self) -> builtins.str:
        '''The resource name of the Dataform Repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#dataform_repository_resource_name ColabSchedule#dataform_repository_resource_name}
        '''
        result = self._values.get("dataform_repository_resource_name")
        assert result is not None, "Required property 'dataform_repository_resource_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''The commit SHA to read repository with. If unset, the file will be read at HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#commit_sha ColabSchedule#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa02e16630308e8b6b7f534ae4a60507b60fdb9ba856401e36d85279a8f09aa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommitSha")
    def reset_commit_sha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitSha", []))

    @builtins.property
    @jsii.member(jsii_name="commitShaInput")
    def commit_sha_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitShaInput"))

    @builtins.property
    @jsii.member(jsii_name="dataformRepositoryResourceNameInput")
    def dataform_repository_resource_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataformRepositoryResourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9d0a3d792ebf2ca597b04e2aeabb08d8dbe0aaaaa73c3f99a57aae43aaa57f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataformRepositoryResourceName")
    def dataform_repository_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataformRepositoryResourceName"))

    @dataform_repository_resource_name.setter
    def dataform_repository_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73ace4efead26a718f367e8d3e57cef688ebb8f93c0e340828d3d50af773e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataformRepositoryResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource]:
        return typing.cast(typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e788c56bd79f127abae2256365b3aa6186b1b3b1b94499eda4354035b83f023e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "generation": "generation"},
)
class ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource:
    def __init__(
        self,
        *,
        uri: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Cloud Storage uri pointing to the ipynb file. Format: gs://bucket/notebook_file.ipynb. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#uri ColabSchedule#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#generation ColabSchedule#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8ca273357a91511e7b14e5879d1fc14f34a4f758f931697cba4feeaed3a299e)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def uri(self) -> builtins.str:
        '''The Cloud Storage uri pointing to the ipynb file. Format: gs://bucket/notebook_file.ipynb.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#uri ColabSchedule#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''The version of the Cloud Storage object to read.

        If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#generation ColabSchedule#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2df7b72be7a29aaa2f5ac3eb65c651b29b8a234a47b64ee8164bcd0d88be008)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d75bd053c7b63a98c2bf5d31ec428cc588eb173e854435e97784b5488498e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee36fcd40fa41a2324ab70e760f840f510f70a6591f8aaddff3ff85038b9ea6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource]:
        return typing.cast(typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534d086e206f374fd04d719b69080ce7e0d203e0888c49f136b295636dc1c41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07c0bfec13b1f483ee3248a40090e7b6f925ac732f38965a2c77bb44498cac41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataformRepositorySource")
    def put_dataform_repository_source(
        self,
        *,
        dataform_repository_resource_name: builtins.str,
        commit_sha: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#dataform_repository_resource_name ColabSchedule#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#commit_sha ColabSchedule#commit_sha}
        '''
        value = ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource(
            dataform_repository_resource_name=dataform_repository_resource_name,
            commit_sha=commit_sha,
        )

        return typing.cast(None, jsii.invoke(self, "putDataformRepositorySource", [value]))

    @jsii.member(jsii_name="putGcsNotebookSource")
    def put_gcs_notebook_source(
        self,
        *,
        uri: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Cloud Storage uri pointing to the ipynb file. Format: gs://bucket/notebook_file.ipynb. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#uri ColabSchedule#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#generation ColabSchedule#generation}
        '''
        value = ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource(
            uri=uri, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcsNotebookSource", [value]))

    @jsii.member(jsii_name="resetDataformRepositorySource")
    def reset_dataform_repository_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataformRepositorySource", []))

    @jsii.member(jsii_name="resetExecutionTimeout")
    def reset_execution_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionTimeout", []))

    @jsii.member(jsii_name="resetExecutionUser")
    def reset_execution_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionUser", []))

    @jsii.member(jsii_name="resetGcsNotebookSource")
    def reset_gcs_notebook_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsNotebookSource", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @builtins.property
    @jsii.member(jsii_name="dataformRepositorySource")
    def dataform_repository_source(
        self,
    ) -> ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference:
        return typing.cast(ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference, jsii.get(self, "dataformRepositorySource"))

    @builtins.property
    @jsii.member(jsii_name="gcsNotebookSource")
    def gcs_notebook_source(
        self,
    ) -> ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference:
        return typing.cast(ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference, jsii.get(self, "gcsNotebookSource"))

    @builtins.property
    @jsii.member(jsii_name="dataformRepositorySourceInput")
    def dataform_repository_source_input(
        self,
    ) -> typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource]:
        return typing.cast(typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource], jsii.get(self, "dataformRepositorySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionTimeoutInput")
    def execution_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="executionUserInput")
    def execution_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionUserInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsNotebookSourceInput")
    def gcs_notebook_source_input(
        self,
    ) -> typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource]:
        return typing.cast(typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource], jsii.get(self, "gcsNotebookSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsOutputUriInput")
    def gcs_output_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcsOutputUriInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookRuntimeTemplateResourceNameInput")
    def notebook_runtime_template_resource_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebookRuntimeTemplateResourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a09a7050534c052737d754d4ed5a54a395d2d8c6f37ca03f4cd4a3546098e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109e83918120714935c5a1b816cfff04b29e6ddb50cf69055346703ad1e6f00e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionUser")
    def execution_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionUser"))

    @execution_user.setter
    def execution_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5487b2d80e31322fef08fda78d3e4a39a84eb60b20aea0a6c97de1edd4c4bc61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcsOutputUri")
    def gcs_output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsOutputUri"))

    @gcs_output_uri.setter
    def gcs_output_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d135a4f58d3f84c85d43170050e2842bb225fd0cb9cf9b0c4d6f4b83756dc59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsOutputUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookRuntimeTemplateResourceName")
    def notebook_runtime_template_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookRuntimeTemplateResourceName"))

    @notebook_runtime_template_resource_name.setter
    def notebook_runtime_template_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45367be0826ffac076270ca3cf90161145ecdf98e55456116a19fa9010e6c926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookRuntimeTemplateResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62bc4f097a913a8e2cb99fc610972dcd468401518bcc7bce420d7633b499e895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob]:
        return typing.cast(typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4659b4b8ded6769b41e0992ae9865dd3cfd93bb68e678187b1636ccb4a1e6ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ColabScheduleCreateNotebookExecutionJobRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleCreateNotebookExecutionJobRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5ca9cf59f8a9daf08d60fb5a8295a25a489d48bcc56d57d83687c9d2fe38839)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotebookExecutionJob")
    def put_notebook_execution_job(
        self,
        *,
        display_name: builtins.str,
        gcs_output_uri: builtins.str,
        notebook_runtime_template_resource_name: builtins.str,
        dataform_repository_source: typing.Optional[typing.Union[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#display_name ColabSchedule#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#gcs_output_uri ColabSchedule#gcs_output_uri}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#notebook_runtime_template_resource_name ColabSchedule#notebook_runtime_template_resource_name}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#dataform_repository_source ColabSchedule#dataform_repository_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). A duration in seconds with up to nine fractional digits, ending with "s". Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#execution_timeout ColabSchedule#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#execution_user ColabSchedule#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#gcs_notebook_source ColabSchedule#gcs_notebook_source}
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#service_account ColabSchedule#service_account}
        '''
        value = ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob(
            display_name=display_name,
            gcs_output_uri=gcs_output_uri,
            notebook_runtime_template_resource_name=notebook_runtime_template_resource_name,
            dataform_repository_source=dataform_repository_source,
            execution_timeout=execution_timeout,
            execution_user=execution_user,
            gcs_notebook_source=gcs_notebook_source,
            service_account=service_account,
        )

        return typing.cast(None, jsii.invoke(self, "putNotebookExecutionJob", [value]))

    @builtins.property
    @jsii.member(jsii_name="notebookExecutionJob")
    def notebook_execution_job(
        self,
    ) -> ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference:
        return typing.cast(ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference, jsii.get(self, "notebookExecutionJob"))

    @builtins.property
    @jsii.member(jsii_name="notebookExecutionJobInput")
    def notebook_execution_job_input(
        self,
    ) -> typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob]:
        return typing.cast(typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob], jsii.get(self, "notebookExecutionJobInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ColabScheduleCreateNotebookExecutionJobRequest]:
        return typing.cast(typing.Optional[ColabScheduleCreateNotebookExecutionJobRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874efeb6adb5c3a8d29f04c2ca74659d14bf01896a4d08a8b82c081a1e2c7a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ColabScheduleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#create ColabSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#delete ColabSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#update ColabSchedule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d556ed4e4bea763eaf1a0e851058faeb527522987197555d08ae60ab8c8a645)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#create ColabSchedule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#delete ColabSchedule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/colab_schedule#update ColabSchedule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColabScheduleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ColabScheduleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.colabSchedule.ColabScheduleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dfe4a60b6b37c7e341b801c4a74ce52ac387137511b303de85a14da4f825a95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c72b21b6383afa5342973e8d10dd2e5906b23e5a4a556bb7d7d28393768f4aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feaafaca03f6f05ebb4352f1069a9ce9fc4166f13b5ff6555ea101c45fbd0762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b75fde8307853bef3234aa41e5c8cf2b3c850b42a26b5a70a475b0e7bd39df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabScheduleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabScheduleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabScheduleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061d968a1e486110d3100ef3f7461287b0b585a6c820fe74d4172a7a2ea59deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ColabSchedule",
    "ColabScheduleConfig",
    "ColabScheduleCreateNotebookExecutionJobRequest",
    "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob",
    "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource",
    "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference",
    "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource",
    "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference",
    "ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference",
    "ColabScheduleCreateNotebookExecutionJobRequestOutputReference",
    "ColabScheduleTimeouts",
    "ColabScheduleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c6f25c4c7d9202254adff00d98f2862135c5556c30a95066a3ca70fcd2477a8b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    create_notebook_execution_job_request: typing.Union[ColabScheduleCreateNotebookExecutionJobRequest, typing.Dict[builtins.str, typing.Any]],
    cron: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    max_concurrent_run_count: builtins.str,
    allow_queueing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_state: typing.Optional[builtins.str] = None,
    end_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_run_count: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ColabScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__03b40d1f652605f7c180f60217566a7e7e89171be4c01f1c810e4025c2f08a84(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29456610995a1b3abb79ddd26fa5ba5b2d09d47fe65b62a685f6397d9c30f44(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acae823ad2c436ec769d05b801f14770b6728caedad6cafa06e5aefc34230ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314ef2d4e29c976c5d1077cf267a0a17e95f965b24584fd71c2e05c42bf1b33e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a57862412b1ac4cead8f906fe8840042ae560dbb86c39d608a6641be05e1d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b6ab9c0a50129485a06639e5570ac2bc1bdc40464c838e91eef0c97586016a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd751d7d4c8aff75066c953eb81b0cf027f0259c3cad867683e7a045ee58723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc8b81e755872bfa955e7e9949cd31c32197e845ae43ab6a3e573defcfdba24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733058d7992eca88f1dc4afe9d1ca1e36f94158f2cac9312bb6b1c4cbf7054d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b5e8275aed850ee13b98c195611ad6a7da37e04ada43789b5315a1ee6d0d88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50420a9b44ce010e21049700ce93965a6664d379810c458a8db02498dc0e060d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269f170273dc086560a9567f78e4da850bb646f568ac0389b3ab9b95a96ddd95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5fe38e812aa703c7df537f6367200afc570fac3c8a44d9277656742d77e795(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    create_notebook_execution_job_request: typing.Union[ColabScheduleCreateNotebookExecutionJobRequest, typing.Dict[builtins.str, typing.Any]],
    cron: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    max_concurrent_run_count: builtins.str,
    allow_queueing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_state: typing.Optional[builtins.str] = None,
    end_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_run_count: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ColabScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad5ae578e86f54d512c67779886f011803cb0447c0f64db57e8ada5df4d912c(
    *,
    notebook_execution_job: typing.Union[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf39db6d5d09fabd5b7998031c2d8139cf006a218b410755800dc8b9d4984b36(
    *,
    display_name: builtins.str,
    gcs_output_uri: builtins.str,
    notebook_runtime_template_resource_name: builtins.str,
    dataform_repository_source: typing.Optional[typing.Union[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
    execution_user: typing.Optional[builtins.str] = None,
    gcs_notebook_source: typing.Optional[typing.Union[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df6e98f559b9fa9a941cc3312f4d3f1b7d234c4436fee34a07a4d4165c08860(
    *,
    dataform_repository_resource_name: builtins.str,
    commit_sha: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa02e16630308e8b6b7f534ae4a60507b60fdb9ba856401e36d85279a8f09aa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9d0a3d792ebf2ca597b04e2aeabb08d8dbe0aaaaa73c3f99a57aae43aaa57f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73ace4efead26a718f367e8d3e57cef688ebb8f93c0e340828d3d50af773e34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e788c56bd79f127abae2256365b3aa6186b1b3b1b94499eda4354035b83f023e(
    value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ca273357a91511e7b14e5879d1fc14f34a4f758f931697cba4feeaed3a299e(
    *,
    uri: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2df7b72be7a29aaa2f5ac3eb65c651b29b8a234a47b64ee8164bcd0d88be008(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d75bd053c7b63a98c2bf5d31ec428cc588eb173e854435e97784b5488498e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee36fcd40fa41a2324ab70e760f840f510f70a6591f8aaddff3ff85038b9ea6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534d086e206f374fd04d719b69080ce7e0d203e0888c49f136b295636dc1c41e(
    value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c0bfec13b1f483ee3248a40090e7b6f925ac732f38965a2c77bb44498cac41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a09a7050534c052737d754d4ed5a54a395d2d8c6f37ca03f4cd4a3546098e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109e83918120714935c5a1b816cfff04b29e6ddb50cf69055346703ad1e6f00e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5487b2d80e31322fef08fda78d3e4a39a84eb60b20aea0a6c97de1edd4c4bc61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d135a4f58d3f84c85d43170050e2842bb225fd0cb9cf9b0c4d6f4b83756dc59b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45367be0826ffac076270ca3cf90161145ecdf98e55456116a19fa9010e6c926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bc4f097a913a8e2cb99fc610972dcd468401518bcc7bce420d7633b499e895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4659b4b8ded6769b41e0992ae9865dd3cfd93bb68e678187b1636ccb4a1e6ef8(
    value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ca9cf59f8a9daf08d60fb5a8295a25a489d48bcc56d57d83687c9d2fe38839(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874efeb6adb5c3a8d29f04c2ca74659d14bf01896a4d08a8b82c081a1e2c7a5a(
    value: typing.Optional[ColabScheduleCreateNotebookExecutionJobRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d556ed4e4bea763eaf1a0e851058faeb527522987197555d08ae60ab8c8a645(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dfe4a60b6b37c7e341b801c4a74ce52ac387137511b303de85a14da4f825a95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72b21b6383afa5342973e8d10dd2e5906b23e5a4a556bb7d7d28393768f4aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feaafaca03f6f05ebb4352f1069a9ce9fc4166f13b5ff6555ea101c45fbd0762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b75fde8307853bef3234aa41e5c8cf2b3c850b42a26b5a70a475b0e7bd39df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061d968a1e486110d3100ef3f7461287b0b585a6c820fe74d4172a7a2ea59deb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ColabScheduleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
