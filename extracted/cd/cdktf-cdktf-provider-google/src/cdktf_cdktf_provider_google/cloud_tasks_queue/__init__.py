r'''
# `google_cloud_tasks_queue`

Refer to the Terraform Registry for docs: [`google_cloud_tasks_queue`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue).
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


class CloudTasksQueue(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueue",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue google_cloud_tasks_queue}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        app_engine_routing_override: typing.Optional[typing.Union["CloudTasksQueueAppEngineRoutingOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        http_target: typing.Optional[typing.Union["CloudTasksQueueHttpTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limits: typing.Optional[typing.Union["CloudTasksQueueRateLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_config: typing.Optional[typing.Union["CloudTasksQueueRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stackdriver_logging_config: typing.Optional[typing.Union["CloudTasksQueueStackdriverLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudTasksQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue google_cloud_tasks_queue} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the queue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#location CloudTasksQueue#location}
        :param app_engine_routing_override: app_engine_routing_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#app_engine_routing_override CloudTasksQueue#app_engine_routing_override}
        :param http_target: http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#http_target CloudTasksQueue#http_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#id CloudTasksQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The queue name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#name CloudTasksQueue#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#project CloudTasksQueue#project}.
        :param rate_limits: rate_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#rate_limits CloudTasksQueue#rate_limits}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#retry_config CloudTasksQueue#retry_config}
        :param stackdriver_logging_config: stackdriver_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#stackdriver_logging_config CloudTasksQueue#stackdriver_logging_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#timeouts CloudTasksQueue#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4b65c7c98de529a56114659ee7eea05c423eb2573bf13ef256640ec5537628)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudTasksQueueConfig(
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
        '''Generates CDKTF code for importing a CloudTasksQueue resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudTasksQueue to import.
        :param import_from_id: The id of the existing CloudTasksQueue that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudTasksQueue to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4167d1fba00044e6b8fe4fae83a8527797864033d79b1f15c20ff69f66e5c06)
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
        :param instance: App instance. By default, the task is sent to an instance which is available when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#instance CloudTasksQueue#instance}
        :param service: App service. By default, the task is sent to the service which is the default service when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service CloudTasksQueue#service}
        :param version: App version. By default, the task is sent to the version which is the default version when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#version CloudTasksQueue#version}
        '''
        value = CloudTasksQueueAppEngineRoutingOverride(
            instance=instance, service=service, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putAppEngineRoutingOverride", [value]))

    @jsii.member(jsii_name="putHttpTarget")
    def put_http_target(
        self,
        *,
        header_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudTasksQueueHttpTargetHeaderOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[typing.Union["CloudTasksQueueHttpTargetOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["CloudTasksQueueHttpTargetOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        uri_override: typing.Optional[typing.Union["CloudTasksQueueHttpTargetUriOverride", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_overrides: header_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#header_overrides CloudTasksQueue#header_overrides}
        :param http_method: The HTTP method to use for the request. When specified, it overrides HttpRequest for the task. Note that if the value is set to GET the body of the task will be ignored at execution time. Possible values: ["HTTP_METHOD_UNSPECIFIED", "POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#http_method CloudTasksQueue#http_method}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#oauth_token CloudTasksQueue#oauth_token}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#oidc_token CloudTasksQueue#oidc_token}
        :param uri_override: uri_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#uri_override CloudTasksQueue#uri_override}
        '''
        value = CloudTasksQueueHttpTarget(
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
        :param max_concurrent_dispatches: The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue. After this threshold has been reached, Cloud Tasks stops dispatching tasks until the number of concurrent requests decreases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_concurrent_dispatches CloudTasksQueue#max_concurrent_dispatches}
        :param max_dispatches_per_second: The maximum rate at which tasks are dispatched from this queue. If unspecified when the queue is created, Cloud Tasks will pick the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_dispatches_per_second CloudTasksQueue#max_dispatches_per_second}
        '''
        value = CloudTasksQueueRateLimits(
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
        :param max_attempts: Number of attempts per task. Cloud Tasks will attempt the task maxAttempts times (that is, if the first attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1. If unspecified when the queue is created, Cloud Tasks will pick the default. -1 indicates unlimited attempts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_attempts CloudTasksQueue#max_attempts}
        :param max_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_backoff CloudTasksQueue#max_backoff}
        :param max_doublings: The time between retries will double maxDoublings times. A task's retry interval starts at minBackoff, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoff up to maxAttempts times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_doublings CloudTasksQueue#max_doublings}
        :param max_retry_duration: If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted. Once maxRetryDuration time has passed and the task has been attempted maxAttempts times, no further attempts will be made and the task will be deleted. If zero, then the task age is unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_retry_duration CloudTasksQueue#max_retry_duration}
        :param min_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#min_backoff CloudTasksQueue#min_backoff}
        '''
        value = CloudTasksQueueRetryConfig(
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
        :param sampling_ratio: Specifies the fraction of operations to write to Stackdriver Logging. This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the default and means that no operations are logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#sampling_ratio CloudTasksQueue#sampling_ratio}
        '''
        value = CloudTasksQueueStackdriverLoggingConfig(sampling_ratio=sampling_ratio)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#create CloudTasksQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#delete CloudTasksQueue#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#update CloudTasksQueue#update}.
        '''
        value = CloudTasksQueueTimeouts(create=create, delete=delete, update=update)

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
    ) -> "CloudTasksQueueAppEngineRoutingOverrideOutputReference":
        return typing.cast("CloudTasksQueueAppEngineRoutingOverrideOutputReference", jsii.get(self, "appEngineRoutingOverride"))

    @builtins.property
    @jsii.member(jsii_name="httpTarget")
    def http_target(self) -> "CloudTasksQueueHttpTargetOutputReference":
        return typing.cast("CloudTasksQueueHttpTargetOutputReference", jsii.get(self, "httpTarget"))

    @builtins.property
    @jsii.member(jsii_name="rateLimits")
    def rate_limits(self) -> "CloudTasksQueueRateLimitsOutputReference":
        return typing.cast("CloudTasksQueueRateLimitsOutputReference", jsii.get(self, "rateLimits"))

    @builtins.property
    @jsii.member(jsii_name="retryConfig")
    def retry_config(self) -> "CloudTasksQueueRetryConfigOutputReference":
        return typing.cast("CloudTasksQueueRetryConfigOutputReference", jsii.get(self, "retryConfig"))

    @builtins.property
    @jsii.member(jsii_name="stackdriverLoggingConfig")
    def stackdriver_logging_config(
        self,
    ) -> "CloudTasksQueueStackdriverLoggingConfigOutputReference":
        return typing.cast("CloudTasksQueueStackdriverLoggingConfigOutputReference", jsii.get(self, "stackdriverLoggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudTasksQueueTimeoutsOutputReference":
        return typing.cast("CloudTasksQueueTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appEngineRoutingOverrideInput")
    def app_engine_routing_override_input(
        self,
    ) -> typing.Optional["CloudTasksQueueAppEngineRoutingOverride"]:
        return typing.cast(typing.Optional["CloudTasksQueueAppEngineRoutingOverride"], jsii.get(self, "appEngineRoutingOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="httpTargetInput")
    def http_target_input(self) -> typing.Optional["CloudTasksQueueHttpTarget"]:
        return typing.cast(typing.Optional["CloudTasksQueueHttpTarget"], jsii.get(self, "httpTargetInput"))

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
    def rate_limits_input(self) -> typing.Optional["CloudTasksQueueRateLimits"]:
        return typing.cast(typing.Optional["CloudTasksQueueRateLimits"], jsii.get(self, "rateLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryConfigInput")
    def retry_config_input(self) -> typing.Optional["CloudTasksQueueRetryConfig"]:
        return typing.cast(typing.Optional["CloudTasksQueueRetryConfig"], jsii.get(self, "retryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stackdriverLoggingConfigInput")
    def stackdriver_logging_config_input(
        self,
    ) -> typing.Optional["CloudTasksQueueStackdriverLoggingConfig"]:
        return typing.cast(typing.Optional["CloudTasksQueueStackdriverLoggingConfig"], jsii.get(self, "stackdriverLoggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudTasksQueueTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudTasksQueueTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb26345cf52f11dcd4ef850ccfa20133568374589e76ce84de78fe88a2f9ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7f4ba3031fd0ec8200ea71bf27105a44f16b2568c2335ecf54309d6b53b2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8c1aedb20aa05e746efc16a9873fc595c872b96889616a6c0348d8866d74be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7b2a24d68b223fa27dcd372bce4798813f55128834c98a42d2451d52c50d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueAppEngineRoutingOverride",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance", "service": "service", "version": "version"},
)
class CloudTasksQueueAppEngineRoutingOverride:
    def __init__(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: App instance. By default, the task is sent to an instance which is available when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#instance CloudTasksQueue#instance}
        :param service: App service. By default, the task is sent to the service which is the default service when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service CloudTasksQueue#service}
        :param version: App version. By default, the task is sent to the version which is the default version when the task is attempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#version CloudTasksQueue#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1c48bc18dd9d5d3d3bad0ae065a1068d71e9d3ba9cccd7e5b48ecee7e3a55f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#instance CloudTasksQueue#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''App service.

        By default, the task is sent to the service which is the default service when the task is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service CloudTasksQueue#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''App version.

        By default, the task is sent to the version which is the default version when the task is attempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#version CloudTasksQueue#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueAppEngineRoutingOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueAppEngineRoutingOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueAppEngineRoutingOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5294b28a75106c79c8d69f7d9c4052e0ef459a31fc71dbc1d983fb0ef4f44cb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f86b4a0660cdc8001b91f44bbc48bfd94884ad95c3feb2deea31b8af2d02e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f739c7806538573b239c8b622b0915e8f2911bdabc9398fc3d27bf81cbb3486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891dc54305d15ea2ed9d7f476f32398dc7fb4f82edab0cbe988df848ade8b745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudTasksQueueAppEngineRoutingOverride]:
        return typing.cast(typing.Optional[CloudTasksQueueAppEngineRoutingOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueAppEngineRoutingOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e47552dc050adf038e62f281feabaef42512ed8a384293aafed1e0ae3023a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueConfig",
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
class CloudTasksQueueConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_engine_routing_override: typing.Optional[typing.Union[CloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
        http_target: typing.Optional[typing.Union["CloudTasksQueueHttpTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rate_limits: typing.Optional[typing.Union["CloudTasksQueueRateLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_config: typing.Optional[typing.Union["CloudTasksQueueRetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stackdriver_logging_config: typing.Optional[typing.Union["CloudTasksQueueStackdriverLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudTasksQueueTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the queue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#location CloudTasksQueue#location}
        :param app_engine_routing_override: app_engine_routing_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#app_engine_routing_override CloudTasksQueue#app_engine_routing_override}
        :param http_target: http_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#http_target CloudTasksQueue#http_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#id CloudTasksQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The queue name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#name CloudTasksQueue#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#project CloudTasksQueue#project}.
        :param rate_limits: rate_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#rate_limits CloudTasksQueue#rate_limits}
        :param retry_config: retry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#retry_config CloudTasksQueue#retry_config}
        :param stackdriver_logging_config: stackdriver_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#stackdriver_logging_config CloudTasksQueue#stackdriver_logging_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#timeouts CloudTasksQueue#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(app_engine_routing_override, dict):
            app_engine_routing_override = CloudTasksQueueAppEngineRoutingOverride(**app_engine_routing_override)
        if isinstance(http_target, dict):
            http_target = CloudTasksQueueHttpTarget(**http_target)
        if isinstance(rate_limits, dict):
            rate_limits = CloudTasksQueueRateLimits(**rate_limits)
        if isinstance(retry_config, dict):
            retry_config = CloudTasksQueueRetryConfig(**retry_config)
        if isinstance(stackdriver_logging_config, dict):
            stackdriver_logging_config = CloudTasksQueueStackdriverLoggingConfig(**stackdriver_logging_config)
        if isinstance(timeouts, dict):
            timeouts = CloudTasksQueueTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72ca0923f5716abfb32b718c95c8c961a7d2deae111cd2080cabb7dfe70971f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#location CloudTasksQueue#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_routing_override(
        self,
    ) -> typing.Optional[CloudTasksQueueAppEngineRoutingOverride]:
        '''app_engine_routing_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#app_engine_routing_override CloudTasksQueue#app_engine_routing_override}
        '''
        result = self._values.get("app_engine_routing_override")
        return typing.cast(typing.Optional[CloudTasksQueueAppEngineRoutingOverride], result)

    @builtins.property
    def http_target(self) -> typing.Optional["CloudTasksQueueHttpTarget"]:
        '''http_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#http_target CloudTasksQueue#http_target}
        '''
        result = self._values.get("http_target")
        return typing.cast(typing.Optional["CloudTasksQueueHttpTarget"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#id CloudTasksQueue#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The queue name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#name CloudTasksQueue#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#project CloudTasksQueue#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limits(self) -> typing.Optional["CloudTasksQueueRateLimits"]:
        '''rate_limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#rate_limits CloudTasksQueue#rate_limits}
        '''
        result = self._values.get("rate_limits")
        return typing.cast(typing.Optional["CloudTasksQueueRateLimits"], result)

    @builtins.property
    def retry_config(self) -> typing.Optional["CloudTasksQueueRetryConfig"]:
        '''retry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#retry_config CloudTasksQueue#retry_config}
        '''
        result = self._values.get("retry_config")
        return typing.cast(typing.Optional["CloudTasksQueueRetryConfig"], result)

    @builtins.property
    def stackdriver_logging_config(
        self,
    ) -> typing.Optional["CloudTasksQueueStackdriverLoggingConfig"]:
        '''stackdriver_logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#stackdriver_logging_config CloudTasksQueue#stackdriver_logging_config}
        '''
        result = self._values.get("stackdriver_logging_config")
        return typing.cast(typing.Optional["CloudTasksQueueStackdriverLoggingConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudTasksQueueTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#timeouts CloudTasksQueue#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudTasksQueueTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTarget",
    jsii_struct_bases=[],
    name_mapping={
        "header_overrides": "headerOverrides",
        "http_method": "httpMethod",
        "oauth_token": "oauthToken",
        "oidc_token": "oidcToken",
        "uri_override": "uriOverride",
    },
)
class CloudTasksQueueHttpTarget:
    def __init__(
        self,
        *,
        header_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudTasksQueueHttpTargetHeaderOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[typing.Union["CloudTasksQueueHttpTargetOauthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["CloudTasksQueueHttpTargetOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        uri_override: typing.Optional[typing.Union["CloudTasksQueueHttpTargetUriOverride", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_overrides: header_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#header_overrides CloudTasksQueue#header_overrides}
        :param http_method: The HTTP method to use for the request. When specified, it overrides HttpRequest for the task. Note that if the value is set to GET the body of the task will be ignored at execution time. Possible values: ["HTTP_METHOD_UNSPECIFIED", "POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#http_method CloudTasksQueue#http_method}
        :param oauth_token: oauth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#oauth_token CloudTasksQueue#oauth_token}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#oidc_token CloudTasksQueue#oidc_token}
        :param uri_override: uri_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#uri_override CloudTasksQueue#uri_override}
        '''
        if isinstance(oauth_token, dict):
            oauth_token = CloudTasksQueueHttpTargetOauthToken(**oauth_token)
        if isinstance(oidc_token, dict):
            oidc_token = CloudTasksQueueHttpTargetOidcToken(**oidc_token)
        if isinstance(uri_override, dict):
            uri_override = CloudTasksQueueHttpTargetUriOverride(**uri_override)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df407753f5711fe89253efdef784bb2bb654c70f76cd1a5c058d7262b26f135)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudTasksQueueHttpTargetHeaderOverrides"]]]:
        '''header_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#header_overrides CloudTasksQueue#header_overrides}
        '''
        result = self._values.get("header_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudTasksQueueHttpTargetHeaderOverrides"]]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''The HTTP method to use for the request.

        When specified, it overrides HttpRequest for the task.
        Note that if the value is set to GET the body of the task will be ignored at execution time. Possible values: ["HTTP_METHOD_UNSPECIFIED", "POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#http_method CloudTasksQueue#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional["CloudTasksQueueHttpTargetOauthToken"]:
        '''oauth_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#oauth_token CloudTasksQueue#oauth_token}
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetOauthToken"], result)

    @builtins.property
    def oidc_token(self) -> typing.Optional["CloudTasksQueueHttpTargetOidcToken"]:
        '''oidc_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#oidc_token CloudTasksQueue#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetOidcToken"], result)

    @builtins.property
    def uri_override(self) -> typing.Optional["CloudTasksQueueHttpTargetUriOverride"]:
        '''uri_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#uri_override CloudTasksQueue#uri_override}
        '''
        result = self._values.get("uri_override")
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetUriOverride"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetHeaderOverrides",
    jsii_struct_bases=[],
    name_mapping={"header": "header"},
)
class CloudTasksQueueHttpTargetHeaderOverrides:
    def __init__(
        self,
        *,
        header: typing.Union["CloudTasksQueueHttpTargetHeaderOverridesHeader", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#header CloudTasksQueue#header}
        '''
        if isinstance(header, dict):
            header = CloudTasksQueueHttpTargetHeaderOverridesHeader(**header)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04204ce0dd466ab5eb3ab29834d0712b3a25e9ea906a22d2c3d3a8e6e1e7d1c4)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
        }

    @builtins.property
    def header(self) -> "CloudTasksQueueHttpTargetHeaderOverridesHeader":
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#header CloudTasksQueue#header}
        '''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast("CloudTasksQueueHttpTargetHeaderOverridesHeader", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTargetHeaderOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetHeaderOverridesHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CloudTasksQueueHttpTargetHeaderOverridesHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The Key of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#key CloudTasksQueue#key}
        :param value: The Value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#value CloudTasksQueue#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d250969d59349dc3d57d0483815f2f2c7c4ee22a3bff4a36338794105ba14a63)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''The Key of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#key CloudTasksQueue#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The Value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#value CloudTasksQueue#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTargetHeaderOverridesHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f36f47cf3c59ebd6f78edf19e21f453b452bf5acea4b111b52df30a03e20e95c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1941f4f1a6de40f752906a178ba710541114edd294a53161e0a6b2cfe5e0b175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528f1a826ba30e2da4726754fd0cd43d7f6363319ea111ead56b3325ffe6503f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudTasksQueueHttpTargetHeaderOverridesHeader]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetHeaderOverridesHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueHttpTargetHeaderOverridesHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3881a7d0103ee209e7ada8280f970c10a8fcb2e116ff77b923e627c9f0e7072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudTasksQueueHttpTargetHeaderOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetHeaderOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db5da5f5a6030ff44c2b04908a0fb44ab48df689a1a2419a998d79c965360c46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudTasksQueueHttpTargetHeaderOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1e3f26049c8bead0343a4ae79c872d94a7ed799a18b21281ae98f934d7b7e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudTasksQueueHttpTargetHeaderOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3d995789828b727a2b85d463a27aa4aa02b3cdafe3cf73f0cdda7a550216a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63a40ca800475f2b4d885fbdc4d3869e879263c688fd6c345532e65343683df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7c0f4e16d49355fee1be8d018eda547de4a35f3e1e68a6e4fa9901f5ff0a7a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudTasksQueueHttpTargetHeaderOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudTasksQueueHttpTargetHeaderOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudTasksQueueHttpTargetHeaderOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596a75c494db0c701c8c5ec99b46be0e1e4d822407e4d121c5ede7b2ee9ac3b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudTasksQueueHttpTargetHeaderOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetHeaderOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8368ed7d4e19f5b92f8d0af4ff6ccc62cc57e70ff9b84ee8f70eaba317648a3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The Key of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#key CloudTasksQueue#key}
        :param value: The Value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#value CloudTasksQueue#value}
        '''
        value_ = CloudTasksQueueHttpTargetHeaderOverridesHeader(key=key, value=value)

        return typing.cast(None, jsii.invoke(self, "putHeader", [value_]))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> CloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference:
        return typing.cast(CloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[CloudTasksQueueHttpTargetHeaderOverridesHeader]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetHeaderOverridesHeader], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueHttpTargetHeaderOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueHttpTargetHeaderOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueHttpTargetHeaderOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93e31b9a844eb8afa794ba3304d28cbfddb88ad1c8055a949fa7db3e492bbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetOauthToken",
    jsii_struct_bases=[],
    name_mapping={"service_account_email": "serviceAccountEmail", "scope": "scope"},
)
class CloudTasksQueueHttpTargetOauthToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service_account_email CloudTasksQueue#service_account_email}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#scope CloudTasksQueue#scope}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982969fe9c72e078326f006aad77b8f784fa9131c8236c955235ca106b2206a5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service_account_email CloudTasksQueue#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#scope CloudTasksQueue#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTargetOauthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueHttpTargetOauthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetOauthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f59789eea6f56b26de87ac464319b6aabef92fe425170811f2fa6590565ff7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f2fc1c6c4109090c474d95936109df10b786d17a8820bc3b204265e00bf8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd7b6d9e4ecc2f1135cd75acb5814f9a2df70e0c6759581af240f6f2c29d333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueHttpTargetOauthToken]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetOauthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueHttpTargetOauthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98a8614931c311a8b2ffcb961d961b3f8f2f19c7c52a115401da754fc012b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetOidcToken",
    jsii_struct_bases=[],
    name_mapping={
        "service_account_email": "serviceAccountEmail",
        "audience": "audience",
    },
)
class CloudTasksQueueHttpTargetOidcToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating OIDC token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service_account_email CloudTasksQueue#service_account_email}
        :param audience: Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#audience CloudTasksQueue#audience}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdde329033daacafb8afacf376cdaec7a008122f0ac76397a97598fc868e2236)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service_account_email CloudTasksQueue#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#audience CloudTasksQueue#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTargetOidcToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueHttpTargetOidcTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetOidcTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08648aac8e36b779cc58c9f95e6a4c92ab98515a0718edf1326429524a1525ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cadd46577ed0deb6b24b5029e236114e31b405deab99f3b6f671320fea6bad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c51e2e4c1647b18abba3658dae722cc2df60b8b51c6de070f2b73923eeeb08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueHttpTargetOidcToken]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetOidcToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueHttpTargetOidcToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abfcd46afa9530fd98b505fc965318b0dcbb5d0644f1fbaf27899ede35b68f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudTasksQueueHttpTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae7e38e8fecdefae7304b0ebe7bb73318299ca835f7ad227c0f0bb34b13e4c02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaderOverrides")
    def put_header_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudTasksQueueHttpTargetHeaderOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70f00039233df0d6c6676e38e9031c4ca36f9c3562c7deb381d70833ade0466)
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
        :param service_account_email: Service account email to be used for generating OAuth token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service_account_email CloudTasksQueue#service_account_email}
        :param scope: OAuth scope to be used for generating OAuth access token. If not specified, "https://www.googleapis.com/auth/cloud-platform" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#scope CloudTasksQueue#scope}
        '''
        value = CloudTasksQueueHttpTargetOauthToken(
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
        :param service_account_email: Service account email to be used for generating OIDC token. The service account must be within the same project as the queue. The caller must have iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#service_account_email CloudTasksQueue#service_account_email}
        :param audience: Audience to be used when generating OIDC token. If not specified, the URI specified in target will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#audience CloudTasksQueue#audience}
        '''
        value = CloudTasksQueueHttpTargetOidcToken(
            service_account_email=service_account_email, audience=audience
        )

        return typing.cast(None, jsii.invoke(self, "putOidcToken", [value]))

    @jsii.member(jsii_name="putUriOverride")
    def put_uri_override(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        path_override: typing.Optional[typing.Union["CloudTasksQueueHttpTargetUriOverridePathOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[builtins.str] = None,
        query_override: typing.Optional[typing.Union["CloudTasksQueueHttpTargetUriOverrideQueryOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        uri_override_enforce_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host override. When specified, replaces the host part of the task URL. For example, if the task URL is "https://www.google.com", and host value is set to "example.net", the overridden URI will be changed to "https://example.net". Host value cannot be an empty string (INVALID_ARGUMENT). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#host CloudTasksQueue#host}
        :param path_override: path_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#path_override CloudTasksQueue#path_override}
        :param port: Port override. When specified, replaces the port part of the task URI. For instance, for a URI http://www.google.com/foo and port=123, the overridden URI becomes http://www.google.com:123/foo. Note that the port value must be a positive integer. Setting the port to 0 (Zero) clears the URI port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#port CloudTasksQueue#port}
        :param query_override: query_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#query_override CloudTasksQueue#query_override}
        :param scheme: Scheme override. When specified, the task URI scheme is replaced by the provided value (HTTP or HTTPS). Possible values: ["HTTP", "HTTPS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#scheme CloudTasksQueue#scheme}
        :param uri_override_enforce_mode: URI Override Enforce Mode. When specified, determines the Target UriOverride mode. If not specified, it defaults to ALWAYS. Possible values: ["ALWAYS", "IF_NOT_EXISTS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#uri_override_enforce_mode CloudTasksQueue#uri_override_enforce_mode}
        '''
        value = CloudTasksQueueHttpTargetUriOverride(
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
    def header_overrides(self) -> CloudTasksQueueHttpTargetHeaderOverridesList:
        return typing.cast(CloudTasksQueueHttpTargetHeaderOverridesList, jsii.get(self, "headerOverrides"))

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(self) -> CloudTasksQueueHttpTargetOauthTokenOutputReference:
        return typing.cast(CloudTasksQueueHttpTargetOauthTokenOutputReference, jsii.get(self, "oauthToken"))

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(self) -> CloudTasksQueueHttpTargetOidcTokenOutputReference:
        return typing.cast(CloudTasksQueueHttpTargetOidcTokenOutputReference, jsii.get(self, "oidcToken"))

    @builtins.property
    @jsii.member(jsii_name="uriOverride")
    def uri_override(self) -> "CloudTasksQueueHttpTargetUriOverrideOutputReference":
        return typing.cast("CloudTasksQueueHttpTargetUriOverrideOutputReference", jsii.get(self, "uriOverride"))

    @builtins.property
    @jsii.member(jsii_name="headerOverridesInput")
    def header_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudTasksQueueHttpTargetHeaderOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudTasksQueueHttpTargetHeaderOverrides]]], jsii.get(self, "headerOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenInput")
    def oauth_token_input(self) -> typing.Optional[CloudTasksQueueHttpTargetOauthToken]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetOauthToken], jsii.get(self, "oauthTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(self) -> typing.Optional[CloudTasksQueueHttpTargetOidcToken]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetOidcToken], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="uriOverrideInput")
    def uri_override_input(
        self,
    ) -> typing.Optional["CloudTasksQueueHttpTargetUriOverride"]:
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetUriOverride"], jsii.get(self, "uriOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4b5364f70e7d4153ed782fcb12f00f973b7930630975725153624ae1c444a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueHttpTarget]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudTasksQueueHttpTarget]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da9929818c5581abf4bd9b69db50f03f31c8638cc694d98393137637e28efff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetUriOverride",
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
class CloudTasksQueueHttpTargetUriOverride:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        path_override: typing.Optional[typing.Union["CloudTasksQueueHttpTargetUriOverridePathOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[builtins.str] = None,
        query_override: typing.Optional[typing.Union["CloudTasksQueueHttpTargetUriOverrideQueryOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        uri_override_enforce_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host override. When specified, replaces the host part of the task URL. For example, if the task URL is "https://www.google.com", and host value is set to "example.net", the overridden URI will be changed to "https://example.net". Host value cannot be an empty string (INVALID_ARGUMENT). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#host CloudTasksQueue#host}
        :param path_override: path_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#path_override CloudTasksQueue#path_override}
        :param port: Port override. When specified, replaces the port part of the task URI. For instance, for a URI http://www.google.com/foo and port=123, the overridden URI becomes http://www.google.com:123/foo. Note that the port value must be a positive integer. Setting the port to 0 (Zero) clears the URI port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#port CloudTasksQueue#port}
        :param query_override: query_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#query_override CloudTasksQueue#query_override}
        :param scheme: Scheme override. When specified, the task URI scheme is replaced by the provided value (HTTP or HTTPS). Possible values: ["HTTP", "HTTPS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#scheme CloudTasksQueue#scheme}
        :param uri_override_enforce_mode: URI Override Enforce Mode. When specified, determines the Target UriOverride mode. If not specified, it defaults to ALWAYS. Possible values: ["ALWAYS", "IF_NOT_EXISTS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#uri_override_enforce_mode CloudTasksQueue#uri_override_enforce_mode}
        '''
        if isinstance(path_override, dict):
            path_override = CloudTasksQueueHttpTargetUriOverridePathOverride(**path_override)
        if isinstance(query_override, dict):
            query_override = CloudTasksQueueHttpTargetUriOverrideQueryOverride(**query_override)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512eaad380d827c7f4d6c38a0c706b5485e284bc1f3dcec57302235d12d5857e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#host CloudTasksQueue#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_override(
        self,
    ) -> typing.Optional["CloudTasksQueueHttpTargetUriOverridePathOverride"]:
        '''path_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#path_override CloudTasksQueue#path_override}
        '''
        result = self._values.get("path_override")
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetUriOverridePathOverride"], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Port override.

        When specified, replaces the port part of the task URI.
        For instance, for a URI http://www.google.com/foo and port=123, the overridden URI becomes http://www.google.com:123/foo.
        Note that the port value must be a positive integer.
        Setting the port to 0 (Zero) clears the URI port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#port CloudTasksQueue#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_override(
        self,
    ) -> typing.Optional["CloudTasksQueueHttpTargetUriOverrideQueryOverride"]:
        '''query_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#query_override CloudTasksQueue#query_override}
        '''
        result = self._values.get("query_override")
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetUriOverrideQueryOverride"], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme override.

        When specified, the task URI scheme is replaced by the provided value (HTTP or HTTPS). Possible values: ["HTTP", "HTTPS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#scheme CloudTasksQueue#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri_override_enforce_mode(self) -> typing.Optional[builtins.str]:
        '''URI Override Enforce Mode.

        When specified, determines the Target UriOverride mode. If not specified, it defaults to ALWAYS. Possible values: ["ALWAYS", "IF_NOT_EXISTS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#uri_override_enforce_mode CloudTasksQueue#uri_override_enforce_mode}
        '''
        result = self._values.get("uri_override_enforce_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTargetUriOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueHttpTargetUriOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetUriOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4a7f1d53cccef1ef6d41fb64965cdcb4eca3b60747fbe45b30a2784774ef268)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPathOverride")
    def put_path_override(self, *, path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param path: The URI path (e.g., /users/1234). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#path CloudTasksQueue#path}
        '''
        value = CloudTasksQueueHttpTargetUriOverridePathOverride(path=path)

        return typing.cast(None, jsii.invoke(self, "putPathOverride", [value]))

    @jsii.member(jsii_name="putQueryOverride")
    def put_query_override(
        self,
        *,
        query_params: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param query_params: The query parameters (e.g., qparam1=123&qparam2=456). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#query_params CloudTasksQueue#query_params}
        '''
        value = CloudTasksQueueHttpTargetUriOverrideQueryOverride(
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
    ) -> "CloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference":
        return typing.cast("CloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference", jsii.get(self, "pathOverride"))

    @builtins.property
    @jsii.member(jsii_name="queryOverride")
    def query_override(
        self,
    ) -> "CloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference":
        return typing.cast("CloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference", jsii.get(self, "queryOverride"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="pathOverrideInput")
    def path_override_input(
        self,
    ) -> typing.Optional["CloudTasksQueueHttpTargetUriOverridePathOverride"]:
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetUriOverridePathOverride"], jsii.get(self, "pathOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="queryOverrideInput")
    def query_override_input(
        self,
    ) -> typing.Optional["CloudTasksQueueHttpTargetUriOverrideQueryOverride"]:
        return typing.cast(typing.Optional["CloudTasksQueueHttpTargetUriOverrideQueryOverride"], jsii.get(self, "queryOverrideInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9d21f07ca7bd7e3ae8f45ab086c69875707e5c93993037f405041cfeab5c7dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05bf1a18c0dcb784e42d8163f4848363db4c693a7944c87a8483a50725572551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd9bb63d993b182f4ba59944ad1505ed144692cdba6b0142bf89f36464c1565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uriOverrideEnforceMode")
    def uri_override_enforce_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uriOverrideEnforceMode"))

    @uri_override_enforce_mode.setter
    def uri_override_enforce_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a50bd8e755ebaa4c38be2837877c21b8d364717332f92c9b5c98c0a3556a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uriOverrideEnforceMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueHttpTargetUriOverride]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetUriOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueHttpTargetUriOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5625057adc1fc6281d18a42e6aadd9295bedb4b94e11fc61f704b78b9c56a567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetUriOverridePathOverride",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class CloudTasksQueueHttpTargetUriOverridePathOverride:
    def __init__(self, *, path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param path: The URI path (e.g., /users/1234). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#path CloudTasksQueue#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4187627f6e13f23da1b3b196c615f573f903c26ab7d16ea3169acc5111a90515)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI path (e.g., /users/1234). Default is an empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#path CloudTasksQueue#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTargetUriOverridePathOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d211d501189e3e9cdc9a622f308f10444dd908ac0bf8dae597b4fe685059e60a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d727c3eefec627ea815a6def4059a3bb4474a2ac8789fd34ea1538ee9b56f9d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudTasksQueueHttpTargetUriOverridePathOverride]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetUriOverridePathOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueHttpTargetUriOverridePathOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8ca2449d4f3ce99cf5659cdbed083192587ab37a78e2438d5c85e108435ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetUriOverrideQueryOverride",
    jsii_struct_bases=[],
    name_mapping={"query_params": "queryParams"},
)
class CloudTasksQueueHttpTargetUriOverrideQueryOverride:
    def __init__(self, *, query_params: typing.Optional[builtins.str] = None) -> None:
        '''
        :param query_params: The query parameters (e.g., qparam1=123&qparam2=456). Default is an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#query_params CloudTasksQueue#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e83a3c427b64e67d11f4380da59dba7ad3c5b568e1db6748f0b68ac5003f96d)
            check_type(argname="argument query_params", value=query_params, expected_type=type_hints["query_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_params is not None:
            self._values["query_params"] = query_params

    @builtins.property
    def query_params(self) -> typing.Optional[builtins.str]:
        '''The query parameters (e.g., qparam1=123&qparam2=456). Default is an empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#query_params CloudTasksQueue#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueHttpTargetUriOverrideQueryOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c2f82f29a4b9b8b7dd96e855d30c20a6e619ace8bab9d4a2e3feae67929075)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92e168dfc704f440a5c6e3a71fb226fabf61c5fd9b272fc4039c57d2dd8a11f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudTasksQueueHttpTargetUriOverrideQueryOverride]:
        return typing.cast(typing.Optional[CloudTasksQueueHttpTargetUriOverrideQueryOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueHttpTargetUriOverrideQueryOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e504197bcd1d4b194af2248e89c82013276320014c956d5822665742bda21c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRateLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_dispatches": "maxConcurrentDispatches",
        "max_dispatches_per_second": "maxDispatchesPerSecond",
    },
)
class CloudTasksQueueRateLimits:
    def __init__(
        self,
        *,
        max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
        max_dispatches_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_dispatches: The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched for this queue. After this threshold has been reached, Cloud Tasks stops dispatching tasks until the number of concurrent requests decreases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_concurrent_dispatches CloudTasksQueue#max_concurrent_dispatches}
        :param max_dispatches_per_second: The maximum rate at which tasks are dispatched from this queue. If unspecified when the queue is created, Cloud Tasks will pick the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_dispatches_per_second CloudTasksQueue#max_dispatches_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c188f34f89da88a0f1a401dcfb01acad45dd07cac777bbee3626637963d04d72)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_concurrent_dispatches CloudTasksQueue#max_concurrent_dispatches}
        '''
        result = self._values.get("max_concurrent_dispatches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_dispatches_per_second(self) -> typing.Optional[jsii.Number]:
        '''The maximum rate at which tasks are dispatched from this queue.

        If unspecified when the queue is created, Cloud Tasks will pick the default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_dispatches_per_second CloudTasksQueue#max_dispatches_per_second}
        '''
        result = self._values.get("max_dispatches_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueRateLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueRateLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRateLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32b9b9c0a63f7c1300a6d9b95d833e89cfd07446214c212450da5bd73ce130a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f70401ebb152ad8f5e511bb20a64ca5a1af9335808a2f0c466d40c892c0fab41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentDispatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDispatchesPerSecond")
    def max_dispatches_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDispatchesPerSecond"))

    @max_dispatches_per_second.setter
    def max_dispatches_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b24d2cab6ed38792ad89060d723cc98409736d473f91f76f959f98876d5fa54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDispatchesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueRateLimits]:
        return typing.cast(typing.Optional[CloudTasksQueueRateLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudTasksQueueRateLimits]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47338008cc06af963e81e997617433c18d45a89e93f9da7c090a6fabc4209f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRetryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_attempts": "maxAttempts",
        "max_backoff": "maxBackoff",
        "max_doublings": "maxDoublings",
        "max_retry_duration": "maxRetryDuration",
        "min_backoff": "minBackoff",
    },
)
class CloudTasksQueueRetryConfig:
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
        :param max_attempts: Number of attempts per task. Cloud Tasks will attempt the task maxAttempts times (that is, if the first attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1. If unspecified when the queue is created, Cloud Tasks will pick the default. -1 indicates unlimited attempts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_attempts CloudTasksQueue#max_attempts}
        :param max_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_backoff CloudTasksQueue#max_backoff}
        :param max_doublings: The time between retries will double maxDoublings times. A task's retry interval starts at minBackoff, then doubles maxDoublings times, then increases linearly, and finally retries retries at intervals of maxBackoff up to maxAttempts times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_doublings CloudTasksQueue#max_doublings}
        :param max_retry_duration: If positive, maxRetryDuration specifies the time limit for retrying a failed task, measured from when the task was first attempted. Once maxRetryDuration time has passed and the task has been attempted maxAttempts times, no further attempts will be made and the task will be deleted. If zero, then the task age is unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_retry_duration CloudTasksQueue#max_retry_duration}
        :param min_backoff: A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#min_backoff CloudTasksQueue#min_backoff}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f2811ac0e591ed79fd26183a9b7c287b8df661459bf427d5e205e59a753522)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_attempts CloudTasksQueue#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_backoff(self) -> typing.Optional[builtins.str]:
        '''A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_backoff CloudTasksQueue#max_backoff}
        '''
        result = self._values.get("max_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_doublings(self) -> typing.Optional[jsii.Number]:
        '''The time between retries will double maxDoublings times.

        A task's retry interval starts at minBackoff, then doubles maxDoublings times,
        then increases linearly, and finally retries retries at intervals of maxBackoff
        up to maxAttempts times.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_doublings CloudTasksQueue#max_doublings}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#max_retry_duration CloudTasksQueue#max_retry_duration}
        '''
        result = self._values.get("max_retry_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_backoff(self) -> typing.Optional[builtins.str]:
        '''A task will be scheduled for retry between minBackoff and maxBackoff duration after it fails, if the queue's RetryConfig specifies that the task should be retried.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#min_backoff CloudTasksQueue#min_backoff}
        '''
        result = self._values.get("min_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueRetryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueRetryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueRetryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa44eedd10a27db6641e71f03076ee78294bac56e68638fc7cc339491a6ca13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96cdb24212b9a4b09c0b8cf9dcbe159faf5e54a7b4ec17308d9fd7691d39d10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBackoff")
    def max_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxBackoff"))

    @max_backoff.setter
    def max_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dc0fdc017d4104ab34380472563fbe905d6b0f1f8b082626ba7ec42fbeb8b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBackoff", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDoublings")
    def max_doublings(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDoublings"))

    @max_doublings.setter
    def max_doublings(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45a466758e50c756c397e3a387720a5d04a1367c8f7bb3d362af471b77c6cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDoublings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetryDuration")
    def max_retry_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRetryDuration"))

    @max_retry_duration.setter
    def max_retry_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b6e6681febdefe45da0fccded2ad178f9a0a89ceb02f4e32d000bf2115cc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minBackoff")
    def min_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minBackoff"))

    @min_backoff.setter
    def min_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b848bed0eefda95625ae4333bd791b6938d70df8d1d5d766a74b1c822420774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minBackoff", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudTasksQueueRetryConfig]:
        return typing.cast(typing.Optional[CloudTasksQueueRetryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueRetryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18b57fa721c854a7077b094515ec33791a71ef45bbf13aa1d60154236183c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueStackdriverLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"sampling_ratio": "samplingRatio"},
)
class CloudTasksQueueStackdriverLoggingConfig:
    def __init__(self, *, sampling_ratio: jsii.Number) -> None:
        '''
        :param sampling_ratio: Specifies the fraction of operations to write to Stackdriver Logging. This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the default and means that no operations are logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#sampling_ratio CloudTasksQueue#sampling_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f818077b4fe25b36b9ab62ed7caf6608ede7d537fbff8993809ebde31290f4)
            check_type(argname="argument sampling_ratio", value=sampling_ratio, expected_type=type_hints["sampling_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sampling_ratio": sampling_ratio,
        }

    @builtins.property
    def sampling_ratio(self) -> jsii.Number:
        '''Specifies the fraction of operations to write to Stackdriver Logging.

        This field may contain any value between 0.0 and 1.0, inclusive. 0.0 is the
        default and means that no operations are logged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#sampling_ratio CloudTasksQueue#sampling_ratio}
        '''
        result = self._values.get("sampling_ratio")
        assert result is not None, "Required property 'sampling_ratio' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueStackdriverLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueStackdriverLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueStackdriverLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1151b61c2a33795681934d7e5e51e7ae95bbede9819a27ee4475f77ed2dbc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e68cc0d654a74ad7fcbe798d7bd4a60366080def91cfce8a8adae4c04af3eeba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudTasksQueueStackdriverLoggingConfig]:
        return typing.cast(typing.Optional[CloudTasksQueueStackdriverLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudTasksQueueStackdriverLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a149839d90144a82e856636ea407526726265a8a75c8a80c8bff50199a427ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudTasksQueueTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#create CloudTasksQueue#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#delete CloudTasksQueue#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#update CloudTasksQueue#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bdb91fbc81ec2def08756553d5d01255a5e8a182081c7c355580e6f1a8765f3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#create CloudTasksQueue#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#delete CloudTasksQueue#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_tasks_queue#update CloudTasksQueue#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudTasksQueueTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudTasksQueueTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudTasksQueue.CloudTasksQueueTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f83bd6954e7b28b58bf1554324a87ef5f285d96f0c604a35e6134cc70efc3d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a56bb4e3d211f674a78b0e3079ae2dbb5dbd1282856f43ea842db47142642d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b624e509eda58d258ef887cb86d0a12d230c1da9412a145b81566340647704d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c0e53b53fe4357eb078fdae7c50d49e88107a617726ccf557503577574d35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653fa230e7363c42e111946e56a3f9ff66b69a4c2431ebc9101994af211a8734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudTasksQueue",
    "CloudTasksQueueAppEngineRoutingOverride",
    "CloudTasksQueueAppEngineRoutingOverrideOutputReference",
    "CloudTasksQueueConfig",
    "CloudTasksQueueHttpTarget",
    "CloudTasksQueueHttpTargetHeaderOverrides",
    "CloudTasksQueueHttpTargetHeaderOverridesHeader",
    "CloudTasksQueueHttpTargetHeaderOverridesHeaderOutputReference",
    "CloudTasksQueueHttpTargetHeaderOverridesList",
    "CloudTasksQueueHttpTargetHeaderOverridesOutputReference",
    "CloudTasksQueueHttpTargetOauthToken",
    "CloudTasksQueueHttpTargetOauthTokenOutputReference",
    "CloudTasksQueueHttpTargetOidcToken",
    "CloudTasksQueueHttpTargetOidcTokenOutputReference",
    "CloudTasksQueueHttpTargetOutputReference",
    "CloudTasksQueueHttpTargetUriOverride",
    "CloudTasksQueueHttpTargetUriOverrideOutputReference",
    "CloudTasksQueueHttpTargetUriOverridePathOverride",
    "CloudTasksQueueHttpTargetUriOverridePathOverrideOutputReference",
    "CloudTasksQueueHttpTargetUriOverrideQueryOverride",
    "CloudTasksQueueHttpTargetUriOverrideQueryOverrideOutputReference",
    "CloudTasksQueueRateLimits",
    "CloudTasksQueueRateLimitsOutputReference",
    "CloudTasksQueueRetryConfig",
    "CloudTasksQueueRetryConfigOutputReference",
    "CloudTasksQueueStackdriverLoggingConfig",
    "CloudTasksQueueStackdriverLoggingConfigOutputReference",
    "CloudTasksQueueTimeouts",
    "CloudTasksQueueTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__af4b65c7c98de529a56114659ee7eea05c423eb2573bf13ef256640ec5537628(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    app_engine_routing_override: typing.Optional[typing.Union[CloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    http_target: typing.Optional[typing.Union[CloudTasksQueueHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limits: typing.Optional[typing.Union[CloudTasksQueueRateLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_config: typing.Optional[typing.Union[CloudTasksQueueRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stackdriver_logging_config: typing.Optional[typing.Union[CloudTasksQueueStackdriverLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudTasksQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b4167d1fba00044e6b8fe4fae83a8527797864033d79b1f15c20ff69f66e5c06(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb26345cf52f11dcd4ef850ccfa20133568374589e76ce84de78fe88a2f9ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7f4ba3031fd0ec8200ea71bf27105a44f16b2568c2335ecf54309d6b53b2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8c1aedb20aa05e746efc16a9873fc595c872b96889616a6c0348d8866d74be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7b2a24d68b223fa27dcd372bce4798813f55128834c98a42d2451d52c50d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1c48bc18dd9d5d3d3bad0ae065a1068d71e9d3ba9cccd7e5b48ecee7e3a55f(
    *,
    instance: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5294b28a75106c79c8d69f7d9c4052e0ef459a31fc71dbc1d983fb0ef4f44cb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f86b4a0660cdc8001b91f44bbc48bfd94884ad95c3feb2deea31b8af2d02e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f739c7806538573b239c8b622b0915e8f2911bdabc9398fc3d27bf81cbb3486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891dc54305d15ea2ed9d7f476f32398dc7fb4f82edab0cbe988df848ade8b745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e47552dc050adf038e62f281feabaef42512ed8a384293aafed1e0ae3023a74(
    value: typing.Optional[CloudTasksQueueAppEngineRoutingOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72ca0923f5716abfb32b718c95c8c961a7d2deae111cd2080cabb7dfe70971f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    app_engine_routing_override: typing.Optional[typing.Union[CloudTasksQueueAppEngineRoutingOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    http_target: typing.Optional[typing.Union[CloudTasksQueueHttpTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rate_limits: typing.Optional[typing.Union[CloudTasksQueueRateLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_config: typing.Optional[typing.Union[CloudTasksQueueRetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stackdriver_logging_config: typing.Optional[typing.Union[CloudTasksQueueStackdriverLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudTasksQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df407753f5711fe89253efdef784bb2bb654c70f76cd1a5c058d7262b26f135(
    *,
    header_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudTasksQueueHttpTargetHeaderOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_method: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[typing.Union[CloudTasksQueueHttpTargetOauthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    oidc_token: typing.Optional[typing.Union[CloudTasksQueueHttpTargetOidcToken, typing.Dict[builtins.str, typing.Any]]] = None,
    uri_override: typing.Optional[typing.Union[CloudTasksQueueHttpTargetUriOverride, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04204ce0dd466ab5eb3ab29834d0712b3a25e9ea906a22d2c3d3a8e6e1e7d1c4(
    *,
    header: typing.Union[CloudTasksQueueHttpTargetHeaderOverridesHeader, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d250969d59349dc3d57d0483815f2f2c7c4ee22a3bff4a36338794105ba14a63(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36f47cf3c59ebd6f78edf19e21f453b452bf5acea4b111b52df30a03e20e95c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1941f4f1a6de40f752906a178ba710541114edd294a53161e0a6b2cfe5e0b175(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528f1a826ba30e2da4726754fd0cd43d7f6363319ea111ead56b3325ffe6503f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3881a7d0103ee209e7ada8280f970c10a8fcb2e116ff77b923e627c9f0e7072(
    value: typing.Optional[CloudTasksQueueHttpTargetHeaderOverridesHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5da5f5a6030ff44c2b04908a0fb44ab48df689a1a2419a998d79c965360c46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1e3f26049c8bead0343a4ae79c872d94a7ed799a18b21281ae98f934d7b7e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3d995789828b727a2b85d463a27aa4aa02b3cdafe3cf73f0cdda7a550216a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63a40ca800475f2b4d885fbdc4d3869e879263c688fd6c345532e65343683df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c0f4e16d49355fee1be8d018eda547de4a35f3e1e68a6e4fa9901f5ff0a7a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596a75c494db0c701c8c5ec99b46be0e1e4d822407e4d121c5ede7b2ee9ac3b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudTasksQueueHttpTargetHeaderOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8368ed7d4e19f5b92f8d0af4ff6ccc62cc57e70ff9b84ee8f70eaba317648a3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93e31b9a844eb8afa794ba3304d28cbfddb88ad1c8055a949fa7db3e492bbee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueHttpTargetHeaderOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982969fe9c72e078326f006aad77b8f784fa9131c8236c955235ca106b2206a5(
    *,
    service_account_email: builtins.str,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f59789eea6f56b26de87ac464319b6aabef92fe425170811f2fa6590565ff7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f2fc1c6c4109090c474d95936109df10b786d17a8820bc3b204265e00bf8fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd7b6d9e4ecc2f1135cd75acb5814f9a2df70e0c6759581af240f6f2c29d333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98a8614931c311a8b2ffcb961d961b3f8f2f19c7c52a115401da754fc012b5b(
    value: typing.Optional[CloudTasksQueueHttpTargetOauthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdde329033daacafb8afacf376cdaec7a008122f0ac76397a97598fc868e2236(
    *,
    service_account_email: builtins.str,
    audience: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08648aac8e36b779cc58c9f95e6a4c92ab98515a0718edf1326429524a1525ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cadd46577ed0deb6b24b5029e236114e31b405deab99f3b6f671320fea6bad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c51e2e4c1647b18abba3658dae722cc2df60b8b51c6de070f2b73923eeeb08d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abfcd46afa9530fd98b505fc965318b0dcbb5d0644f1fbaf27899ede35b68f3(
    value: typing.Optional[CloudTasksQueueHttpTargetOidcToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7e38e8fecdefae7304b0ebe7bb73318299ca835f7ad227c0f0bb34b13e4c02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70f00039233df0d6c6676e38e9031c4ca36f9c3562c7deb381d70833ade0466(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudTasksQueueHttpTargetHeaderOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4b5364f70e7d4153ed782fcb12f00f973b7930630975725153624ae1c444a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da9929818c5581abf4bd9b69db50f03f31c8638cc694d98393137637e28efff(
    value: typing.Optional[CloudTasksQueueHttpTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512eaad380d827c7f4d6c38a0c706b5485e284bc1f3dcec57302235d12d5857e(
    *,
    host: typing.Optional[builtins.str] = None,
    path_override: typing.Optional[typing.Union[CloudTasksQueueHttpTargetUriOverridePathOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[builtins.str] = None,
    query_override: typing.Optional[typing.Union[CloudTasksQueueHttpTargetUriOverrideQueryOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    scheme: typing.Optional[builtins.str] = None,
    uri_override_enforce_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a7f1d53cccef1ef6d41fb64965cdcb4eca3b60747fbe45b30a2784774ef268(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d21f07ca7bd7e3ae8f45ab086c69875707e5c93993037f405041cfeab5c7dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bf1a18c0dcb784e42d8163f4848363db4c693a7944c87a8483a50725572551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd9bb63d993b182f4ba59944ad1505ed144692cdba6b0142bf89f36464c1565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a50bd8e755ebaa4c38be2837877c21b8d364717332f92c9b5c98c0a3556a5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5625057adc1fc6281d18a42e6aadd9295bedb4b94e11fc61f704b78b9c56a567(
    value: typing.Optional[CloudTasksQueueHttpTargetUriOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4187627f6e13f23da1b3b196c615f573f903c26ab7d16ea3169acc5111a90515(
    *,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d211d501189e3e9cdc9a622f308f10444dd908ac0bf8dae597b4fe685059e60a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d727c3eefec627ea815a6def4059a3bb4474a2ac8789fd34ea1538ee9b56f9d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8ca2449d4f3ce99cf5659cdbed083192587ab37a78e2438d5c85e108435ecb(
    value: typing.Optional[CloudTasksQueueHttpTargetUriOverridePathOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e83a3c427b64e67d11f4380da59dba7ad3c5b568e1db6748f0b68ac5003f96d(
    *,
    query_params: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c2f82f29a4b9b8b7dd96e855d30c20a6e619ace8bab9d4a2e3feae67929075(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e168dfc704f440a5c6e3a71fb226fabf61c5fd9b272fc4039c57d2dd8a11f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e504197bcd1d4b194af2248e89c82013276320014c956d5822665742bda21c(
    value: typing.Optional[CloudTasksQueueHttpTargetUriOverrideQueryOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c188f34f89da88a0f1a401dcfb01acad45dd07cac777bbee3626637963d04d72(
    *,
    max_concurrent_dispatches: typing.Optional[jsii.Number] = None,
    max_dispatches_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b9b9c0a63f7c1300a6d9b95d833e89cfd07446214c212450da5bd73ce130a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70401ebb152ad8f5e511bb20a64ca5a1af9335808a2f0c466d40c892c0fab41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b24d2cab6ed38792ad89060d723cc98409736d473f91f76f959f98876d5fa54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47338008cc06af963e81e997617433c18d45a89e93f9da7c090a6fabc4209f84(
    value: typing.Optional[CloudTasksQueueRateLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f2811ac0e591ed79fd26183a9b7c287b8df661459bf427d5e205e59a753522(
    *,
    max_attempts: typing.Optional[jsii.Number] = None,
    max_backoff: typing.Optional[builtins.str] = None,
    max_doublings: typing.Optional[jsii.Number] = None,
    max_retry_duration: typing.Optional[builtins.str] = None,
    min_backoff: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa44eedd10a27db6641e71f03076ee78294bac56e68638fc7cc339491a6ca13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cdb24212b9a4b09c0b8cf9dcbe159faf5e54a7b4ec17308d9fd7691d39d10f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dc0fdc017d4104ab34380472563fbe905d6b0f1f8b082626ba7ec42fbeb8b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45a466758e50c756c397e3a387720a5d04a1367c8f7bb3d362af471b77c6cc9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b6e6681febdefe45da0fccded2ad178f9a0a89ceb02f4e32d000bf2115cc34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b848bed0eefda95625ae4333bd791b6938d70df8d1d5d766a74b1c822420774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18b57fa721c854a7077b094515ec33791a71ef45bbf13aa1d60154236183c00(
    value: typing.Optional[CloudTasksQueueRetryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f818077b4fe25b36b9ab62ed7caf6608ede7d537fbff8993809ebde31290f4(
    *,
    sampling_ratio: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1151b61c2a33795681934d7e5e51e7ae95bbede9819a27ee4475f77ed2dbc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68cc0d654a74ad7fcbe798d7bd4a60366080def91cfce8a8adae4c04af3eeba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a149839d90144a82e856636ea407526726265a8a75c8a80c8bff50199a427ab(
    value: typing.Optional[CloudTasksQueueStackdriverLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdb91fbc81ec2def08756553d5d01255a5e8a182081c7c355580e6f1a8765f3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f83bd6954e7b28b58bf1554324a87ef5f285d96f0c604a35e6134cc70efc3d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a56bb4e3d211f674a78b0e3079ae2dbb5dbd1282856f43ea842db47142642d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b624e509eda58d258ef887cb86d0a12d230c1da9412a145b81566340647704d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c0e53b53fe4357eb078fdae7c50d49e88107a617726ccf557503577574d35b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653fa230e7363c42e111946e56a3f9ff66b69a4c2431ebc9101994af211a8734(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudTasksQueueTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
