r'''
# `google_cloud_tasks_queue`

Refer to the Terraform Registry for docs: [`google_cloud_tasks_queue`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue).
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


class GoogleCloudTasksQueue(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueue",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue google_cloud_tasks_queue}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        app_engine_routing_override: typing.Optional[typing.Union["GoogleCloudTasksQueueAppEngineRoutingOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        http_target: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limits: typing.Optional[typing.Union["GoogleCloudTasksQueueRateLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_config: typing.Optional[typing.Union["GoogleCloudTasksQueueRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stackdriver_logging_config: typing.Optional[typing.Union["GoogleCloudTasksQueueStackdriverLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudTasksQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue google_cloud_tasks_queue} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the queue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#location GoogleCloudTasksQueue#location}
        :param app_engine_routing_override: app_engine_routing_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#app_engine_routing_override GoogleCloudTasksQueue#app_engine_routing_override}
        :param http_target: http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#http_target GoogleCloudTasksQueue#http_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#id GoogleCloudTasksQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The queue name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#name GoogleCloudTasksQueue#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#project GoogleCloudTasksQueue#project}.
        :param rate_limits: rate_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#rate_limits GoogleCloudTasksQueue#rate_limits}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#retry_config GoogleCloudTasksQueue#retry_config}
        :param stackdriver_logging_config: stackdriver_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#stackdriver_logging_config GoogleCloudTasksQueue#stackdriver_logging_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#timeouts GoogleCloudTasksQueue#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc2dcc2c493c66f584508e1cee8ed35375436ec3571fb08b6edba953114811b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudTasksQueueConfig(
            location=location,
            app_engine_routing_override=app_engine_routing_override,
            http_target=http_target,
            id=id,
            name=name,
            project=project,
            rate_limits=rate_limits,
            retry_config=retry_config,
            stackdriver_logging_config=stackdriver_logging_config,
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
        '''Generates CDKTF code for importing a GoogleCloudTasksQueue resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudTasksQueue to import.
        :param import_from_id: The id of the existing GoogleCloudTasksQueue that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudTasksQueue to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e604894383f7c3bc0e6be8e8fcb95e5a3308e7559c693532354ecfc4f0578df6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAppEngineRoutingOverride")
    def put_app_engine_routing_override(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: App instance. By default, the task is sent to an instance which is available when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#instance GoogleCloudTasksQueue#instance}
        :param service: App service. By default, the task is sent to the service which is the default service when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service GoogleCloudTasksQueue#service}
        :param version: App version. By default, the task is sent to the version which is the default version when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#version GoogleCloudTasksQueue#version}
        '''
        value = GoogleCloudTasksQueueAppEngineRoutingOverride(
            instance=instance, service=service, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putAppEngineRoutingOverride", [value]))

    @jsii.member(jsii_name="putHttpTarget")
    def put_http_target(
        self,
        *,
        header_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudTasksQueueHttpTargetHeaderOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        uri_override: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetUriOverride", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_overrides: header_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#header_overrides GoogleCloudTasksQueue#header_overrides}
        :param http_method: The HTTP method to use for the request. When specified, it overrides HttpRequest for the task. Note that if the value is set to GET the body of the task will be ignored at execution time. Possible values: ["HTTP_METHOD_UNSPECIFIED", "POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#http_method GoogleCloudTasksQueue#http_method}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#oauth_token GoogleCloudTasksQueue#oauth_token}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#oidc_token GoogleCloudTasksQueue#oidc_token}
        :param uri_override: uri_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#uri_override GoogleCloudTasksQueue#uri_override}
        '''
        value = GoogleCloudTasksQueueHttpTarget(
            header_overrides=header_overrides,
            http_method=http_method,
            oauth_token=oauth_token,
            oidc_token=oidc_token,
            uri_override=uri_override,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpTarget", [value]))

    @jsii.member(jsii_name="putRateLimits")
    def put_rate_limits(
        self,
        *,
        max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
        max_dispatches_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_dispatches: The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue. After this threshold has been reached, Cloud Tasks stops dispatching tasks until the number of concurrent requests decreases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_concurrent_dispatches GoogleCloudTasksQueue#max_concurrent_dispatches}
        :param max_dispatches_per_second: The maximum rate at which tasks are dispatched from this queue. If unspecified when the queue is created, Cloud Tasks will pick the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_dispatches_per_second GoogleCloudTasksQueue#max_dispatches_per_second}
        '''
        value = GoogleCloudTasksQueueRateLimits(
            max_concurrent_dispatches=max_concurrent_dispatches,
            max_dispatches_per_second=max_dispatches_per_second,
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimits", [value]))

    @jsii.member(jsii_name="putRetryConfig")
    def put_retry_config(
        self,
        *,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_backoff: typing.Optional[builtins.str] = None,
        max_doublings: typing.Optional[jsii.Number] = None,
        max_retry_duration: typing.Optional[builtins.str] = None,
        min_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Number of attempts per task. Cloud Tasks will attempt the task maxAttempts times (that is, if the first attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1. If unspecified when the queue is created, Cloud Tasks will pick the default. -1 indicates unlimited attempts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_attempts GoogleCloudTasksQueue#max_attempts}
        :param max_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_backoff GoogleCloudTasksQueue#max_backoff}
        :param max_doublings: The time between retries will double maxDoublings times. A task's retry interval starts at minBackoff, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoff up to maxAttempts times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_doublings GoogleCloudTasksQueue#max_doublings}
        :param max_retry_duration: If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted. Once maxRetryDuration time has passed and the task has been attempted maxAttempts times, no further attempts will be made and the task will be deleted. If zero, then the task age is unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_retry_duration GoogleCloudTasksQueue#max_retry_duration}
        :param min_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#min_backoff GoogleCloudTasksQueue#min_backoff}
        '''
        value = GoogleCloudTasksQueueRetryConfig(
            max_attempts=max_attempts,
            max_backoff=max_backoff,
            max_doublings=max_doublings,
            max_retry_duration=max_retry_duration,
            min_backoff=min_backoff,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryConfig", [value]))

    @jsii.member(jsii_name="putStackdriverLoggingConfig")
    def put_stackdriver_logging_config(self, *, sampling_ratio: jsii.Number) -> None:
        '''
        :param sampling_ratio: Specifies the fraction of operations to write to Stackdriver Logging. This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the default and means that no operations are logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#sampling_ratio GoogleCloudTasksQueue#sampling_ratio}
        '''
        value = GoogleCloudTasksQueueStackdriverLoggingConfig(
            sampling_ratio=sampling_ratio
        )

        return typing.cast(None, jsii.invoke(self, "putStackdriverLoggingConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#create GoogleCloudTasksQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#delete GoogleCloudTasksQueue#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#update GoogleCloudTasksQueue#update}.
        '''
        value = GoogleCloudTasksQueueTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAppEngineRoutingOverride")
    def reset_app_engine_routing_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineRoutingOverride", []))

    @jsii.member(jsii_name="resetHttpTarget")
    def reset_http_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpTarget", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRateLimits")
    def reset_rate_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimits", []))

    @jsii.member(jsii_name="resetRetryConfig")
    def reset_retry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryConfig", []))

    @jsii.member(jsii_name="resetStackdriverLoggingConfig")
    def reset_stackdriver_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStackdriverLoggingConfig", []))

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
    @jsii.member(jsii_name="appEngineRoutingOverride")
    def app_engine_routing_override(
        self,
    ) -> "GoogleCloudTasksQueueAppEngineRoutingOverrideOutputReference":
        return typing.cast("GoogleCloudTasksQueueAppEngineRoutingOverrideOutputReference", jsii.get(self, "appEngineRoutingOverride"))

    @builtins.property
    @jsii.member(jsii_name="httpTarget")
    def http_target(self) -> "GoogleCloudTasksQueueHttpTargetOutputReference":
        return typing.cast("GoogleCloudTasksQueueHttpTargetOutputReference", jsii.get(self, "httpTarget"))

    @builtins.property
    @jsii.member(jsii_name="rateLimits")
    def rate_limits(self) -> "GoogleCloudTasksQueueRateLimitsOutputReference":
        return typing.cast("GoogleCloudTasksQueueRateLimitsOutputReference", jsii.get(self, "rateLimits"))

    @builtins.property
    @jsii.member(jsii_name="retryConfig")
    def retry_config(self) -> "GoogleCloudTasksQueueRetryConfigOutputReference":
        return typing.cast("GoogleCloudTasksQueueRetryConfigOutputReference", jsii.get(self, "retryConfig"))

    @builtins.property
    @jsii.member(jsii_name="stackdriverLoggingConfig")
    def stackdriver_logging_config(
        self,
    ) -> "GoogleCloudTasksQueueStackdriverLoggingConfigOutputReference":
        return typing.cast("GoogleCloudTasksQueueStackdriverLoggingConfigOutputReference", jsii.get(self, "stackdriverLoggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudTasksQueueTimeoutsOutputReference":
        return typing.cast("GoogleCloudTasksQueueTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appEngineRoutingOverrideInput")
    def app_engine_routing_override_input(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueAppEngineRoutingOverride"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueAppEngineRoutingOverride"], jsii.get(self, "appEngineRoutingOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="httpTargetInput")
    def http_target_input(self) -> typing.Optional["GoogleCloudTasksQueueHttpTarget"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTarget"], jsii.get(self, "httpTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitsInput")
    def rate_limits_input(self) -> typing.Optional["GoogleCloudTasksQueueRateLimits"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueRateLimits"], jsii.get(self, "rateLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryConfigInput")
    def retry_config_input(self) -> typing.Optional["GoogleCloudTasksQueueRetryConfig"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueRetryConfig"], jsii.get(self, "retryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stackdriverLoggingConfigInput")
    def stackdriver_logging_config_input(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueStackdriverLoggingConfig"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueStackdriverLoggingConfig"], jsii.get(self, "stackdriverLoggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudTasksQueueTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudTasksQueueTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42d04b862f2cf547c0c393e30961915be51b0b7a67e907772a1733685c304de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008b71a9a2ddcfd1576b755119e31bded29aacf43b487da6b348d9ce5ba903d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9198f6ec5b32a0006965d6cab54507cad51860099d574b44feb2609e39480b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f98aec4a9d068488ef31bd5fb496de41804c6946aa5758a9701d496443e920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueAppEngineRoutingOverride",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance", "service": "service", "version": "version"},
)
class GoogleCloudTasksQueueAppEngineRoutingOverride:
    def __init__(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: App instance. By default, the task is sent to an instance which is available when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#instance GoogleCloudTasksQueue#instance}
        :param service: App service. By default, the task is sent to the service which is the default service when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service GoogleCloudTasksQueue#service}
        :param version: App version. By default, the task is sent to the version which is the default version when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#version GoogleCloudTasksQueue#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e1475321db8f04d08f81bee7e4b1993e9c12e19cb51f6401c11f1ede7cbe11)
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
        '''App instance.

        By default, the task is sent to an instance which is available when the task is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#instance GoogleCloudTasksQueue#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''App service.

        By default, the task is sent to the service which is the default service when the task is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service GoogleCloudTasksQueue#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''App version.

        By default, the task is sent to the version which is the default version when the task is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#version GoogleCloudTasksQueue#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueAppEngineRoutingOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueAppEngineRoutingOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueAppEngineRoutingOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6f8eda373ebd32300c8e38d4978a12ee2d8c36d2c564a05ece07e79aca90bb2)
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
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__23358fbfcdf6cc5cf396e7b53c2b79a36ee05fd06601a1e1d75ae608231655ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5d8811fd0039e621b0074b3282c9e9332f67c7f522cef02ea678c79632ef3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0807b1928c3e2a3b20ec7cb5331e1a46c3f581849b89eb6ca98449120f56b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueAppEngineRoutingOverride]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueAppEngineRoutingOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueAppEngineRoutingOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b4d138c0d1706eeb92686d43ea22e0f96235c114d83f7160001bcff13e96ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueConfig",
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
        "app_engine_routing_override": "appEngineRoutingOverride",
        "http_target": "httpTarget",
        "id": "id",
        "name": "name",
        "project": "project",
        "rate_limits": "rateLimits",
        "retry_config": "retryConfig",
        "stackdriver_logging_config": "stackdriverLoggingConfig",
        "timeouts": "timeouts",
    },
)
class GoogleCloudTasksQueueConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_engine_routing_override: typing.Optional[typing.Union[GoogleCloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
        http_target: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limits: typing.Optional[typing.Union["GoogleCloudTasksQueueRateLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_config: typing.Optional[typing.Union["GoogleCloudTasksQueueRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stackdriver_logging_config: typing.Optional[typing.Union["GoogleCloudTasksQueueStackdriverLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudTasksQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the queue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#location GoogleCloudTasksQueue#location}
        :param app_engine_routing_override: app_engine_routing_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#app_engine_routing_override GoogleCloudTasksQueue#app_engine_routing_override}
        :param http_target: http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#http_target GoogleCloudTasksQueue#http_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#id GoogleCloudTasksQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The queue name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#name GoogleCloudTasksQueue#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#project GoogleCloudTasksQueue#project}.
        :param rate_limits: rate_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#rate_limits GoogleCloudTasksQueue#rate_limits}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#retry_config GoogleCloudTasksQueue#retry_config}
        :param stackdriver_logging_config: stackdriver_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#stackdriver_logging_config GoogleCloudTasksQueue#stackdriver_logging_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#timeouts GoogleCloudTasksQueue#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(app_engine_routing_override, dict):
            app_engine_routing_override = GoogleCloudTasksQueueAppEngineRoutingOverride(**app_engine_routing_override)
        if isinstance(http_target, dict):
            http_target = GoogleCloudTasksQueueHttpTarget(**http_target)
        if isinstance(rate_limits, dict):
            rate_limits = GoogleCloudTasksQueueRateLimits(**rate_limits)
        if isinstance(retry_config, dict):
            retry_config = GoogleCloudTasksQueueRetryConfig(**retry_config)
        if isinstance(stackdriver_logging_config, dict):
            stackdriver_logging_config = GoogleCloudTasksQueueStackdriverLoggingConfig(**stackdriver_logging_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudTasksQueueTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900bc1fdcf9b3e4b1c789eb4391746d40a41bb2bb41f80fbef14fe9e113682e0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument app_engine_routing_override", value=app_engine_routing_override, expected_type=type_hints["app_engine_routing_override"])
            check_type(argname="argument http_target", value=http_target, expected_type=type_hints["http_target"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rate_limits", value=rate_limits, expected_type=type_hints["rate_limits"])
            check_type(argname="argument retry_config", value=retry_config, expected_type=type_hints["retry_config"])
            check_type(argname="argument stackdriver_logging_config", value=stackdriver_logging_config, expected_type=type_hints["stackdriver_logging_config"])
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
        if app_engine_routing_override is not None:
            self._values["app_engine_routing_override"] = app_engine_routing_override
        if http_target is not None:
            self._values["http_target"] = http_target
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if rate_limits is not None:
            self._values["rate_limits"] = rate_limits
        if retry_config is not None:
            self._values["retry_config"] = retry_config
        if stackdriver_logging_config is not None:
            self._values["stackdriver_logging_config"] = stackdriver_logging_config
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
        '''The location of the queue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#location GoogleCloudTasksQueue#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_routing_override(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueAppEngineRoutingOverride]:
        '''app_engine_routing_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#app_engine_routing_override GoogleCloudTasksQueue#app_engine_routing_override}
        '''
        result = self._values.get("app_engine_routing_override")
        return typing.cast(typing.Optional[GoogleCloudTasksQueueAppEngineRoutingOverride], result)

    @builtins.property
    def http_target(self) -> typing.Optional["GoogleCloudTasksQueueHttpTarget"]:
        '''http_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#http_target GoogleCloudTasksQueue#http_target}
        '''
        result = self._values.get("http_target")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTarget"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#id GoogleCloudTasksQueue#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The queue name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#name GoogleCloudTasksQueue#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#project GoogleCloudTasksQueue#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limits(self) -> typing.Optional["GoogleCloudTasksQueueRateLimits"]:
        '''rate_limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#rate_limits GoogleCloudTasksQueue#rate_limits}
        '''
        result = self._values.get("rate_limits")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueRateLimits"], result)

    @builtins.property
    def retry_config(self) -> typing.Optional["GoogleCloudTasksQueueRetryConfig"]:
        '''retry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#retry_config GoogleCloudTasksQueue#retry_config}
        '''
        result = self._values.get("retry_config")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueRetryConfig"], result)

    @builtins.property
    def stackdriver_logging_config(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueStackdriverLoggingConfig"]:
        '''stackdriver_logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#stackdriver_logging_config GoogleCloudTasksQueue#stackdriver_logging_config}
        '''
        result = self._values.get("stackdriver_logging_config")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueStackdriverLoggingConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudTasksQueueTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#timeouts GoogleCloudTasksQueue#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTarget",
    jsii_struct_bases=[],
    name_mapping={
        "header_overrides": "headerOverrides",
        "http_method": "httpMethod",
        "oauth_token": "oauthToken",
        "oidc_token": "oidcToken",
        "uri_override": "uriOverride",
    },
)
class GoogleCloudTasksQueueHttpTarget:
    def __init__(
        self,
        *,
        header_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudTasksQueueHttpTargetHeaderOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        uri_override: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetUriOverride", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_overrides: header_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#header_overrides GoogleCloudTasksQueue#header_overrides}
        :param http_method: The HTTP method to use for the request. When specified, it overrides HttpRequest for the task. Note that if the value is set to GET the body of the task will be ignored at execution time. Possible values: ["HTTP_METHOD_UNSPECIFIED", "POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#http_method GoogleCloudTasksQueue#http_method}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#oauth_token GoogleCloudTasksQueue#oauth_token}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#oidc_token GoogleCloudTasksQueue#oidc_token}
        :param uri_override: uri_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#uri_override GoogleCloudTasksQueue#uri_override}
        '''
        if isinstance(oauth_token, dict):
            oauth_token = GoogleCloudTasksQueueHttpTargetOauthToken(**oauth_token)
        if isinstance(oidc_token, dict):
            oidc_token = GoogleCloudTasksQueueHttpTargetOidcToken(**oidc_token)
        if isinstance(uri_override, dict):
            uri_override = GoogleCloudTasksQueueHttpTargetUriOverride(**uri_override)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d292a674a4fa9953f26e870f51c3bbd9776a599616ff4c5fbacba415e493644)
            check_type(argname="argument header_overrides", value=header_overrides, expected_type=type_hints["header_overrides"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument oidc_token", value=oidc_token, expected_type=type_hints["oidc_token"])
            check_type(argname="argument uri_override", value=uri_override, expected_type=type_hints["uri_override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_overrides is not None:
            self._values["header_overrides"] = header_overrides
        if http_method is not None:
            self._values["http_method"] = http_method
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token
        if oidc_token is not None:
            self._values["oidc_token"] = oidc_token
        if uri_override is not None:
            self._values["uri_override"] = uri_override

    @builtins.property
    def header_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudTasksQueueHttpTargetHeaderOverrides"]]]:
        '''header_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#header_overrides GoogleCloudTasksQueue#header_overrides}
        '''
        result = self._values.get("header_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudTasksQueueHttpTargetHeaderOverrides"]]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''The HTTP method to use for the request.

        When specified, it overrides HttpRequest for the task.
        Note that if the value is set to GET the body of the task will be ignored at execution time. Possible values: ["HTTP_METHOD_UNSPECIFIED", "POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#http_method GoogleCloudTasksQueue#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueHttpTargetOauthToken"]:
        '''oauth_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#oauth_token GoogleCloudTasksQueue#oauth_token}
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetOauthToken"], result)

    @builtins.property
    def oidc_token(self) -> typing.Optional["GoogleCloudTasksQueueHttpTargetOidcToken"]:
        '''oidc_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#oidc_token GoogleCloudTasksQueue#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetOidcToken"], result)

    @builtins.property
    def uri_override(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverride"]:
        '''uri_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#uri_override GoogleCloudTasksQueue#uri_override}
        '''
        result = self._values.get("uri_override")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverride"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetHeaderOverrides",
    jsii_struct_bases=[],
    name_mapping={"header": "header"},
)
class GoogleCloudTasksQueueHttpTargetHeaderOverrides:
    def __init__(
        self,
        *,
        header: typing.Union["GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#header GoogleCloudTasksQueue#header}
        '''
        if isinstance(header, dict):
            header = GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader(**header)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6c03c5f3d7c3c8c64c62be7f305ce0691e0f6faefe1b7ea97da1cc23026516)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
        }

    @builtins.property
    def header(self) -> "GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader":
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#header GoogleCloudTasksQueue#header}
        '''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast("GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTargetHeaderOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The Key of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#key GoogleCloudTasksQueue#key}
        :param value: The Value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#value GoogleCloudTasksQueue#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe4207c19fc0f4ba2b55fd75ee7a8ebd3b5b63381ba6d98d4efe26b49bb445b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''The Key of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#key GoogleCloudTasksQueue#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The Value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#value GoogleCloudTasksQueue#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b357d5d70742a7feb8d99e0b02503a86e3fcb5055c3085fd2cc6e9ff88f26a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e831f2e381ced98e39e8b3c733f627a9478c67ca7d6f973731a61a06ebd865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872b9130d9dcf43d6ecadc82ef8bc1aa6689e913d090adc0bdf1b2ebf12ba243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0184c3e3c623564757f818b8a53768c2294b1210da4d47dfca19289976e4b3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudTasksQueueHttpTargetHeaderOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetHeaderOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b48157131a266bad5fe1033b6a387d2624b651e61f9a991f915ca4af46bc71bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudTasksQueueHttpTargetHeaderOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0aae4a05e8b6568fcf29d2d421bceb5feb12f3cac493cb9c3b280cae9c465a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudTasksQueueHttpTargetHeaderOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d56f0ccf0fee26fa2dc43da43ac780ad7c67143bbd39587c6ce94dd0e4f03a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df43ca7f09a61718dac6c159a1c36638c7674adcdd4ba5bdfb988e8482fad919)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54dfccd8ef1150a3eed5b0e46f8301cf10cbd4f8f35b0a411cf0cb29cdffb506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudTasksQueueHttpTargetHeaderOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudTasksQueueHttpTargetHeaderOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudTasksQueueHttpTargetHeaderOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39685bbed64f9f73c330c3dcf6258cd486f5b48ffb8756b3a451288cd85f8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudTasksQueueHttpTargetHeaderOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetHeaderOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f72060532b8043c17fa3c563710aa6b1708ef853f611657a870a50bfe47aa99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The Key of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#key GoogleCloudTasksQueue#key}
        :param value: The Value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#value GoogleCloudTasksQueue#value}
        '''
        value_ = GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader(
            key=key, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putHeader", [value_]))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(
        self,
    ) -> GoogleCloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference:
        return typing.cast(GoogleCloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueHttpTargetHeaderOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueHttpTargetHeaderOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueHttpTargetHeaderOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16719e9dc1cbef29452fa41936080d9c8f73f290db3f1b74fd2e632ceee27ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetOauthToken",
    jsii_struct_bases=[],
    name_mapping={"service_account_email": "serviceAccountEmail", "scope": "scope"},
)
class GoogleCloudTasksQueueHttpTargetOauthToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service_account_email GoogleCloudTasksQueue#service_account_email}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#scope GoogleCloudTasksQueue#scope}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ce4a01af64a6def75a376ef56c1a487023882faac763804d342dca22677244)
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

        The service account must be within the same project as the queue.
        The caller must have iam.serviceAccounts.actAs permission for the service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service_account_email GoogleCloudTasksQueue#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#scope GoogleCloudTasksQueue#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTargetOauthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueHttpTargetOauthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetOauthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3f84cccbfa2d1bb5bbcc5d05bcdf09a51b118bfb10bf67c65cc4b060105c9e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c389df2d0dd18fbaa0003e94f6eb48cf37b89d7c0da0086f7d00846a093c2057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c75cdc9087313c424b4c005b2b3d3aea8fb06b6cb7f8eb95f9462cea596fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetOauthToken]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetOauthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueHttpTargetOauthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3673c3fd4f754b2589bb877369e8b2e20ec536fa7fff0cb6136a849415b48f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetOidcToken",
    jsii_struct_bases=[],
    name_mapping={
        "service_account_email": "serviceAccountEmail",
        "audience": "audience",
    },
)
class GoogleCloudTasksQueueHttpTargetOidcToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OIDC token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service_account_email GoogleCloudTasksQueue#service_account_email}
        :param audience: Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#audience GoogleCloudTasksQueue#audience}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c86f0c1ac3213e0c472a6e4468c0be7607bf504bddc450d467be3b5aa8bee8)
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_email": service_account_email,
        }
        if audience is not None:
            self._values["audience"] = audience

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''Service account email to be used for generating OIDC token.

        The service account must be within the same project as the queue.
        The caller must have iam.serviceAccounts.actAs permission for the service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service_account_email GoogleCloudTasksQueue#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#audience GoogleCloudTasksQueue#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTargetOidcToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueHttpTargetOidcTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetOidcTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dc16b2151368b4b993a03bfe4200d5e789a8b824b9da392706613ef5cfd475f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff248f7cff95166e0f65576326012914b3e5401e8fd59f618dcb85030c51c311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26725d20559629cdf9d692d0fb948653463203d403bd078ec1a67ffcae511bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetOidcToken]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetOidcToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueHttpTargetOidcToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a249aaf00307915e0cb22ffc02c35c8dba2a0511d7669f43543bb87d8cb2c2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudTasksQueueHttpTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b562f4fc4b38e717614b3e7bd27eac46c188d20954e7ecd26c9b4ac891a3f1d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaderOverrides")
    def put_header_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudTasksQueueHttpTargetHeaderOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40026c8f878021517334191665c0d674dc8dcf91d02c6e1931f9e7417d59a15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaderOverrides", [value]))

    @jsii.member(jsii_name="putOauthToken")
    def put_oauth_token(
        self,
        *,
        service_account_email: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service_account_email GoogleCloudTasksQueue#service_account_email}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#scope GoogleCloudTasksQueue#scope}
        '''
        value = GoogleCloudTasksQueueHttpTargetOauthToken(
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
        :param service_account_email: Service account email to be used for generating OIDC token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#service_account_email GoogleCloudTasksQueue#service_account_email}
        :param audience: Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#audience GoogleCloudTasksQueue#audience}
        '''
        value = GoogleCloudTasksQueueHttpTargetOidcToken(
            service_account_email=service_account_email, audience=audience
        )

        return typing.cast(None, jsii.invoke(self, "putOidcToken", [value]))

    @jsii.member(jsii_name="putUriOverride")
    def put_uri_override(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        path_override: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetUriOverridePathOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[builtins.str] = None,
        query_override: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        uri_override_enforce_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host override. When specified, replaces the host part of the task URL. For example, if the task URL is "https://www.google.com", and host value is set to "example.net", the overridden URI will be changed to "https://example.net". Host value cannot be an empty string (INVALID_ARGUMENT). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#host GoogleCloudTasksQueue#host}
        :param path_override: path_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#path_override GoogleCloudTasksQueue#path_override}
        :param port: Port override. When specified, replaces the port part of the task URI. For instance, for a URI http://www.google.com/foo and port=123, the overridden URI becomes http://www.google.com:123/foo. Note that the port value must be a positive integer. Setting the port to 0 (Zero) clears the URI port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#port GoogleCloudTasksQueue#port}
        :param query_override: query_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#query_override GoogleCloudTasksQueue#query_override}
        :param scheme: Scheme override. When specified, the task URI scheme is replaced by the provided value (HTTP or HTTPS). Possible values: ["HTTP", "HTTPS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#scheme GoogleCloudTasksQueue#scheme}
        :param uri_override_enforce_mode: URI Override Enforce Mode. When specified, determines the Target UriOverride mode. If not specified, it defaults to ALWAYS. Possible values: ["ALWAYS", "IF_NOT_EXISTS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#uri_override_enforce_mode GoogleCloudTasksQueue#uri_override_enforce_mode}
        '''
        value = GoogleCloudTasksQueueHttpTargetUriOverride(
            host=host,
            path_override=path_override,
            port=port,
            query_override=query_override,
            scheme=scheme,
            uri_override_enforce_mode=uri_override_enforce_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putUriOverride", [value]))

    @jsii.member(jsii_name="resetHeaderOverrides")
    def reset_header_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderOverrides", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetOauthToken")
    def reset_oauth_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthToken", []))

    @jsii.member(jsii_name="resetOidcToken")
    def reset_oidc_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcToken", []))

    @jsii.member(jsii_name="resetUriOverride")
    def reset_uri_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUriOverride", []))

    @builtins.property
    @jsii.member(jsii_name="headerOverrides")
    def header_overrides(self) -> GoogleCloudTasksQueueHttpTargetHeaderOverridesList:
        return typing.cast(GoogleCloudTasksQueueHttpTargetHeaderOverridesList, jsii.get(self, "headerOverrides"))

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(self) -> GoogleCloudTasksQueueHttpTargetOauthTokenOutputReference:
        return typing.cast(GoogleCloudTasksQueueHttpTargetOauthTokenOutputReference, jsii.get(self, "oauthToken"))

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(self) -> GoogleCloudTasksQueueHttpTargetOidcTokenOutputReference:
        return typing.cast(GoogleCloudTasksQueueHttpTargetOidcTokenOutputReference, jsii.get(self, "oidcToken"))

    @builtins.property
    @jsii.member(jsii_name="uriOverride")
    def uri_override(
        self,
    ) -> "GoogleCloudTasksQueueHttpTargetUriOverrideOutputReference":
        return typing.cast("GoogleCloudTasksQueueHttpTargetUriOverrideOutputReference", jsii.get(self, "uriOverride"))

    @builtins.property
    @jsii.member(jsii_name="headerOverridesInput")
    def header_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudTasksQueueHttpTargetHeaderOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudTasksQueueHttpTargetHeaderOverrides]]], jsii.get(self, "headerOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenInput")
    def oauth_token_input(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetOauthToken]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetOauthToken], jsii.get(self, "oauthTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetOidcToken]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetOidcToken], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="uriOverrideInput")
    def uri_override_input(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverride"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverride"], jsii.get(self, "uriOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdf9d7b110be0a82386a188bf65ae91901297546818ab8f3049d115a9b88ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudTasksQueueHttpTarget]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueHttpTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3660cb5f3905fac8d60413f9e48903f0024f219224552777f75969be3ebb0d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetUriOverride",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "path_override": "pathOverride",
        "port": "port",
        "query_override": "queryOverride",
        "scheme": "scheme",
        "uri_override_enforce_mode": "uriOverrideEnforceMode",
    },
)
class GoogleCloudTasksQueueHttpTargetUriOverride:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        path_override: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetUriOverridePathOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[builtins.str] = None,
        query_override: typing.Optional[typing.Union["GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        uri_override_enforce_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host override. When specified, replaces the host part of the task URL. For example, if the task URL is "https://www.google.com", and host value is set to "example.net", the overridden URI will be changed to "https://example.net". Host value cannot be an empty string (INVALID_ARGUMENT). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#host GoogleCloudTasksQueue#host}
        :param path_override: path_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#path_override GoogleCloudTasksQueue#path_override}
        :param port: Port override. When specified, replaces the port part of the task URI. For instance, for a URI http://www.google.com/foo and port=123, the overridden URI becomes http://www.google.com:123/foo. Note that the port value must be a positive integer. Setting the port to 0 (Zero) clears the URI port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#port GoogleCloudTasksQueue#port}
        :param query_override: query_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#query_override GoogleCloudTasksQueue#query_override}
        :param scheme: Scheme override. When specified, the task URI scheme is replaced by the provided value (HTTP or HTTPS). Possible values: ["HTTP", "HTTPS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#scheme GoogleCloudTasksQueue#scheme}
        :param uri_override_enforce_mode: URI Override Enforce Mode. When specified, determines the Target UriOverride mode. If not specified, it defaults to ALWAYS. Possible values: ["ALWAYS", "IF_NOT_EXISTS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#uri_override_enforce_mode GoogleCloudTasksQueue#uri_override_enforce_mode}
        '''
        if isinstance(path_override, dict):
            path_override = GoogleCloudTasksQueueHttpTargetUriOverridePathOverride(**path_override)
        if isinstance(query_override, dict):
            query_override = GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride(**query_override)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aef4039afd5adde50b07bd1c902484c9ea2cea12e3a5a936b34204479936e48)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument path_override", value=path_override, expected_type=type_hints["path_override"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument query_override", value=query_override, expected_type=type_hints["query_override"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
            check_type(argname="argument uri_override_enforce_mode", value=uri_override_enforce_mode, expected_type=type_hints["uri_override_enforce_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if path_override is not None:
            self._values["path_override"] = path_override
        if port is not None:
            self._values["port"] = port
        if query_override is not None:
            self._values["query_override"] = query_override
        if scheme is not None:
            self._values["scheme"] = scheme
        if uri_override_enforce_mode is not None:
            self._values["uri_override_enforce_mode"] = uri_override_enforce_mode

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host override.

        When specified, replaces the host part of the task URL.
        For example, if the task URL is "https://www.google.com", and host value
        is set to "example.net", the overridden URI will be changed to "https://example.net".
        Host value cannot be an empty string (INVALID_ARGUMENT).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#host GoogleCloudTasksQueue#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_override(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverridePathOverride"]:
        '''path_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#path_override GoogleCloudTasksQueue#path_override}
        '''
        result = self._values.get("path_override")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverridePathOverride"], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Port override.

        When specified, replaces the port part of the task URI.
        For instance, for a URI http://www.google.com/foo and port=123, the overridden URI becomes http://www.google.com:123/foo.
        Note that the port value must be a positive integer.
        Setting the port to 0 (Zero) clears the URI port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#port GoogleCloudTasksQueue#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_override(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride"]:
        '''query_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#query_override GoogleCloudTasksQueue#query_override}
        '''
        result = self._values.get("query_override")
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride"], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme override.

        When specified, the task URI scheme is replaced by the provided value (HTTP or HTTPS). Possible values: ["HTTP", "HTTPS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#scheme GoogleCloudTasksQueue#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri_override_enforce_mode(self) -> typing.Optional[builtins.str]:
        '''URI Override Enforce Mode.

        When specified, determines the Target UriOverride mode. If not specified, it defaults to ALWAYS. Possible values: ["ALWAYS", "IF_NOT_EXISTS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#uri_override_enforce_mode GoogleCloudTasksQueue#uri_override_enforce_mode}
        '''
        result = self._values.get("uri_override_enforce_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTargetUriOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueHttpTargetUriOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetUriOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb44303fd5af80aac8d3173a8bd996b7aab2ec9a7bd4dedd632af420b7e71129)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPathOverride")
    def put_path_override(self, *, path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param path: The URI path (e.g., /users/1234). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#path GoogleCloudTasksQueue#path}
        '''
        value = GoogleCloudTasksQueueHttpTargetUriOverridePathOverride(path=path)

        return typing.cast(None, jsii.invoke(self, "putPathOverride", [value]))

    @jsii.member(jsii_name="putQueryOverride")
    def put_query_override(
        self,
        *,
        query_params: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param query_params: The query parameters (e.g., qparam1=123&qparam2=456). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#query_params GoogleCloudTasksQueue#query_params}
        '''
        value = GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride(
            query_params=query_params
        )

        return typing.cast(None, jsii.invoke(self, "putQueryOverride", [value]))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPathOverride")
    def reset_path_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathOverride", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetQueryOverride")
    def reset_query_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryOverride", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @jsii.member(jsii_name="resetUriOverrideEnforceMode")
    def reset_uri_override_enforce_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUriOverrideEnforceMode", []))

    @builtins.property
    @jsii.member(jsii_name="pathOverride")
    def path_override(
        self,
    ) -> "GoogleCloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference":
        return typing.cast("GoogleCloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference", jsii.get(self, "pathOverride"))

    @builtins.property
    @jsii.member(jsii_name="queryOverride")
    def query_override(
        self,
    ) -> "GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference":
        return typing.cast("GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference", jsii.get(self, "queryOverride"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="pathOverrideInput")
    def path_override_input(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverridePathOverride"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverridePathOverride"], jsii.get(self, "pathOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="queryOverrideInput")
    def query_override_input(
        self,
    ) -> typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride"]:
        return typing.cast(typing.Optional["GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride"], jsii.get(self, "queryOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriOverrideEnforceModeInput")
    def uri_override_enforce_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriOverrideEnforceModeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6188714f52807a7effdd27932b564a773461bbbc31597dc35dbf8c2ea58f06b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15aaf946bac490f7d5c41f40186de0945f743a7e407529341408d631bf4f4aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf16023d112dcb07b1aa9c71d227e2860d850f5573ff195518bf9d325c74a680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uriOverrideEnforceMode")
    def uri_override_enforce_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uriOverrideEnforceMode"))

    @uri_override_enforce_mode.setter
    def uri_override_enforce_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16089e5ebb7f7f8f26c06f22555af3d5758b39ca206ec90d22cc48eead02a1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uriOverrideEnforceMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverride]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f284f8699b639bc78f0f1036aa269a1fa4b96bead5bf08bfa7443550b2b25bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetUriOverridePathOverride",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class GoogleCloudTasksQueueHttpTargetUriOverridePathOverride:
    def __init__(self, *, path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param path: The URI path (e.g., /users/1234). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#path GoogleCloudTasksQueue#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6ae6fe129fc1eec86e6902be9fed37a56f8163234a8afcfacdf12466c1a195)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI path (e.g., /users/1234). Default is an empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#path GoogleCloudTasksQueue#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTargetUriOverridePathOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4979c41fbab702980acf1ace0a5f0938afc0d08f3695d2f2dc703d161077c992)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e79c599f97aa3dcc779a20fe2922075dfc26955d728a7f4ced5bc7475df8ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverridePathOverride]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverridePathOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverridePathOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2190943b671c5ec5c4bc84f801334d3c08e8f8b648cee2165a3d7211f9e8fd2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride",
    jsii_struct_bases=[],
    name_mapping={"query_params": "queryParams"},
)
class GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride:
    def __init__(self, *, query_params: typing.Optional[builtins.str] = None) -> None:
        '''
        :param query_params: The query parameters (e.g., qparam1=123&qparam2=456). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#query_params GoogleCloudTasksQueue#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4561be878d174d3558d47167ec3a391a3c086950e572377fae751f13788031)
            check_type(argname="argument query_params", value=query_params, expected_type=type_hints["query_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_params is not None:
            self._values["query_params"] = query_params

    @builtins.property
    def query_params(self) -> typing.Optional[builtins.str]:
        '''The query parameters (e.g., qparam1=123&qparam2=456). Default is an empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#query_params GoogleCloudTasksQueue#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8609c3c00a39be8f7c3254acdf747eb2c9a2e401043ddb1567b1459010743ede)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQueryParams")
    def reset_query_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParams", []))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryParams"))

    @query_params.setter
    def query_params(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae396420fc1cfeca45b7033914063f6a4c1b767d75a55e929ae0d15c7acd04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3eac0ae8eac8a68794ec73547207df32ff1ba2547f8898d7baaa27257059e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueRateLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_dispatches": "maxConcurrentDispatches",
        "max_dispatches_per_second": "maxDispatchesPerSecond",
    },
)
class GoogleCloudTasksQueueRateLimits:
    def __init__(
        self,
        *,
        max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
        max_dispatches_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_dispatches: The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue. After this threshold has been reached, Cloud Tasks stops dispatching tasks until the number of concurrent requests decreases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_concurrent_dispatches GoogleCloudTasksQueue#max_concurrent_dispatches}
        :param max_dispatches_per_second: The maximum rate at which tasks are dispatched from this queue. If unspecified when the queue is created, Cloud Tasks will pick the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_dispatches_per_second GoogleCloudTasksQueue#max_dispatches_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08cda1a1056d2701c0e49ea0f592f2c085181fd334aa32b797bbac516ac7a68)
            check_type(argname="argument max_concurrent_dispatches", value=max_concurrent_dispatches, expected_type=type_hints["max_concurrent_dispatches"])
            check_type(argname="argument max_dispatches_per_second", value=max_dispatches_per_second, expected_type=type_hints["max_dispatches_per_second"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_dispatches is not None:
            self._values["max_concurrent_dispatches"] = max_concurrent_dispatches
        if max_dispatches_per_second is not None:
            self._values["max_dispatches_per_second"] = max_dispatches_per_second

    @builtins.property
    def max_concurrent_dispatches(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue.

        After this threshold has been
        reached, Cloud Tasks stops dispatching tasks until the number of
        concurrent requests decreases.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_concurrent_dispatches GoogleCloudTasksQueue#max_concurrent_dispatches}
        '''
        result = self._values.get("max_concurrent_dispatches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_dispatches_per_second(self) -> typing.Optional[jsii.Number]:
        '''The maximum rate at which tasks are dispatched from this queue.

        If unspecified when the queue is created, Cloud Tasks will pick the default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_dispatches_per_second GoogleCloudTasksQueue#max_dispatches_per_second}
        '''
        result = self._values.get("max_dispatches_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueRateLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueRateLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueRateLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e8ca7d552941d80c898c6c7c1c1a9253491578fd220a54a1c9d88c2a24352c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxConcurrentDispatches")
    def reset_max_concurrent_dispatches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentDispatches", []))

    @jsii.member(jsii_name="resetMaxDispatchesPerSecond")
    def reset_max_dispatches_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDispatchesPerSecond", []))

    @builtins.property
    @jsii.member(jsii_name="maxBurstSize")
    def max_burst_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBurstSize"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentDispatchesInput")
    def max_concurrent_dispatches_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentDispatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDispatchesPerSecondInput")
    def max_dispatches_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDispatchesPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentDispatches")
    def max_concurrent_dispatches(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentDispatches"))

    @max_concurrent_dispatches.setter
    def max_concurrent_dispatches(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc229f715873a3aaaea154925aa9bfbdea47fa02ed6d1fa1efaa488191579b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentDispatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDispatchesPerSecond")
    def max_dispatches_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDispatchesPerSecond"))

    @max_dispatches_per_second.setter
    def max_dispatches_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be0ef6879ab7355a79bab57dba83ab0ea3cd7c397304da59d9aeaebd9091f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDispatchesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudTasksQueueRateLimits]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueRateLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueRateLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25403e5dbff20524aae48ff0ec9c1d1aa149f65a3e623f5986d62f03912893d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueRetryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "max_backoff": "maxBackoff",
        "max_doublings": "maxDoublings",
        "max_retry_duration": "maxRetryDuration",
        "min_backoff": "minBackoff",
    },
)
class GoogleCloudTasksQueueRetryConfig:
    def __init__(
        self,
        *,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_backoff: typing.Optional[builtins.str] = None,
        max_doublings: typing.Optional[jsii.Number] = None,
        max_retry_duration: typing.Optional[builtins.str] = None,
        min_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_attempts: Number of attempts per task. Cloud Tasks will attempt the task maxAttempts times (that is, if the first attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1. If unspecified when the queue is created, Cloud Tasks will pick the default. -1 indicates unlimited attempts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_attempts GoogleCloudTasksQueue#max_attempts}
        :param max_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_backoff GoogleCloudTasksQueue#max_backoff}
        :param max_doublings: The time between retries will double maxDoublings times. A task's retry interval starts at minBackoff, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoff up to maxAttempts times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_doublings GoogleCloudTasksQueue#max_doublings}
        :param max_retry_duration: If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted. Once maxRetryDuration time has passed and the task has been attempted maxAttempts times, no further attempts will be made and the task will be deleted. If zero, then the task age is unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_retry_duration GoogleCloudTasksQueue#max_retry_duration}
        :param min_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#min_backoff GoogleCloudTasksQueue#min_backoff}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319fdede4bf0c3b76e7cf2aee88d2daf48d045da5ab224c7a306b05cc7feadb3)
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument max_backoff", value=max_backoff, expected_type=type_hints["max_backoff"])
            check_type(argname="argument max_doublings", value=max_doublings, expected_type=type_hints["max_doublings"])
            check_type(argname="argument max_retry_duration", value=max_retry_duration, expected_type=type_hints["max_retry_duration"])
            check_type(argname="argument min_backoff", value=min_backoff, expected_type=type_hints["min_backoff"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if max_backoff is not None:
            self._values["max_backoff"] = max_backoff
        if max_doublings is not None:
            self._values["max_doublings"] = max_doublings
        if max_retry_duration is not None:
            self._values["max_retry_duration"] = max_retry_duration
        if min_backoff is not None:
            self._values["min_backoff"] = min_backoff

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''Number of attempts per task.

        Cloud Tasks will attempt the task maxAttempts times (that is, if
        the first attempt fails, then there will be maxAttempts - 1
        retries). Must be >= -1.

        If unspecified when the queue is created, Cloud Tasks will pick
        the default.

        -1 indicates unlimited attempts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_attempts GoogleCloudTasksQueue#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_backoff(self) -> typing.Optional[builtins.str]:
        '''A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_backoff GoogleCloudTasksQueue#max_backoff}
        '''
        result = self._values.get("max_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_doublings(self) -> typing.Optional[jsii.Number]:
        '''The time between retries will double maxDoublings times.

        A task's retry interval starts at minBackoff, then doubles maxDoublings times,
        then increases linearly, and finally retries retries at intervals of maxBackoff
        up to maxAttempts times.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_doublings GoogleCloudTasksQueue#max_doublings}
        '''
        result = self._values.get("max_doublings")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retry_duration(self) -> typing.Optional[builtins.str]:
        '''If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted.

        Once maxRetryDuration time has passed and the task has
        been attempted maxAttempts times, no further attempts will be
        made and the task will be deleted.

        If zero, then the task age is unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#max_retry_duration GoogleCloudTasksQueue#max_retry_duration}
        '''
        result = self._values.get("max_retry_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_backoff(self) -> typing.Optional[builtins.str]:
        '''A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#min_backoff GoogleCloudTasksQueue#min_backoff}
        '''
        result = self._values.get("min_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueRetryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueRetryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueRetryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7428c686286c8bd444254fcd23a903350ad5d6b820a4120d9767f65cc42ba05e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxAttempts")
    def reset_max_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttempts", []))

    @jsii.member(jsii_name="resetMaxBackoff")
    def reset_max_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBackoff", []))

    @jsii.member(jsii_name="resetMaxDoublings")
    def reset_max_doublings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDoublings", []))

    @jsii.member(jsii_name="resetMaxRetryDuration")
    def reset_max_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetryDuration", []))

    @jsii.member(jsii_name="resetMinBackoff")
    def reset_min_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinBackoff", []))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBackoffInput")
    def max_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDoublingsInput")
    def max_doublings_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDoublingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetryDurationInput")
    def max_retry_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxRetryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minBackoffInput")
    def min_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e951677ffa2c476d086dcec5db40171eba36fa68bf041b5968438b6fc13670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBackoff")
    def max_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxBackoff"))

    @max_backoff.setter
    def max_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0517fafc6ee468156db22fa0b27015e6452bc8d8e5e458d9a50efa98b9afd03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBackoff", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDoublings")
    def max_doublings(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDoublings"))

    @max_doublings.setter
    def max_doublings(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4059fed930e4eea4419e45bffd7698a3dce321ec72e2eba4fad94ccbced7b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDoublings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetryDuration")
    def max_retry_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRetryDuration"))

    @max_retry_duration.setter
    def max_retry_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3d663854a5b66e09f1662798c0788562c962da8ceab9cb2f6cbbeca0e40e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minBackoff")
    def min_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minBackoff"))

    @min_backoff.setter
    def min_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3783cec0c67fdf88c3e569baea38a187fac79ef5d8499afcb0b035c0eacc46ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minBackoff", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudTasksQueueRetryConfig]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueRetryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueRetryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39241218571a0f8ca9733b6ff03dcc6c7553d4a41f826dea1bb7b8f85916469e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueStackdriverLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"sampling_ratio": "samplingRatio"},
)
class GoogleCloudTasksQueueStackdriverLoggingConfig:
    def __init__(self, *, sampling_ratio: jsii.Number) -> None:
        '''
        :param sampling_ratio: Specifies the fraction of operations to write to Stackdriver Logging. This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the default and means that no operations are logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#sampling_ratio GoogleCloudTasksQueue#sampling_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc06141cf6d47e1447111e37296ded173ac46e517bee0c38dbd78640567f472)
            check_type(argname="argument sampling_ratio", value=sampling_ratio, expected_type=type_hints["sampling_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sampling_ratio": sampling_ratio,
        }

    @builtins.property
    def sampling_ratio(self) -> jsii.Number:
        '''Specifies the fraction of operations to write to Stackdriver Logging.

        This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the
        default and means that no operations are logged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#sampling_ratio GoogleCloudTasksQueue#sampling_ratio}
        '''
        result = self._values.get("sampling_ratio")
        assert result is not None, "Required property 'sampling_ratio' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueStackdriverLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueStackdriverLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueStackdriverLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a77b072bf1672199fdbbd934a0e53b4cba17a7fd24b88693b63c43b5da5a112f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="samplingRatioInput")
    def sampling_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingRatio")
    def sampling_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingRatio"))

    @sampling_ratio.setter
    def sampling_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca466085fa26584156fc38e396ddf2de77a872f8fe7fb5d9106a37859f426dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudTasksQueueStackdriverLoggingConfig]:
        return typing.cast(typing.Optional[GoogleCloudTasksQueueStackdriverLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudTasksQueueStackdriverLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a49e7d00e7fb1cadf1d69f540f583f464e23a4bd5b1197ed6ebcb01295dc15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudTasksQueueTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#create GoogleCloudTasksQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#delete GoogleCloudTasksQueue#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#update GoogleCloudTasksQueue#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0957ed95acfb3aa0eaec0af686c23721291054042af473034e300aca8e0031)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#create GoogleCloudTasksQueue#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#delete GoogleCloudTasksQueue#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_tasks_queue#update GoogleCloudTasksQueue#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudTasksQueueTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudTasksQueueTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudTasksQueue.GoogleCloudTasksQueueTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec1a7cfc686e463f8067b38a9a90c5a5cf57b8c333b451de374fce2ec68556e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2725c01034c850204643f8b6804d0f214203199208bed94d43430a1e63bb4f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75c7295259a2a3a32b4f6dafe0eed6fa7f1f7f49cde309dcf7146ec6ed3905f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0bed431536b787004dec119f4493b4dd08912d79500363d10f50be371222db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bff66a35c8a65385df799234419befaffc662a6d323fc0d6ee14cabaceb36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudTasksQueue",
    "GoogleCloudTasksQueueAppEngineRoutingOverride",
    "GoogleCloudTasksQueueAppEngineRoutingOverrideOutputReference",
    "GoogleCloudTasksQueueConfig",
    "GoogleCloudTasksQueueHttpTarget",
    "GoogleCloudTasksQueueHttpTargetHeaderOverrides",
    "GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader",
    "GoogleCloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference",
    "GoogleCloudTasksQueueHttpTargetHeaderOverridesList",
    "GoogleCloudTasksQueueHttpTargetHeaderOverridesOutputReference",
    "GoogleCloudTasksQueueHttpTargetOauthToken",
    "GoogleCloudTasksQueueHttpTargetOauthTokenOutputReference",
    "GoogleCloudTasksQueueHttpTargetOidcToken",
    "GoogleCloudTasksQueueHttpTargetOidcTokenOutputReference",
    "GoogleCloudTasksQueueHttpTargetOutputReference",
    "GoogleCloudTasksQueueHttpTargetUriOverride",
    "GoogleCloudTasksQueueHttpTargetUriOverrideOutputReference",
    "GoogleCloudTasksQueueHttpTargetUriOverridePathOverride",
    "GoogleCloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference",
    "GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride",
    "GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference",
    "GoogleCloudTasksQueueRateLimits",
    "GoogleCloudTasksQueueRateLimitsOutputReference",
    "GoogleCloudTasksQueueRetryConfig",
    "GoogleCloudTasksQueueRetryConfigOutputReference",
    "GoogleCloudTasksQueueStackdriverLoggingConfig",
    "GoogleCloudTasksQueueStackdriverLoggingConfigOutputReference",
    "GoogleCloudTasksQueueTimeouts",
    "GoogleCloudTasksQueueTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9cc2dcc2c493c66f584508e1cee8ed35375436ec3571fb08b6edba953114811b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    app_engine_routing_override: typing.Optional[typing.Union[GoogleCloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    http_target: typing.Optional[typing.Union[GoogleCloudTasksQueueHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limits: typing.Optional[typing.Union[GoogleCloudTasksQueueRateLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_config: typing.Optional[typing.Union[GoogleCloudTasksQueueRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stackdriver_logging_config: typing.Optional[typing.Union[GoogleCloudTasksQueueStackdriverLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudTasksQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e604894383f7c3bc0e6be8e8fcb95e5a3308e7559c693532354ecfc4f0578df6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42d04b862f2cf547c0c393e30961915be51b0b7a67e907772a1733685c304de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008b71a9a2ddcfd1576b755119e31bded29aacf43b487da6b348d9ce5ba903d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9198f6ec5b32a0006965d6cab54507cad51860099d574b44feb2609e39480b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f98aec4a9d068488ef31bd5fb496de41804c6946aa5758a9701d496443e920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e1475321db8f04d08f81bee7e4b1993e9c12e19cb51f6401c11f1ede7cbe11(
    *,
    instance: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f8eda373ebd32300c8e38d4978a12ee2d8c36d2c564a05ece07e79aca90bb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23358fbfcdf6cc5cf396e7b53c2b79a36ee05fd06601a1e1d75ae608231655ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5d8811fd0039e621b0074b3282c9e9332f67c7f522cef02ea678c79632ef3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0807b1928c3e2a3b20ec7cb5331e1a46c3f581849b89eb6ca98449120f56b67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b4d138c0d1706eeb92686d43ea22e0f96235c114d83f7160001bcff13e96ef(
    value: typing.Optional[GoogleCloudTasksQueueAppEngineRoutingOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900bc1fdcf9b3e4b1c789eb4391746d40a41bb2bb41f80fbef14fe9e113682e0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    app_engine_routing_override: typing.Optional[typing.Union[GoogleCloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    http_target: typing.Optional[typing.Union[GoogleCloudTasksQueueHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limits: typing.Optional[typing.Union[GoogleCloudTasksQueueRateLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_config: typing.Optional[typing.Union[GoogleCloudTasksQueueRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stackdriver_logging_config: typing.Optional[typing.Union[GoogleCloudTasksQueueStackdriverLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudTasksQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d292a674a4fa9953f26e870f51c3bbd9776a599616ff4c5fbacba415e493644(
    *,
    header_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudTasksQueueHttpTargetHeaderOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_method: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[typing.Union[GoogleCloudTasksQueueHttpTargetOauthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    oidc_token: typing.Optional[typing.Union[GoogleCloudTasksQueueHttpTargetOidcToken, typing.Dict[builtins.str, typing.Any]]] = None,
    uri_override: typing.Optional[typing.Union[GoogleCloudTasksQueueHttpTargetUriOverride, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6c03c5f3d7c3c8c64c62be7f305ce0691e0f6faefe1b7ea97da1cc23026516(
    *,
    header: typing.Union[GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe4207c19fc0f4ba2b55fd75ee7a8ebd3b5b63381ba6d98d4efe26b49bb445b(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b357d5d70742a7feb8d99e0b02503a86e3fcb5055c3085fd2cc6e9ff88f26a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e831f2e381ced98e39e8b3c733f627a9478c67ca7d6f973731a61a06ebd865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872b9130d9dcf43d6ecadc82ef8bc1aa6689e913d090adc0bdf1b2ebf12ba243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0184c3e3c623564757f818b8a53768c2294b1210da4d47dfca19289976e4b3fb(
    value: typing.Optional[GoogleCloudTasksQueueHttpTargetHeaderOverridesHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48157131a266bad5fe1033b6a387d2624b651e61f9a991f915ca4af46bc71bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0aae4a05e8b6568fcf29d2d421bceb5feb12f3cac493cb9c3b280cae9c465a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d56f0ccf0fee26fa2dc43da43ac780ad7c67143bbd39587c6ce94dd0e4f03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df43ca7f09a61718dac6c159a1c36638c7674adcdd4ba5bdfb988e8482fad919(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54dfccd8ef1150a3eed5b0e46f8301cf10cbd4f8f35b0a411cf0cb29cdffb506(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39685bbed64f9f73c330c3dcf6258cd486f5b48ffb8756b3a451288cd85f8f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudTasksQueueHttpTargetHeaderOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f72060532b8043c17fa3c563710aa6b1708ef853f611657a870a50bfe47aa99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16719e9dc1cbef29452fa41936080d9c8f73f290db3f1b74fd2e632ceee27ae4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueHttpTargetHeaderOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ce4a01af64a6def75a376ef56c1a487023882faac763804d342dca22677244(
    *,
    service_account_email: builtins.str,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f84cccbfa2d1bb5bbcc5d05bcdf09a51b118bfb10bf67c65cc4b060105c9e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c389df2d0dd18fbaa0003e94f6eb48cf37b89d7c0da0086f7d00846a093c2057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c75cdc9087313c424b4c005b2b3d3aea8fb06b6cb7f8eb95f9462cea596fff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3673c3fd4f754b2589bb877369e8b2e20ec536fa7fff0cb6136a849415b48f91(
    value: typing.Optional[GoogleCloudTasksQueueHttpTargetOauthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c86f0c1ac3213e0c472a6e4468c0be7607bf504bddc450d467be3b5aa8bee8(
    *,
    service_account_email: builtins.str,
    audience: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc16b2151368b4b993a03bfe4200d5e789a8b824b9da392706613ef5cfd475f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff248f7cff95166e0f65576326012914b3e5401e8fd59f618dcb85030c51c311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26725d20559629cdf9d692d0fb948653463203d403bd078ec1a67ffcae511bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a249aaf00307915e0cb22ffc02c35c8dba2a0511d7669f43543bb87d8cb2c2e8(
    value: typing.Optional[GoogleCloudTasksQueueHttpTargetOidcToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b562f4fc4b38e717614b3e7bd27eac46c188d20954e7ecd26c9b4ac891a3f1d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40026c8f878021517334191665c0d674dc8dcf91d02c6e1931f9e7417d59a15e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudTasksQueueHttpTargetHeaderOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdf9d7b110be0a82386a188bf65ae91901297546818ab8f3049d115a9b88ddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3660cb5f3905fac8d60413f9e48903f0024f219224552777f75969be3ebb0d9(
    value: typing.Optional[GoogleCloudTasksQueueHttpTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aef4039afd5adde50b07bd1c902484c9ea2cea12e3a5a936b34204479936e48(
    *,
    host: typing.Optional[builtins.str] = None,
    path_override: typing.Optional[typing.Union[GoogleCloudTasksQueueHttpTargetUriOverridePathOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[builtins.str] = None,
    query_override: typing.Optional[typing.Union[GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    scheme: typing.Optional[builtins.str] = None,
    uri_override_enforce_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb44303fd5af80aac8d3173a8bd996b7aab2ec9a7bd4dedd632af420b7e71129(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6188714f52807a7effdd27932b564a773461bbbc31597dc35dbf8c2ea58f06b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15aaf946bac490f7d5c41f40186de0945f743a7e407529341408d631bf4f4aad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf16023d112dcb07b1aa9c71d227e2860d850f5573ff195518bf9d325c74a680(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16089e5ebb7f7f8f26c06f22555af3d5758b39ca206ec90d22cc48eead02a1d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f284f8699b639bc78f0f1036aa269a1fa4b96bead5bf08bfa7443550b2b25bc3(
    value: typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6ae6fe129fc1eec86e6902be9fed37a56f8163234a8afcfacdf12466c1a195(
    *,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4979c41fbab702980acf1ace0a5f0938afc0d08f3695d2f2dc703d161077c992(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e79c599f97aa3dcc779a20fe2922075dfc26955d728a7f4ced5bc7475df8ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2190943b671c5ec5c4bc84f801334d3c08e8f8b648cee2165a3d7211f9e8fd2e(
    value: typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverridePathOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4561be878d174d3558d47167ec3a391a3c086950e572377fae751f13788031(
    *,
    query_params: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8609c3c00a39be8f7c3254acdf747eb2c9a2e401043ddb1567b1459010743ede(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae396420fc1cfeca45b7033914063f6a4c1b767d75a55e929ae0d15c7acd04a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3eac0ae8eac8a68794ec73547207df32ff1ba2547f8898d7baaa27257059e6(
    value: typing.Optional[GoogleCloudTasksQueueHttpTargetUriOverrideQueryOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08cda1a1056d2701c0e49ea0f592f2c085181fd334aa32b797bbac516ac7a68(
    *,
    max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
    max_dispatches_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8ca7d552941d80c898c6c7c1c1a9253491578fd220a54a1c9d88c2a24352c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc229f715873a3aaaea154925aa9bfbdea47fa02ed6d1fa1efaa488191579b3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be0ef6879ab7355a79bab57dba83ab0ea3cd7c397304da59d9aeaebd9091f80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25403e5dbff20524aae48ff0ec9c1d1aa149f65a3e623f5986d62f03912893d(
    value: typing.Optional[GoogleCloudTasksQueueRateLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319fdede4bf0c3b76e7cf2aee88d2daf48d045da5ab224c7a306b05cc7feadb3(
    *,
    max_attempts: typing.Optional[jsii.Number] = None,
    max_backoff: typing.Optional[builtins.str] = None,
    max_doublings: typing.Optional[jsii.Number] = None,
    max_retry_duration: typing.Optional[builtins.str] = None,
    min_backoff: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7428c686286c8bd444254fcd23a903350ad5d6b820a4120d9767f65cc42ba05e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e951677ffa2c476d086dcec5db40171eba36fa68bf041b5968438b6fc13670(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0517fafc6ee468156db22fa0b27015e6452bc8d8e5e458d9a50efa98b9afd03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4059fed930e4eea4419e45bffd7698a3dce321ec72e2eba4fad94ccbced7b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3d663854a5b66e09f1662798c0788562c962da8ceab9cb2f6cbbeca0e40e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3783cec0c67fdf88c3e569baea38a187fac79ef5d8499afcb0b035c0eacc46ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39241218571a0f8ca9733b6ff03dcc6c7553d4a41f826dea1bb7b8f85916469e(
    value: typing.Optional[GoogleCloudTasksQueueRetryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc06141cf6d47e1447111e37296ded173ac46e517bee0c38dbd78640567f472(
    *,
    sampling_ratio: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77b072bf1672199fdbbd934a0e53b4cba17a7fd24b88693b63c43b5da5a112f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca466085fa26584156fc38e396ddf2de77a872f8fe7fb5d9106a37859f426dc3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a49e7d00e7fb1cadf1d69f540f583f464e23a4bd5b1197ed6ebcb01295dc15(
    value: typing.Optional[GoogleCloudTasksQueueStackdriverLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0957ed95acfb3aa0eaec0af686c23721291054042af473034e300aca8e0031(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1a7cfc686e463f8067b38a9a90c5a5cf57b8c333b451de374fce2ec68556e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2725c01034c850204643f8b6804d0f214203199208bed94d43430a1e63bb4f1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75c7295259a2a3a32b4f6dafe0eed6fa7f1f7f49cde309dcf7146ec6ed3905f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0bed431536b787004dec119f4493b4dd08912d79500363d10f50be371222db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bff66a35c8a65385df799234419befaffc662a6d323fc0d6ee14cabaceb36c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudTasksQueueTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
