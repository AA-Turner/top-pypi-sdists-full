r'''
# `google_cloud_scheduler_job`

Refer to the Terraform Registry for docs: [`google_cloud_scheduler_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job).
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


class GoogleCloudSchedulerJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job google_cloud_scheduler_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        app_engine_http_target: typing.Optional[typing.Union["GoogleCloudSchedulerJobAppEngineHttpTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        attempt_deadline: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_target: typing.Optional[typing.Union["GoogleCloudSchedulerJobHttpTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        pubsub_target: typing.Optional[typing.Union["GoogleCloudSchedulerJobPubsubTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        retry_config: typing.Optional[typing.Union["GoogleCloudSchedulerJobRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudSchedulerJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job google_cloud_scheduler_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#name GoogleCloudSchedulerJob#name}
        :param app_engine_http_target: app_engine_http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#app_engine_http_target GoogleCloudSchedulerJob#app_engine_http_target}
        :param attempt_deadline: The deadline for job attempts. If the request handler does not respond by this deadline then the request is cancelled and the attempt is marked as a DEADLINE_EXCEEDED failure. The failed attempt can be viewed in execution logs. Cloud Scheduler will retry the job according to the RetryConfig. The allowed duration for this deadline is: - For HTTP targets, between 15 seconds and 30 minutes. - For App Engine HTTP targets, between 15 seconds and 24 hours. - **Note**: For PubSub targets, this field is ignored - setting it will introduce an unresolvable diff. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#attempt_deadline GoogleCloudSchedulerJob#attempt_deadline}
        :param description: A human-readable description for the job. This string must not contain more than 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#description GoogleCloudSchedulerJob#description}
        :param http_target: http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_target GoogleCloudSchedulerJob#http_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#id GoogleCloudSchedulerJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param paused: Sets the job to a paused state. Jobs default to being enabled when this property is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#paused GoogleCloudSchedulerJob#paused}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#project GoogleCloudSchedulerJob#project}.
        :param pubsub_target: pubsub_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#pubsub_target GoogleCloudSchedulerJob#pubsub_target}
        :param region: Region where the scheduler job resides. If it is not provided, Terraform will use the provider default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#region GoogleCloudSchedulerJob#region}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#retry_config GoogleCloudSchedulerJob#retry_config}
        :param schedule: Describes the schedule on which the job will be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#schedule GoogleCloudSchedulerJob#schedule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#timeouts GoogleCloudSchedulerJob#timeouts}
        :param time_zone: Specifies the time zone to be used in interpreting schedule. The value of this field must be a time zone name from the tz database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#time_zone GoogleCloudSchedulerJob#time_zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17a957b9dd1c197be1d710cb7cc4c543bc06f14ce05aa58e69094d83f9d8759)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudSchedulerJobConfig(
            name=name,
            app_engine_http_target=app_engine_http_target,
            attempt_deadline=attempt_deadline,
            description=description,
            http_target=http_target,
            id=id,
            paused=paused,
            project=project,
            pubsub_target=pubsub_target,
            region=region,
            retry_config=retry_config,
            schedule=schedule,
            timeouts=timeouts,
            time_zone=time_zone,
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
        '''Generates CDKTF code for importing a GoogleCloudSchedulerJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudSchedulerJob to import.
        :param import_from_id: The id of the existing GoogleCloudSchedulerJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudSchedulerJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4705824e932bf6b787b51b284124e24d79f89a9bb1ed00ce01e91fbdf7cdb7e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAppEngineHttpTarget")
    def put_app_engine_http_target(
        self,
        *,
        relative_uri: builtins.str,
        app_engine_routing: typing.Optional[typing.Union["GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relative_uri: The relative URI. The relative URL must begin with "/" and must be a valid HTTP relative URL. It can contain a path, query string arguments, and # fragments. If the relative URL is empty, then the root path "/" will be used. No spaces are allowed, and the maximum length allowed is 2083 characters Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#relative_uri GoogleCloudSchedulerJob#relative_uri}
        :param app_engine_routing: app_engine_routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#app_engine_routing GoogleCloudSchedulerJob#app_engine_routing}
        :param body: HTTP request body. A request body is allowed only if the HTTP method is POST or PUT. It will result in invalid argument error to set a body on a job with an incompatible HttpMethod. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#body GoogleCloudSchedulerJob#body}
        :param headers: HTTP request headers. This map contains the header field names and values. Headers can be set when the job is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#headers GoogleCloudSchedulerJob#headers}
        :param http_method: Which HTTP method to use for the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_method GoogleCloudSchedulerJob#http_method}
        '''
        value = GoogleCloudSchedulerJobAppEngineHttpTarget(
            relative_uri=relative_uri,
            app_engine_routing=app_engine_routing,
            body=body,
            headers=headers,
            http_method=http_method,
        )

        return typing.cast(None, jsii.invoke(self, "putAppEngineHttpTarget", [value]))

    @jsii.member(jsii_name="putHttpTarget")
    def put_http_target(
        self,
        *,
        uri: builtins.str,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[typing.Union["GoogleCloudSchedulerJobHttpTargetOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GoogleCloudSchedulerJobHttpTargetOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param uri: The full URI path that the request will be sent to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#uri GoogleCloudSchedulerJob#uri}
        :param body: HTTP request body. A request body is allowed only if the HTTP method is POST, PUT, or PATCH. It is an error to set body on a job with an incompatible HttpMethod. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#body GoogleCloudSchedulerJob#body}
        :param headers: This map contains the header field names and values. Repeated headers are not supported, but a header value can contain commas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#headers GoogleCloudSchedulerJob#headers}
        :param http_method: Which HTTP method to use for the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_method GoogleCloudSchedulerJob#http_method}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#oauth_token GoogleCloudSchedulerJob#oauth_token}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#oidc_token GoogleCloudSchedulerJob#oidc_token}
        '''
        value = GoogleCloudSchedulerJobHttpTarget(
            uri=uri,
            body=body,
            headers=headers,
            http_method=http_method,
            oauth_token=oauth_token,
            oidc_token=oidc_token,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpTarget", [value]))

    @jsii.member(jsii_name="putPubsubTarget")
    def put_pubsub_target(
        self,
        *,
        topic_name: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic_name: The full resource name for the Cloud Pub/Sub topic to which messages will be published when a job is delivered. ~>**NOTE:** The topic name must be in the same format as required by PubSub's PublishRequest.name, e.g. 'projects/my-project/topics/my-topic'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#topic_name GoogleCloudSchedulerJob#topic_name}
        :param attributes: Attributes for PubsubMessage. Pubsub message must contain either non-empty data, or at least one attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#attributes GoogleCloudSchedulerJob#attributes}
        :param data: The message payload for PubsubMessage. Pubsub message must contain either non-empty data, or at least one attribute. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#data GoogleCloudSchedulerJob#data}
        '''
        value = GoogleCloudSchedulerJobPubsubTarget(
            topic_name=topic_name, attributes=attributes, data=data
        )

        return typing.cast(None, jsii.invoke(self, "putPubsubTarget", [value]))

    @jsii.member(jsii_name="putRetryConfig")
    def put_retry_config(
        self,
        *,
        max_backoff_duration: typing.Optional[builtins.str] = None,
        max_doublings: typing.Optional[jsii.Number] = None,
        max_retry_duration: typing.Optional[builtins.str] = None,
        min_backoff_duration: typing.Optional[builtins.str] = None,
        retry_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_backoff_duration: The maximum amount of time to wait before retrying a job after it fails. A duration in seconds with up to nine fractional digits, terminated by 's'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_backoff_duration GoogleCloudSchedulerJob#max_backoff_duration}
        :param max_doublings: The time between retries will double maxDoublings times. A job's retry interval starts at minBackoffDuration, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoffDuration up to retryCount times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_doublings GoogleCloudSchedulerJob#max_doublings}
        :param max_retry_duration: The time limit for retrying a failed job, measured from time when an execution was first attempted. If specified with retryCount, the job will be retried until both limits are reached. A duration in seconds with up to nine fractional digits, terminated by 's'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_retry_duration GoogleCloudSchedulerJob#max_retry_duration}
        :param min_backoff_duration: The minimum amount of time to wait before retrying a job after it fails. A duration in seconds with up to nine fractional digits, terminated by 's'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#min_backoff_duration GoogleCloudSchedulerJob#min_backoff_duration}
        :param retry_count: The number of attempts that the system will make to run a job using the exponential backoff procedure described by maxDoublings. Values greater than 5 and negative values are not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#retry_count GoogleCloudSchedulerJob#retry_count}
        '''
        value = GoogleCloudSchedulerJobRetryConfig(
            max_backoff_duration=max_backoff_duration,
            max_doublings=max_doublings,
            max_retry_duration=max_retry_duration,
            min_backoff_duration=min_backoff_duration,
            retry_count=retry_count,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#create GoogleCloudSchedulerJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#delete GoogleCloudSchedulerJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#update GoogleCloudSchedulerJob#update}.
        '''
        value = GoogleCloudSchedulerJobTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAppEngineHttpTarget")
    def reset_app_engine_http_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineHttpTarget", []))

    @jsii.member(jsii_name="resetAttemptDeadline")
    def reset_attempt_deadline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttemptDeadline", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHttpTarget")
    def reset_http_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpTarget", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPaused")
    def reset_paused(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaused", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPubsubTarget")
    def reset_pubsub_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubTarget", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRetryConfig")
    def reset_retry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryConfig", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

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
    @jsii.member(jsii_name="appEngineHttpTarget")
    def app_engine_http_target(
        self,
    ) -> "GoogleCloudSchedulerJobAppEngineHttpTargetOutputReference":
        return typing.cast("GoogleCloudSchedulerJobAppEngineHttpTargetOutputReference", jsii.get(self, "appEngineHttpTarget"))

    @builtins.property
    @jsii.member(jsii_name="httpTarget")
    def http_target(self) -> "GoogleCloudSchedulerJobHttpTargetOutputReference":
        return typing.cast("GoogleCloudSchedulerJobHttpTargetOutputReference", jsii.get(self, "httpTarget"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTarget")
    def pubsub_target(self) -> "GoogleCloudSchedulerJobPubsubTargetOutputReference":
        return typing.cast("GoogleCloudSchedulerJobPubsubTargetOutputReference", jsii.get(self, "pubsubTarget"))

    @builtins.property
    @jsii.member(jsii_name="retryConfig")
    def retry_config(self) -> "GoogleCloudSchedulerJobRetryConfigOutputReference":
        return typing.cast("GoogleCloudSchedulerJobRetryConfigOutputReference", jsii.get(self, "retryConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudSchedulerJobTimeoutsOutputReference":
        return typing.cast("GoogleCloudSchedulerJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appEngineHttpTargetInput")
    def app_engine_http_target_input(
        self,
    ) -> typing.Optional["GoogleCloudSchedulerJobAppEngineHttpTarget"]:
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobAppEngineHttpTarget"], jsii.get(self, "appEngineHttpTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="attemptDeadlineInput")
    def attempt_deadline_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attemptDeadlineInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpTargetInput")
    def http_target_input(self) -> typing.Optional["GoogleCloudSchedulerJobHttpTarget"]:
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobHttpTarget"], jsii.get(self, "httpTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pausedInput")
    def paused_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pausedInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTargetInput")
    def pubsub_target_input(
        self,
    ) -> typing.Optional["GoogleCloudSchedulerJobPubsubTarget"]:
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobPubsubTarget"], jsii.get(self, "pubsubTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="retryConfigInput")
    def retry_config_input(
        self,
    ) -> typing.Optional["GoogleCloudSchedulerJobRetryConfig"]:
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobRetryConfig"], jsii.get(self, "retryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudSchedulerJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudSchedulerJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="attemptDeadline")
    def attempt_deadline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attemptDeadline"))

    @attempt_deadline.setter
    def attempt_deadline(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10d53a014154fb726bd06e390549f787142b8a8977c9a50b598de72389d712d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attemptDeadline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0085163a8613701724463fc58fdae636f07ca0f45d867656fdc03e8d1e3d1ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465d3778d880cb77b81f8cc99ab6ce37d6d63f3c7d42dff6e7c663cdadd982bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6885d09538aacff710b7ce085c9ad2ee9b02b0bcf4939a1e163eb91a472be9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paused")
    def paused(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "paused"))

    @paused.setter
    def paused(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db8cdf1291d838f628e0ce8643501c9d6a563d63f327af056aa542bfe310dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paused", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bb7e8a3fd65471cce24d00545245c4218d4129ff4b00cc0ef2443fdbecf11f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a2e585907a939b8e6af6fa5ccded3cd9159b8048f1e41e3457645824151f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3863c55c7189c41d49e37cc08bedaae0b0c66517c465b89155bc0bc4feeaa771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73cfc1f22184fe3263a2912668a13b899d2b8a7c29cdfc8f3fb84a770fbf1268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobAppEngineHttpTarget",
    jsii_struct_bases=[],
    name_mapping={
        "relative_uri": "relativeUri",
        "app_engine_routing": "appEngineRouting",
        "body": "body",
        "headers": "headers",
        "http_method": "httpMethod",
    },
)
class GoogleCloudSchedulerJobAppEngineHttpTarget:
    def __init__(
        self,
        *,
        relative_uri: builtins.str,
        app_engine_routing: typing.Optional[typing.Union["GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relative_uri: The relative URI. The relative URL must begin with "/" and must be a valid HTTP relative URL. It can contain a path, query string arguments, and # fragments. If the relative URL is empty, then the root path "/" will be used. No spaces are allowed, and the maximum length allowed is 2083 characters Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#relative_uri GoogleCloudSchedulerJob#relative_uri}
        :param app_engine_routing: app_engine_routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#app_engine_routing GoogleCloudSchedulerJob#app_engine_routing}
        :param body: HTTP request body. A request body is allowed only if the HTTP method is POST or PUT. It will result in invalid argument error to set a body on a job with an incompatible HttpMethod. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#body GoogleCloudSchedulerJob#body}
        :param headers: HTTP request headers. This map contains the header field names and values. Headers can be set when the job is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#headers GoogleCloudSchedulerJob#headers}
        :param http_method: Which HTTP method to use for the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_method GoogleCloudSchedulerJob#http_method}
        '''
        if isinstance(app_engine_routing, dict):
            app_engine_routing = GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting(**app_engine_routing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194423cd9f1337b57928f1ce452e06c02fa2a5ac7c00c4e963e4a5c7b9497aec)
            check_type(argname="argument relative_uri", value=relative_uri, expected_type=type_hints["relative_uri"])
            check_type(argname="argument app_engine_routing", value=app_engine_routing, expected_type=type_hints["app_engine_routing"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "relative_uri": relative_uri,
        }
        if app_engine_routing is not None:
            self._values["app_engine_routing"] = app_engine_routing
        if body is not None:
            self._values["body"] = body
        if headers is not None:
            self._values["headers"] = headers
        if http_method is not None:
            self._values["http_method"] = http_method

    @builtins.property
    def relative_uri(self) -> builtins.str:
        '''The relative URI.

        The relative URL must begin with "/" and must be a valid HTTP relative URL.
        It can contain a path, query string arguments, and # fragments.
        If the relative URL is empty, then the root path "/" will be used.
        No spaces are allowed, and the maximum length allowed is 2083 characters

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#relative_uri GoogleCloudSchedulerJob#relative_uri}
        '''
        result = self._values.get("relative_uri")
        assert result is not None, "Required property 'relative_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_routing(
        self,
    ) -> typing.Optional["GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting"]:
        '''app_engine_routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#app_engine_routing GoogleCloudSchedulerJob#app_engine_routing}
        '''
        result = self._values.get("app_engine_routing")
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting"], result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''HTTP request body.

        A request body is allowed only if the HTTP method is POST or PUT.
        It will result in invalid argument error to set a body on a job with an incompatible HttpMethod.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#body GoogleCloudSchedulerJob#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP request headers. This map contains the header field names and values. Headers can be set when the job is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#headers GoogleCloudSchedulerJob#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''Which HTTP method to use for the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_method GoogleCloudSchedulerJob#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobAppEngineHttpTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance", "service": "service", "version": "version"},
)
class GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting:
    def __init__(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: App instance. By default, the job is sent to an instance which is available when the job is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#instance GoogleCloudSchedulerJob#instance}
        :param service: App service. By default, the job is sent to the service which is the default service when the job is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service GoogleCloudSchedulerJob#service}
        :param version: App version. By default, the job is sent to the version which is the default version when the job is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#version GoogleCloudSchedulerJob#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eaa2af7827c32cb3b2d79e5c59b44c6d9fc0a7bff5aa478ae07139d7158b6c1)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance
        if service is not None:
            self._values["service"] = service
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''App instance. By default, the job is sent to an instance which is available when the job is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#instance GoogleCloudSchedulerJob#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''App service.

        By default, the job is sent to the service which is the default service when the job is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service GoogleCloudSchedulerJob#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''App version.

        By default, the job is sent to the version which is the default version when the job is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#version GoogleCloudSchedulerJob#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f7e6d5ff7d66c9cffa60c2c31a1a814689aae2ef7209d3bc571347fd366cfe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79f8a2db8796b6bba9e0e7fe7f2a66711954933d1d264f6ffe6fb439b244fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7883790cf8a84cbd9eed7267dc572ae1a00c5980533eee6da6c71340e32c5fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de41c26ba0e1953cee7aad273b20e4af11dfa5b416a2ccfd5b3b9c4289e72339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de1043454b88ec62c68f8101f4d026f9d81c6f78c9b68cfa88e6518c7ae4e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudSchedulerJobAppEngineHttpTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobAppEngineHttpTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3f817a46071cf26725604ec92e235472cf3e798421d41bb2941f1f3b821ac75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAppEngineRouting")
    def put_app_engine_routing(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: App instance. By default, the job is sent to an instance which is available when the job is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#instance GoogleCloudSchedulerJob#instance}
        :param service: App service. By default, the job is sent to the service which is the default service when the job is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service GoogleCloudSchedulerJob#service}
        :param version: App version. By default, the job is sent to the version which is the default version when the job is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#version GoogleCloudSchedulerJob#version}
        '''
        value = GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting(
            instance=instance, service=service, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putAppEngineRouting", [value]))

    @jsii.member(jsii_name="resetAppEngineRouting")
    def reset_app_engine_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineRouting", []))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @builtins.property
    @jsii.member(jsii_name="appEngineRouting")
    def app_engine_routing(
        self,
    ) -> GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRoutingOutputReference:
        return typing.cast(GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRoutingOutputReference, jsii.get(self, "appEngineRouting"))

    @builtins.property
    @jsii.member(jsii_name="appEngineRoutingInput")
    def app_engine_routing_input(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting], jsii.get(self, "appEngineRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeUriInput")
    def relative_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativeUriInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37daabcf45ddbd27a082fdfa0b0c22905e1c986e1deaae90b7faab4029d5117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3682f884782e9f37182cef2d749bba8f4b1645be64e24ec9d9dfa6e6838104b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f60d85d34494c7542240ae08de1499e15df461a88a8da42a18c769895e9d4fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeUri")
    def relative_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativeUri"))

    @relative_uri.setter
    def relative_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b6a686eaa56174dd2692261190780a79f3708bd6a45a35053c87444ba62ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTarget]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44587c798f993c30559bb1a126eb04d2998e2e774910217048a37f1f049722aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobConfig",
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
        "app_engine_http_target": "appEngineHttpTarget",
        "attempt_deadline": "attemptDeadline",
        "description": "description",
        "http_target": "httpTarget",
        "id": "id",
        "paused": "paused",
        "project": "project",
        "pubsub_target": "pubsubTarget",
        "region": "region",
        "retry_config": "retryConfig",
        "schedule": "schedule",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
    },
)
class GoogleCloudSchedulerJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_engine_http_target: typing.Optional[typing.Union[GoogleCloudSchedulerJobAppEngineHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
        attempt_deadline: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_target: typing.Optional[typing.Union["GoogleCloudSchedulerJobHttpTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        pubsub_target: typing.Optional[typing.Union["GoogleCloudSchedulerJobPubsubTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        retry_config: typing.Optional[typing.Union["GoogleCloudSchedulerJobRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudSchedulerJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#name GoogleCloudSchedulerJob#name}
        :param app_engine_http_target: app_engine_http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#app_engine_http_target GoogleCloudSchedulerJob#app_engine_http_target}
        :param attempt_deadline: The deadline for job attempts. If the request handler does not respond by this deadline then the request is cancelled and the attempt is marked as a DEADLINE_EXCEEDED failure. The failed attempt can be viewed in execution logs. Cloud Scheduler will retry the job according to the RetryConfig. The allowed duration for this deadline is: - For HTTP targets, between 15 seconds and 30 minutes. - For App Engine HTTP targets, between 15 seconds and 24 hours. - **Note**: For PubSub targets, this field is ignored - setting it will introduce an unresolvable diff. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#attempt_deadline GoogleCloudSchedulerJob#attempt_deadline}
        :param description: A human-readable description for the job. This string must not contain more than 500 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#description GoogleCloudSchedulerJob#description}
        :param http_target: http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_target GoogleCloudSchedulerJob#http_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#id GoogleCloudSchedulerJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param paused: Sets the job to a paused state. Jobs default to being enabled when this property is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#paused GoogleCloudSchedulerJob#paused}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#project GoogleCloudSchedulerJob#project}.
        :param pubsub_target: pubsub_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#pubsub_target GoogleCloudSchedulerJob#pubsub_target}
        :param region: Region where the scheduler job resides. If it is not provided, Terraform will use the provider default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#region GoogleCloudSchedulerJob#region}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#retry_config GoogleCloudSchedulerJob#retry_config}
        :param schedule: Describes the schedule on which the job will be executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#schedule GoogleCloudSchedulerJob#schedule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#timeouts GoogleCloudSchedulerJob#timeouts}
        :param time_zone: Specifies the time zone to be used in interpreting schedule. The value of this field must be a time zone name from the tz database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#time_zone GoogleCloudSchedulerJob#time_zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(app_engine_http_target, dict):
            app_engine_http_target = GoogleCloudSchedulerJobAppEngineHttpTarget(**app_engine_http_target)
        if isinstance(http_target, dict):
            http_target = GoogleCloudSchedulerJobHttpTarget(**http_target)
        if isinstance(pubsub_target, dict):
            pubsub_target = GoogleCloudSchedulerJobPubsubTarget(**pubsub_target)
        if isinstance(retry_config, dict):
            retry_config = GoogleCloudSchedulerJobRetryConfig(**retry_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudSchedulerJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c254f30c458b15c62b56aacfdabf6e6c3fb873d28c556df3eb8a63fe7115d11)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument app_engine_http_target", value=app_engine_http_target, expected_type=type_hints["app_engine_http_target"])
            check_type(argname="argument attempt_deadline", value=attempt_deadline, expected_type=type_hints["attempt_deadline"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument http_target", value=http_target, expected_type=type_hints["http_target"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument paused", value=paused, expected_type=type_hints["paused"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument pubsub_target", value=pubsub_target, expected_type=type_hints["pubsub_target"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument retry_config", value=retry_config, expected_type=type_hints["retry_config"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if app_engine_http_target is not None:
            self._values["app_engine_http_target"] = app_engine_http_target
        if attempt_deadline is not None:
            self._values["attempt_deadline"] = attempt_deadline
        if description is not None:
            self._values["description"] = description
        if http_target is not None:
            self._values["http_target"] = http_target
        if id is not None:
            self._values["id"] = id
        if paused is not None:
            self._values["paused"] = paused
        if project is not None:
            self._values["project"] = project
        if pubsub_target is not None:
            self._values["pubsub_target"] = pubsub_target
        if region is not None:
            self._values["region"] = region
        if retry_config is not None:
            self._values["retry_config"] = retry_config
        if schedule is not None:
            self._values["schedule"] = schedule
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone

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
        '''The name of the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#name GoogleCloudSchedulerJob#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_http_target(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTarget]:
        '''app_engine_http_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#app_engine_http_target GoogleCloudSchedulerJob#app_engine_http_target}
        '''
        result = self._values.get("app_engine_http_target")
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTarget], result)

    @builtins.property
    def attempt_deadline(self) -> typing.Optional[builtins.str]:
        '''The deadline for job attempts.

        If the request handler does not respond by this deadline then the request is
        cancelled and the attempt is marked as a DEADLINE_EXCEEDED failure. The failed attempt can be viewed in
        execution logs. Cloud Scheduler will retry the job according to the RetryConfig.
        The allowed duration for this deadline is:

        - For HTTP targets, between 15 seconds and 30 minutes.
        - For App Engine HTTP targets, between 15 seconds and 24 hours.
        - **Note**: For PubSub targets, this field is ignored - setting it will introduce an unresolvable diff.
          A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#attempt_deadline GoogleCloudSchedulerJob#attempt_deadline}
        '''
        result = self._values.get("attempt_deadline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description for the job. This string must not contain more than 500 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#description GoogleCloudSchedulerJob#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_target(self) -> typing.Optional["GoogleCloudSchedulerJobHttpTarget"]:
        '''http_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_target GoogleCloudSchedulerJob#http_target}
        '''
        result = self._values.get("http_target")
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobHttpTarget"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#id GoogleCloudSchedulerJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Sets the job to a paused state. Jobs default to being enabled when this property is not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#paused GoogleCloudSchedulerJob#paused}
        '''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#project GoogleCloudSchedulerJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_target(self) -> typing.Optional["GoogleCloudSchedulerJobPubsubTarget"]:
        '''pubsub_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#pubsub_target GoogleCloudSchedulerJob#pubsub_target}
        '''
        result = self._values.get("pubsub_target")
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobPubsubTarget"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the scheduler job resides. If it is not provided, Terraform will use the provider default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#region GoogleCloudSchedulerJob#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_config(self) -> typing.Optional["GoogleCloudSchedulerJobRetryConfig"]:
        '''retry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#retry_config GoogleCloudSchedulerJob#retry_config}
        '''
        result = self._values.get("retry_config")
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobRetryConfig"], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Describes the schedule on which the job will be executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#schedule GoogleCloudSchedulerJob#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudSchedulerJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#timeouts GoogleCloudSchedulerJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone to be used in interpreting schedule.

        The value of this field must be a time zone name from the tz database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#time_zone GoogleCloudSchedulerJob#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobHttpTarget",
    jsii_struct_bases=[],
    name_mapping={
        "uri": "uri",
        "body": "body",
        "headers": "headers",
        "http_method": "httpMethod",
        "oauth_token": "oauthToken",
        "oidc_token": "oidcToken",
    },
)
class GoogleCloudSchedulerJobHttpTarget:
    def __init__(
        self,
        *,
        uri: builtins.str,
        body: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[typing.Union["GoogleCloudSchedulerJobHttpTargetOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GoogleCloudSchedulerJobHttpTargetOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param uri: The full URI path that the request will be sent to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#uri GoogleCloudSchedulerJob#uri}
        :param body: HTTP request body. A request body is allowed only if the HTTP method is POST, PUT, or PATCH. It is an error to set body on a job with an incompatible HttpMethod. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#body GoogleCloudSchedulerJob#body}
        :param headers: This map contains the header field names and values. Repeated headers are not supported, but a header value can contain commas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#headers GoogleCloudSchedulerJob#headers}
        :param http_method: Which HTTP method to use for the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_method GoogleCloudSchedulerJob#http_method}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#oauth_token GoogleCloudSchedulerJob#oauth_token}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#oidc_token GoogleCloudSchedulerJob#oidc_token}
        '''
        if isinstance(oauth_token, dict):
            oauth_token = GoogleCloudSchedulerJobHttpTargetOauthToken(**oauth_token)
        if isinstance(oidc_token, dict):
            oidc_token = GoogleCloudSchedulerJobHttpTargetOidcToken(**oidc_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac44289c94fc80538c31a151425b2c21e29329e4db72fad3b9e4d49f13976f2)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument oidc_token", value=oidc_token, expected_type=type_hints["oidc_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if body is not None:
            self._values["body"] = body
        if headers is not None:
            self._values["headers"] = headers
        if http_method is not None:
            self._values["http_method"] = http_method
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token
        if oidc_token is not None:
            self._values["oidc_token"] = oidc_token

    @builtins.property
    def uri(self) -> builtins.str:
        '''The full URI path that the request will be sent to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#uri GoogleCloudSchedulerJob#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''HTTP request body.

        A request body is allowed only if the HTTP method is POST, PUT, or PATCH.
        It is an error to set body on a job with an incompatible HttpMethod.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#body GoogleCloudSchedulerJob#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''This map contains the header field names and values.

        Repeated headers are not supported, but a header value can contain commas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#headers GoogleCloudSchedulerJob#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''Which HTTP method to use for the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#http_method GoogleCloudSchedulerJob#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(
        self,
    ) -> typing.Optional["GoogleCloudSchedulerJobHttpTargetOauthToken"]:
        '''oauth_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#oauth_token GoogleCloudSchedulerJob#oauth_token}
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobHttpTargetOauthToken"], result)

    @builtins.property
    def oidc_token(
        self,
    ) -> typing.Optional["GoogleCloudSchedulerJobHttpTargetOidcToken"]:
        '''oidc_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#oidc_token GoogleCloudSchedulerJob#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional["GoogleCloudSchedulerJobHttpTargetOidcToken"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobHttpTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobHttpTargetOauthToken",
    jsii_struct_bases=[],
    name_mapping={"service_account_email": "serviceAccountEmail", "scope": "scope"},
)
class GoogleCloudSchedulerJobHttpTargetOauthToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service_account_email GoogleCloudSchedulerJob#service_account_email}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#scope GoogleCloudSchedulerJob#scope}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238a15636e18836bb7f10642d2c2d36bf750e09cf962f3d448fc91973b460dec)
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_email": service_account_email,
        }
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''Service account email to be used for generating OAuth token.

        The service account must be within the same project as the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service_account_email GoogleCloudSchedulerJob#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#scope GoogleCloudSchedulerJob#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobHttpTargetOauthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudSchedulerJobHttpTargetOauthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobHttpTargetOauthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20fb89224f6fc3a1071048ea64fa36eb773f3ead4b3108aa9d09eb07a85cfb2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc640c7f789477458da57a524b4e93958e748a65b40a8f15ba7dee916d31491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51028bc0baee1849518a830ce5f9126df54fa5f4395bd570f90b0e15b3e610bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobHttpTargetOauthToken]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobHttpTargetOauthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudSchedulerJobHttpTargetOauthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812d1458b82987f8fb0179f034a0558dec3418a575889038adf592cfd0fe80f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobHttpTargetOidcToken",
    jsii_struct_bases=[],
    name_mapping={
        "service_account_email": "serviceAccountEmail",
        "audience": "audience",
    },
)
class GoogleCloudSchedulerJobHttpTargetOidcToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service_account_email GoogleCloudSchedulerJob#service_account_email}
        :param audience: Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#audience GoogleCloudSchedulerJob#audience}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d4603c810b5e9ec190bf1f5d05de26307011980337897c007a3a800c2721d3)
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_email": service_account_email,
        }
        if audience is not None:
            self._values["audience"] = audience

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''Service account email to be used for generating OAuth token.

        The service account must be within the same project as the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service_account_email GoogleCloudSchedulerJob#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#audience GoogleCloudSchedulerJob#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobHttpTargetOidcToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudSchedulerJobHttpTargetOidcTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobHttpTargetOidcTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cff4b44c468a424f531b826b1598860edebd00671dd519e0f9a3153760516f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0020e3f00adc54e37fa6955a3c81ede65e5322d823eee4de41749f3e368da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c709bdeafd1e5ccd4b8d60b44c39012d152a7841e6f5e03391224f81ab1f607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobHttpTargetOidcToken]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobHttpTargetOidcToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudSchedulerJobHttpTargetOidcToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a526a352eab426bb5d6663d057c5447690a545d6da6dde0ce6b3906517ec89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudSchedulerJobHttpTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobHttpTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__194a34e9a42c2fec631b1a9e0c6cb08b8efe535c688f2ab8d8f9cc9b77f4237b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthToken")
    def put_oauth_token(
        self,
        *,
        service_account_email: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service_account_email GoogleCloudSchedulerJob#service_account_email}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#scope GoogleCloudSchedulerJob#scope}
        '''
        value = GoogleCloudSchedulerJobHttpTargetOauthToken(
            service_account_email=service_account_email, scope=scope
        )

        return typing.cast(None, jsii.invoke(self, "putOauthToken", [value]))

    @jsii.member(jsii_name="putOidcToken")
    def put_oidc_token(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#service_account_email GoogleCloudSchedulerJob#service_account_email}
        :param audience: Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#audience GoogleCloudSchedulerJob#audience}
        '''
        value = GoogleCloudSchedulerJobHttpTargetOidcToken(
            service_account_email=service_account_email, audience=audience
        )

        return typing.cast(None, jsii.invoke(self, "putOidcToken", [value]))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetOauthToken")
    def reset_oauth_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthToken", []))

    @jsii.member(jsii_name="resetOidcToken")
    def reset_oidc_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(self) -> GoogleCloudSchedulerJobHttpTargetOauthTokenOutputReference:
        return typing.cast(GoogleCloudSchedulerJobHttpTargetOauthTokenOutputReference, jsii.get(self, "oauthToken"))

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(self) -> GoogleCloudSchedulerJobHttpTargetOidcTokenOutputReference:
        return typing.cast(GoogleCloudSchedulerJobHttpTargetOidcTokenOutputReference, jsii.get(self, "oidcToken"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenInput")
    def oauth_token_input(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobHttpTargetOauthToken]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobHttpTargetOauthToken], jsii.get(self, "oauthTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(
        self,
    ) -> typing.Optional[GoogleCloudSchedulerJobHttpTargetOidcToken]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobHttpTargetOidcToken], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415cb45d99fd961cf8d84477a9fbd153c3f37538c2693ef387effd0f17f5221b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc4d004405455ee9de49699f9df72c6c51379e79c3f481d5e420fe9ae6c14ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f472539fb29688265608278b1fd01234c7883854835fa2819da94caa7e00e040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb8b088018d366f7ea44cefb1f8327c4a264e9a1fd8f7e32b05c1d33d5ef7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudSchedulerJobHttpTarget]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobHttpTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudSchedulerJobHttpTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3b990067f843f0508bfedd22b1bae2b5986dde68855b1e879d1026ce083981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobPubsubTarget",
    jsii_struct_bases=[],
    name_mapping={
        "topic_name": "topicName",
        "attributes": "attributes",
        "data": "data",
    },
)
class GoogleCloudSchedulerJobPubsubTarget:
    def __init__(
        self,
        *,
        topic_name: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic_name: The full resource name for the Cloud Pub/Sub topic to which messages will be published when a job is delivered. ~>**NOTE:** The topic name must be in the same format as required by PubSub's PublishRequest.name, e.g. 'projects/my-project/topics/my-topic'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#topic_name GoogleCloudSchedulerJob#topic_name}
        :param attributes: Attributes for PubsubMessage. Pubsub message must contain either non-empty data, or at least one attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#attributes GoogleCloudSchedulerJob#attributes}
        :param data: The message payload for PubsubMessage. Pubsub message must contain either non-empty data, or at least one attribute. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#data GoogleCloudSchedulerJob#data}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f7a3faf1a24fa815ef25c40c4fa4d85b8bca49960c4fb02b85ba8b101ca5f0)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_name": topic_name,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if data is not None:
            self._values["data"] = data

    @builtins.property
    def topic_name(self) -> builtins.str:
        '''The full resource name for the Cloud Pub/Sub topic to which messages will be published when a job is delivered.

        ~>**NOTE:**
        The topic name must be in the same format as required by PubSub's
        PublishRequest.name, e.g. 'projects/my-project/topics/my-topic'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#topic_name GoogleCloudSchedulerJob#topic_name}
        '''
        result = self._values.get("topic_name")
        assert result is not None, "Required property 'topic_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Attributes for PubsubMessage. Pubsub message must contain either non-empty data, or at least one attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#attributes GoogleCloudSchedulerJob#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''The message payload for PubsubMessage. Pubsub message must contain either non-empty data, or at least one attribute.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#data GoogleCloudSchedulerJob#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobPubsubTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudSchedulerJobPubsubTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobPubsubTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56805d97a0d329f2131a9dbf3c46737b4024fc4199de071378e08410ed7aa443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="topicNameInput")
    def topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0474456fb1d8d814278be5a8b9f68aa7338f03dab7f03b764dad936021476ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010b5ad5b5214d32d1f155fa950fed2db4cc853abeb88d978d020bf171dceb1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2523c41f16849f3653460e15b0018145b9af909156c2fcac69451c245f116183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudSchedulerJobPubsubTarget]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobPubsubTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudSchedulerJobPubsubTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e18cba469e6be7dbd4062da7ca59fbbdb8e457302457464172968a68a55af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobRetryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_backoff_duration": "maxBackoffDuration",
        "max_doublings": "maxDoublings",
        "max_retry_duration": "maxRetryDuration",
        "min_backoff_duration": "minBackoffDuration",
        "retry_count": "retryCount",
    },
)
class GoogleCloudSchedulerJobRetryConfig:
    def __init__(
        self,
        *,
        max_backoff_duration: typing.Optional[builtins.str] = None,
        max_doublings: typing.Optional[jsii.Number] = None,
        max_retry_duration: typing.Optional[builtins.str] = None,
        min_backoff_duration: typing.Optional[builtins.str] = None,
        retry_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_backoff_duration: The maximum amount of time to wait before retrying a job after it fails. A duration in seconds with up to nine fractional digits, terminated by 's'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_backoff_duration GoogleCloudSchedulerJob#max_backoff_duration}
        :param max_doublings: The time between retries will double maxDoublings times. A job's retry interval starts at minBackoffDuration, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoffDuration up to retryCount times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_doublings GoogleCloudSchedulerJob#max_doublings}
        :param max_retry_duration: The time limit for retrying a failed job, measured from time when an execution was first attempted. If specified with retryCount, the job will be retried until both limits are reached. A duration in seconds with up to nine fractional digits, terminated by 's'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_retry_duration GoogleCloudSchedulerJob#max_retry_duration}
        :param min_backoff_duration: The minimum amount of time to wait before retrying a job after it fails. A duration in seconds with up to nine fractional digits, terminated by 's'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#min_backoff_duration GoogleCloudSchedulerJob#min_backoff_duration}
        :param retry_count: The number of attempts that the system will make to run a job using the exponential backoff procedure described by maxDoublings. Values greater than 5 and negative values are not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#retry_count GoogleCloudSchedulerJob#retry_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f3ba1c893ad8ee7c5a81e358ecab9682ceaf44c067f9a3023704de4c02d17cb)
            check_type(argname="argument max_backoff_duration", value=max_backoff_duration, expected_type=type_hints["max_backoff_duration"])
            check_type(argname="argument max_doublings", value=max_doublings, expected_type=type_hints["max_doublings"])
            check_type(argname="argument max_retry_duration", value=max_retry_duration, expected_type=type_hints["max_retry_duration"])
            check_type(argname="argument min_backoff_duration", value=min_backoff_duration, expected_type=type_hints["min_backoff_duration"])
            check_type(argname="argument retry_count", value=retry_count, expected_type=type_hints["retry_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_backoff_duration is not None:
            self._values["max_backoff_duration"] = max_backoff_duration
        if max_doublings is not None:
            self._values["max_doublings"] = max_doublings
        if max_retry_duration is not None:
            self._values["max_retry_duration"] = max_retry_duration
        if min_backoff_duration is not None:
            self._values["min_backoff_duration"] = min_backoff_duration
        if retry_count is not None:
            self._values["retry_count"] = retry_count

    @builtins.property
    def max_backoff_duration(self) -> typing.Optional[builtins.str]:
        '''The maximum amount of time to wait before retrying a job after it fails.

        A duration in seconds with up to nine fractional digits, terminated by 's'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_backoff_duration GoogleCloudSchedulerJob#max_backoff_duration}
        '''
        result = self._values.get("max_backoff_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_doublings(self) -> typing.Optional[jsii.Number]:
        '''The time between retries will double maxDoublings times.

        A job's retry interval starts at minBackoffDuration,
        then doubles maxDoublings times, then increases linearly,
        and finally retries retries at intervals of maxBackoffDuration up to retryCount times.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_doublings GoogleCloudSchedulerJob#max_doublings}
        '''
        result = self._values.get("max_doublings")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retry_duration(self) -> typing.Optional[builtins.str]:
        '''The time limit for retrying a failed job, measured from time when an execution was first attempted.

        If specified with retryCount, the job will be retried until both limits are reached.
        A duration in seconds with up to nine fractional digits, terminated by 's'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#max_retry_duration GoogleCloudSchedulerJob#max_retry_duration}
        '''
        result = self._values.get("max_retry_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_backoff_duration(self) -> typing.Optional[builtins.str]:
        '''The minimum amount of time to wait before retrying a job after it fails.

        A duration in seconds with up to nine fractional digits, terminated by 's'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#min_backoff_duration GoogleCloudSchedulerJob#min_backoff_duration}
        '''
        result = self._values.get("min_backoff_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_count(self) -> typing.Optional[jsii.Number]:
        '''The number of attempts that the system will make to run a job using the exponential backoff procedure described by maxDoublings.

        Values greater than 5 and negative values are not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#retry_count GoogleCloudSchedulerJob#retry_count}
        '''
        result = self._values.get("retry_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobRetryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudSchedulerJobRetryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobRetryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd66c94c4c904c6843d37dae937093a6e11a33246dbee1a3ace697e19cbfde91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxBackoffDuration")
    def reset_max_backoff_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBackoffDuration", []))

    @jsii.member(jsii_name="resetMaxDoublings")
    def reset_max_doublings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDoublings", []))

    @jsii.member(jsii_name="resetMaxRetryDuration")
    def reset_max_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetryDuration", []))

    @jsii.member(jsii_name="resetMinBackoffDuration")
    def reset_min_backoff_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinBackoffDuration", []))

    @jsii.member(jsii_name="resetRetryCount")
    def reset_retry_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxBackoffDurationInput")
    def max_backoff_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxBackoffDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDoublingsInput")
    def max_doublings_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDoublingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetryDurationInput")
    def max_retry_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxRetryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minBackoffDurationInput")
    def min_backoff_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minBackoffDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retryCountInput")
    def retry_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBackoffDuration")
    def max_backoff_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxBackoffDuration"))

    @max_backoff_duration.setter
    def max_backoff_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51527e4ec6a6244bafd434535f08ec2e6467e6180e1f65ed2995067e0f42b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBackoffDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDoublings")
    def max_doublings(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDoublings"))

    @max_doublings.setter
    def max_doublings(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e38298ded2078bb673c18a7db9cc2294eade428fcf70e7541c6b33dfda9c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDoublings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetryDuration")
    def max_retry_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRetryDuration"))

    @max_retry_duration.setter
    def max_retry_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4856e740edde90af4ecaa1fe1bbcb82eaf7ea1e18aa6d472b8c36680a20a308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minBackoffDuration")
    def min_backoff_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minBackoffDuration"))

    @min_backoff_duration.setter
    def min_backoff_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54417b54006dfa10406c709e13c0a1455337078e71a1496e03f7602fc9b1adc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minBackoffDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryCount")
    def retry_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryCount"))

    @retry_count.setter
    def retry_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6d220ead7b1b4a8aad010b038a349b8bb28b54fc9f97377b96fec4950ebce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudSchedulerJobRetryConfig]:
        return typing.cast(typing.Optional[GoogleCloudSchedulerJobRetryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudSchedulerJobRetryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd8629018ad06ccef20b3cb4f8a2fead21c46b7d8e975a005826b284cec47d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudSchedulerJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#create GoogleCloudSchedulerJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#delete GoogleCloudSchedulerJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#update GoogleCloudSchedulerJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fedc3b5824f67a1ac80bc4be3934cfee597805c53f0ea8e8126add5153b3733)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#create GoogleCloudSchedulerJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#delete GoogleCloudSchedulerJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_scheduler_job#update GoogleCloudSchedulerJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudSchedulerJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudSchedulerJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudSchedulerJob.GoogleCloudSchedulerJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcdc9ce274434a25fbf03e34d52fb8e6f0a818988ae69ca025fa401b9d0fa3e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e7fc9ebd6a133ef9d90f9ec436fde08fd8b37b3e379a19bb2cc64cb567c5302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883fb8870819715cafa0276fd90d64eb881b85b51f56ef5625adef1aa95af3ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c226d64561eed4bb63d89b38424619e76e8a22488d6a88075118daeead3c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudSchedulerJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudSchedulerJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudSchedulerJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062b21389e33e1f06458d7b9b05db6f5eeac0b34b81499cc560b1d12fe30ae91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudSchedulerJob",
    "GoogleCloudSchedulerJobAppEngineHttpTarget",
    "GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting",
    "GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRoutingOutputReference",
    "GoogleCloudSchedulerJobAppEngineHttpTargetOutputReference",
    "GoogleCloudSchedulerJobConfig",
    "GoogleCloudSchedulerJobHttpTarget",
    "GoogleCloudSchedulerJobHttpTargetOauthToken",
    "GoogleCloudSchedulerJobHttpTargetOauthTokenOutputReference",
    "GoogleCloudSchedulerJobHttpTargetOidcToken",
    "GoogleCloudSchedulerJobHttpTargetOidcTokenOutputReference",
    "GoogleCloudSchedulerJobHttpTargetOutputReference",
    "GoogleCloudSchedulerJobPubsubTarget",
    "GoogleCloudSchedulerJobPubsubTargetOutputReference",
    "GoogleCloudSchedulerJobRetryConfig",
    "GoogleCloudSchedulerJobRetryConfigOutputReference",
    "GoogleCloudSchedulerJobTimeouts",
    "GoogleCloudSchedulerJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c17a957b9dd1c197be1d710cb7cc4c543bc06f14ce05aa58e69094d83f9d8759(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    app_engine_http_target: typing.Optional[typing.Union[GoogleCloudSchedulerJobAppEngineHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    attempt_deadline: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_target: typing.Optional[typing.Union[GoogleCloudSchedulerJobHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    pubsub_target: typing.Optional[typing.Union[GoogleCloudSchedulerJobPubsubTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    retry_config: typing.Optional[typing.Union[GoogleCloudSchedulerJobRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudSchedulerJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4705824e932bf6b787b51b284124e24d79f89a9bb1ed00ce01e91fbdf7cdb7e8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10d53a014154fb726bd06e390549f787142b8a8977c9a50b598de72389d712d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0085163a8613701724463fc58fdae636f07ca0f45d867656fdc03e8d1e3d1ad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465d3778d880cb77b81f8cc99ab6ce37d6d63f3c7d42dff6e7c663cdadd982bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6885d09538aacff710b7ce085c9ad2ee9b02b0bcf4939a1e163eb91a472be9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db8cdf1291d838f628e0ce8643501c9d6a563d63f327af056aa542bfe310dfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bb7e8a3fd65471cce24d00545245c4218d4129ff4b00cc0ef2443fdbecf11f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a2e585907a939b8e6af6fa5ccded3cd9159b8048f1e41e3457645824151f2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3863c55c7189c41d49e37cc08bedaae0b0c66517c465b89155bc0bc4feeaa771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73cfc1f22184fe3263a2912668a13b899d2b8a7c29cdfc8f3fb84a770fbf1268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194423cd9f1337b57928f1ce452e06c02fa2a5ac7c00c4e963e4a5c7b9497aec(
    *,
    relative_uri: builtins.str,
    app_engine_routing: typing.Optional[typing.Union[GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    body: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    http_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eaa2af7827c32cb3b2d79e5c59b44c6d9fc0a7bff5aa478ae07139d7158b6c1(
    *,
    instance: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7e6d5ff7d66c9cffa60c2c31a1a814689aae2ef7209d3bc571347fd366cfe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79f8a2db8796b6bba9e0e7fe7f2a66711954933d1d264f6ffe6fb439b244fe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7883790cf8a84cbd9eed7267dc572ae1a00c5980533eee6da6c71340e32c5fc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de41c26ba0e1953cee7aad273b20e4af11dfa5b416a2ccfd5b3b9c4289e72339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de1043454b88ec62c68f8101f4d026f9d81c6f78c9b68cfa88e6518c7ae4e6b(
    value: typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTargetAppEngineRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f817a46071cf26725604ec92e235472cf3e798421d41bb2941f1f3b821ac75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37daabcf45ddbd27a082fdfa0b0c22905e1c986e1deaae90b7faab4029d5117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3682f884782e9f37182cef2d749bba8f4b1645be64e24ec9d9dfa6e6838104b0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f60d85d34494c7542240ae08de1499e15df461a88a8da42a18c769895e9d4fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b6a686eaa56174dd2692261190780a79f3708bd6a45a35053c87444ba62ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44587c798f993c30559bb1a126eb04d2998e2e774910217048a37f1f049722aa(
    value: typing.Optional[GoogleCloudSchedulerJobAppEngineHttpTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c254f30c458b15c62b56aacfdabf6e6c3fb873d28c556df3eb8a63fe7115d11(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    app_engine_http_target: typing.Optional[typing.Union[GoogleCloudSchedulerJobAppEngineHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    attempt_deadline: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_target: typing.Optional[typing.Union[GoogleCloudSchedulerJobHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    pubsub_target: typing.Optional[typing.Union[GoogleCloudSchedulerJobPubsubTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    retry_config: typing.Optional[typing.Union[GoogleCloudSchedulerJobRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudSchedulerJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac44289c94fc80538c31a151425b2c21e29329e4db72fad3b9e4d49f13976f2(
    *,
    uri: builtins.str,
    body: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    http_method: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[typing.Union[GoogleCloudSchedulerJobHttpTargetOauthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    oidc_token: typing.Optional[typing.Union[GoogleCloudSchedulerJobHttpTargetOidcToken, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238a15636e18836bb7f10642d2c2d36bf750e09cf962f3d448fc91973b460dec(
    *,
    service_account_email: builtins.str,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fb89224f6fc3a1071048ea64fa36eb773f3ead4b3108aa9d09eb07a85cfb2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc640c7f789477458da57a524b4e93958e748a65b40a8f15ba7dee916d31491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51028bc0baee1849518a830ce5f9126df54fa5f4395bd570f90b0e15b3e610bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812d1458b82987f8fb0179f034a0558dec3418a575889038adf592cfd0fe80f2(
    value: typing.Optional[GoogleCloudSchedulerJobHttpTargetOauthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d4603c810b5e9ec190bf1f5d05de26307011980337897c007a3a800c2721d3(
    *,
    service_account_email: builtins.str,
    audience: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cff4b44c468a424f531b826b1598860edebd00671dd519e0f9a3153760516f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0020e3f00adc54e37fa6955a3c81ede65e5322d823eee4de41749f3e368da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c709bdeafd1e5ccd4b8d60b44c39012d152a7841e6f5e03391224f81ab1f607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a526a352eab426bb5d6663d057c5447690a545d6da6dde0ce6b3906517ec89e(
    value: typing.Optional[GoogleCloudSchedulerJobHttpTargetOidcToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194a34e9a42c2fec631b1a9e0c6cb08b8efe535c688f2ab8d8f9cc9b77f4237b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415cb45d99fd961cf8d84477a9fbd153c3f37538c2693ef387effd0f17f5221b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc4d004405455ee9de49699f9df72c6c51379e79c3f481d5e420fe9ae6c14ab(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f472539fb29688265608278b1fd01234c7883854835fa2819da94caa7e00e040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb8b088018d366f7ea44cefb1f8327c4a264e9a1fd8f7e32b05c1d33d5ef7dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3b990067f843f0508bfedd22b1bae2b5986dde68855b1e879d1026ce083981(
    value: typing.Optional[GoogleCloudSchedulerJobHttpTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f7a3faf1a24fa815ef25c40c4fa4d85b8bca49960c4fb02b85ba8b101ca5f0(
    *,
    topic_name: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56805d97a0d329f2131a9dbf3c46737b4024fc4199de071378e08410ed7aa443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0474456fb1d8d814278be5a8b9f68aa7338f03dab7f03b764dad936021476ecf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010b5ad5b5214d32d1f155fa950fed2db4cc853abeb88d978d020bf171dceb1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2523c41f16849f3653460e15b0018145b9af909156c2fcac69451c245f116183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e18cba469e6be7dbd4062da7ca59fbbdb8e457302457464172968a68a55af4(
    value: typing.Optional[GoogleCloudSchedulerJobPubsubTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3ba1c893ad8ee7c5a81e358ecab9682ceaf44c067f9a3023704de4c02d17cb(
    *,
    max_backoff_duration: typing.Optional[builtins.str] = None,
    max_doublings: typing.Optional[jsii.Number] = None,
    max_retry_duration: typing.Optional[builtins.str] = None,
    min_backoff_duration: typing.Optional[builtins.str] = None,
    retry_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd66c94c4c904c6843d37dae937093a6e11a33246dbee1a3ace697e19cbfde91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51527e4ec6a6244bafd434535f08ec2e6467e6180e1f65ed2995067e0f42b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e38298ded2078bb673c18a7db9cc2294eade428fcf70e7541c6b33dfda9c83(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4856e740edde90af4ecaa1fe1bbcb82eaf7ea1e18aa6d472b8c36680a20a308(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54417b54006dfa10406c709e13c0a1455337078e71a1496e03f7602fc9b1adc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6d220ead7b1b4a8aad010b038a349b8bb28b54fc9f97377b96fec4950ebce3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd8629018ad06ccef20b3cb4f8a2fead21c46b7d8e975a005826b284cec47d3(
    value: typing.Optional[GoogleCloudSchedulerJobRetryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fedc3b5824f67a1ac80bc4be3934cfee597805c53f0ea8e8126add5153b3733(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdc9ce274434a25fbf03e34d52fb8e6f0a818988ae69ca025fa401b9d0fa3e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7fc9ebd6a133ef9d90f9ec436fde08fd8b37b3e379a19bb2cc64cb567c5302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883fb8870819715cafa0276fd90d64eb881b85b51f56ef5625adef1aa95af3ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c226d64561eed4bb63d89b38424619e76e8a22488d6a88075118daeead3c66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062b21389e33e1f06458d7b9b05db6f5eeac0b34b81499cc560b1d12fe30ae91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudSchedulerJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
