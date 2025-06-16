r'''
# `google_colab_schedule`

Refer to the Terraform Registry for docs: [`google_colab_schedule`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule).
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


class GoogleColabSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule google_colab_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        create_notebook_execution_job_request: typing.Union["GoogleColabScheduleCreateNotebookExecutionJobRequest", typing.Dict[builtins.str, typing.Any]],
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
        timeouts: typing.Optional[typing.Union["GoogleColabScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule google_colab_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param create_notebook_execution_job_request: create_notebook_execution_job_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#create_notebook_execution_job_request GoogleColabSchedule#create_notebook_execution_job_request}
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#cron GoogleColabSchedule#cron}
        :param display_name: Required. The display name of the Schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#display_name GoogleColabSchedule#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#location GoogleColabSchedule#location}
        :param max_concurrent_run_count: Maximum number of runs that can be started concurrently for this Schedule. This is the limit for starting the scheduled requests and not the execution of the notebook execution jobs created by the requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#max_concurrent_run_count GoogleColabSchedule#max_concurrent_run_count}
        :param allow_queueing: Whether new scheduled runs can be queued when max_concurrent_runs limit is reached. If set to true, new runs will be queued instead of skipped. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#allow_queueing GoogleColabSchedule#allow_queueing}
        :param desired_state: Desired state of the Colab Schedule. Set this field to 'ACTIVE' to start/resume the schedule, and 'PAUSED' to pause the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#desired_state GoogleColabSchedule#desired_state}
        :param end_time: Timestamp after which no new runs can be scheduled. If specified, the schedule will be completed when either end_time is reached or when scheduled_run_count >= max_run_count. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#end_time GoogleColabSchedule#end_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#id GoogleColabSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_run_count: Maximum run count of the schedule. If specified, The schedule will be completed when either startedRunCount >= maxRunCount or when endTime is reached. If not specified, new runs will keep getting scheduled until this Schedule is paused or deleted. Already scheduled runs will be allowed to complete. Unset if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#max_run_count GoogleColabSchedule#max_run_count}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#project GoogleColabSchedule#project}.
        :param start_time: The timestamp after which the first run can be scheduled. Defaults to the schedule creation time. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#start_time GoogleColabSchedule#start_time}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#timeouts GoogleColabSchedule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b29ca65a8ac43ac9526db59264718458b3a5f29f719d616f7cdd54379721e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleColabScheduleConfig(
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
        '''Generates CDKTF code for importing a GoogleColabSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleColabSchedule to import.
        :param import_from_id: The id of the existing GoogleColabSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleColabSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c6ec7cf409c6f5fc3f5d9fe2859f63cea861b8d82fd6e1a6e62fb0a38535ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCreateNotebookExecutionJobRequest")
    def put_create_notebook_execution_job_request(
        self,
        *,
        notebook_execution_job: typing.Union["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param notebook_execution_job: notebook_execution_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#notebook_execution_job GoogleColabSchedule#notebook_execution_job}
        '''
        value = GoogleColabScheduleCreateNotebookExecutionJobRequest(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#create GoogleColabSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#delete GoogleColabSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#update GoogleColabSchedule#update}.
        '''
        value = GoogleColabScheduleTimeouts(
            create=create, delete=delete, update=update
        )

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
    ) -> "GoogleColabScheduleCreateNotebookExecutionJobRequestOutputReference":
        return typing.cast("GoogleColabScheduleCreateNotebookExecutionJobRequestOutputReference", jsii.get(self, "createNotebookExecutionJobRequest"))

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
    def timeouts(self) -> "GoogleColabScheduleTimeoutsOutputReference":
        return typing.cast("GoogleColabScheduleTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleColabScheduleCreateNotebookExecutionJobRequest"]:
        return typing.cast(typing.Optional["GoogleColabScheduleCreateNotebookExecutionJobRequest"], jsii.get(self, "createNotebookExecutionJobRequestInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleColabScheduleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleColabScheduleTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1ba3fe8b216443dfef476ccfcee799f8dbe7ace0b2decc11ad5c8d75902ce55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowQueueing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cron")
    def cron(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cron"))

    @cron.setter
    def cron(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f672265cc35dc945fcb685d31371dc78172f585fb1da5ceb4ccc41b321ba608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98de71f3a35ce160bbd0a0b89bc7974994bdf918f0f084bb534da72117f6f47f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753af60a5cc3ab765d50dd0c8cd7c3e318a3d9d6370f4a4e807b0846186b034d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0395630199afd1da8d25d57317910e55c7cfef339b8f36ba51e786382a224228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5972ba6c199096749ed4cdb0878e8c7b96260246d9797e5e5b4e9cb217152414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6f60be24c76c08ce34f7b5dfd6b212829336ec3688bfc712b0de8869fac385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRunCount")
    def max_concurrent_run_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxConcurrentRunCount"))

    @max_concurrent_run_count.setter
    def max_concurrent_run_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27f5194f0f28c3488189c17b6bc587e86f36f9b56c55e9a6c7b29fd1543c66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRunCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRunCount")
    def max_run_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRunCount"))

    @max_run_count.setter
    def max_run_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3704c1d3209a679c2aba66568bf638fae30e5fb7dd7169cff4f6d295ef4ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRunCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57992e8ee696237552cda73b291a2ea86f7bee371b8bfb80dcf3a07d81660c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c559adcb32322ee837e85ceaa9ad3b2eff609a2ffa11f25591c4374f9e54b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleConfig",
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
class GoogleColabScheduleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        create_notebook_execution_job_request: typing.Union["GoogleColabScheduleCreateNotebookExecutionJobRequest", typing.Dict[builtins.str, typing.Any]],
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
        timeouts: typing.Optional[typing.Union["GoogleColabScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param create_notebook_execution_job_request: create_notebook_execution_job_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#create_notebook_execution_job_request GoogleColabSchedule#create_notebook_execution_job_request}
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#cron GoogleColabSchedule#cron}
        :param display_name: Required. The display name of the Schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#display_name GoogleColabSchedule#display_name}
        :param location: The location for the resource: https://cloud.google.com/colab/docs/locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#location GoogleColabSchedule#location}
        :param max_concurrent_run_count: Maximum number of runs that can be started concurrently for this Schedule. This is the limit for starting the scheduled requests and not the execution of the notebook execution jobs created by the requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#max_concurrent_run_count GoogleColabSchedule#max_concurrent_run_count}
        :param allow_queueing: Whether new scheduled runs can be queued when max_concurrent_runs limit is reached. If set to true, new runs will be queued instead of skipped. Default to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#allow_queueing GoogleColabSchedule#allow_queueing}
        :param desired_state: Desired state of the Colab Schedule. Set this field to 'ACTIVE' to start/resume the schedule, and 'PAUSED' to pause the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#desired_state GoogleColabSchedule#desired_state}
        :param end_time: Timestamp after which no new runs can be scheduled. If specified, the schedule will be completed when either end_time is reached or when scheduled_run_count >= max_run_count. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#end_time GoogleColabSchedule#end_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#id GoogleColabSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_run_count: Maximum run count of the schedule. If specified, The schedule will be completed when either startedRunCount >= maxRunCount or when endTime is reached. If not specified, new runs will keep getting scheduled until this Schedule is paused or deleted. Already scheduled runs will be allowed to complete. Unset if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#max_run_count GoogleColabSchedule#max_run_count}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#project GoogleColabSchedule#project}.
        :param start_time: The timestamp after which the first run can be scheduled. Defaults to the schedule creation time. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#start_time GoogleColabSchedule#start_time}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#timeouts GoogleColabSchedule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(create_notebook_execution_job_request, dict):
            create_notebook_execution_job_request = GoogleColabScheduleCreateNotebookExecutionJobRequest(**create_notebook_execution_job_request)
        if isinstance(timeouts, dict):
            timeouts = GoogleColabScheduleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e060f749490b23870d799d1dca7de77a801cc51acda7958cf97e05440138d3)
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
    ) -> "GoogleColabScheduleCreateNotebookExecutionJobRequest":
        '''create_notebook_execution_job_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#create_notebook_execution_job_request GoogleColabSchedule#create_notebook_execution_job_request}
        '''
        result = self._values.get("create_notebook_execution_job_request")
        assert result is not None, "Required property 'create_notebook_execution_job_request' is missing"
        return typing.cast("GoogleColabScheduleCreateNotebookExecutionJobRequest", result)

    @builtins.property
    def cron(self) -> builtins.str:
        '''Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#cron GoogleColabSchedule#cron}
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required. The display name of the Schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#display_name GoogleColabSchedule#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource: https://cloud.google.com/colab/docs/locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#location GoogleColabSchedule#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_concurrent_run_count(self) -> builtins.str:
        '''Maximum number of runs that can be started concurrently for this Schedule.

        This is the limit for starting the scheduled requests and not the execution of the notebook execution jobs created by the requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#max_concurrent_run_count GoogleColabSchedule#max_concurrent_run_count}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#allow_queueing GoogleColabSchedule#allow_queueing}
        '''
        result = self._values.get("allow_queueing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Desired state of the Colab Schedule.

        Set this field to 'ACTIVE' to start/resume the schedule, and 'PAUSED' to pause the schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#desired_state GoogleColabSchedule#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Timestamp after which no new runs can be scheduled.

        If specified, the schedule will be completed when either end_time is reached or when scheduled_run_count >= max_run_count. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#end_time GoogleColabSchedule#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#id GoogleColabSchedule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_run_count(self) -> typing.Optional[builtins.str]:
        '''Maximum run count of the schedule.

        If specified, The schedule will be completed when either startedRunCount >= maxRunCount or when endTime is reached. If not specified, new runs will keep getting scheduled until this Schedule is paused or deleted. Already scheduled runs will be allowed to complete. Unset if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#max_run_count GoogleColabSchedule#max_run_count}
        '''
        result = self._values.get("max_run_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#project GoogleColabSchedule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The timestamp after which the first run can be scheduled.

        Defaults to the schedule creation time. Must be in the RFC 3339 (https://www.ietf.org/rfc/rfc3339.txt) format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#start_time GoogleColabSchedule#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleColabScheduleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#timeouts GoogleColabSchedule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleColabScheduleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequest",
    jsii_struct_bases=[],
    name_mapping={"notebook_execution_job": "notebookExecutionJob"},
)
class GoogleColabScheduleCreateNotebookExecutionJobRequest:
    def __init__(
        self,
        *,
        notebook_execution_job: typing.Union["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param notebook_execution_job: notebook_execution_job block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#notebook_execution_job GoogleColabSchedule#notebook_execution_job}
        '''
        if isinstance(notebook_execution_job, dict):
            notebook_execution_job = GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob(**notebook_execution_job)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8d306f206e5e2010f0cf9566b2ef3cca891b9153c8c0a90a2ec682048df002)
            check_type(argname="argument notebook_execution_job", value=notebook_execution_job, expected_type=type_hints["notebook_execution_job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notebook_execution_job": notebook_execution_job,
        }

    @builtins.property
    def notebook_execution_job(
        self,
    ) -> "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob":
        '''notebook_execution_job block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#notebook_execution_job GoogleColabSchedule#notebook_execution_job}
        '''
        result = self._values.get("notebook_execution_job")
        assert result is not None, "Required property 'notebook_execution_job' is missing"
        return typing.cast("GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabScheduleCreateNotebookExecutionJobRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob",
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
class GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        gcs_output_uri: builtins.str,
        notebook_runtime_template_resource_name: builtins.str,
        dataform_repository_source: typing.Optional[typing.Union["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#display_name GoogleColabSchedule#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#gcs_output_uri GoogleColabSchedule#gcs_output_uri}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#notebook_runtime_template_resource_name GoogleColabSchedule#notebook_runtime_template_resource_name}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#dataform_repository_source GoogleColabSchedule#dataform_repository_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). A duration in seconds with up to nine fractional digits, ending with "s". Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#execution_timeout GoogleColabSchedule#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#execution_user GoogleColabSchedule#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#gcs_notebook_source GoogleColabSchedule#gcs_notebook_source}
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#service_account GoogleColabSchedule#service_account}
        '''
        if isinstance(dataform_repository_source, dict):
            dataform_repository_source = GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource(**dataform_repository_source)
        if isinstance(gcs_notebook_source, dict):
            gcs_notebook_source = GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource(**gcs_notebook_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077ad80b03b740a653ab03593067b62ef655d7f5319391ea29773ca9abb33085)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#display_name GoogleColabSchedule#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcs_output_uri(self) -> builtins.str:
        '''The Cloud Storage location to upload the result to. Format:'gs://bucket-name'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#gcs_output_uri GoogleColabSchedule#gcs_output_uri}
        '''
        result = self._values.get("gcs_output_uri")
        assert result is not None, "Required property 'gcs_output_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notebook_runtime_template_resource_name(self) -> builtins.str:
        '''The NotebookRuntimeTemplate to source compute configuration from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#notebook_runtime_template_resource_name GoogleColabSchedule#notebook_runtime_template_resource_name}
        '''
        result = self._values.get("notebook_runtime_template_resource_name")
        assert result is not None, "Required property 'notebook_runtime_template_resource_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataform_repository_source(
        self,
    ) -> typing.Optional["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource"]:
        '''dataform_repository_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#dataform_repository_source GoogleColabSchedule#dataform_repository_source}
        '''
        result = self._values.get("dataform_repository_source")
        return typing.cast(typing.Optional["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource"], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[builtins.str]:
        '''Max running time of the execution job in seconds (default 86400s / 24 hrs).

        A duration in seconds with up to nine fractional digits, ending with "s". Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#execution_timeout GoogleColabSchedule#execution_timeout}
        '''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_user(self) -> typing.Optional[builtins.str]:
        '''The user email to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#execution_user GoogleColabSchedule#execution_user}
        '''
        result = self._values.get("execution_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_notebook_source(
        self,
    ) -> typing.Optional["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource"]:
        '''gcs_notebook_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#gcs_notebook_source GoogleColabSchedule#gcs_notebook_source}
        '''
        result = self._values.get("gcs_notebook_source")
        return typing.cast(typing.Optional["GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account to run the execution as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#service_account GoogleColabSchedule#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource",
    jsii_struct_bases=[],
    name_mapping={
        "dataform_repository_resource_name": "dataformRepositoryResourceName",
        "commit_sha": "commitSha",
    },
)
class GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource:
    def __init__(
        self,
        *,
        dataform_repository_resource_name: builtins.str,
        commit_sha: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#dataform_repository_resource_name GoogleColabSchedule#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#commit_sha GoogleColabSchedule#commit_sha}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adcb1d261c3c376fe31a8aa5364b2442d8b82bb0e355fdb3f31f159cb68a0d8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#dataform_repository_resource_name GoogleColabSchedule#dataform_repository_resource_name}
        '''
        result = self._values.get("dataform_repository_resource_name")
        assert result is not None, "Required property 'dataform_repository_resource_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''The commit SHA to read repository with. If unset, the file will be read at HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#commit_sha GoogleColabSchedule#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25aab0192c7c92073c4ba7ca8f3a072059c75cafa4897cbc47eebb948c813648)
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
            type_hints = typing.get_type_hints(_typecheckingstub__938b4e9988c3b88473688a3014eeb6915cf796d4e65ec611f7bd76af9c707497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataformRepositoryResourceName")
    def dataform_repository_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataformRepositoryResourceName"))

    @dataform_repository_resource_name.setter
    def dataform_repository_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a631018f8bfc1fea2f4eacc7b5fc99837b555fb4155879ce0a69b46c68219ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataformRepositoryResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource]:
        return typing.cast(typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f97708461864f2544774d752d18020f35bcb578bafe24e0b00faf1cfdda888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "generation": "generation"},
)
class GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource:
    def __init__(
        self,
        *,
        uri: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Cloud Storage uri pointing to the ipynb file. Format: gs://bucket/notebook_file.ipynb. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#uri GoogleColabSchedule#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#generation GoogleColabSchedule#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b13bc6758442b4caee10bceecf40e68fd1ec9947c87d55cad76203b9d86dc8f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#uri GoogleColabSchedule#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''The version of the Cloud Storage object to read.

        If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#generation GoogleColabSchedule#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0da1dc5cc46fe2b2e42d4d3ebcaec0903464a5f3d80251c652dd84348cfdac45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b640abff9586557b8179d161d8c61b6eb31c1193aa6e0b53d5d04b9b97f0ac38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35236c2fe82e7c28f9e1df6cd97c3178511712fe2889d5a2976b3509135a3338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource]:
        return typing.cast(typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565c287c57af0123ca01cf00a22b9462df7bc606fb21f11aa634cf80708ac3ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa40b6311843d96cb32dbd39380c2d969f5d72c2a30a71eb37ae8f692f3c4bdd)
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
        :param dataform_repository_resource_name: The resource name of the Dataform Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#dataform_repository_resource_name GoogleColabSchedule#dataform_repository_resource_name}
        :param commit_sha: The commit SHA to read repository with. If unset, the file will be read at HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#commit_sha GoogleColabSchedule#commit_sha}
        '''
        value = GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource(
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
        :param uri: The Cloud Storage uri pointing to the ipynb file. Format: gs://bucket/notebook_file.ipynb. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#uri GoogleColabSchedule#uri}
        :param generation: The version of the Cloud Storage object to read. If unset, the current version of the object is read. See https://cloud.google.com/storage/docs/metadata#generation-number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#generation GoogleColabSchedule#generation}
        '''
        value = GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource(
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
    ) -> GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference:
        return typing.cast(GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference, jsii.get(self, "dataformRepositorySource"))

    @builtins.property
    @jsii.member(jsii_name="gcsNotebookSource")
    def gcs_notebook_source(
        self,
    ) -> GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference:
        return typing.cast(GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference, jsii.get(self, "gcsNotebookSource"))

    @builtins.property
    @jsii.member(jsii_name="dataformRepositorySourceInput")
    def dataform_repository_source_input(
        self,
    ) -> typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource]:
        return typing.cast(typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource], jsii.get(self, "dataformRepositorySourceInput"))

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
    ) -> typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource]:
        return typing.cast(typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource], jsii.get(self, "gcsNotebookSourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d6765120a621e5b75d5d6b06519e6c0b51476816af662939c813d33147a81658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9d2d3b2211a6a569606895b92b2cc44094ee5b6357534e4fda106ca1b02473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionUser")
    def execution_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionUser"))

    @execution_user.setter
    def execution_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003de3081f978e94b0cbe598431c643114d0aea21f8fb00b8d4aef69a38d90e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gcsOutputUri")
    def gcs_output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsOutputUri"))

    @gcs_output_uri.setter
    def gcs_output_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c47fc7dcd1cc77a9398503857e0b247f4d28488b588e1fbdd0b8028266f6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcsOutputUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebookRuntimeTemplateResourceName")
    def notebook_runtime_template_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookRuntimeTemplateResourceName"))

    @notebook_runtime_template_resource_name.setter
    def notebook_runtime_template_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1e472e241da9e3c845cd4294145c71ad2981c773f459d0838212b6bcc13386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookRuntimeTemplateResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978f87d3f3f20ace432db382a72e49821e02cd7cd732d145f9de61c87f26f5af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob]:
        return typing.cast(typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dcc60358de2761cecd6cb47c8d043b35ce6e1677a723afa008e3062edea158e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleColabScheduleCreateNotebookExecutionJobRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleCreateNotebookExecutionJobRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e5a9627061572c082bc51eba0ea27a763ddc5e93a128d55608847d95c1c4acf)
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
        dataform_repository_source: typing.Optional[typing.Union[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        execution_user: typing.Optional[builtins.str] = None,
        gcs_notebook_source: typing.Optional[typing.Union[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Required. The display name of the Notebook Execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#display_name GoogleColabSchedule#display_name}
        :param gcs_output_uri: The Cloud Storage location to upload the result to. Format:'gs://bucket-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#gcs_output_uri GoogleColabSchedule#gcs_output_uri}
        :param notebook_runtime_template_resource_name: The NotebookRuntimeTemplate to source compute configuration from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#notebook_runtime_template_resource_name GoogleColabSchedule#notebook_runtime_template_resource_name}
        :param dataform_repository_source: dataform_repository_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#dataform_repository_source GoogleColabSchedule#dataform_repository_source}
        :param execution_timeout: Max running time of the execution job in seconds (default 86400s / 24 hrs). A duration in seconds with up to nine fractional digits, ending with "s". Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#execution_timeout GoogleColabSchedule#execution_timeout}
        :param execution_user: The user email to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#execution_user GoogleColabSchedule#execution_user}
        :param gcs_notebook_source: gcs_notebook_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#gcs_notebook_source GoogleColabSchedule#gcs_notebook_source}
        :param service_account: The service account to run the execution as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#service_account GoogleColabSchedule#service_account}
        '''
        value = GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob(
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
    ) -> GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference:
        return typing.cast(GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference, jsii.get(self, "notebookExecutionJob"))

    @builtins.property
    @jsii.member(jsii_name="notebookExecutionJobInput")
    def notebook_execution_job_input(
        self,
    ) -> typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob]:
        return typing.cast(typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob], jsii.get(self, "notebookExecutionJobInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequest]:
        return typing.cast(typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b80808c75d7d152060d81e1ccafa2b5b23b2759efffc19a3ad8fab958d6680b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleColabScheduleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#create GoogleColabSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#delete GoogleColabSchedule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#update GoogleColabSchedule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abe342bd1d3fa4960b6aba6178ae069bf742bbf3a019adf6bde847507326c51)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#create GoogleColabSchedule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#delete GoogleColabSchedule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_colab_schedule#update GoogleColabSchedule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleColabScheduleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleColabScheduleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleColabSchedule.GoogleColabScheduleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d95a342e20da8acd0f33ede2d4ac5b03d247707dd7183598f13d026f2d8ae8d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a03e369d0b26d8464232c8217880ac7027d6c88a49009c629628815da32f77bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52cd466ccbd1d4b4172e529930e27f9196f31384f54c86f4f90124e7bfd6cab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dcbad6cf1f95759a8ace0b7d9c3a5aee0c22b6e097e9a3edf9ac41fd154b9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabScheduleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabScheduleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabScheduleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946664d62474a6afa522f80a8e53ab05ce1ca98fceb675907c395a2eb4b85bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleColabSchedule",
    "GoogleColabScheduleConfig",
    "GoogleColabScheduleCreateNotebookExecutionJobRequest",
    "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob",
    "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource",
    "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySourceOutputReference",
    "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource",
    "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSourceOutputReference",
    "GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobOutputReference",
    "GoogleColabScheduleCreateNotebookExecutionJobRequestOutputReference",
    "GoogleColabScheduleTimeouts",
    "GoogleColabScheduleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__93b29ca65a8ac43ac9526db59264718458b3a5f29f719d616f7cdd54379721e8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    create_notebook_execution_job_request: typing.Union[GoogleColabScheduleCreateNotebookExecutionJobRequest, typing.Dict[builtins.str, typing.Any]],
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
    timeouts: typing.Optional[typing.Union[GoogleColabScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__98c6ec7cf409c6f5fc3f5d9fe2859f63cea861b8d82fd6e1a6e62fb0a38535ac(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba3fe8b216443dfef476ccfcee799f8dbe7ace0b2decc11ad5c8d75902ce55b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f672265cc35dc945fcb685d31371dc78172f585fb1da5ceb4ccc41b321ba608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98de71f3a35ce160bbd0a0b89bc7974994bdf918f0f084bb534da72117f6f47f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753af60a5cc3ab765d50dd0c8cd7c3e318a3d9d6370f4a4e807b0846186b034d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0395630199afd1da8d25d57317910e55c7cfef339b8f36ba51e786382a224228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5972ba6c199096749ed4cdb0878e8c7b96260246d9797e5e5b4e9cb217152414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6f60be24c76c08ce34f7b5dfd6b212829336ec3688bfc712b0de8869fac385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27f5194f0f28c3488189c17b6bc587e86f36f9b56c55e9a6c7b29fd1543c66a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3704c1d3209a679c2aba66568bf638fae30e5fb7dd7169cff4f6d295ef4ceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57992e8ee696237552cda73b291a2ea86f7bee371b8bfb80dcf3a07d81660c49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c559adcb32322ee837e85ceaa9ad3b2eff609a2ffa11f25591c4374f9e54b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e060f749490b23870d799d1dca7de77a801cc51acda7958cf97e05440138d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    create_notebook_execution_job_request: typing.Union[GoogleColabScheduleCreateNotebookExecutionJobRequest, typing.Dict[builtins.str, typing.Any]],
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
    timeouts: typing.Optional[typing.Union[GoogleColabScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8d306f206e5e2010f0cf9566b2ef3cca891b9153c8c0a90a2ec682048df002(
    *,
    notebook_execution_job: typing.Union[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077ad80b03b740a653ab03593067b62ef655d7f5319391ea29773ca9abb33085(
    *,
    display_name: builtins.str,
    gcs_output_uri: builtins.str,
    notebook_runtime_template_resource_name: builtins.str,
    dataform_repository_source: typing.Optional[typing.Union[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
    execution_user: typing.Optional[builtins.str] = None,
    gcs_notebook_source: typing.Optional[typing.Union[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adcb1d261c3c376fe31a8aa5364b2442d8b82bb0e355fdb3f31f159cb68a0d8(
    *,
    dataform_repository_resource_name: builtins.str,
    commit_sha: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25aab0192c7c92073c4ba7ca8f3a072059c75cafa4897cbc47eebb948c813648(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938b4e9988c3b88473688a3014eeb6915cf796d4e65ec611f7bd76af9c707497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a631018f8bfc1fea2f4eacc7b5fc99837b555fb4155879ce0a69b46c68219ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f97708461864f2544774d752d18020f35bcb578bafe24e0b00faf1cfdda888(
    value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobDataformRepositorySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b13bc6758442b4caee10bceecf40e68fd1ec9947c87d55cad76203b9d86dc8f(
    *,
    uri: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da1dc5cc46fe2b2e42d4d3ebcaec0903464a5f3d80251c652dd84348cfdac45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b640abff9586557b8179d161d8c61b6eb31c1193aa6e0b53d5d04b9b97f0ac38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35236c2fe82e7c28f9e1df6cd97c3178511712fe2889d5a2976b3509135a3338(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565c287c57af0123ca01cf00a22b9462df7bc606fb21f11aa634cf80708ac3ce(
    value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJobGcsNotebookSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa40b6311843d96cb32dbd39380c2d969f5d72c2a30a71eb37ae8f692f3c4bdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6765120a621e5b75d5d6b06519e6c0b51476816af662939c813d33147a81658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9d2d3b2211a6a569606895b92b2cc44094ee5b6357534e4fda106ca1b02473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003de3081f978e94b0cbe598431c643114d0aea21f8fb00b8d4aef69a38d90e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c47fc7dcd1cc77a9398503857e0b247f4d28488b588e1fbdd0b8028266f6f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1e472e241da9e3c845cd4294145c71ad2981c773f459d0838212b6bcc13386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978f87d3f3f20ace432db382a72e49821e02cd7cd732d145f9de61c87f26f5af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcc60358de2761cecd6cb47c8d043b35ce6e1677a723afa008e3062edea158e(
    value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequestNotebookExecutionJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5a9627061572c082bc51eba0ea27a763ddc5e93a128d55608847d95c1c4acf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b80808c75d7d152060d81e1ccafa2b5b23b2759efffc19a3ad8fab958d6680b(
    value: typing.Optional[GoogleColabScheduleCreateNotebookExecutionJobRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abe342bd1d3fa4960b6aba6178ae069bf742bbf3a019adf6bde847507326c51(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95a342e20da8acd0f33ede2d4ac5b03d247707dd7183598f13d026f2d8ae8d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03e369d0b26d8464232c8217880ac7027d6c88a49009c629628815da32f77bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52cd466ccbd1d4b4172e529930e27f9196f31384f54c86f4f90124e7bfd6cab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcbad6cf1f95759a8ace0b7d9c3a5aee0c22b6e097e9a3edf9ac41fd154b9ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946664d62474a6afa522f80a8e53ab05ce1ca98fceb675907c395a2eb4b85bbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleColabScheduleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
