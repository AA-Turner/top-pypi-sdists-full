r'''
# `google_app_engine_flexible_app_version`

Refer to the Terraform Registry for docs: [`google_app_engine_flexible_app_version`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version).
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


class AppEngineFlexibleAppVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version google_app_engine_flexible_app_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        liveness_check: typing.Union["AppEngineFlexibleAppVersionLivenessCheck", typing.Dict[builtins.str, typing.Any]],
        readiness_check: typing.Union["AppEngineFlexibleAppVersionReadinessCheck", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        api_config: typing.Optional[typing.Union["AppEngineFlexibleAppVersionApiConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        automatic_scaling: typing.Optional[typing.Union["AppEngineFlexibleAppVersionAutomaticScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        default_expiration: typing.Optional[builtins.str] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoints_api_service: typing.Optional[typing.Union["AppEngineFlexibleAppVersionEndpointsApiService", typing.Dict[builtins.str, typing.Any]]] = None,
        entrypoint: typing.Optional[typing.Union["AppEngineFlexibleAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        flexible_runtime_settings: typing.Optional[typing.Union["AppEngineFlexibleAppVersionFlexibleRuntimeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        manual_scaling: typing.Optional[typing.Union["AppEngineFlexibleAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["AppEngineFlexibleAppVersionNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        nobuild_files_regex: typing.Optional[builtins.str] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Union["AppEngineFlexibleAppVersionResources", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        runtime_channel: typing.Optional[builtins.str] = None,
        runtime_main_executable_path: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        serving_status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppEngineFlexibleAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["AppEngineFlexibleAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version google_app_engine_flexible_app_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param liveness_check: liveness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#liveness_check AppEngineFlexibleAppVersion#liveness_check}
        :param readiness_check: readiness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#readiness_check AppEngineFlexibleAppVersion#readiness_check}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime AppEngineFlexibleAppVersion#runtime}
        :param service: AppEngine service resource. Can contain numbers, letters, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#service AppEngineFlexibleAppVersion#service}
        :param api_config: api_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#api_config AppEngineFlexibleAppVersion#api_config}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#automatic_scaling AppEngineFlexibleAppVersion#automatic_scaling}
        :param beta_settings: Metadata settings that are supplied to this version to enable beta runtime features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#beta_settings AppEngineFlexibleAppVersion#beta_settings}
        :param default_expiration: Duration that static files should be cached by web proxies and browsers. Only applicable if the corresponding StaticFilesHandler does not specify its own expiration time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#default_expiration AppEngineFlexibleAppVersion#default_expiration}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#delete_service_on_destroy AppEngineFlexibleAppVersion#delete_service_on_destroy}
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#deployment AppEngineFlexibleAppVersion#deployment}
        :param endpoints_api_service: endpoints_api_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#endpoints_api_service AppEngineFlexibleAppVersion#endpoints_api_service}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#entrypoint AppEngineFlexibleAppVersion#entrypoint}
        :param env_variables: Environment variables available to the application. As these are not returned in the API request, Terraform will not detect any changes made outside of the Terraform config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#env_variables AppEngineFlexibleAppVersion#env_variables}
        :param flexible_runtime_settings: flexible_runtime_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#flexible_runtime_settings AppEngineFlexibleAppVersion#flexible_runtime_settings}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#handlers AppEngineFlexibleAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#id AppEngineFlexibleAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#inbound_services AppEngineFlexibleAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G ManualScaling: B1, B2, B4, B8, B4_1G Defaults to F1 for AutomaticScaling and B1 for ManualScaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instance_class AppEngineFlexibleAppVersion#instance_class}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#manual_scaling AppEngineFlexibleAppVersion#manual_scaling}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#network AppEngineFlexibleAppVersion#network}
        :param nobuild_files_regex: Files that match this pattern will not be built into this version. Only applicable for Go runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#nobuild_files_regex AppEngineFlexibleAppVersion#nobuild_files_regex}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#noop_on_destroy AppEngineFlexibleAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#project AppEngineFlexibleAppVersion#project}.
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#resources AppEngineFlexibleAppVersion#resources}
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_api_version AppEngineFlexibleAppVersion#runtime_api_version}
        :param runtime_channel: The channel of the runtime to use. Only available for some runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_channel AppEngineFlexibleAppVersion#runtime_channel}
        :param runtime_main_executable_path: The path or name of the app's main executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_main_executable_path AppEngineFlexibleAppVersion#runtime_main_executable_path}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#service_account AppEngineFlexibleAppVersion#service_account}
        :param serving_status: Current serving status of this version. Only the versions with a SERVING status create instances and can be billed. Default value: "SERVING" Possible values: ["SERVING", "STOPPED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#serving_status AppEngineFlexibleAppVersion#serving_status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeouts AppEngineFlexibleAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#version_id AppEngineFlexibleAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#vpc_access_connector AppEngineFlexibleAppVersion#vpc_access_connector}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46baa41731a0b8bcab1d56572382b0fc47f1b379830be99af8384c3ce21ec26)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppEngineFlexibleAppVersionConfig(
            liveness_check=liveness_check,
            readiness_check=readiness_check,
            runtime=runtime,
            service=service,
            api_config=api_config,
            automatic_scaling=automatic_scaling,
            beta_settings=beta_settings,
            default_expiration=default_expiration,
            delete_service_on_destroy=delete_service_on_destroy,
            deployment=deployment,
            endpoints_api_service=endpoints_api_service,
            entrypoint=entrypoint,
            env_variables=env_variables,
            flexible_runtime_settings=flexible_runtime_settings,
            handlers=handlers,
            id=id,
            inbound_services=inbound_services,
            instance_class=instance_class,
            manual_scaling=manual_scaling,
            network=network,
            nobuild_files_regex=nobuild_files_regex,
            noop_on_destroy=noop_on_destroy,
            project=project,
            resources=resources,
            runtime_api_version=runtime_api_version,
            runtime_channel=runtime_channel,
            runtime_main_executable_path=runtime_main_executable_path,
            service_account=service_account,
            serving_status=serving_status,
            timeouts=timeouts,
            version_id=version_id,
            vpc_access_connector=vpc_access_connector,
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
        '''Generates CDKTF code for importing a AppEngineFlexibleAppVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppEngineFlexibleAppVersion to import.
        :param import_from_id: The id of the existing AppEngineFlexibleAppVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppEngineFlexibleAppVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e356b2ae56c4c12b5c10f812816282e3c38845b320c4aa61c917d3a70dde7f5a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApiConfig")
    def put_api_config(
        self,
        *,
        script: builtins.str,
        auth_fail_action: typing.Optional[builtins.str] = None,
        login: typing.Optional[builtins.str] = None,
        security_level: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script AppEngineFlexibleAppVersion#script}
        :param auth_fail_action: Action to take when users access resources that require authentication. Default value: "AUTH_FAIL_ACTION_REDIRECT" Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#auth_fail_action AppEngineFlexibleAppVersion#auth_fail_action}
        :param login: Level of login required to access this resource. Default value: "LOGIN_OPTIONAL" Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#login AppEngineFlexibleAppVersion#login}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#security_level AppEngineFlexibleAppVersion#security_level}
        :param url: URL to serve the endpoint at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#url AppEngineFlexibleAppVersion#url}
        '''
        value = AppEngineFlexibleAppVersionApiConfig(
            script=script,
            auth_fail_action=auth_fail_action,
            login=login,
            security_level=security_level,
            url=url,
        )

        return typing.cast(None, jsii.invoke(self, "putApiConfig", [value]))

    @jsii.member(jsii_name="putAutomaticScaling")
    def put_automatic_scaling(
        self,
        *,
        cpu_utilization: typing.Union["AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization", typing.Dict[builtins.str, typing.Any]],
        cool_down_period: typing.Optional[builtins.str] = None,
        disk_utilization: typing.Optional[typing.Union["AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_requests: typing.Optional[jsii.Number] = None,
        max_idle_instances: typing.Optional[jsii.Number] = None,
        max_pending_latency: typing.Optional[builtins.str] = None,
        max_total_instances: typing.Optional[jsii.Number] = None,
        min_idle_instances: typing.Optional[jsii.Number] = None,
        min_pending_latency: typing.Optional[builtins.str] = None,
        min_total_instances: typing.Optional[jsii.Number] = None,
        network_utilization: typing.Optional[typing.Union["AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        request_utilization: typing.Optional[typing.Union["AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cpu_utilization AppEngineFlexibleAppVersion#cpu_utilization}
        :param cool_down_period: The time period that the Autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. Default: 120s Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cool_down_period AppEngineFlexibleAppVersion#cool_down_period}
        :param disk_utilization: disk_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disk_utilization AppEngineFlexibleAppVersion#disk_utilization}
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_concurrent_requests AppEngineFlexibleAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_idle_instances AppEngineFlexibleAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_pending_latency AppEngineFlexibleAppVersion#max_pending_latency}
        :param max_total_instances: Maximum number of instances that should be started to handle requests for this version. Default: 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_total_instances AppEngineFlexibleAppVersion#max_total_instances}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_idle_instances AppEngineFlexibleAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_pending_latency AppEngineFlexibleAppVersion#min_pending_latency}
        :param min_total_instances: Minimum number of running instances that should be maintained for this version. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_total_instances AppEngineFlexibleAppVersion#min_total_instances}
        :param network_utilization: network_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#network_utilization AppEngineFlexibleAppVersion#network_utilization}
        :param request_utilization: request_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#request_utilization AppEngineFlexibleAppVersion#request_utilization}
        '''
        value = AppEngineFlexibleAppVersionAutomaticScaling(
            cpu_utilization=cpu_utilization,
            cool_down_period=cool_down_period,
            disk_utilization=disk_utilization,
            max_concurrent_requests=max_concurrent_requests,
            max_idle_instances=max_idle_instances,
            max_pending_latency=max_pending_latency,
            max_total_instances=max_total_instances,
            min_idle_instances=min_idle_instances,
            min_pending_latency=min_pending_latency,
            min_total_instances=min_total_instances,
            network_utilization=network_utilization,
            request_utilization=request_utilization,
        )

        return typing.cast(None, jsii.invoke(self, "putAutomaticScaling", [value]))

    @jsii.member(jsii_name="putDeployment")
    def put_deployment(
        self,
        *,
        cloud_build_options: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeploymentCloudBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        container: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeploymentContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_build_options: cloud_build_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cloud_build_options AppEngineFlexibleAppVersion#cloud_build_options}
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#container AppEngineFlexibleAppVersion#container}
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#files AppEngineFlexibleAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#zip AppEngineFlexibleAppVersion#zip}
        '''
        value = AppEngineFlexibleAppVersionDeployment(
            cloud_build_options=cloud_build_options,
            container=container,
            files=files,
            zip=zip,
        )

        return typing.cast(None, jsii.invoke(self, "putDeployment", [value]))

    @jsii.member(jsii_name="putEndpointsApiService")
    def put_endpoints_api_service(
        self,
        *,
        name: builtins.str,
        config_id: typing.Optional[builtins.str] = None,
        disable_trace_sampling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rollout_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Endpoints service name which is the name of the "service" resource in the Service Management API. For example "myapi.endpoints.myproject.cloud.goog". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        :param config_id: Endpoints service configuration ID as specified by the Service Management API. For example "2016-09-19r1". By default, the rollout strategy for Endpoints is "FIXED". This means that Endpoints starts up with a particular configuration ID. When a new configuration is rolled out, Endpoints must be given the new configuration ID. The configId field is used to give the configuration ID and is required in this case. Endpoints also has a rollout strategy called "MANAGED". When using this, Endpoints fetches the latest configuration and does not need the configuration ID. In this case, configId must be omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#config_id AppEngineFlexibleAppVersion#config_id}
        :param disable_trace_sampling: Enable or disable trace sampling. By default, this is set to false for enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disable_trace_sampling AppEngineFlexibleAppVersion#disable_trace_sampling}
        :param rollout_strategy: Endpoints rollout strategy. If FIXED, configId must be specified. If MANAGED, configId must be omitted. Default value: "FIXED" Possible values: ["FIXED", "MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#rollout_strategy AppEngineFlexibleAppVersion#rollout_strategy}
        '''
        value = AppEngineFlexibleAppVersionEndpointsApiService(
            name=name,
            config_id=config_id,
            disable_trace_sampling=disable_trace_sampling,
            rollout_strategy=rollout_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointsApiService", [value]))

    @jsii.member(jsii_name="putEntrypoint")
    def put_entrypoint(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#shell AppEngineFlexibleAppVersion#shell}
        '''
        value = AppEngineFlexibleAppVersionEntrypoint(shell=shell)

        return typing.cast(None, jsii.invoke(self, "putEntrypoint", [value]))

    @jsii.member(jsii_name="putFlexibleRuntimeSettings")
    def put_flexible_runtime_settings(
        self,
        *,
        operating_system: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operating_system: Operating System of the application runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#operating_system AppEngineFlexibleAppVersion#operating_system}
        :param runtime_version: The runtime version of an App Engine flexible application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_version AppEngineFlexibleAppVersion#runtime_version}
        '''
        value = AppEngineFlexibleAppVersionFlexibleRuntimeSettings(
            operating_system=operating_system, runtime_version=runtime_version
        )

        return typing.cast(None, jsii.invoke(self, "putFlexibleRuntimeSettings", [value]))

    @jsii.member(jsii_name="putHandlers")
    def put_handlers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eadd705340bc124c07d9dd7af6c0af2e86d96c8b7056e95577d8ff89c34c67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHandlers", [value]))

    @jsii.member(jsii_name="putLivenessCheck")
    def put_liveness_check(
        self,
        *,
        path: builtins.str,
        check_interval: typing.Optional[builtins.str] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[builtins.str] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        :param check_interval: Interval between health checks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#check_interval AppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before considering the VM unhealthy. Default: 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#failure_threshold AppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#host AppEngineFlexibleAppVersion#host}
        :param initial_delay: The initial delay before starting to execute the checks. Default: "300s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#initial_delay AppEngineFlexibleAppVersion#initial_delay}
        :param success_threshold: Number of consecutive successful checks required before considering the VM healthy. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#success_threshold AppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeout AppEngineFlexibleAppVersion#timeout}
        '''
        value = AppEngineFlexibleAppVersionLivenessCheck(
            path=path,
            check_interval=check_interval,
            failure_threshold=failure_threshold,
            host=host,
            initial_delay=initial_delay,
            success_threshold=success_threshold,
            timeout=timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putLivenessCheck", [value]))

    @jsii.member(jsii_name="putManualScaling")
    def put_manual_scaling(self, *, instances: jsii.Number) -> None:
        '''
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instances AppEngineFlexibleAppVersion#instances}
        '''
        value = AppEngineFlexibleAppVersionManualScaling(instances=instances)

        return typing.cast(None, jsii.invoke(self, "putManualScaling", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        *,
        name: builtins.str,
        forwarded_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_tag: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Google Compute Engine network where the virtual machines are created. Specify the short name, not the resource path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        :param forwarded_ports: List of ports, or port pairs, to forward from the virtual machine to the application container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#forwarded_ports AppEngineFlexibleAppVersion#forwarded_ports}
        :param instance_tag: Tag to apply to the instance during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instance_tag AppEngineFlexibleAppVersion#instance_tag}
        :param session_affinity: Enable session affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#session_affinity AppEngineFlexibleAppVersion#session_affinity}
        :param subnetwork: Google Cloud Platform sub-network where the virtual machines are created. Specify the short name, not the resource path. If the network that the instance is being created in is a Legacy network, then the IP address is allocated from the IPv4Range. If the network that the instance is being created in is an auto Subnet Mode Network, then only network name should be specified (not the subnetworkName) and the IP address is created from the IPCidrRange of the subnetwork that exists in that zone for that network. If the network that the instance is being created in is a custom Subnet Mode Network, then the subnetworkName must be specified and the IP address is created from the IPCidrRange of the subnetwork. If specified, the subnetwork must exist in the same region as the App Engine flexible environment application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#subnetwork AppEngineFlexibleAppVersion#subnetwork}
        '''
        value = AppEngineFlexibleAppVersionNetwork(
            name=name,
            forwarded_ports=forwarded_ports,
            instance_tag=instance_tag,
            session_affinity=session_affinity,
            subnetwork=subnetwork,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putReadinessCheck")
    def put_readiness_check(
        self,
        *,
        path: builtins.str,
        app_start_timeout: typing.Optional[builtins.str] = None,
        check_interval: typing.Optional[builtins.str] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        :param app_start_timeout: A maximum time limit on application initialization, measured from moment the application successfully replies to a healthcheck until it is ready to serve traffic. Default: "300s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#app_start_timeout AppEngineFlexibleAppVersion#app_start_timeout}
        :param check_interval: Interval between health checks. Default: "5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#check_interval AppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before removing traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#failure_threshold AppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#host AppEngineFlexibleAppVersion#host}
        :param success_threshold: Number of consecutive successful checks required before receiving traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#success_threshold AppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeout AppEngineFlexibleAppVersion#timeout}
        '''
        value = AppEngineFlexibleAppVersionReadinessCheck(
            path=path,
            app_start_timeout=app_start_timeout,
            check_interval=check_interval,
            failure_threshold=failure_threshold,
            host=host,
            success_threshold=success_threshold,
            timeout=timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putReadinessCheck", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        disk_gb: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionResourcesVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cpu: Number of CPU cores needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cpu AppEngineFlexibleAppVersion#cpu}
        :param disk_gb: Disk size (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disk_gb AppEngineFlexibleAppVersion#disk_gb}
        :param memory_gb: Memory (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#memory_gb AppEngineFlexibleAppVersion#memory_gb}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#volumes AppEngineFlexibleAppVersion#volumes}
        '''
        value = AppEngineFlexibleAppVersionResources(
            cpu=cpu, disk_gb=disk_gb, memory_gb=memory_gb, volumes=volumes
        )

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#create AppEngineFlexibleAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#delete AppEngineFlexibleAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#update AppEngineFlexibleAppVersion#update}.
        '''
        value = AppEngineFlexibleAppVersionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcAccessConnector")
    def put_vpc_access_connector(self, *, name: builtins.str) -> None:
        '''
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        '''
        value = AppEngineFlexibleAppVersionVpcAccessConnector(name=name)

        return typing.cast(None, jsii.invoke(self, "putVpcAccessConnector", [value]))

    @jsii.member(jsii_name="resetApiConfig")
    def reset_api_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiConfig", []))

    @jsii.member(jsii_name="resetAutomaticScaling")
    def reset_automatic_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticScaling", []))

    @jsii.member(jsii_name="resetBetaSettings")
    def reset_beta_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBetaSettings", []))

    @jsii.member(jsii_name="resetDefaultExpiration")
    def reset_default_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultExpiration", []))

    @jsii.member(jsii_name="resetDeleteServiceOnDestroy")
    def reset_delete_service_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteServiceOnDestroy", []))

    @jsii.member(jsii_name="resetDeployment")
    def reset_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeployment", []))

    @jsii.member(jsii_name="resetEndpointsApiService")
    def reset_endpoints_api_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointsApiService", []))

    @jsii.member(jsii_name="resetEntrypoint")
    def reset_entrypoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntrypoint", []))

    @jsii.member(jsii_name="resetEnvVariables")
    def reset_env_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvVariables", []))

    @jsii.member(jsii_name="resetFlexibleRuntimeSettings")
    def reset_flexible_runtime_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlexibleRuntimeSettings", []))

    @jsii.member(jsii_name="resetHandlers")
    def reset_handlers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandlers", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInboundServices")
    def reset_inbound_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInboundServices", []))

    @jsii.member(jsii_name="resetInstanceClass")
    def reset_instance_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceClass", []))

    @jsii.member(jsii_name="resetManualScaling")
    def reset_manual_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualScaling", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNobuildFilesRegex")
    def reset_nobuild_files_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNobuildFilesRegex", []))

    @jsii.member(jsii_name="resetNoopOnDestroy")
    def reset_noop_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoopOnDestroy", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRuntimeApiVersion")
    def reset_runtime_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeApiVersion", []))

    @jsii.member(jsii_name="resetRuntimeChannel")
    def reset_runtime_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeChannel", []))

    @jsii.member(jsii_name="resetRuntimeMainExecutablePath")
    def reset_runtime_main_executable_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeMainExecutablePath", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetServingStatus")
    def reset_serving_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServingStatus", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersionId")
    def reset_version_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionId", []))

    @jsii.member(jsii_name="resetVpcAccessConnector")
    def reset_vpc_access_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccessConnector", []))

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
    @jsii.member(jsii_name="apiConfig")
    def api_config(self) -> "AppEngineFlexibleAppVersionApiConfigOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionApiConfigOutputReference", jsii.get(self, "apiConfig"))

    @builtins.property
    @jsii.member(jsii_name="automaticScaling")
    def automatic_scaling(
        self,
    ) -> "AppEngineFlexibleAppVersionAutomaticScalingOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionAutomaticScalingOutputReference", jsii.get(self, "automaticScaling"))

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(self) -> "AppEngineFlexibleAppVersionDeploymentOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionDeploymentOutputReference", jsii.get(self, "deployment"))

    @builtins.property
    @jsii.member(jsii_name="endpointsApiService")
    def endpoints_api_service(
        self,
    ) -> "AppEngineFlexibleAppVersionEndpointsApiServiceOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionEndpointsApiServiceOutputReference", jsii.get(self, "endpointsApiService"))

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> "AppEngineFlexibleAppVersionEntrypointOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionEntrypointOutputReference", jsii.get(self, "entrypoint"))

    @builtins.property
    @jsii.member(jsii_name="flexibleRuntimeSettings")
    def flexible_runtime_settings(
        self,
    ) -> "AppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference", jsii.get(self, "flexibleRuntimeSettings"))

    @builtins.property
    @jsii.member(jsii_name="handlers")
    def handlers(self) -> "AppEngineFlexibleAppVersionHandlersList":
        return typing.cast("AppEngineFlexibleAppVersionHandlersList", jsii.get(self, "handlers"))

    @builtins.property
    @jsii.member(jsii_name="livenessCheck")
    def liveness_check(
        self,
    ) -> "AppEngineFlexibleAppVersionLivenessCheckOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionLivenessCheckOutputReference", jsii.get(self, "livenessCheck"))

    @builtins.property
    @jsii.member(jsii_name="manualScaling")
    def manual_scaling(
        self,
    ) -> "AppEngineFlexibleAppVersionManualScalingOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionManualScalingOutputReference", jsii.get(self, "manualScaling"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "AppEngineFlexibleAppVersionNetworkOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="readinessCheck")
    def readiness_check(
        self,
    ) -> "AppEngineFlexibleAppVersionReadinessCheckOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionReadinessCheckOutputReference", jsii.get(self, "readinessCheck"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "AppEngineFlexibleAppVersionResourcesOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AppEngineFlexibleAppVersionTimeoutsOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnector")
    def vpc_access_connector(
        self,
    ) -> "AppEngineFlexibleAppVersionVpcAccessConnectorOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionVpcAccessConnectorOutputReference", jsii.get(self, "vpcAccessConnector"))

    @builtins.property
    @jsii.member(jsii_name="apiConfigInput")
    def api_config_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionApiConfig"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionApiConfig"], jsii.get(self, "apiConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticScalingInput")
    def automatic_scaling_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionAutomaticScaling"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionAutomaticScaling"], jsii.get(self, "automaticScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="betaSettingsInput")
    def beta_settings_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "betaSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultExpirationInput")
    def default_expiration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteServiceOnDestroyInput")
    def delete_service_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteServiceOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentInput")
    def deployment_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionDeployment"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionDeployment"], jsii.get(self, "deploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsApiServiceInput")
    def endpoints_api_service_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionEndpointsApiService"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionEndpointsApiService"], jsii.get(self, "endpointsApiServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="entrypointInput")
    def entrypoint_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionEntrypoint"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionEntrypoint"], jsii.get(self, "entrypointInput"))

    @builtins.property
    @jsii.member(jsii_name="envVariablesInput")
    def env_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="flexibleRuntimeSettingsInput")
    def flexible_runtime_settings_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionFlexibleRuntimeSettings"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionFlexibleRuntimeSettings"], jsii.get(self, "flexibleRuntimeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="handlersInput")
    def handlers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionHandlers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionHandlers"]]], jsii.get(self, "handlersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inboundServicesInput")
    def inbound_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inboundServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceClassInput")
    def instance_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceClassInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessCheckInput")
    def liveness_check_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionLivenessCheck"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionLivenessCheck"], jsii.get(self, "livenessCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="manualScalingInput")
    def manual_scaling_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionManualScaling"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionManualScaling"], jsii.get(self, "manualScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["AppEngineFlexibleAppVersionNetwork"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nobuildFilesRegexInput")
    def nobuild_files_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nobuildFilesRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="noopOnDestroyInput")
    def noop_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noopOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="readinessCheckInput")
    def readiness_check_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionReadinessCheck"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionReadinessCheck"], jsii.get(self, "readinessCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionResources"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeApiVersionInput")
    def runtime_api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeApiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeChannelInput")
    def runtime_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeMainExecutablePathInput")
    def runtime_main_executable_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeMainExecutablePathInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="servingStatusInput")
    def serving_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servingStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppEngineFlexibleAppVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppEngineFlexibleAppVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionIdInput")
    def version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnectorInput")
    def vpc_access_connector_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionVpcAccessConnector"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionVpcAccessConnector"], jsii.get(self, "vpcAccessConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="betaSettings")
    def beta_settings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "betaSettings"))

    @beta_settings.setter
    def beta_settings(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43936e328a204423669fcc377e5250e960607d64ae1e1b5d13477e6b160108c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "betaSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultExpiration")
    def default_expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultExpiration"))

    @default_expiration.setter
    def default_expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3de01269a4e61bb09c9b3e83a0e4ef233fe0e2f04aa74c15eba9e39be7cf86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultExpiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteServiceOnDestroy")
    def delete_service_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteServiceOnDestroy"))

    @delete_service_on_destroy.setter
    def delete_service_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842ad4b62da031d61fa2b8610807ada57dbc1116479986aae8920467556c39ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteServiceOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envVariables")
    def env_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "envVariables"))

    @env_variables.setter
    def env_variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935cb89345a43ba055cbfc9325e4f805f31a43befaa961d30deb9313f76b9968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f1cb210e4b45d91d2e1c2e79bcb2e69e39eabdd28b069c416f582010c08d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundServices")
    def inbound_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inboundServices"))

    @inbound_services.setter
    def inbound_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e42b7b034ece8ea72f89a87203544303e2409e8f17044a845782117db4ef40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceClass")
    def instance_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceClass"))

    @instance_class.setter
    def instance_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66baf3c26f53a1895261cea2362df893a44e8258b3a43f509ba7288eda32f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nobuildFilesRegex")
    def nobuild_files_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nobuildFilesRegex"))

    @nobuild_files_regex.setter
    def nobuild_files_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c84b655326c0e4da77f47d2e5580b33a4dc22147b43456812881a93ac2567f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nobuildFilesRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noopOnDestroy")
    def noop_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noopOnDestroy"))

    @noop_on_destroy.setter
    def noop_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9277434eb630bf83f650924d247716ab26d315709b863041b4558885f5b00890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noopOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afafea02b62c5ca0e3835fff1eea08b5b44d50f3dbed836ce9fa4f412b699092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58ba58195f3ea7b06a6d311bd57eb253f5a374b8974df6a04751c8b412891e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeApiVersion")
    def runtime_api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeApiVersion"))

    @runtime_api_version.setter
    def runtime_api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e77d29c845e8d2460d93d3631568e9d1aad90b39d902d1de8e2f39317d97be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeChannel")
    def runtime_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeChannel"))

    @runtime_channel.setter
    def runtime_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c7a653259a27ca13dea9c36cdce953838aefaabccae9e85459a6d0ce51495f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeMainExecutablePath")
    def runtime_main_executable_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeMainExecutablePath"))

    @runtime_main_executable_path.setter
    def runtime_main_executable_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ccac7695545e0c88c9cb0099e56ebfcc0e049620ddba9e1c8d51106515b948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeMainExecutablePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663aa1aefe0081cffcc74aff636604118e98e3ce2febd709e462ae9fb0ca655a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5127f6c6cf8a14c847cd371918efae09972bd5c7a7595d71c32c0773aed09702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servingStatus")
    def serving_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servingStatus"))

    @serving_status.setter
    def serving_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7226339c4cac65f79693a3d48a8c4238f1cc9e774a6876054d85dad7a9a372ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servingStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309e2aa1426ec3f78583c0932b186644dbee5a7a2024fc636f9409061e19939b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionApiConfig",
    jsii_struct_bases=[],
    name_mapping={
        "script": "script",
        "auth_fail_action": "authFailAction",
        "login": "login",
        "security_level": "securityLevel",
        "url": "url",
    },
)
class AppEngineFlexibleAppVersionApiConfig:
    def __init__(
        self,
        *,
        script: builtins.str,
        auth_fail_action: typing.Optional[builtins.str] = None,
        login: typing.Optional[builtins.str] = None,
        security_level: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param script: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script AppEngineFlexibleAppVersion#script}
        :param auth_fail_action: Action to take when users access resources that require authentication. Default value: "AUTH_FAIL_ACTION_REDIRECT" Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#auth_fail_action AppEngineFlexibleAppVersion#auth_fail_action}
        :param login: Level of login required to access this resource. Default value: "LOGIN_OPTIONAL" Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#login AppEngineFlexibleAppVersion#login}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#security_level AppEngineFlexibleAppVersion#security_level}
        :param url: URL to serve the endpoint at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#url AppEngineFlexibleAppVersion#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e340960f181a5b2b488acc4d868bfad10312739207d323bf1ac85a0d270aa6a)
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument auth_fail_action", value=auth_fail_action, expected_type=type_hints["auth_fail_action"])
            check_type(argname="argument login", value=login, expected_type=type_hints["login"])
            check_type(argname="argument security_level", value=security_level, expected_type=type_hints["security_level"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script": script,
        }
        if auth_fail_action is not None:
            self._values["auth_fail_action"] = auth_fail_action
        if login is not None:
            self._values["login"] = login
        if security_level is not None:
            self._values["security_level"] = security_level
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def script(self) -> builtins.str:
        '''Path to the script from the application root directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script AppEngineFlexibleAppVersion#script}
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_fail_action(self) -> typing.Optional[builtins.str]:
        '''Action to take when users access resources that require authentication. Default value: "AUTH_FAIL_ACTION_REDIRECT" Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#auth_fail_action AppEngineFlexibleAppVersion#auth_fail_action}
        '''
        result = self._values.get("auth_fail_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login(self) -> typing.Optional[builtins.str]:
        '''Level of login required to access this resource. Default value: "LOGIN_OPTIONAL" Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#login AppEngineFlexibleAppVersion#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#security_level AppEngineFlexibleAppVersion#security_level}
        '''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''URL to serve the endpoint at.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#url AppEngineFlexibleAppVersion#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionApiConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionApiConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionApiConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aa1373194e2042d8e4a3002a6d251500fbe8a43b6b8f0e70a17454735a3dee3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthFailAction")
    def reset_auth_fail_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthFailAction", []))

    @jsii.member(jsii_name="resetLogin")
    def reset_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogin", []))

    @jsii.member(jsii_name="resetSecurityLevel")
    def reset_security_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityLevel", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="authFailActionInput")
    def auth_fail_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authFailActionInput"))

    @builtins.property
    @jsii.member(jsii_name="loginInput")
    def login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="securityLevelInput")
    def security_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="authFailAction")
    def auth_fail_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authFailAction"))

    @auth_fail_action.setter
    def auth_fail_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda7f99f7efb6cc7c9c948da8de817cacf7d3b157667969bb4b03a2b915f88e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authFailAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "login"))

    @login.setter
    def login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f42230c079693f5daa9658c4ab10b5566b79e3b71123c100b1bbe9fbd0514e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "login", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43157cb358ab8b736712cd84d101f382d0fc3afb1c6bd4cec39a28e9584268cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @security_level.setter
    def security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2c57a27946e8e77e845748a11f477f78f4aa55e2f69540bc53796e988feadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c47aeed0e6a9cd2c4bd625be74a535988449aba66a6eadd3a2bc929cf885b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineFlexibleAppVersionApiConfig]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionApiConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionApiConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9acd96a8d246ac854f77dbcf5d78e8a7ba530e1388502e0aa0de9291fa7b4f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScaling",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_utilization": "cpuUtilization",
        "cool_down_period": "coolDownPeriod",
        "disk_utilization": "diskUtilization",
        "max_concurrent_requests": "maxConcurrentRequests",
        "max_idle_instances": "maxIdleInstances",
        "max_pending_latency": "maxPendingLatency",
        "max_total_instances": "maxTotalInstances",
        "min_idle_instances": "minIdleInstances",
        "min_pending_latency": "minPendingLatency",
        "min_total_instances": "minTotalInstances",
        "network_utilization": "networkUtilization",
        "request_utilization": "requestUtilization",
    },
)
class AppEngineFlexibleAppVersionAutomaticScaling:
    def __init__(
        self,
        *,
        cpu_utilization: typing.Union["AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization", typing.Dict[builtins.str, typing.Any]],
        cool_down_period: typing.Optional[builtins.str] = None,
        disk_utilization: typing.Optional[typing.Union["AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_requests: typing.Optional[jsii.Number] = None,
        max_idle_instances: typing.Optional[jsii.Number] = None,
        max_pending_latency: typing.Optional[builtins.str] = None,
        max_total_instances: typing.Optional[jsii.Number] = None,
        min_idle_instances: typing.Optional[jsii.Number] = None,
        min_pending_latency: typing.Optional[builtins.str] = None,
        min_total_instances: typing.Optional[jsii.Number] = None,
        network_utilization: typing.Optional[typing.Union["AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        request_utilization: typing.Optional[typing.Union["AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cpu_utilization AppEngineFlexibleAppVersion#cpu_utilization}
        :param cool_down_period: The time period that the Autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. Default: 120s Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cool_down_period AppEngineFlexibleAppVersion#cool_down_period}
        :param disk_utilization: disk_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disk_utilization AppEngineFlexibleAppVersion#disk_utilization}
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_concurrent_requests AppEngineFlexibleAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_idle_instances AppEngineFlexibleAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_pending_latency AppEngineFlexibleAppVersion#max_pending_latency}
        :param max_total_instances: Maximum number of instances that should be started to handle requests for this version. Default: 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_total_instances AppEngineFlexibleAppVersion#max_total_instances}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_idle_instances AppEngineFlexibleAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_pending_latency AppEngineFlexibleAppVersion#min_pending_latency}
        :param min_total_instances: Minimum number of running instances that should be maintained for this version. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_total_instances AppEngineFlexibleAppVersion#min_total_instances}
        :param network_utilization: network_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#network_utilization AppEngineFlexibleAppVersion#network_utilization}
        :param request_utilization: request_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#request_utilization AppEngineFlexibleAppVersion#request_utilization}
        '''
        if isinstance(cpu_utilization, dict):
            cpu_utilization = AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization(**cpu_utilization)
        if isinstance(disk_utilization, dict):
            disk_utilization = AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization(**disk_utilization)
        if isinstance(network_utilization, dict):
            network_utilization = AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization(**network_utilization)
        if isinstance(request_utilization, dict):
            request_utilization = AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization(**request_utilization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f292286440d5b53f2bac3996f50b11a5945066340b1452b28a18f6dfd269a6a)
            check_type(argname="argument cpu_utilization", value=cpu_utilization, expected_type=type_hints["cpu_utilization"])
            check_type(argname="argument cool_down_period", value=cool_down_period, expected_type=type_hints["cool_down_period"])
            check_type(argname="argument disk_utilization", value=disk_utilization, expected_type=type_hints["disk_utilization"])
            check_type(argname="argument max_concurrent_requests", value=max_concurrent_requests, expected_type=type_hints["max_concurrent_requests"])
            check_type(argname="argument max_idle_instances", value=max_idle_instances, expected_type=type_hints["max_idle_instances"])
            check_type(argname="argument max_pending_latency", value=max_pending_latency, expected_type=type_hints["max_pending_latency"])
            check_type(argname="argument max_total_instances", value=max_total_instances, expected_type=type_hints["max_total_instances"])
            check_type(argname="argument min_idle_instances", value=min_idle_instances, expected_type=type_hints["min_idle_instances"])
            check_type(argname="argument min_pending_latency", value=min_pending_latency, expected_type=type_hints["min_pending_latency"])
            check_type(argname="argument min_total_instances", value=min_total_instances, expected_type=type_hints["min_total_instances"])
            check_type(argname="argument network_utilization", value=network_utilization, expected_type=type_hints["network_utilization"])
            check_type(argname="argument request_utilization", value=request_utilization, expected_type=type_hints["request_utilization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu_utilization": cpu_utilization,
        }
        if cool_down_period is not None:
            self._values["cool_down_period"] = cool_down_period
        if disk_utilization is not None:
            self._values["disk_utilization"] = disk_utilization
        if max_concurrent_requests is not None:
            self._values["max_concurrent_requests"] = max_concurrent_requests
        if max_idle_instances is not None:
            self._values["max_idle_instances"] = max_idle_instances
        if max_pending_latency is not None:
            self._values["max_pending_latency"] = max_pending_latency
        if max_total_instances is not None:
            self._values["max_total_instances"] = max_total_instances
        if min_idle_instances is not None:
            self._values["min_idle_instances"] = min_idle_instances
        if min_pending_latency is not None:
            self._values["min_pending_latency"] = min_pending_latency
        if min_total_instances is not None:
            self._values["min_total_instances"] = min_total_instances
        if network_utilization is not None:
            self._values["network_utilization"] = network_utilization
        if request_utilization is not None:
            self._values["request_utilization"] = request_utilization

    @builtins.property
    def cpu_utilization(
        self,
    ) -> "AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization":
        '''cpu_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cpu_utilization AppEngineFlexibleAppVersion#cpu_utilization}
        '''
        result = self._values.get("cpu_utilization")
        assert result is not None, "Required property 'cpu_utilization' is missing"
        return typing.cast("AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization", result)

    @builtins.property
    def cool_down_period(self) -> typing.Optional[builtins.str]:
        '''The time period that the Autoscaler should wait before it starts collecting information from a new instance.

        This prevents the autoscaler from collecting information when the instance is initializing,
        during which the collected usage would not be reliable. Default: 120s

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cool_down_period AppEngineFlexibleAppVersion#cool_down_period}
        '''
        result = self._values.get("cool_down_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_utilization(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization"]:
        '''disk_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disk_utilization AppEngineFlexibleAppVersion#disk_utilization}
        '''
        result = self._values.get("disk_utilization")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization"], result)

    @builtins.property
    def max_concurrent_requests(self) -> typing.Optional[jsii.Number]:
        '''Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance.

        Defaults to a runtime-specific value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_concurrent_requests AppEngineFlexibleAppVersion#max_concurrent_requests}
        '''
        result = self._values.get("max_concurrent_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle instances that should be maintained for this version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_idle_instances AppEngineFlexibleAppVersion#max_idle_instances}
        '''
        result = self._values.get("max_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_pending_latency AppEngineFlexibleAppVersion#max_pending_latency}
        '''
        result = self._values.get("max_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_total_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of instances that should be started to handle requests for this version. Default: 20.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#max_total_instances AppEngineFlexibleAppVersion#max_total_instances}
        '''
        result = self._values.get("max_total_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of idle instances that should be maintained for this version.

        Only applicable for the default version of a service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_idle_instances AppEngineFlexibleAppVersion#min_idle_instances}
        '''
        result = self._values.get("min_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_pending_latency AppEngineFlexibleAppVersion#min_pending_latency}
        '''
        result = self._values.get("min_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_total_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of running instances that should be maintained for this version. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#min_total_instances AppEngineFlexibleAppVersion#min_total_instances}
        '''
        result = self._values.get("min_total_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_utilization(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization"]:
        '''network_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#network_utilization AppEngineFlexibleAppVersion#network_utilization}
        '''
        result = self._values.get("network_utilization")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization"], result)

    @builtins.property
    def request_utilization(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"]:
        '''request_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#request_utilization AppEngineFlexibleAppVersion#request_utilization}
        '''
        result = self._values.get("request_utilization")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionAutomaticScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_utilization": "targetUtilization",
        "aggregation_window_length": "aggregationWindowLength",
    },
)
class AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization:
    def __init__(
        self,
        *,
        target_utilization: jsii.Number,
        aggregation_window_length: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_utilization: Target CPU utilization ratio to maintain when scaling. Must be between 0 and 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_utilization AppEngineFlexibleAppVersion#target_utilization}
        :param aggregation_window_length: Period of time over which CPU utilization is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#aggregation_window_length AppEngineFlexibleAppVersion#aggregation_window_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4249c050c7b6ac7898badc8cdfff5049a65e260e57428eb36ea6169ccc7fe77a)
            check_type(argname="argument target_utilization", value=target_utilization, expected_type=type_hints["target_utilization"])
            check_type(argname="argument aggregation_window_length", value=aggregation_window_length, expected_type=type_hints["aggregation_window_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_utilization": target_utilization,
        }
        if aggregation_window_length is not None:
            self._values["aggregation_window_length"] = aggregation_window_length

    @builtins.property
    def target_utilization(self) -> jsii.Number:
        '''Target CPU utilization ratio to maintain when scaling. Must be between 0 and 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_utilization AppEngineFlexibleAppVersion#target_utilization}
        '''
        result = self._values.get("target_utilization")
        assert result is not None, "Required property 'target_utilization' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def aggregation_window_length(self) -> typing.Optional[builtins.str]:
        '''Period of time over which CPU utilization is calculated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#aggregation_window_length AppEngineFlexibleAppVersion#aggregation_window_length}
        '''
        result = self._values.get("aggregation_window_length")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1601cc0345dce1dbbfbf3837b5e1f9ce7891dbbe977dccc11b0c0ed32effcd47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregationWindowLength")
    def reset_aggregation_window_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationWindowLength", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationWindowLengthInput")
    def aggregation_window_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationWindowLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="targetUtilizationInput")
    def target_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationWindowLength")
    def aggregation_window_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationWindowLength"))

    @aggregation_window_length.setter
    def aggregation_window_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bf159713491ca330604e9204a93a4972682ff387a53e23587980b215c8c512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationWindowLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetUtilization")
    def target_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetUtilization"))

    @target_utilization.setter
    def target_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbeae3e48b5339ebfc03b2449bd6d99b4a690b018e439fe51a59aefc507a72a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__accff91caacc593833b2f00a73e9876ad4a29c2717fc4fbdaac3bffd76927d67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_read_bytes_per_second": "targetReadBytesPerSecond",
        "target_read_ops_per_second": "targetReadOpsPerSecond",
        "target_write_bytes_per_second": "targetWriteBytesPerSecond",
        "target_write_ops_per_second": "targetWriteOpsPerSecond",
    },
)
class AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization:
    def __init__(
        self,
        *,
        target_read_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_read_ops_per_second: typing.Optional[jsii.Number] = None,
        target_write_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_write_ops_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_read_bytes_per_second: Target bytes read per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_read_bytes_per_second AppEngineFlexibleAppVersion#target_read_bytes_per_second}
        :param target_read_ops_per_second: Target ops read per seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_read_ops_per_second AppEngineFlexibleAppVersion#target_read_ops_per_second}
        :param target_write_bytes_per_second: Target bytes written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_write_bytes_per_second AppEngineFlexibleAppVersion#target_write_bytes_per_second}
        :param target_write_ops_per_second: Target ops written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_write_ops_per_second AppEngineFlexibleAppVersion#target_write_ops_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6cb7f36ec168bf0e0db1987e8fd48b0612086f94c3e95208f887e2e612c5b19)
            check_type(argname="argument target_read_bytes_per_second", value=target_read_bytes_per_second, expected_type=type_hints["target_read_bytes_per_second"])
            check_type(argname="argument target_read_ops_per_second", value=target_read_ops_per_second, expected_type=type_hints["target_read_ops_per_second"])
            check_type(argname="argument target_write_bytes_per_second", value=target_write_bytes_per_second, expected_type=type_hints["target_write_bytes_per_second"])
            check_type(argname="argument target_write_ops_per_second", value=target_write_ops_per_second, expected_type=type_hints["target_write_ops_per_second"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_read_bytes_per_second is not None:
            self._values["target_read_bytes_per_second"] = target_read_bytes_per_second
        if target_read_ops_per_second is not None:
            self._values["target_read_ops_per_second"] = target_read_ops_per_second
        if target_write_bytes_per_second is not None:
            self._values["target_write_bytes_per_second"] = target_write_bytes_per_second
        if target_write_ops_per_second is not None:
            self._values["target_write_ops_per_second"] = target_write_ops_per_second

    @builtins.property
    def target_read_bytes_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target bytes read per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_read_bytes_per_second AppEngineFlexibleAppVersion#target_read_bytes_per_second}
        '''
        result = self._values.get("target_read_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_read_ops_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target ops read per seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_read_ops_per_second AppEngineFlexibleAppVersion#target_read_ops_per_second}
        '''
        result = self._values.get("target_read_ops_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_write_bytes_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target bytes written per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_write_bytes_per_second AppEngineFlexibleAppVersion#target_write_bytes_per_second}
        '''
        result = self._values.get("target_write_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_write_ops_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target ops written per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_write_ops_per_second AppEngineFlexibleAppVersion#target_write_ops_per_second}
        '''
        result = self._values.get("target_write_ops_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7477868ecf60d73c6a728a346b976937949ab7ee708c420a20dce2bc41a71019)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTargetReadBytesPerSecond")
    def reset_target_read_bytes_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetReadBytesPerSecond", []))

    @jsii.member(jsii_name="resetTargetReadOpsPerSecond")
    def reset_target_read_ops_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetReadOpsPerSecond", []))

    @jsii.member(jsii_name="resetTargetWriteBytesPerSecond")
    def reset_target_write_bytes_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetWriteBytesPerSecond", []))

    @jsii.member(jsii_name="resetTargetWriteOpsPerSecond")
    def reset_target_write_ops_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetWriteOpsPerSecond", []))

    @builtins.property
    @jsii.member(jsii_name="targetReadBytesPerSecondInput")
    def target_read_bytes_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetReadBytesPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetReadOpsPerSecondInput")
    def target_read_ops_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetReadOpsPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetWriteBytesPerSecondInput")
    def target_write_bytes_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetWriteBytesPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetWriteOpsPerSecondInput")
    def target_write_ops_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetWriteOpsPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetReadBytesPerSecond")
    def target_read_bytes_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReadBytesPerSecond"))

    @target_read_bytes_per_second.setter
    def target_read_bytes_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c38a5e060028fcdf07277a12e4d299a2b080261eff0436d7feb0910d15ee00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReadBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetReadOpsPerSecond")
    def target_read_ops_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReadOpsPerSecond"))

    @target_read_ops_per_second.setter
    def target_read_ops_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878b60c1b9c037bc828955fa2d7218dc308be512ee74e80aa39469bc8f489053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReadOpsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetWriteBytesPerSecond")
    def target_write_bytes_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetWriteBytesPerSecond"))

    @target_write_bytes_per_second.setter
    def target_write_bytes_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe4c5065e16f13f0828f3dc61775df531119f1ba786b8d17bbeee01f8533fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetWriteBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetWriteOpsPerSecond")
    def target_write_ops_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetWriteOpsPerSecond"))

    @target_write_ops_per_second.setter
    def target_write_ops_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280be15a44f4247c3fb4d465dcc25ef67576d9ce10643e29e5fa28c2a59d6a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetWriteOpsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3aa1ad199f6203ad40f92f3ec1ce99f2295a64e0acef5e525ede34b75941620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_received_bytes_per_second": "targetReceivedBytesPerSecond",
        "target_received_packets_per_second": "targetReceivedPacketsPerSecond",
        "target_sent_bytes_per_second": "targetSentBytesPerSecond",
        "target_sent_packets_per_second": "targetSentPacketsPerSecond",
    },
)
class AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization:
    def __init__(
        self,
        *,
        target_received_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_received_packets_per_second: typing.Optional[jsii.Number] = None,
        target_sent_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_sent_packets_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_received_bytes_per_second: Target bytes received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_received_bytes_per_second AppEngineFlexibleAppVersion#target_received_bytes_per_second}
        :param target_received_packets_per_second: Target packets received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_received_packets_per_second AppEngineFlexibleAppVersion#target_received_packets_per_second}
        :param target_sent_bytes_per_second: Target bytes sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_sent_bytes_per_second AppEngineFlexibleAppVersion#target_sent_bytes_per_second}
        :param target_sent_packets_per_second: Target packets sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_sent_packets_per_second AppEngineFlexibleAppVersion#target_sent_packets_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd9e939069da4c6f670272f6eb16f44c2fad908d59edbf72ebe8e6508befb05)
            check_type(argname="argument target_received_bytes_per_second", value=target_received_bytes_per_second, expected_type=type_hints["target_received_bytes_per_second"])
            check_type(argname="argument target_received_packets_per_second", value=target_received_packets_per_second, expected_type=type_hints["target_received_packets_per_second"])
            check_type(argname="argument target_sent_bytes_per_second", value=target_sent_bytes_per_second, expected_type=type_hints["target_sent_bytes_per_second"])
            check_type(argname="argument target_sent_packets_per_second", value=target_sent_packets_per_second, expected_type=type_hints["target_sent_packets_per_second"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_received_bytes_per_second is not None:
            self._values["target_received_bytes_per_second"] = target_received_bytes_per_second
        if target_received_packets_per_second is not None:
            self._values["target_received_packets_per_second"] = target_received_packets_per_second
        if target_sent_bytes_per_second is not None:
            self._values["target_sent_bytes_per_second"] = target_sent_bytes_per_second
        if target_sent_packets_per_second is not None:
            self._values["target_sent_packets_per_second"] = target_sent_packets_per_second

    @builtins.property
    def target_received_bytes_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target bytes received per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_received_bytes_per_second AppEngineFlexibleAppVersion#target_received_bytes_per_second}
        '''
        result = self._values.get("target_received_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_received_packets_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target packets received per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_received_packets_per_second AppEngineFlexibleAppVersion#target_received_packets_per_second}
        '''
        result = self._values.get("target_received_packets_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_sent_bytes_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target bytes sent per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_sent_bytes_per_second AppEngineFlexibleAppVersion#target_sent_bytes_per_second}
        '''
        result = self._values.get("target_sent_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_sent_packets_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target packets sent per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_sent_packets_per_second AppEngineFlexibleAppVersion#target_sent_packets_per_second}
        '''
        result = self._values.get("target_sent_packets_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c9c5ec3a2622ceed8a301a84f5600b693927881cc30c7542a99f56bce623120)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTargetReceivedBytesPerSecond")
    def reset_target_received_bytes_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetReceivedBytesPerSecond", []))

    @jsii.member(jsii_name="resetTargetReceivedPacketsPerSecond")
    def reset_target_received_packets_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetReceivedPacketsPerSecond", []))

    @jsii.member(jsii_name="resetTargetSentBytesPerSecond")
    def reset_target_sent_bytes_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSentBytesPerSecond", []))

    @jsii.member(jsii_name="resetTargetSentPacketsPerSecond")
    def reset_target_sent_packets_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetSentPacketsPerSecond", []))

    @builtins.property
    @jsii.member(jsii_name="targetReceivedBytesPerSecondInput")
    def target_received_bytes_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetReceivedBytesPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetReceivedPacketsPerSecondInput")
    def target_received_packets_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetReceivedPacketsPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSentBytesPerSecondInput")
    def target_sent_bytes_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetSentBytesPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSentPacketsPerSecondInput")
    def target_sent_packets_per_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetSentPacketsPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetReceivedBytesPerSecond")
    def target_received_bytes_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReceivedBytesPerSecond"))

    @target_received_bytes_per_second.setter
    def target_received_bytes_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3932ce9b21f75d17c8f20d796b515eff587784c3daa198e50eaf80320b432c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReceivedBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetReceivedPacketsPerSecond")
    def target_received_packets_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReceivedPacketsPerSecond"))

    @target_received_packets_per_second.setter
    def target_received_packets_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8027863260aa7c455bb24f3513786412899ab2ec23effc33620db2c9c0ee2c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReceivedPacketsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSentBytesPerSecond")
    def target_sent_bytes_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSentBytesPerSecond"))

    @target_sent_bytes_per_second.setter
    def target_sent_bytes_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e37c5ff3f3db9529545b14984e2470d2de482913c39a9f41fa68a2d8a6db612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSentBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSentPacketsPerSecond")
    def target_sent_packets_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSentPacketsPerSecond"))

    @target_sent_packets_per_second.setter
    def target_sent_packets_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f055b7ce0606cfcbc949106d6bdd8485e2eb22f9be3450227b75b70b8adbc5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSentPacketsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f856d5d7f18d99b99412d4aa391e1431ba5c7ef357ea923ec0839b2fb1fb964b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineFlexibleAppVersionAutomaticScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c440e2c760fceacf783f7077e22592488d50091d0c118253a5e0cb7a66531468)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCpuUtilization")
    def put_cpu_utilization(
        self,
        *,
        target_utilization: jsii.Number,
        aggregation_window_length: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_utilization: Target CPU utilization ratio to maintain when scaling. Must be between 0 and 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_utilization AppEngineFlexibleAppVersion#target_utilization}
        :param aggregation_window_length: Period of time over which CPU utilization is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#aggregation_window_length AppEngineFlexibleAppVersion#aggregation_window_length}
        '''
        value = AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization(
            target_utilization=target_utilization,
            aggregation_window_length=aggregation_window_length,
        )

        return typing.cast(None, jsii.invoke(self, "putCpuUtilization", [value]))

    @jsii.member(jsii_name="putDiskUtilization")
    def put_disk_utilization(
        self,
        *,
        target_read_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_read_ops_per_second: typing.Optional[jsii.Number] = None,
        target_write_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_write_ops_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_read_bytes_per_second: Target bytes read per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_read_bytes_per_second AppEngineFlexibleAppVersion#target_read_bytes_per_second}
        :param target_read_ops_per_second: Target ops read per seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_read_ops_per_second AppEngineFlexibleAppVersion#target_read_ops_per_second}
        :param target_write_bytes_per_second: Target bytes written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_write_bytes_per_second AppEngineFlexibleAppVersion#target_write_bytes_per_second}
        :param target_write_ops_per_second: Target ops written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_write_ops_per_second AppEngineFlexibleAppVersion#target_write_ops_per_second}
        '''
        value = AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization(
            target_read_bytes_per_second=target_read_bytes_per_second,
            target_read_ops_per_second=target_read_ops_per_second,
            target_write_bytes_per_second=target_write_bytes_per_second,
            target_write_ops_per_second=target_write_ops_per_second,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskUtilization", [value]))

    @jsii.member(jsii_name="putNetworkUtilization")
    def put_network_utilization(
        self,
        *,
        target_received_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_received_packets_per_second: typing.Optional[jsii.Number] = None,
        target_sent_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_sent_packets_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_received_bytes_per_second: Target bytes received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_received_bytes_per_second AppEngineFlexibleAppVersion#target_received_bytes_per_second}
        :param target_received_packets_per_second: Target packets received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_received_packets_per_second AppEngineFlexibleAppVersion#target_received_packets_per_second}
        :param target_sent_bytes_per_second: Target bytes sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_sent_bytes_per_second AppEngineFlexibleAppVersion#target_sent_bytes_per_second}
        :param target_sent_packets_per_second: Target packets sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_sent_packets_per_second AppEngineFlexibleAppVersion#target_sent_packets_per_second}
        '''
        value = AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization(
            target_received_bytes_per_second=target_received_bytes_per_second,
            target_received_packets_per_second=target_received_packets_per_second,
            target_sent_bytes_per_second=target_sent_bytes_per_second,
            target_sent_packets_per_second=target_sent_packets_per_second,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkUtilization", [value]))

    @jsii.member(jsii_name="putRequestUtilization")
    def put_request_utilization(
        self,
        *,
        target_concurrent_requests: typing.Optional[jsii.Number] = None,
        target_request_count_per_second: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_concurrent_requests: Target number of concurrent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_concurrent_requests AppEngineFlexibleAppVersion#target_concurrent_requests}
        :param target_request_count_per_second: Target requests per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_request_count_per_second AppEngineFlexibleAppVersion#target_request_count_per_second}
        '''
        value = AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization(
            target_concurrent_requests=target_concurrent_requests,
            target_request_count_per_second=target_request_count_per_second,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestUtilization", [value]))

    @jsii.member(jsii_name="resetCoolDownPeriod")
    def reset_cool_down_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolDownPeriod", []))

    @jsii.member(jsii_name="resetDiskUtilization")
    def reset_disk_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskUtilization", []))

    @jsii.member(jsii_name="resetMaxConcurrentRequests")
    def reset_max_concurrent_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentRequests", []))

    @jsii.member(jsii_name="resetMaxIdleInstances")
    def reset_max_idle_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleInstances", []))

    @jsii.member(jsii_name="resetMaxPendingLatency")
    def reset_max_pending_latency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPendingLatency", []))

    @jsii.member(jsii_name="resetMaxTotalInstances")
    def reset_max_total_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTotalInstances", []))

    @jsii.member(jsii_name="resetMinIdleInstances")
    def reset_min_idle_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinIdleInstances", []))

    @jsii.member(jsii_name="resetMinPendingLatency")
    def reset_min_pending_latency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinPendingLatency", []))

    @jsii.member(jsii_name="resetMinTotalInstances")
    def reset_min_total_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTotalInstances", []))

    @jsii.member(jsii_name="resetNetworkUtilization")
    def reset_network_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkUtilization", []))

    @jsii.member(jsii_name="resetRequestUtilization")
    def reset_request_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestUtilization", []))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilization")
    def cpu_utilization(
        self,
    ) -> AppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference:
        return typing.cast(AppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference, jsii.get(self, "cpuUtilization"))

    @builtins.property
    @jsii.member(jsii_name="diskUtilization")
    def disk_utilization(
        self,
    ) -> AppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference:
        return typing.cast(AppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference, jsii.get(self, "diskUtilization"))

    @builtins.property
    @jsii.member(jsii_name="networkUtilization")
    def network_utilization(
        self,
    ) -> AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference:
        return typing.cast(AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference, jsii.get(self, "networkUtilization"))

    @builtins.property
    @jsii.member(jsii_name="requestUtilization")
    def request_utilization(
        self,
    ) -> "AppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference", jsii.get(self, "requestUtilization"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriodInput")
    def cool_down_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coolDownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationInput")
    def cpu_utilization_input(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization], jsii.get(self, "cpuUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="diskUtilizationInput")
    def disk_utilization_input(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization], jsii.get(self, "diskUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRequestsInput")
    def max_concurrent_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleInstancesInput")
    def max_idle_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPendingLatencyInput")
    def max_pending_latency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxPendingLatencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTotalInstancesInput")
    def max_total_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTotalInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minIdleInstancesInput")
    def min_idle_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minIdleInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minPendingLatencyInput")
    def min_pending_latency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minPendingLatencyInput"))

    @builtins.property
    @jsii.member(jsii_name="minTotalInstancesInput")
    def min_total_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minTotalInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUtilizationInput")
    def network_utilization_input(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization], jsii.get(self, "networkUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUtilizationInput")
    def request_utilization_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"], jsii.get(self, "requestUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriod")
    def cool_down_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coolDownPeriod"))

    @cool_down_period.setter
    def cool_down_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03392d2466377da4e5ad2b625614c72a92d2f75d329e9b08838af87b75621f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRequests")
    def max_concurrent_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentRequests"))

    @max_concurrent_requests.setter
    def max_concurrent_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4be6db8fafe0a26d15ff8c00bc5b195d9c386279322002b6abe331ae495f838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIdleInstances")
    def max_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleInstances"))

    @max_idle_instances.setter
    def max_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91f684db00e6eb9ca23693c587b31b7a213cc7763a030f6ff7dad3fb38b6b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingLatency")
    def max_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxPendingLatency"))

    @max_pending_latency.setter
    def max_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a296fa73f23ebc3f6f1d6b34be9f0169060d8d4d75c96c7f1a744387b901732e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTotalInstances")
    def max_total_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTotalInstances"))

    @max_total_instances.setter
    def max_total_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcad5d19680bba3da7f5a9bf38f6c3bf902e0939f547bd62a11fcfc799f09c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTotalInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minIdleInstances")
    def min_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minIdleInstances"))

    @min_idle_instances.setter
    def min_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be49b6cf8dfa907963c67c9bbe3a0864d5a393f71b265d67a3df2ac3df899df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minPendingLatency")
    def min_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minPendingLatency"))

    @min_pending_latency.setter
    def min_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75733115ed2e723bbe36b011bbe5d620be3c874ce402da81abd69fde8b5981f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTotalInstances")
    def min_total_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minTotalInstances"))

    @min_total_instances.setter
    def min_total_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f11f8c1a4bb0602518283e03de0f8b75f70227af933e628907f79bb68ce88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTotalInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScaling]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1d3379eb51b7804205bd89b449d002e8ea6865b3e89255b350419e0eb0c745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_concurrent_requests": "targetConcurrentRequests",
        "target_request_count_per_second": "targetRequestCountPerSecond",
    },
)
class AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization:
    def __init__(
        self,
        *,
        target_concurrent_requests: typing.Optional[jsii.Number] = None,
        target_request_count_per_second: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_concurrent_requests: Target number of concurrent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_concurrent_requests AppEngineFlexibleAppVersion#target_concurrent_requests}
        :param target_request_count_per_second: Target requests per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_request_count_per_second AppEngineFlexibleAppVersion#target_request_count_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfaf1954449d8dbc3ab6c60cf4331a39dfaaa86addf0313bd70a7e41f92a972)
            check_type(argname="argument target_concurrent_requests", value=target_concurrent_requests, expected_type=type_hints["target_concurrent_requests"])
            check_type(argname="argument target_request_count_per_second", value=target_request_count_per_second, expected_type=type_hints["target_request_count_per_second"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_concurrent_requests is not None:
            self._values["target_concurrent_requests"] = target_concurrent_requests
        if target_request_count_per_second is not None:
            self._values["target_request_count_per_second"] = target_request_count_per_second

    @builtins.property
    def target_concurrent_requests(self) -> typing.Optional[jsii.Number]:
        '''Target number of concurrent requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_concurrent_requests AppEngineFlexibleAppVersion#target_concurrent_requests}
        '''
        result = self._values.get("target_concurrent_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_request_count_per_second(self) -> typing.Optional[builtins.str]:
        '''Target requests per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#target_request_count_per_second AppEngineFlexibleAppVersion#target_request_count_per_second}
        '''
        result = self._values.get("target_request_count_per_second")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__993cf687a7223b28238791fdfaddaa7e41626f6eebf94a528ee642a28f8b1673)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTargetConcurrentRequests")
    def reset_target_concurrent_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetConcurrentRequests", []))

    @jsii.member(jsii_name="resetTargetRequestCountPerSecond")
    def reset_target_request_count_per_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetRequestCountPerSecond", []))

    @builtins.property
    @jsii.member(jsii_name="targetConcurrentRequestsInput")
    def target_concurrent_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetConcurrentRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRequestCountPerSecondInput")
    def target_request_count_per_second_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRequestCountPerSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="targetConcurrentRequests")
    def target_concurrent_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetConcurrentRequests"))

    @target_concurrent_requests.setter
    def target_concurrent_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8a000d94dc01f639dbd2c067aedcd7c9007bf5053e2f42c0262a148de26e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetConcurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRequestCountPerSecond")
    def target_request_count_per_second(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRequestCountPerSecond"))

    @target_request_count_per_second.setter
    def target_request_count_per_second(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbfc99275bb97004bef724e94206928a29d88a68d00c3da98536671a54e39af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRequestCountPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4534c63888e89a664617eccbb139af650136c189b04b52343eec0e01c8f8ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "liveness_check": "livenessCheck",
        "readiness_check": "readinessCheck",
        "runtime": "runtime",
        "service": "service",
        "api_config": "apiConfig",
        "automatic_scaling": "automaticScaling",
        "beta_settings": "betaSettings",
        "default_expiration": "defaultExpiration",
        "delete_service_on_destroy": "deleteServiceOnDestroy",
        "deployment": "deployment",
        "endpoints_api_service": "endpointsApiService",
        "entrypoint": "entrypoint",
        "env_variables": "envVariables",
        "flexible_runtime_settings": "flexibleRuntimeSettings",
        "handlers": "handlers",
        "id": "id",
        "inbound_services": "inboundServices",
        "instance_class": "instanceClass",
        "manual_scaling": "manualScaling",
        "network": "network",
        "nobuild_files_regex": "nobuildFilesRegex",
        "noop_on_destroy": "noopOnDestroy",
        "project": "project",
        "resources": "resources",
        "runtime_api_version": "runtimeApiVersion",
        "runtime_channel": "runtimeChannel",
        "runtime_main_executable_path": "runtimeMainExecutablePath",
        "service_account": "serviceAccount",
        "serving_status": "servingStatus",
        "timeouts": "timeouts",
        "version_id": "versionId",
        "vpc_access_connector": "vpcAccessConnector",
    },
)
class AppEngineFlexibleAppVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        liveness_check: typing.Union["AppEngineFlexibleAppVersionLivenessCheck", typing.Dict[builtins.str, typing.Any]],
        readiness_check: typing.Union["AppEngineFlexibleAppVersionReadinessCheck", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        api_config: typing.Optional[typing.Union[AppEngineFlexibleAppVersionApiConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        automatic_scaling: typing.Optional[typing.Union[AppEngineFlexibleAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        default_expiration: typing.Optional[builtins.str] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoints_api_service: typing.Optional[typing.Union["AppEngineFlexibleAppVersionEndpointsApiService", typing.Dict[builtins.str, typing.Any]]] = None,
        entrypoint: typing.Optional[typing.Union["AppEngineFlexibleAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        flexible_runtime_settings: typing.Optional[typing.Union["AppEngineFlexibleAppVersionFlexibleRuntimeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        manual_scaling: typing.Optional[typing.Union["AppEngineFlexibleAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["AppEngineFlexibleAppVersionNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        nobuild_files_regex: typing.Optional[builtins.str] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Union["AppEngineFlexibleAppVersionResources", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        runtime_channel: typing.Optional[builtins.str] = None,
        runtime_main_executable_path: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        serving_status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppEngineFlexibleAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["AppEngineFlexibleAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param liveness_check: liveness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#liveness_check AppEngineFlexibleAppVersion#liveness_check}
        :param readiness_check: readiness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#readiness_check AppEngineFlexibleAppVersion#readiness_check}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime AppEngineFlexibleAppVersion#runtime}
        :param service: AppEngine service resource. Can contain numbers, letters, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#service AppEngineFlexibleAppVersion#service}
        :param api_config: api_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#api_config AppEngineFlexibleAppVersion#api_config}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#automatic_scaling AppEngineFlexibleAppVersion#automatic_scaling}
        :param beta_settings: Metadata settings that are supplied to this version to enable beta runtime features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#beta_settings AppEngineFlexibleAppVersion#beta_settings}
        :param default_expiration: Duration that static files should be cached by web proxies and browsers. Only applicable if the corresponding StaticFilesHandler does not specify its own expiration time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#default_expiration AppEngineFlexibleAppVersion#default_expiration}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#delete_service_on_destroy AppEngineFlexibleAppVersion#delete_service_on_destroy}
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#deployment AppEngineFlexibleAppVersion#deployment}
        :param endpoints_api_service: endpoints_api_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#endpoints_api_service AppEngineFlexibleAppVersion#endpoints_api_service}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#entrypoint AppEngineFlexibleAppVersion#entrypoint}
        :param env_variables: Environment variables available to the application. As these are not returned in the API request, Terraform will not detect any changes made outside of the Terraform config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#env_variables AppEngineFlexibleAppVersion#env_variables}
        :param flexible_runtime_settings: flexible_runtime_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#flexible_runtime_settings AppEngineFlexibleAppVersion#flexible_runtime_settings}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#handlers AppEngineFlexibleAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#id AppEngineFlexibleAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#inbound_services AppEngineFlexibleAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G ManualScaling: B1, B2, B4, B8, B4_1G Defaults to F1 for AutomaticScaling and B1 for ManualScaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instance_class AppEngineFlexibleAppVersion#instance_class}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#manual_scaling AppEngineFlexibleAppVersion#manual_scaling}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#network AppEngineFlexibleAppVersion#network}
        :param nobuild_files_regex: Files that match this pattern will not be built into this version. Only applicable for Go runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#nobuild_files_regex AppEngineFlexibleAppVersion#nobuild_files_regex}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#noop_on_destroy AppEngineFlexibleAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#project AppEngineFlexibleAppVersion#project}.
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#resources AppEngineFlexibleAppVersion#resources}
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_api_version AppEngineFlexibleAppVersion#runtime_api_version}
        :param runtime_channel: The channel of the runtime to use. Only available for some runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_channel AppEngineFlexibleAppVersion#runtime_channel}
        :param runtime_main_executable_path: The path or name of the app's main executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_main_executable_path AppEngineFlexibleAppVersion#runtime_main_executable_path}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#service_account AppEngineFlexibleAppVersion#service_account}
        :param serving_status: Current serving status of this version. Only the versions with a SERVING status create instances and can be billed. Default value: "SERVING" Possible values: ["SERVING", "STOPPED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#serving_status AppEngineFlexibleAppVersion#serving_status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeouts AppEngineFlexibleAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#version_id AppEngineFlexibleAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#vpc_access_connector AppEngineFlexibleAppVersion#vpc_access_connector}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(liveness_check, dict):
            liveness_check = AppEngineFlexibleAppVersionLivenessCheck(**liveness_check)
        if isinstance(readiness_check, dict):
            readiness_check = AppEngineFlexibleAppVersionReadinessCheck(**readiness_check)
        if isinstance(api_config, dict):
            api_config = AppEngineFlexibleAppVersionApiConfig(**api_config)
        if isinstance(automatic_scaling, dict):
            automatic_scaling = AppEngineFlexibleAppVersionAutomaticScaling(**automatic_scaling)
        if isinstance(deployment, dict):
            deployment = AppEngineFlexibleAppVersionDeployment(**deployment)
        if isinstance(endpoints_api_service, dict):
            endpoints_api_service = AppEngineFlexibleAppVersionEndpointsApiService(**endpoints_api_service)
        if isinstance(entrypoint, dict):
            entrypoint = AppEngineFlexibleAppVersionEntrypoint(**entrypoint)
        if isinstance(flexible_runtime_settings, dict):
            flexible_runtime_settings = AppEngineFlexibleAppVersionFlexibleRuntimeSettings(**flexible_runtime_settings)
        if isinstance(manual_scaling, dict):
            manual_scaling = AppEngineFlexibleAppVersionManualScaling(**manual_scaling)
        if isinstance(network, dict):
            network = AppEngineFlexibleAppVersionNetwork(**network)
        if isinstance(resources, dict):
            resources = AppEngineFlexibleAppVersionResources(**resources)
        if isinstance(timeouts, dict):
            timeouts = AppEngineFlexibleAppVersionTimeouts(**timeouts)
        if isinstance(vpc_access_connector, dict):
            vpc_access_connector = AppEngineFlexibleAppVersionVpcAccessConnector(**vpc_access_connector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1809754fe940e05679993049eac52967aabf82acf792de8ed99ba349f63f62)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument liveness_check", value=liveness_check, expected_type=type_hints["liveness_check"])
            check_type(argname="argument readiness_check", value=readiness_check, expected_type=type_hints["readiness_check"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument api_config", value=api_config, expected_type=type_hints["api_config"])
            check_type(argname="argument automatic_scaling", value=automatic_scaling, expected_type=type_hints["automatic_scaling"])
            check_type(argname="argument beta_settings", value=beta_settings, expected_type=type_hints["beta_settings"])
            check_type(argname="argument default_expiration", value=default_expiration, expected_type=type_hints["default_expiration"])
            check_type(argname="argument delete_service_on_destroy", value=delete_service_on_destroy, expected_type=type_hints["delete_service_on_destroy"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument endpoints_api_service", value=endpoints_api_service, expected_type=type_hints["endpoints_api_service"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument env_variables", value=env_variables, expected_type=type_hints["env_variables"])
            check_type(argname="argument flexible_runtime_settings", value=flexible_runtime_settings, expected_type=type_hints["flexible_runtime_settings"])
            check_type(argname="argument handlers", value=handlers, expected_type=type_hints["handlers"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inbound_services", value=inbound_services, expected_type=type_hints["inbound_services"])
            check_type(argname="argument instance_class", value=instance_class, expected_type=type_hints["instance_class"])
            check_type(argname="argument manual_scaling", value=manual_scaling, expected_type=type_hints["manual_scaling"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument nobuild_files_regex", value=nobuild_files_regex, expected_type=type_hints["nobuild_files_regex"])
            check_type(argname="argument noop_on_destroy", value=noop_on_destroy, expected_type=type_hints["noop_on_destroy"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument runtime_api_version", value=runtime_api_version, expected_type=type_hints["runtime_api_version"])
            check_type(argname="argument runtime_channel", value=runtime_channel, expected_type=type_hints["runtime_channel"])
            check_type(argname="argument runtime_main_executable_path", value=runtime_main_executable_path, expected_type=type_hints["runtime_main_executable_path"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument serving_status", value=serving_status, expected_type=type_hints["serving_status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument vpc_access_connector", value=vpc_access_connector, expected_type=type_hints["vpc_access_connector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "liveness_check": liveness_check,
            "readiness_check": readiness_check,
            "runtime": runtime,
            "service": service,
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
        if api_config is not None:
            self._values["api_config"] = api_config
        if automatic_scaling is not None:
            self._values["automatic_scaling"] = automatic_scaling
        if beta_settings is not None:
            self._values["beta_settings"] = beta_settings
        if default_expiration is not None:
            self._values["default_expiration"] = default_expiration
        if delete_service_on_destroy is not None:
            self._values["delete_service_on_destroy"] = delete_service_on_destroy
        if deployment is not None:
            self._values["deployment"] = deployment
        if endpoints_api_service is not None:
            self._values["endpoints_api_service"] = endpoints_api_service
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if env_variables is not None:
            self._values["env_variables"] = env_variables
        if flexible_runtime_settings is not None:
            self._values["flexible_runtime_settings"] = flexible_runtime_settings
        if handlers is not None:
            self._values["handlers"] = handlers
        if id is not None:
            self._values["id"] = id
        if inbound_services is not None:
            self._values["inbound_services"] = inbound_services
        if instance_class is not None:
            self._values["instance_class"] = instance_class
        if manual_scaling is not None:
            self._values["manual_scaling"] = manual_scaling
        if network is not None:
            self._values["network"] = network
        if nobuild_files_regex is not None:
            self._values["nobuild_files_regex"] = nobuild_files_regex
        if noop_on_destroy is not None:
            self._values["noop_on_destroy"] = noop_on_destroy
        if project is not None:
            self._values["project"] = project
        if resources is not None:
            self._values["resources"] = resources
        if runtime_api_version is not None:
            self._values["runtime_api_version"] = runtime_api_version
        if runtime_channel is not None:
            self._values["runtime_channel"] = runtime_channel
        if runtime_main_executable_path is not None:
            self._values["runtime_main_executable_path"] = runtime_main_executable_path
        if service_account is not None:
            self._values["service_account"] = service_account
        if serving_status is not None:
            self._values["serving_status"] = serving_status
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version_id is not None:
            self._values["version_id"] = version_id
        if vpc_access_connector is not None:
            self._values["vpc_access_connector"] = vpc_access_connector

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
    def liveness_check(self) -> "AppEngineFlexibleAppVersionLivenessCheck":
        '''liveness_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#liveness_check AppEngineFlexibleAppVersion#liveness_check}
        '''
        result = self._values.get("liveness_check")
        assert result is not None, "Required property 'liveness_check' is missing"
        return typing.cast("AppEngineFlexibleAppVersionLivenessCheck", result)

    @builtins.property
    def readiness_check(self) -> "AppEngineFlexibleAppVersionReadinessCheck":
        '''readiness_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#readiness_check AppEngineFlexibleAppVersion#readiness_check}
        '''
        result = self._values.get("readiness_check")
        assert result is not None, "Required property 'readiness_check' is missing"
        return typing.cast("AppEngineFlexibleAppVersionReadinessCheck", result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''Desired runtime. Example python27.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime AppEngineFlexibleAppVersion#runtime}
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''AppEngine service resource. Can contain numbers, letters, and hyphens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#service AppEngineFlexibleAppVersion#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_config(self) -> typing.Optional[AppEngineFlexibleAppVersionApiConfig]:
        '''api_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#api_config AppEngineFlexibleAppVersion#api_config}
        '''
        result = self._values.get("api_config")
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionApiConfig], result)

    @builtins.property
    def automatic_scaling(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionAutomaticScaling]:
        '''automatic_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#automatic_scaling AppEngineFlexibleAppVersion#automatic_scaling}
        '''
        result = self._values.get("automatic_scaling")
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionAutomaticScaling], result)

    @builtins.property
    def beta_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata settings that are supplied to this version to enable beta runtime features.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#beta_settings AppEngineFlexibleAppVersion#beta_settings}
        '''
        result = self._values.get("beta_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def default_expiration(self) -> typing.Optional[builtins.str]:
        '''Duration that static files should be cached by web proxies and browsers.

        Only applicable if the corresponding StaticFilesHandler does not specify its own expiration time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#default_expiration AppEngineFlexibleAppVersion#default_expiration}
        '''
        result = self._values.get("default_expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_service_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the service will be deleted if it is the last version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#delete_service_on_destroy AppEngineFlexibleAppVersion#delete_service_on_destroy}
        '''
        result = self._values.get("delete_service_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deployment(self) -> typing.Optional["AppEngineFlexibleAppVersionDeployment"]:
        '''deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#deployment AppEngineFlexibleAppVersion#deployment}
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionDeployment"], result)

    @builtins.property
    def endpoints_api_service(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionEndpointsApiService"]:
        '''endpoints_api_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#endpoints_api_service AppEngineFlexibleAppVersion#endpoints_api_service}
        '''
        result = self._values.get("endpoints_api_service")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionEndpointsApiService"], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional["AppEngineFlexibleAppVersionEntrypoint"]:
        '''entrypoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#entrypoint AppEngineFlexibleAppVersion#entrypoint}
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionEntrypoint"], result)

    @builtins.property
    def env_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables available to the application.

        As these are not returned in the API request, Terraform will not detect any changes made outside of the Terraform config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#env_variables AppEngineFlexibleAppVersion#env_variables}
        '''
        result = self._values.get("env_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def flexible_runtime_settings(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionFlexibleRuntimeSettings"]:
        '''flexible_runtime_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#flexible_runtime_settings AppEngineFlexibleAppVersion#flexible_runtime_settings}
        '''
        result = self._values.get("flexible_runtime_settings")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionFlexibleRuntimeSettings"], result)

    @builtins.property
    def handlers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionHandlers"]]]:
        '''handlers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#handlers AppEngineFlexibleAppVersion#handlers}
        '''
        result = self._values.get("handlers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionHandlers"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#id AppEngineFlexibleAppVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inbound_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the types of messages that this application is able to receive.

        Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#inbound_services AppEngineFlexibleAppVersion#inbound_services}
        '''
        result = self._values.get("inbound_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_class(self) -> typing.Optional[builtins.str]:
        '''Instance class that is used to run this version.

        Valid values are
        AutomaticScaling: F1, F2, F4, F4_1G
        ManualScaling: B1, B2, B4, B8, B4_1G
        Defaults to F1 for AutomaticScaling and B1 for ManualScaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instance_class AppEngineFlexibleAppVersion#instance_class}
        '''
        result = self._values.get("instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_scaling(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionManualScaling"]:
        '''manual_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#manual_scaling AppEngineFlexibleAppVersion#manual_scaling}
        '''
        result = self._values.get("manual_scaling")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionManualScaling"], result)

    @builtins.property
    def network(self) -> typing.Optional["AppEngineFlexibleAppVersionNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#network AppEngineFlexibleAppVersion#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionNetwork"], result)

    @builtins.property
    def nobuild_files_regex(self) -> typing.Optional[builtins.str]:
        '''Files that match this pattern will not be built into this version. Only applicable for Go runtimes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#nobuild_files_regex AppEngineFlexibleAppVersion#nobuild_files_regex}
        '''
        result = self._values.get("nobuild_files_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noop_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the application version will not be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#noop_on_destroy AppEngineFlexibleAppVersion#noop_on_destroy}
        '''
        result = self._values.get("noop_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#project AppEngineFlexibleAppVersion#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Optional["AppEngineFlexibleAppVersionResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#resources AppEngineFlexibleAppVersion#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionResources"], result)

    @builtins.property
    def runtime_api_version(self) -> typing.Optional[builtins.str]:
        '''The version of the API in the given runtime environment.

        Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref'
        Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_api_version AppEngineFlexibleAppVersion#runtime_api_version}
        '''
        result = self._values.get("runtime_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_channel(self) -> typing.Optional[builtins.str]:
        '''The channel of the runtime to use. Only available for some runtimes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_channel AppEngineFlexibleAppVersion#runtime_channel}
        '''
        result = self._values.get("runtime_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_main_executable_path(self) -> typing.Optional[builtins.str]:
        '''The path or name of the app's main executable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_main_executable_path AppEngineFlexibleAppVersion#runtime_main_executable_path}
        '''
        result = self._values.get("runtime_main_executable_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The identity that the deployed version will run as.

        Admin API will use the App Engine Appspot service account as
        default if this field is neither provided in app.yaml file nor through CLI flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#service_account AppEngineFlexibleAppVersion#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serving_status(self) -> typing.Optional[builtins.str]:
        '''Current serving status of this version.

        Only the versions with a SERVING status create instances and can be billed. Default value: "SERVING" Possible values: ["SERVING", "STOPPED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#serving_status AppEngineFlexibleAppVersion#serving_status}
        '''
        result = self._values.get("serving_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppEngineFlexibleAppVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeouts AppEngineFlexibleAppVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionTimeouts"], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Relative name of the version within the service.

        For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens.
        Reserved names,"default", "latest", and any name with the prefix "ah-".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#version_id AppEngineFlexibleAppVersion#version_id}
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_access_connector(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionVpcAccessConnector"]:
        '''vpc_access_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#vpc_access_connector AppEngineFlexibleAppVersion#vpc_access_connector}
        '''
        result = self._values.get("vpc_access_connector")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionVpcAccessConnector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_build_options": "cloudBuildOptions",
        "container": "container",
        "files": "files",
        "zip": "zip",
    },
)
class AppEngineFlexibleAppVersionDeployment:
    def __init__(
        self,
        *,
        cloud_build_options: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeploymentCloudBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        container: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeploymentContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["AppEngineFlexibleAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_build_options: cloud_build_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cloud_build_options AppEngineFlexibleAppVersion#cloud_build_options}
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#container AppEngineFlexibleAppVersion#container}
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#files AppEngineFlexibleAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#zip AppEngineFlexibleAppVersion#zip}
        '''
        if isinstance(cloud_build_options, dict):
            cloud_build_options = AppEngineFlexibleAppVersionDeploymentCloudBuildOptions(**cloud_build_options)
        if isinstance(container, dict):
            container = AppEngineFlexibleAppVersionDeploymentContainer(**container)
        if isinstance(zip, dict):
            zip = AppEngineFlexibleAppVersionDeploymentZip(**zip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96cad41cf94b5d26b54ae8fe13b282b954e366f54eaac906df13d75e5b96b808)
            check_type(argname="argument cloud_build_options", value=cloud_build_options, expected_type=type_hints["cloud_build_options"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument zip", value=zip, expected_type=type_hints["zip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_build_options is not None:
            self._values["cloud_build_options"] = cloud_build_options
        if container is not None:
            self._values["container"] = container
        if files is not None:
            self._values["files"] = files
        if zip is not None:
            self._values["zip"] = zip

    @builtins.property
    def cloud_build_options(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionDeploymentCloudBuildOptions"]:
        '''cloud_build_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cloud_build_options AppEngineFlexibleAppVersion#cloud_build_options}
        '''
        result = self._values.get("cloud_build_options")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionDeploymentCloudBuildOptions"], result)

    @builtins.property
    def container(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionDeploymentContainer"]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#container AppEngineFlexibleAppVersion#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionDeploymentContainer"], result)

    @builtins.property
    def files(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionDeploymentFiles"]]]:
        '''files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#files AppEngineFlexibleAppVersion#files}
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionDeploymentFiles"]]], result)

    @builtins.property
    def zip(self) -> typing.Optional["AppEngineFlexibleAppVersionDeploymentZip"]:
        '''zip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#zip AppEngineFlexibleAppVersion#zip}
        '''
        result = self._values.get("zip")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionDeploymentZip"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentCloudBuildOptions",
    jsii_struct_bases=[],
    name_mapping={
        "app_yaml_path": "appYamlPath",
        "cloud_build_timeout": "cloudBuildTimeout",
    },
)
class AppEngineFlexibleAppVersionDeploymentCloudBuildOptions:
    def __init__(
        self,
        *,
        app_yaml_path: builtins.str,
        cloud_build_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_yaml_path: Path to the yaml file used in deployment, used to determine runtime configuration details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#app_yaml_path AppEngineFlexibleAppVersion#app_yaml_path}
        :param cloud_build_timeout: The Cloud Build timeout used as part of any dependent builds performed by version creation. Defaults to 10 minutes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cloud_build_timeout AppEngineFlexibleAppVersion#cloud_build_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b42c7bde6c616abe71723c3497729f29da76ecfdb9bf6a79d45f8732bd42169)
            check_type(argname="argument app_yaml_path", value=app_yaml_path, expected_type=type_hints["app_yaml_path"])
            check_type(argname="argument cloud_build_timeout", value=cloud_build_timeout, expected_type=type_hints["cloud_build_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_yaml_path": app_yaml_path,
        }
        if cloud_build_timeout is not None:
            self._values["cloud_build_timeout"] = cloud_build_timeout

    @builtins.property
    def app_yaml_path(self) -> builtins.str:
        '''Path to the yaml file used in deployment, used to determine runtime configuration details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#app_yaml_path AppEngineFlexibleAppVersion#app_yaml_path}
        '''
        result = self._values.get("app_yaml_path")
        assert result is not None, "Required property 'app_yaml_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_build_timeout(self) -> typing.Optional[builtins.str]:
        '''The Cloud Build timeout used as part of any dependent builds performed by version creation. Defaults to 10 minutes.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cloud_build_timeout AppEngineFlexibleAppVersion#cloud_build_timeout}
        '''
        result = self._values.get("cloud_build_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionDeploymentCloudBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6abe9c0d4c49fe1f8a82aafc4694ca8fbed2715a89c88c35ae938dcbb251d153)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudBuildTimeout")
    def reset_cloud_build_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudBuildTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="appYamlPathInput")
    def app_yaml_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appYamlPathInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudBuildTimeoutInput")
    def cloud_build_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBuildTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="appYamlPath")
    def app_yaml_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appYamlPath"))

    @app_yaml_path.setter
    def app_yaml_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03c854b922da5455ae099bef5ae2fedd7affb389cfae90c707e966a74572f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appYamlPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudBuildTimeout")
    def cloud_build_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudBuildTimeout"))

    @cloud_build_timeout.setter
    def cloud_build_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8789a78b70ec85d21a55b4cca55784233d7768780a4129e65065e226cd3a46b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudBuildTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionDeploymentCloudBuildOptions]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionDeploymentCloudBuildOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionDeploymentCloudBuildOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89475283d117da42ecc765877fb0370f6b23599cecfcaaad035d75d6c6ecc79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentContainer",
    jsii_struct_bases=[],
    name_mapping={"image": "image"},
)
class AppEngineFlexibleAppVersionDeploymentContainer:
    def __init__(self, *, image: builtins.str) -> None:
        '''
        :param image: URI to the hosted container image in Google Container Registry. The URI must be fully qualified and include a tag or digest. Examples: "gcr.io/my-project/image:tag" or "gcr.io/my-project/image@digest" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#image AppEngineFlexibleAppVersion#image}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30057c8255603628183d50bb74b326b5293e7f5b0c80e68ca56935c4dd679b07)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }

    @builtins.property
    def image(self) -> builtins.str:
        '''URI to the hosted container image in Google Container Registry.

        The URI must be fully qualified and include a tag or digest.
        Examples: "gcr.io/my-project/image:tag" or "gcr.io/my-project/image@digest"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#image AppEngineFlexibleAppVersion#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionDeploymentContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionDeploymentContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__909f25812f8f3fac2b447295cf15ed18639ea1d48d152184c60f00750a5035f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddec4b6f732e219612f60d22f1d26bea656473be610735f4b98d00e6d612397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionDeploymentContainer]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionDeploymentContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionDeploymentContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03f3f25cb95b24bbf512c60005bcd7019221e0d57ac749ccfc432f09c46b4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentFiles",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "source_url": "sourceUrl", "sha1_sum": "sha1Sum"},
)
class AppEngineFlexibleAppVersionDeploymentFiles:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_url: builtins.str,
        sha1_sum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}.
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#source_url AppEngineFlexibleAppVersion#source_url}
        :param sha1_sum: SHA1 checksum of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#sha1_sum AppEngineFlexibleAppVersion#sha1_sum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25bbabff0c673ad9df9c0ce1d8a269e91df7434b2a68cfae48be5e705715cb04)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_url", value=source_url, expected_type=type_hints["source_url"])
            check_type(argname="argument sha1_sum", value=sha1_sum, expected_type=type_hints["sha1_sum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "source_url": source_url,
        }
        if sha1_sum is not None:
            self._values["sha1_sum"] = sha1_sum

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_url(self) -> builtins.str:
        '''Source URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#source_url AppEngineFlexibleAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha1_sum(self) -> typing.Optional[builtins.str]:
        '''SHA1 checksum of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#sha1_sum AppEngineFlexibleAppVersion#sha1_sum}
        '''
        result = self._values.get("sha1_sum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionDeploymentFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionDeploymentFilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentFilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4eb394a01425e4ec86d6d315e0d582654049b4e96e7b982b6bd9e3f01ce5e2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppEngineFlexibleAppVersionDeploymentFilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d1d45afbc87a8fd78913085a14e1e060039b4e611488fd206b7a9f2b4f71b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppEngineFlexibleAppVersionDeploymentFilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820b07a267fffa2eb9cd2ac2fcb59ed7fb08bc8b39c60b08ae0f37de620bcd68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__160dac37cfb76fdeb56b07f58ef474871620d50cc4fcb9021122bed56b51c75b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4270b10950b8593138bc7b9d7b75a4b8173b5f6e73a925c225a194adc84ea24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionDeploymentFiles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionDeploymentFiles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48acd37cf2b94cb4bd4b9580ba0446a8bfef82db696aab3aba522ae7888aefa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineFlexibleAppVersionDeploymentFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec22779e36378fa9e4d21ee1cfe6588cebec8aa945d61369f88f5652cbf99278)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSha1Sum")
    def reset_sha1_sum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha1Sum", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sha1SumInput")
    def sha1_sum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha1SumInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrlInput")
    def source_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e3e928dfed5c278caa769a891243216c228dda044f7d7e858121c9e26b93b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sha1Sum")
    def sha1_sum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1Sum"))

    @sha1_sum.setter
    def sha1_sum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26bbc1cd12e268282755369cc0e75160acd9fe29be5fda6ef73b80dd4ccc1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha1Sum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f186a7335a3c8c9c26b254f2c81f5277e32d90e9099f2ab4c3fa6356786cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionDeploymentFiles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionDeploymentFiles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionDeploymentFiles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b0b73d4be4b745c026265829f518ef9252e6bc66f0eb5a85f39db740e4d36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineFlexibleAppVersionDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4f8f09bb50b50b03a63d10ce8f7e4df82e08b9bb8f5e84fbe599d20dd78c801)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudBuildOptions")
    def put_cloud_build_options(
        self,
        *,
        app_yaml_path: builtins.str,
        cloud_build_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_yaml_path: Path to the yaml file used in deployment, used to determine runtime configuration details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#app_yaml_path AppEngineFlexibleAppVersion#app_yaml_path}
        :param cloud_build_timeout: The Cloud Build timeout used as part of any dependent builds performed by version creation. Defaults to 10 minutes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cloud_build_timeout AppEngineFlexibleAppVersion#cloud_build_timeout}
        '''
        value = AppEngineFlexibleAppVersionDeploymentCloudBuildOptions(
            app_yaml_path=app_yaml_path, cloud_build_timeout=cloud_build_timeout
        )

        return typing.cast(None, jsii.invoke(self, "putCloudBuildOptions", [value]))

    @jsii.member(jsii_name="putContainer")
    def put_container(self, *, image: builtins.str) -> None:
        '''
        :param image: URI to the hosted container image in Google Container Registry. The URI must be fully qualified and include a tag or digest. Examples: "gcr.io/my-project/image:tag" or "gcr.io/my-project/image@digest" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#image AppEngineFlexibleAppVersion#image}
        '''
        value = AppEngineFlexibleAppVersionDeploymentContainer(image=image)

        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putFiles")
    def put_files(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123699a947c23f57f36fe20628ac7b91f50339aead23fddc86e790283ee44486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFiles", [value]))

    @jsii.member(jsii_name="putZip")
    def put_zip(
        self,
        *,
        source_url: builtins.str,
        files_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#source_url AppEngineFlexibleAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#files_count AppEngineFlexibleAppVersion#files_count}
        '''
        value = AppEngineFlexibleAppVersionDeploymentZip(
            source_url=source_url, files_count=files_count
        )

        return typing.cast(None, jsii.invoke(self, "putZip", [value]))

    @jsii.member(jsii_name="resetCloudBuildOptions")
    def reset_cloud_build_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudBuildOptions", []))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetFiles")
    def reset_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFiles", []))

    @jsii.member(jsii_name="resetZip")
    def reset_zip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZip", []))

    @builtins.property
    @jsii.member(jsii_name="cloudBuildOptions")
    def cloud_build_options(
        self,
    ) -> AppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference:
        return typing.cast(AppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference, jsii.get(self, "cloudBuildOptions"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(
        self,
    ) -> AppEngineFlexibleAppVersionDeploymentContainerOutputReference:
        return typing.cast(AppEngineFlexibleAppVersionDeploymentContainerOutputReference, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> AppEngineFlexibleAppVersionDeploymentFilesList:
        return typing.cast(AppEngineFlexibleAppVersionDeploymentFilesList, jsii.get(self, "files"))

    @builtins.property
    @jsii.member(jsii_name="zip")
    def zip(self) -> "AppEngineFlexibleAppVersionDeploymentZipOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionDeploymentZipOutputReference", jsii.get(self, "zip"))

    @builtins.property
    @jsii.member(jsii_name="cloudBuildOptionsInput")
    def cloud_build_options_input(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionDeploymentCloudBuildOptions]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionDeploymentCloudBuildOptions], jsii.get(self, "cloudBuildOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionDeploymentContainer]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionDeploymentContainer], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="filesInput")
    def files_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionDeploymentFiles]]], jsii.get(self, "filesInput"))

    @builtins.property
    @jsii.member(jsii_name="zipInput")
    def zip_input(self) -> typing.Optional["AppEngineFlexibleAppVersionDeploymentZip"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionDeploymentZip"], jsii.get(self, "zipInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineFlexibleAppVersionDeployment]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd8d2fa61c6e08d17f4c2ba392495b36b8a205b29603a6cb61b29a6152ee490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentZip",
    jsii_struct_bases=[],
    name_mapping={"source_url": "sourceUrl", "files_count": "filesCount"},
)
class AppEngineFlexibleAppVersionDeploymentZip:
    def __init__(
        self,
        *,
        source_url: builtins.str,
        files_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#source_url AppEngineFlexibleAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#files_count AppEngineFlexibleAppVersion#files_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68439297c89d8937975a842ee1740bc734d54acd43b45bd21e0c975d069f6b1)
            check_type(argname="argument source_url", value=source_url, expected_type=type_hints["source_url"])
            check_type(argname="argument files_count", value=files_count, expected_type=type_hints["files_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_url": source_url,
        }
        if files_count is not None:
            self._values["files_count"] = files_count

    @builtins.property
    def source_url(self) -> builtins.str:
        '''Source URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#source_url AppEngineFlexibleAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def files_count(self) -> typing.Optional[jsii.Number]:
        '''files count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#files_count AppEngineFlexibleAppVersion#files_count}
        '''
        result = self._values.get("files_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionDeploymentZip(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionDeploymentZipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionDeploymentZipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf8b7a9fa0647bacecb3daeeb562f10d9b97139ab327b232307f1ec962c8419)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilesCount")
    def reset_files_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilesCount", []))

    @builtins.property
    @jsii.member(jsii_name="filesCountInput")
    def files_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "filesCountInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrlInput")
    def source_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="filesCount")
    def files_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "filesCount"))

    @files_count.setter
    def files_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defc07fe841db3786658ed06aaf0a273025dba10173c366beedf987d6613794e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1dc159009d2df176f9707da9c8cbea4ceea9bc209611b81639f1a1d91411a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionDeploymentZip]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionDeploymentZip], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionDeploymentZip],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db97f59adb636320a8c84f58fb2b64792117ff848a01518db199fff5499584c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionEndpointsApiService",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "config_id": "configId",
        "disable_trace_sampling": "disableTraceSampling",
        "rollout_strategy": "rolloutStrategy",
    },
)
class AppEngineFlexibleAppVersionEndpointsApiService:
    def __init__(
        self,
        *,
        name: builtins.str,
        config_id: typing.Optional[builtins.str] = None,
        disable_trace_sampling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rollout_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Endpoints service name which is the name of the "service" resource in the Service Management API. For example "myapi.endpoints.myproject.cloud.goog". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        :param config_id: Endpoints service configuration ID as specified by the Service Management API. For example "2016-09-19r1". By default, the rollout strategy for Endpoints is "FIXED". This means that Endpoints starts up with a particular configuration ID. When a new configuration is rolled out, Endpoints must be given the new configuration ID. The configId field is used to give the configuration ID and is required in this case. Endpoints also has a rollout strategy called "MANAGED". When using this, Endpoints fetches the latest configuration and does not need the configuration ID. In this case, configId must be omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#config_id AppEngineFlexibleAppVersion#config_id}
        :param disable_trace_sampling: Enable or disable trace sampling. By default, this is set to false for enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disable_trace_sampling AppEngineFlexibleAppVersion#disable_trace_sampling}
        :param rollout_strategy: Endpoints rollout strategy. If FIXED, configId must be specified. If MANAGED, configId must be omitted. Default value: "FIXED" Possible values: ["FIXED", "MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#rollout_strategy AppEngineFlexibleAppVersion#rollout_strategy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a8679c2e2e1ee030ea41fead9b577f32fa98edc11ec1a43133b08f0706140b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument config_id", value=config_id, expected_type=type_hints["config_id"])
            check_type(argname="argument disable_trace_sampling", value=disable_trace_sampling, expected_type=type_hints["disable_trace_sampling"])
            check_type(argname="argument rollout_strategy", value=rollout_strategy, expected_type=type_hints["rollout_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if config_id is not None:
            self._values["config_id"] = config_id
        if disable_trace_sampling is not None:
            self._values["disable_trace_sampling"] = disable_trace_sampling
        if rollout_strategy is not None:
            self._values["rollout_strategy"] = rollout_strategy

    @builtins.property
    def name(self) -> builtins.str:
        '''Endpoints service name which is the name of the "service" resource in the Service Management API. For example "myapi.endpoints.myproject.cloud.goog".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_id(self) -> typing.Optional[builtins.str]:
        '''Endpoints service configuration ID as specified by the Service Management API. For example "2016-09-19r1".

        By default, the rollout strategy for Endpoints is "FIXED". This means that Endpoints starts up with a particular configuration ID.
        When a new configuration is rolled out, Endpoints must be given the new configuration ID. The configId field is used to give the configuration ID
        and is required in this case.

        Endpoints also has a rollout strategy called "MANAGED". When using this, Endpoints fetches the latest configuration and does not need
        the configuration ID. In this case, configId must be omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#config_id AppEngineFlexibleAppVersion#config_id}
        '''
        result = self._values.get("config_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_trace_sampling(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable trace sampling. By default, this is set to false for enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disable_trace_sampling AppEngineFlexibleAppVersion#disable_trace_sampling}
        '''
        result = self._values.get("disable_trace_sampling")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rollout_strategy(self) -> typing.Optional[builtins.str]:
        '''Endpoints rollout strategy.

        If FIXED, configId must be specified. If MANAGED, configId must be omitted. Default value: "FIXED" Possible values: ["FIXED", "MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#rollout_strategy AppEngineFlexibleAppVersion#rollout_strategy}
        '''
        result = self._values.get("rollout_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionEndpointsApiService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionEndpointsApiServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionEndpointsApiServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e20194d6c15fcf539e7791a4afbdef17ad844ff1a1f13c728fa2e0db145a9ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfigId")
    def reset_config_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigId", []))

    @jsii.member(jsii_name="resetDisableTraceSampling")
    def reset_disable_trace_sampling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableTraceSampling", []))

    @jsii.member(jsii_name="resetRolloutStrategy")
    def reset_rollout_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="configIdInput")
    def config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configIdInput"))

    @builtins.property
    @jsii.member(jsii_name="disableTraceSamplingInput")
    def disable_trace_sampling_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTraceSamplingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutStrategyInput")
    def rollout_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rolloutStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea528667176f31bd6359f2d4c7b57a5e136d4a1fbc8263b673cbbe68caa66d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableTraceSampling")
    def disable_trace_sampling(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableTraceSampling"))

    @disable_trace_sampling.setter
    def disable_trace_sampling(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980fdf2985c9e3c24898ba53a2aebd3e75da82b59e4ada2370a34defa31021a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTraceSampling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46beee5c56a5b96ce196811ee3ce67687f3cb66c60b394b41185a76011b44cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rolloutStrategy")
    def rollout_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutStrategy"))

    @rollout_strategy.setter
    def rollout_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3ffca21766a4e199a1815b718f1af114153c9dd0714ed8454c025effbf26b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionEndpointsApiService]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionEndpointsApiService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionEndpointsApiService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5aff6716c7d5e501a3936a26e321a54b4f1b59f662a27d3b8552db474afb9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionEntrypoint",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell"},
)
class AppEngineFlexibleAppVersionEntrypoint:
    def __init__(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#shell AppEngineFlexibleAppVersion#shell}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550d177dfe0de0347a2fc3199881f27c9c28877e1282ec571b3854631e656a46)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "shell": shell,
        }

    @builtins.property
    def shell(self) -> builtins.str:
        '''The format should be a shell command that can be fed to bash -c.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#shell AppEngineFlexibleAppVersion#shell}
        '''
        result = self._values.get("shell")
        assert result is not None, "Required property 'shell' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionEntrypoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionEntrypointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionEntrypointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07611c600260835e3c544f4e875b358f52cf85d6d38582cbfe496ca7ddbbf567)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="shellInput")
    def shell_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shellInput"))

    @builtins.property
    @jsii.member(jsii_name="shell")
    def shell(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shell"))

    @shell.setter
    def shell(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5206b86cfec1e5b110f6ef7b24bb13f98bd1c9f1dc9ebc017c7955c2989fc3cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineFlexibleAppVersionEntrypoint]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionEntrypoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionEntrypoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9ae8f10d269acec70c5779ae7d754208b0e83bb2a600dba92ec61ed70ceef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionFlexibleRuntimeSettings",
    jsii_struct_bases=[],
    name_mapping={
        "operating_system": "operatingSystem",
        "runtime_version": "runtimeVersion",
    },
)
class AppEngineFlexibleAppVersionFlexibleRuntimeSettings:
    def __init__(
        self,
        *,
        operating_system: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operating_system: Operating System of the application runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#operating_system AppEngineFlexibleAppVersion#operating_system}
        :param runtime_version: The runtime version of an App Engine flexible application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_version AppEngineFlexibleAppVersion#runtime_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0fb01e6e138973058a58f649614b8f57d7abb3c9cbedcefed8379cbc6c4fd3b)
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Operating System of the application runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#operating_system AppEngineFlexibleAppVersion#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''The runtime version of an App Engine flexible application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#runtime_version AppEngineFlexibleAppVersion#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionFlexibleRuntimeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80607c306349b5c9286a1fcfe4c217b1713c69ba2bbb8137dfa890a09be42f96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOperatingSystem")
    def reset_operating_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperatingSystem", []))

    @jsii.member(jsii_name="resetRuntimeVersion")
    def reset_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeVersion", []))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670fc1558fc14a657870e58425c2f819f2862ec298cc398640f4aab00cac201e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c560aad2bbfb4c73f7302d042e0314d7f25e1cc30be5a840d6d71e4c1f6fe68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionFlexibleRuntimeSettings]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionFlexibleRuntimeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionFlexibleRuntimeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1829302a1e46c6afae1979e4d4921252a4b2c524b777bb44c05078da1efbb15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionHandlers",
    jsii_struct_bases=[],
    name_mapping={
        "auth_fail_action": "authFailAction",
        "login": "login",
        "redirect_http_response_code": "redirectHttpResponseCode",
        "script": "script",
        "security_level": "securityLevel",
        "static_files": "staticFiles",
        "url_regex": "urlRegex",
    },
)
class AppEngineFlexibleAppVersionHandlers:
    def __init__(
        self,
        *,
        auth_fail_action: typing.Optional[builtins.str] = None,
        login: typing.Optional[builtins.str] = None,
        redirect_http_response_code: typing.Optional[builtins.str] = None,
        script: typing.Optional[typing.Union["AppEngineFlexibleAppVersionHandlersScript", typing.Dict[builtins.str, typing.Any]]] = None,
        security_level: typing.Optional[builtins.str] = None,
        static_files: typing.Optional[typing.Union["AppEngineFlexibleAppVersionHandlersStaticFiles", typing.Dict[builtins.str, typing.Any]]] = None,
        url_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_fail_action: Actions to take when the user is not logged in. Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#auth_fail_action AppEngineFlexibleAppVersion#auth_fail_action}
        :param login: Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#login AppEngineFlexibleAppVersion#login}
        :param redirect_http_response_code: 30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#redirect_http_response_code AppEngineFlexibleAppVersion#redirect_http_response_code}
        :param script: script block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script AppEngineFlexibleAppVersion#script}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#security_level AppEngineFlexibleAppVersion#security_level}
        :param static_files: static_files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#static_files AppEngineFlexibleAppVersion#static_files}
        :param url_regex: URL prefix. Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings. All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#url_regex AppEngineFlexibleAppVersion#url_regex}
        '''
        if isinstance(script, dict):
            script = AppEngineFlexibleAppVersionHandlersScript(**script)
        if isinstance(static_files, dict):
            static_files = AppEngineFlexibleAppVersionHandlersStaticFiles(**static_files)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb143b4d7faf50f3f36ab7ed0611d16cd654fecb5b79e8d67b3f59046a9d9799)
            check_type(argname="argument auth_fail_action", value=auth_fail_action, expected_type=type_hints["auth_fail_action"])
            check_type(argname="argument login", value=login, expected_type=type_hints["login"])
            check_type(argname="argument redirect_http_response_code", value=redirect_http_response_code, expected_type=type_hints["redirect_http_response_code"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument security_level", value=security_level, expected_type=type_hints["security_level"])
            check_type(argname="argument static_files", value=static_files, expected_type=type_hints["static_files"])
            check_type(argname="argument url_regex", value=url_regex, expected_type=type_hints["url_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_fail_action is not None:
            self._values["auth_fail_action"] = auth_fail_action
        if login is not None:
            self._values["login"] = login
        if redirect_http_response_code is not None:
            self._values["redirect_http_response_code"] = redirect_http_response_code
        if script is not None:
            self._values["script"] = script
        if security_level is not None:
            self._values["security_level"] = security_level
        if static_files is not None:
            self._values["static_files"] = static_files
        if url_regex is not None:
            self._values["url_regex"] = url_regex

    @builtins.property
    def auth_fail_action(self) -> typing.Optional[builtins.str]:
        '''Actions to take when the user is not logged in. Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#auth_fail_action AppEngineFlexibleAppVersion#auth_fail_action}
        '''
        result = self._values.get("auth_fail_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login(self) -> typing.Optional[builtins.str]:
        '''Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#login AppEngineFlexibleAppVersion#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_http_response_code(self) -> typing.Optional[builtins.str]:
        '''30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#redirect_http_response_code AppEngineFlexibleAppVersion#redirect_http_response_code}
        '''
        result = self._values.get("redirect_http_response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional["AppEngineFlexibleAppVersionHandlersScript"]:
        '''script block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script AppEngineFlexibleAppVersion#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionHandlersScript"], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#security_level AppEngineFlexibleAppVersion#security_level}
        '''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_files(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionHandlersStaticFiles"]:
        '''static_files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#static_files AppEngineFlexibleAppVersion#static_files}
        '''
        result = self._values.get("static_files")
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionHandlersStaticFiles"], result)

    @builtins.property
    def url_regex(self) -> typing.Optional[builtins.str]:
        '''URL prefix.

        Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings.
        All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#url_regex AppEngineFlexibleAppVersion#url_regex}
        '''
        result = self._values.get("url_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionHandlers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionHandlersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionHandlersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__339c69850331de4db97b63a27a751f5b74ee21eb53995eb09c2e24fa16bdc403)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppEngineFlexibleAppVersionHandlersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8da93fb8fd9252491575281851afecad93b71bf013f33aefce4d3a49ac32f36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppEngineFlexibleAppVersionHandlersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cc04cd039ec0c6a4d5b64bff8b87cccf6e8da7f51f09cf7426d574e941ef2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae392cdb14576baebf4dcc500e4efad3be9ecd4bbf67a613e0947ada256d0a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__067f009e4827dbca39826f1d72a33769d2b11621cc896e4abcd9cd5909702e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionHandlers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionHandlers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionHandlers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42a4777631b065a9f582ff4dab9c8551e0dc35d2430437fa13801e8ac09f812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineFlexibleAppVersionHandlersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionHandlersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a20e76bd21781abf657c6f62c8fb20ba8d944053d92a5f41788bb882aa2e2f8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putScript")
    def put_script(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script_path AppEngineFlexibleAppVersion#script_path}
        '''
        value = AppEngineFlexibleAppVersionHandlersScript(script_path=script_path)

        return typing.cast(None, jsii.invoke(self, "putScript", [value]))

    @jsii.member(jsii_name="putStaticFiles")
    def put_static_files(
        self,
        *,
        application_readable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mime_type: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        require_matching_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upload_path_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#application_readable AppEngineFlexibleAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Default is '0s' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#expiration AppEngineFlexibleAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#http_headers AppEngineFlexibleAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#mime_type AppEngineFlexibleAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#require_matching_file AppEngineFlexibleAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#upload_path_regex AppEngineFlexibleAppVersion#upload_path_regex}
        '''
        value = AppEngineFlexibleAppVersionHandlersStaticFiles(
            application_readable=application_readable,
            expiration=expiration,
            http_headers=http_headers,
            mime_type=mime_type,
            path=path,
            require_matching_file=require_matching_file,
            upload_path_regex=upload_path_regex,
        )

        return typing.cast(None, jsii.invoke(self, "putStaticFiles", [value]))

    @jsii.member(jsii_name="resetAuthFailAction")
    def reset_auth_fail_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthFailAction", []))

    @jsii.member(jsii_name="resetLogin")
    def reset_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogin", []))

    @jsii.member(jsii_name="resetRedirectHttpResponseCode")
    def reset_redirect_http_response_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectHttpResponseCode", []))

    @jsii.member(jsii_name="resetScript")
    def reset_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScript", []))

    @jsii.member(jsii_name="resetSecurityLevel")
    def reset_security_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityLevel", []))

    @jsii.member(jsii_name="resetStaticFiles")
    def reset_static_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticFiles", []))

    @jsii.member(jsii_name="resetUrlRegex")
    def reset_url_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRegex", []))

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> "AppEngineFlexibleAppVersionHandlersScriptOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionHandlersScriptOutputReference", jsii.get(self, "script"))

    @builtins.property
    @jsii.member(jsii_name="staticFiles")
    def static_files(
        self,
    ) -> "AppEngineFlexibleAppVersionHandlersStaticFilesOutputReference":
        return typing.cast("AppEngineFlexibleAppVersionHandlersStaticFilesOutputReference", jsii.get(self, "staticFiles"))

    @builtins.property
    @jsii.member(jsii_name="authFailActionInput")
    def auth_fail_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authFailActionInput"))

    @builtins.property
    @jsii.member(jsii_name="loginInput")
    def login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectHttpResponseCodeInput")
    def redirect_http_response_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectHttpResponseCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionHandlersScript"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionHandlersScript"], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="securityLevelInput")
    def security_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="staticFilesInput")
    def static_files_input(
        self,
    ) -> typing.Optional["AppEngineFlexibleAppVersionHandlersStaticFiles"]:
        return typing.cast(typing.Optional["AppEngineFlexibleAppVersionHandlersStaticFiles"], jsii.get(self, "staticFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRegexInput")
    def url_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="authFailAction")
    def auth_fail_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authFailAction"))

    @auth_fail_action.setter
    def auth_fail_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758a95bc64e2af96d7bbcc3231a8f999746a495243f88528d103df463a29e42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authFailAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "login"))

    @login.setter
    def login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9070b37b672cfa4244482645b693a59aa02447868ff17252acbd4313aa72e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "login", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectHttpResponseCode")
    def redirect_http_response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectHttpResponseCode"))

    @redirect_http_response_code.setter
    def redirect_http_response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699d3a4a93c78b56bf086080c8ecba2020c42a2180bad00bc367255de97024d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectHttpResponseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @security_level.setter
    def security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6ff79e5712cee24b5609bc017f245237d9e08dcf7f5107f87bd6bb14243d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlRegex")
    def url_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlRegex"))

    @url_regex.setter
    def url_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3b5462597c847d2a4213d60ea802f136a5703aac13058f7e6a22350c57dbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionHandlers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionHandlers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionHandlers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f972d4b316bb75b053f1c1016ddce499d8d735125dd8b8a921731223fcdec334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionHandlersScript",
    jsii_struct_bases=[],
    name_mapping={"script_path": "scriptPath"},
)
class AppEngineFlexibleAppVersionHandlersScript:
    def __init__(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script_path AppEngineFlexibleAppVersion#script_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4ef84ced88babff899f76fe51e026a273c47f4a5e90e8366c617ce8046d2a0)
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script_path": script_path,
        }

    @builtins.property
    def script_path(self) -> builtins.str:
        '''Path to the script from the application root directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#script_path AppEngineFlexibleAppVersion#script_path}
        '''
        result = self._values.get("script_path")
        assert result is not None, "Required property 'script_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionHandlersScript(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionHandlersScriptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionHandlersScriptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dedaa0f72224c55e1e737c1d9611a6b0ac4e3f57848f6488b88ccf539a69e4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scriptPathInput")
    def script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptPath")
    def script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptPath"))

    @script_path.setter
    def script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcebaa894b1beacb7fdddece32d1d25eb343b95bbab95b4dacdcbfa19111ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionHandlersScript]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionHandlersScript], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionHandlersScript],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce809aa1fc276d05f3379fd773685ad11088d009297904642aa091c160c6dd3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionHandlersStaticFiles",
    jsii_struct_bases=[],
    name_mapping={
        "application_readable": "applicationReadable",
        "expiration": "expiration",
        "http_headers": "httpHeaders",
        "mime_type": "mimeType",
        "path": "path",
        "require_matching_file": "requireMatchingFile",
        "upload_path_regex": "uploadPathRegex",
    },
)
class AppEngineFlexibleAppVersionHandlersStaticFiles:
    def __init__(
        self,
        *,
        application_readable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mime_type: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        require_matching_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upload_path_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#application_readable AppEngineFlexibleAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Default is '0s' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#expiration AppEngineFlexibleAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#http_headers AppEngineFlexibleAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#mime_type AppEngineFlexibleAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#require_matching_file AppEngineFlexibleAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#upload_path_regex AppEngineFlexibleAppVersion#upload_path_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb2367fd5068af79157f1403f60cd371e0f76c860a1078e2d8de605fb791061)
            check_type(argname="argument application_readable", value=application_readable, expected_type=type_hints["application_readable"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument mime_type", value=mime_type, expected_type=type_hints["mime_type"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument require_matching_file", value=require_matching_file, expected_type=type_hints["require_matching_file"])
            check_type(argname="argument upload_path_regex", value=upload_path_regex, expected_type=type_hints["upload_path_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_readable is not None:
            self._values["application_readable"] = application_readable
        if expiration is not None:
            self._values["expiration"] = expiration
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if mime_type is not None:
            self._values["mime_type"] = mime_type
        if path is not None:
            self._values["path"] = path
        if require_matching_file is not None:
            self._values["require_matching_file"] = require_matching_file
        if upload_path_regex is not None:
            self._values["upload_path_regex"] = upload_path_regex

    @builtins.property
    def application_readable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether files should also be uploaded as code data.

        By default, files declared in static file handlers are
        uploaded as static data and are only served to end users; they cannot be read by the application. If enabled,
        uploads are charged against both your code and static data storage resource quotas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#application_readable AppEngineFlexibleAppVersion#application_readable}
        '''
        result = self._values.get("application_readable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Time a static file served by this handler should be cached by web proxies and browsers.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s".
        Default is '0s'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#expiration AppEngineFlexibleAppVersion#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#http_headers AppEngineFlexibleAppVersion#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mime_type(self) -> typing.Optional[builtins.str]:
        '''MIME type used to serve all files served by this handler.

        Defaults to file-specific MIME types, which are derived from each file's filename extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#mime_type AppEngineFlexibleAppVersion#mime_type}
        '''
        result = self._values.get("mime_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to the static files matched by the URL pattern, from the application root directory.

        The path can refer to text matched in groupings in the URL pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_matching_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this handler should match the request if the file referenced by the handler does not exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#require_matching_file AppEngineFlexibleAppVersion#require_matching_file}
        '''
        result = self._values.get("require_matching_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upload_path_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression that matches the file paths for all files that should be referenced by this handler.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#upload_path_regex AppEngineFlexibleAppVersion#upload_path_regex}
        '''
        result = self._values.get("upload_path_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionHandlersStaticFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionHandlersStaticFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionHandlersStaticFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bbcb983dac25b7c44e27f8df60d8835ea5cbd3bedb4689f153aef0bf3e2147f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApplicationReadable")
    def reset_application_readable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationReadable", []))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetMimeType")
    def reset_mime_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMimeType", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRequireMatchingFile")
    def reset_require_matching_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireMatchingFile", []))

    @jsii.member(jsii_name="resetUploadPathRegex")
    def reset_upload_path_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUploadPathRegex", []))

    @builtins.property
    @jsii.member(jsii_name="applicationReadableInput")
    def application_readable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "applicationReadableInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="mimeTypeInput")
    def mime_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mimeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="requireMatchingFileInput")
    def require_matching_file_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireMatchingFileInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadPathRegexInput")
    def upload_path_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uploadPathRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationReadable")
    def application_readable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "applicationReadable"))

    @application_readable.setter
    def application_readable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416c53b5a96f1616ec6cb58dc9f45e76ef993e79da87a2ebde0e44e055173ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationReadable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2e13a5f86b7de829738e4426f9ef1c206257bf8a5be9ac596a728377cf15c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "httpHeaders"))

    @http_headers.setter
    def http_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b82bfd25f6062a683733e976bc6a599725b83a495812316f1cf676df39815dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mimeType")
    def mime_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mimeType"))

    @mime_type.setter
    def mime_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d25d980a41efb6ccf3422f6576e7401585346c9e6e90a08ec35ace4b79278f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mimeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd711ef84ccd16328a7aa219d74bc976058ecac71fad44a81f29ce4608ccc601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireMatchingFile")
    def require_matching_file(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireMatchingFile"))

    @require_matching_file.setter
    def require_matching_file(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e72a59509f7217409dc99b496fb82a8aa8032044559cc11aefaf6d05325919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireMatchingFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadPathRegex")
    def upload_path_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uploadPathRegex"))

    @upload_path_regex.setter
    def upload_path_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8c621f2b4476efa7e015d6e6379ebe7470a956c421b99f255c5f24c1f96126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadPathRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionHandlersStaticFiles]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionHandlersStaticFiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionHandlersStaticFiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432c7b5d4b33b7876c199ec86701c6452c5f917ae2e76ab8110125025deb58ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionLivenessCheck",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "check_interval": "checkInterval",
        "failure_threshold": "failureThreshold",
        "host": "host",
        "initial_delay": "initialDelay",
        "success_threshold": "successThreshold",
        "timeout": "timeout",
    },
)
class AppEngineFlexibleAppVersionLivenessCheck:
    def __init__(
        self,
        *,
        path: builtins.str,
        check_interval: typing.Optional[builtins.str] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[builtins.str] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        :param check_interval: Interval between health checks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#check_interval AppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before considering the VM unhealthy. Default: 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#failure_threshold AppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#host AppEngineFlexibleAppVersion#host}
        :param initial_delay: The initial delay before starting to execute the checks. Default: "300s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#initial_delay AppEngineFlexibleAppVersion#initial_delay}
        :param success_threshold: Number of consecutive successful checks required before considering the VM healthy. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#success_threshold AppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeout AppEngineFlexibleAppVersion#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934246427f811a373c77f0a5872c9155129dfdd999639fbe73c6fa87f6a6f8cf)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument check_interval", value=check_interval, expected_type=type_hints["check_interval"])
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument initial_delay", value=initial_delay, expected_type=type_hints["initial_delay"])
            check_type(argname="argument success_threshold", value=success_threshold, expected_type=type_hints["success_threshold"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if check_interval is not None:
            self._values["check_interval"] = check_interval
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if host is not None:
            self._values["host"] = host
        if initial_delay is not None:
            self._values["initial_delay"] = initial_delay
        if success_threshold is not None:
            self._values["success_threshold"] = success_threshold
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def path(self) -> builtins.str:
        '''The request path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def check_interval(self) -> typing.Optional[builtins.str]:
        '''Interval between health checks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#check_interval AppEngineFlexibleAppVersion#check_interval}
        '''
        result = self._values.get("check_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failed checks required before considering the VM unhealthy. Default: 4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#failure_threshold AppEngineFlexibleAppVersion#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#host AppEngineFlexibleAppVersion#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[builtins.str]:
        '''The initial delay before starting to execute the checks. Default: "300s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#initial_delay AppEngineFlexibleAppVersion#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successful checks required before considering the VM healthy. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#success_threshold AppEngineFlexibleAppVersion#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Time before the check is considered failed. Default: "4s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeout AppEngineFlexibleAppVersion#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionLivenessCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionLivenessCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionLivenessCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff9ff6b3e2954c31809a33acd65b4529b3a714a33657a6b45dedeb853702c02f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCheckInterval")
    def reset_check_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckInterval", []))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetInitialDelay")
    def reset_initial_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelay", []))

    @jsii.member(jsii_name="resetSuccessThreshold")
    def reset_success_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessThreshold", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="checkIntervalInput")
    def check_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelayInput")
    def initial_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initialDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="successThresholdInput")
    def success_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="checkInterval")
    def check_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkInterval"))

    @check_interval.setter
    def check_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8963d106c7d3e03c8465431a36843f00e402d23b89aaf236c3c51be108c31453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcacd9de3f4a7ae097e4b38417d4758aabaf001c880e5e4d51b4b7b298c29260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a6922390f4d335948fd25bacaae8cfc30ff421ae42bb583819f1f0f8edf3fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abaafa338392202c2f2dcca7cbbc39e25ef8aa2df3180e109d8ec78571fe881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2b0627562960c4a612970278da997120d4c056bab532323cd7f53720d5912d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b770588c5a8412cc80dfa4129a02f414f88c28c62adc24480463773eaeb35ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecebbcf3b121c9b10799432a122dee8e665648e4cf2ae8ad4927d3703187cf26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionLivenessCheck]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionLivenessCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionLivenessCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d600d0d7f6f91930c5491263e46e5f52ec05fee5404e5dcb4672be65e82fbff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionManualScaling",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class AppEngineFlexibleAppVersionManualScaling:
    def __init__(self, *, instances: jsii.Number) -> None:
        '''
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instances AppEngineFlexibleAppVersion#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5352a3c7c731eadb8bf8f29bb637015560ceb1fed008eab82bba24ff56cd28)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instances": instances,
        }

    @builtins.property
    def instances(self) -> jsii.Number:
        '''Number of instances to assign to the service at the start.

        **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2
        Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instances AppEngineFlexibleAppVersion#instances}
        '''
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionManualScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionManualScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionManualScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__499c18e7d2c14467097338bca06c4b81cc7dfad66e44dd3e8d1d08ac336838b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7365b4685ad7891354464ce914bf8b8ff2fa788391297f01613fff111a88efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionManualScaling]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionManualScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionManualScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f66a655c5f434e542dd762f1fc8a37f1cb28fed5be71b1aa7cd4845c9a0067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "forwarded_ports": "forwardedPorts",
        "instance_tag": "instanceTag",
        "session_affinity": "sessionAffinity",
        "subnetwork": "subnetwork",
    },
)
class AppEngineFlexibleAppVersionNetwork:
    def __init__(
        self,
        *,
        name: builtins.str,
        forwarded_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_tag: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Google Compute Engine network where the virtual machines are created. Specify the short name, not the resource path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        :param forwarded_ports: List of ports, or port pairs, to forward from the virtual machine to the application container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#forwarded_ports AppEngineFlexibleAppVersion#forwarded_ports}
        :param instance_tag: Tag to apply to the instance during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instance_tag AppEngineFlexibleAppVersion#instance_tag}
        :param session_affinity: Enable session affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#session_affinity AppEngineFlexibleAppVersion#session_affinity}
        :param subnetwork: Google Cloud Platform sub-network where the virtual machines are created. Specify the short name, not the resource path. If the network that the instance is being created in is a Legacy network, then the IP address is allocated from the IPv4Range. If the network that the instance is being created in is an auto Subnet Mode Network, then only network name should be specified (not the subnetworkName) and the IP address is created from the IPCidrRange of the subnetwork that exists in that zone for that network. If the network that the instance is being created in is a custom Subnet Mode Network, then the subnetworkName must be specified and the IP address is created from the IPCidrRange of the subnetwork. If specified, the subnetwork must exist in the same region as the App Engine flexible environment application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#subnetwork AppEngineFlexibleAppVersion#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099930e67f98b35fff6aab9482de800b73c99a228756e33a35de887d93bef718)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument forwarded_ports", value=forwarded_ports, expected_type=type_hints["forwarded_ports"])
            check_type(argname="argument instance_tag", value=instance_tag, expected_type=type_hints["instance_tag"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if forwarded_ports is not None:
            self._values["forwarded_ports"] = forwarded_ports
        if instance_tag is not None:
            self._values["instance_tag"] = instance_tag
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork

    @builtins.property
    def name(self) -> builtins.str:
        '''Google Compute Engine network where the virtual machines are created. Specify the short name, not the resource path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forwarded_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of ports, or port pairs, to forward from the virtual machine to the application container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#forwarded_ports AppEngineFlexibleAppVersion#forwarded_ports}
        '''
        result = self._values.get("forwarded_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_tag(self) -> typing.Optional[builtins.str]:
        '''Tag to apply to the instance during creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#instance_tag AppEngineFlexibleAppVersion#instance_tag}
        '''
        result = self._values.get("instance_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable session affinity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#session_affinity AppEngineFlexibleAppVersion#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Platform sub-network where the virtual machines are created. Specify the short name, not the resource path.

        If the network that the instance is being created in is a Legacy network, then the IP address is allocated from the IPv4Range.
        If the network that the instance is being created in is an auto Subnet Mode Network, then only network name should be specified (not the subnetworkName) and the IP address is created from the IPCidrRange of the subnetwork that exists in that zone for that network.
        If the network that the instance is being created in is a custom Subnet Mode Network, then the subnetworkName must be specified and the IP address is created from the IPCidrRange of the subnetwork.
        If specified, the subnetwork must exist in the same region as the App Engine flexible environment application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#subnetwork AppEngineFlexibleAppVersion#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb42511a026b9d098e61119c42fe5033ef9459bd1c6facb3c9482287473989e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetForwardedPorts")
    def reset_forwarded_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedPorts", []))

    @jsii.member(jsii_name="resetInstanceTag")
    def reset_instance_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceTag", []))

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @builtins.property
    @jsii.member(jsii_name="forwardedPortsInput")
    def forwarded_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forwardedPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTagInput")
    def instance_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTagInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedPorts")
    def forwarded_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardedPorts"))

    @forwarded_ports.setter
    def forwarded_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfe0162f79c13e7cf58c3152c966d52068516559163f9d71301ef9d8125b1d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardedPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTag")
    def instance_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTag"))

    @instance_tag.setter
    def instance_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6acf02723000d1156da882ad26394f042df0f0820e5423892b7877162b51bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960e35f3f58fde9cd0ad3d1aedbe1f76f087ef8ac98c5197425bd10bdf937bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1202113447ede38e87811fd8ea7b2e41122bbe8c092f377d4503739b67a256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a763f8e74d5f08b91aac020c84e3b3886c3edeac02368277b1da951599454b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineFlexibleAppVersionNetwork]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad3d7a1b31e938359fe9cc71dab10a82a04204a8c9f3bb00b23151b752cf772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionReadinessCheck",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "app_start_timeout": "appStartTimeout",
        "check_interval": "checkInterval",
        "failure_threshold": "failureThreshold",
        "host": "host",
        "success_threshold": "successThreshold",
        "timeout": "timeout",
    },
)
class AppEngineFlexibleAppVersionReadinessCheck:
    def __init__(
        self,
        *,
        path: builtins.str,
        app_start_timeout: typing.Optional[builtins.str] = None,
        check_interval: typing.Optional[builtins.str] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        :param app_start_timeout: A maximum time limit on application initialization, measured from moment the application successfully replies to a healthcheck until it is ready to serve traffic. Default: "300s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#app_start_timeout AppEngineFlexibleAppVersion#app_start_timeout}
        :param check_interval: Interval between health checks. Default: "5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#check_interval AppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before removing traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#failure_threshold AppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#host AppEngineFlexibleAppVersion#host}
        :param success_threshold: Number of consecutive successful checks required before receiving traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#success_threshold AppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeout AppEngineFlexibleAppVersion#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e243a8bae05eeedf728d15c34138eb144d6d47cd2f320b4450fa321dcb6521)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument app_start_timeout", value=app_start_timeout, expected_type=type_hints["app_start_timeout"])
            check_type(argname="argument check_interval", value=check_interval, expected_type=type_hints["check_interval"])
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument success_threshold", value=success_threshold, expected_type=type_hints["success_threshold"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if app_start_timeout is not None:
            self._values["app_start_timeout"] = app_start_timeout
        if check_interval is not None:
            self._values["check_interval"] = check_interval
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if host is not None:
            self._values["host"] = host
        if success_threshold is not None:
            self._values["success_threshold"] = success_threshold
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def path(self) -> builtins.str:
        '''The request path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#path AppEngineFlexibleAppVersion#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_start_timeout(self) -> typing.Optional[builtins.str]:
        '''A maximum time limit on application initialization, measured from moment the application successfully replies to a healthcheck until it is ready to serve traffic.

        Default: "300s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#app_start_timeout AppEngineFlexibleAppVersion#app_start_timeout}
        '''
        result = self._values.get("app_start_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_interval(self) -> typing.Optional[builtins.str]:
        '''Interval between health checks.  Default: "5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#check_interval AppEngineFlexibleAppVersion#check_interval}
        '''
        result = self._values.get("check_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failed checks required before removing traffic. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#failure_threshold AppEngineFlexibleAppVersion#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#host AppEngineFlexibleAppVersion#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successful checks required before receiving traffic. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#success_threshold AppEngineFlexibleAppVersion#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Time before the check is considered failed. Default: "4s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#timeout AppEngineFlexibleAppVersion#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionReadinessCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionReadinessCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionReadinessCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2554ff77138da66e90e748425d0f5e754c61644f469c4ba375ad480e9ec5c0e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppStartTimeout")
    def reset_app_start_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppStartTimeout", []))

    @jsii.member(jsii_name="resetCheckInterval")
    def reset_check_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckInterval", []))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetSuccessThreshold")
    def reset_success_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessThreshold", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="appStartTimeoutInput")
    def app_start_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appStartTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="checkIntervalInput")
    def check_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="successThresholdInput")
    def success_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="appStartTimeout")
    def app_start_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appStartTimeout"))

    @app_start_timeout.setter
    def app_start_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5be6d51711894d650a8ad1f2d64a68ad80b201710119cab7d87369be4684621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appStartTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="checkInterval")
    def check_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkInterval"))

    @check_interval.setter
    def check_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb0f0c4dc99cacaa6664833cb2bb8c8e73f4ea85112448966085d676c4b338f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84644d9cb6d6373bb46f3414fec47ee6f1fb318c6138e7dfd34bfa79f073b7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccbbafcbed299d374c9e133c61c5c971d60d0d5c8db4637c2d0028725be14bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2679fc707764c45286733417b3584e05369ff9b0d08d7804ca70c64f0c96bbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f270971ec27391ef000173d4b1981ef11c664b6a6bd96b543d41ab7042bcc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a34c1832224046ce75de5284249540327d856829b09f74b3e0a4fa98a27089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionReadinessCheck]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionReadinessCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionReadinessCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46490c07d6efdf99eb62032898aa29477cd637b1ea131496567f23e9a584a44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionResources",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "disk_gb": "diskGb",
        "memory_gb": "memoryGb",
        "volumes": "volumes",
    },
)
class AppEngineFlexibleAppVersionResources:
    def __init__(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        disk_gb: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionResourcesVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cpu: Number of CPU cores needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cpu AppEngineFlexibleAppVersion#cpu}
        :param disk_gb: Disk size (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disk_gb AppEngineFlexibleAppVersion#disk_gb}
        :param memory_gb: Memory (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#memory_gb AppEngineFlexibleAppVersion#memory_gb}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#volumes AppEngineFlexibleAppVersion#volumes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf03490cd409124774919d686e3fbb7bc9c96c9d0115c5b12960c4d3cfaca65)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument disk_gb", value=disk_gb, expected_type=type_hints["disk_gb"])
            check_type(argname="argument memory_gb", value=memory_gb, expected_type=type_hints["memory_gb"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if disk_gb is not None:
            self._values["disk_gb"] = disk_gb
        if memory_gb is not None:
            self._values["memory_gb"] = memory_gb
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''Number of CPU cores needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#cpu AppEngineFlexibleAppVersion#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_gb(self) -> typing.Optional[jsii.Number]:
        '''Disk size (GB) needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#disk_gb AppEngineFlexibleAppVersion#disk_gb}
        '''
        result = self._values.get("disk_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#memory_gb AppEngineFlexibleAppVersion#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionResourcesVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#volumes AppEngineFlexibleAppVersion#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionResourcesVolumes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63a4a29d0b2cc0c1962d0ecf159b0457c949768c23f146b1c7d0e9181383c69d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineFlexibleAppVersionResourcesVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091c6d3351ee1e80f80b99dc5562a578b93b6107c46fa3d45fea406c26cce8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetDiskGb")
    def reset_disk_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskGb", []))

    @jsii.member(jsii_name="resetMemoryGb")
    def reset_memory_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGb", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "AppEngineFlexibleAppVersionResourcesVolumesList":
        return typing.cast("AppEngineFlexibleAppVersionResourcesVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="diskGbInput")
    def disk_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskGbInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGbInput")
    def memory_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGbInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionResourcesVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineFlexibleAppVersionResourcesVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b52215b81eb3639c81e5cfe3dc35867b6469945a151720d68288bd33ee078b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskGb")
    def disk_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskGb"))

    @disk_gb.setter
    def disk_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b19da1fb491cfa4bad597adce0815faea7ac7eea8f3f53a2ba4b795226bfce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f9c567314b40c83e9bcc03956a90dab07cfdb8261ebe0bf95d9bd3e49d8152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineFlexibleAppVersionResources]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202a187b1a90a1f3952428110ba1dfdbdcf9aba33e367758833f18d8371886dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionResourcesVolumes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "size_gb": "sizeGb", "volume_type": "volumeType"},
)
class AppEngineFlexibleAppVersionResourcesVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        size_gb: jsii.Number,
        volume_type: builtins.str,
    ) -> None:
        '''
        :param name: Unique name for the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        :param size_gb: Volume size in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#size_gb AppEngineFlexibleAppVersion#size_gb}
        :param volume_type: Underlying volume type, e.g. 'tmpfs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#volume_type AppEngineFlexibleAppVersion#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336b7c220fe115940c58e133a0b2d01add54108c4c59a77e779d7323dd2d935f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument size_gb", value=size_gb, expected_type=type_hints["size_gb"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "size_gb": size_gb,
            "volume_type": volume_type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Unique name for the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_gb(self) -> jsii.Number:
        '''Volume size in gigabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#size_gb AppEngineFlexibleAppVersion#size_gb}
        '''
        result = self._values.get("size_gb")
        assert result is not None, "Required property 'size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_type(self) -> builtins.str:
        '''Underlying volume type, e.g. 'tmpfs'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#volume_type AppEngineFlexibleAppVersion#volume_type}
        '''
        result = self._values.get("volume_type")
        assert result is not None, "Required property 'volume_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionResourcesVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionResourcesVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionResourcesVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8068f524bd3dfef3ccc821e29f218e28ffc08a4cbdbb9a9a9f06feea3488aae6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppEngineFlexibleAppVersionResourcesVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cbcbe0ecf7f47ea49cc495dc1ae514c8e411efb787de9cc72068d3df5304aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppEngineFlexibleAppVersionResourcesVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5016af623a2ac6f4f1f1a2bc06b80e76949cc362c5fd9e1151b69f47627b30c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c34a190144609fdb3e6367793760a21b716a116568024a91ae424f343df844e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3eea630d1f9f949bcef691fb7ecf99796f24d2462ce30b8a3983ed327af1bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionResourcesVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionResourcesVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionResourcesVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28593493b66704bee6346920877a61478cf8d2be6c2e8881dfe50101cff07ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineFlexibleAppVersionResourcesVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionResourcesVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__799e05dfda4a1ba73666600a9552e4adf94306b1fa071973692b9130633473b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGbInput")
    def size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21b140c1ab474ab7ff5b467f31f5a64a4ed7e3de47daa033d100e22f80539cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @size_gb.setter
    def size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1b4fd1cbc2ce53d7fe770df503cb7ec84e318e3072f83de23a75ec2f9c7d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aaa2ae212a291b5dee3352c157424be854fbafb07d69052e8696c00f773abae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionResourcesVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionResourcesVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionResourcesVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7655adbf738d3d021777e4a65345637a1d231500a5005a159eb3c69c3e185fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AppEngineFlexibleAppVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#create AppEngineFlexibleAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#delete AppEngineFlexibleAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#update AppEngineFlexibleAppVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23198e67c6f4a60cf948cf01fa795ddf96d36fc98efbcbc72badde100bf301d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#create AppEngineFlexibleAppVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#delete AppEngineFlexibleAppVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#update AppEngineFlexibleAppVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9faf4267dc58b94a385a1caecc9fe2c8c3b9fed087511d3fcee944144411616d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3f6effebb728f2d3e77c8a6cd1eaca56bb9203627798d0df796ad0f02a85932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b35c8dcae69d3b1b4c8948b6469afbc641f4247678783c55d81b9ccf60e395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7478fcf681388e7606af9fef86b581158b07619634e84f54c2b00331b00ef495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d181c8fe3d1cc712fde25591e4fc5fc5ffee2919fd60faf60a9c990768825b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionVpcAccessConnector",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class AppEngineFlexibleAppVersionVpcAccessConnector:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f32165dae6bfda366452e2c7aad099d37ac658220d757f1e293ffdae84991d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_flexible_app_version#name AppEngineFlexibleAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineFlexibleAppVersionVpcAccessConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineFlexibleAppVersionVpcAccessConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineFlexibleAppVersion.AppEngineFlexibleAppVersionVpcAccessConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84e4d6d528e55a2405414f973592f8947a9aa1be333eb11768d631e1d44f6de5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff05a6cc15c1fa6b5e9398676f34fb29484765391529644edde2b87381b2a75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineFlexibleAppVersionVpcAccessConnector]:
        return typing.cast(typing.Optional[AppEngineFlexibleAppVersionVpcAccessConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineFlexibleAppVersionVpcAccessConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c42e8f465c4db3c81db8d327e2c43d61ab0af7f14e969d6332820e85a20a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppEngineFlexibleAppVersion",
    "AppEngineFlexibleAppVersionApiConfig",
    "AppEngineFlexibleAppVersionApiConfigOutputReference",
    "AppEngineFlexibleAppVersionAutomaticScaling",
    "AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization",
    "AppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference",
    "AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization",
    "AppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference",
    "AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization",
    "AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference",
    "AppEngineFlexibleAppVersionAutomaticScalingOutputReference",
    "AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization",
    "AppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference",
    "AppEngineFlexibleAppVersionConfig",
    "AppEngineFlexibleAppVersionDeployment",
    "AppEngineFlexibleAppVersionDeploymentCloudBuildOptions",
    "AppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference",
    "AppEngineFlexibleAppVersionDeploymentContainer",
    "AppEngineFlexibleAppVersionDeploymentContainerOutputReference",
    "AppEngineFlexibleAppVersionDeploymentFiles",
    "AppEngineFlexibleAppVersionDeploymentFilesList",
    "AppEngineFlexibleAppVersionDeploymentFilesOutputReference",
    "AppEngineFlexibleAppVersionDeploymentOutputReference",
    "AppEngineFlexibleAppVersionDeploymentZip",
    "AppEngineFlexibleAppVersionDeploymentZipOutputReference",
    "AppEngineFlexibleAppVersionEndpointsApiService",
    "AppEngineFlexibleAppVersionEndpointsApiServiceOutputReference",
    "AppEngineFlexibleAppVersionEntrypoint",
    "AppEngineFlexibleAppVersionEntrypointOutputReference",
    "AppEngineFlexibleAppVersionFlexibleRuntimeSettings",
    "AppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference",
    "AppEngineFlexibleAppVersionHandlers",
    "AppEngineFlexibleAppVersionHandlersList",
    "AppEngineFlexibleAppVersionHandlersOutputReference",
    "AppEngineFlexibleAppVersionHandlersScript",
    "AppEngineFlexibleAppVersionHandlersScriptOutputReference",
    "AppEngineFlexibleAppVersionHandlersStaticFiles",
    "AppEngineFlexibleAppVersionHandlersStaticFilesOutputReference",
    "AppEngineFlexibleAppVersionLivenessCheck",
    "AppEngineFlexibleAppVersionLivenessCheckOutputReference",
    "AppEngineFlexibleAppVersionManualScaling",
    "AppEngineFlexibleAppVersionManualScalingOutputReference",
    "AppEngineFlexibleAppVersionNetwork",
    "AppEngineFlexibleAppVersionNetworkOutputReference",
    "AppEngineFlexibleAppVersionReadinessCheck",
    "AppEngineFlexibleAppVersionReadinessCheckOutputReference",
    "AppEngineFlexibleAppVersionResources",
    "AppEngineFlexibleAppVersionResourcesOutputReference",
    "AppEngineFlexibleAppVersionResourcesVolumes",
    "AppEngineFlexibleAppVersionResourcesVolumesList",
    "AppEngineFlexibleAppVersionResourcesVolumesOutputReference",
    "AppEngineFlexibleAppVersionTimeouts",
    "AppEngineFlexibleAppVersionTimeoutsOutputReference",
    "AppEngineFlexibleAppVersionVpcAccessConnector",
    "AppEngineFlexibleAppVersionVpcAccessConnectorOutputReference",
]

publication.publish()

def _typecheckingstub__e46baa41731a0b8bcab1d56572382b0fc47f1b379830be99af8384c3ce21ec26(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    liveness_check: typing.Union[AppEngineFlexibleAppVersionLivenessCheck, typing.Dict[builtins.str, typing.Any]],
    readiness_check: typing.Union[AppEngineFlexibleAppVersionReadinessCheck, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    api_config: typing.Optional[typing.Union[AppEngineFlexibleAppVersionApiConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    automatic_scaling: typing.Optional[typing.Union[AppEngineFlexibleAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    default_expiration: typing.Optional[builtins.str] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment: typing.Optional[typing.Union[AppEngineFlexibleAppVersionDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoints_api_service: typing.Optional[typing.Union[AppEngineFlexibleAppVersionEndpointsApiService, typing.Dict[builtins.str, typing.Any]]] = None,
    entrypoint: typing.Optional[typing.Union[AppEngineFlexibleAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    flexible_runtime_settings: typing.Optional[typing.Union[AppEngineFlexibleAppVersionFlexibleRuntimeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    manual_scaling: typing.Optional[typing.Union[AppEngineFlexibleAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[AppEngineFlexibleAppVersionNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    nobuild_files_regex: typing.Optional[builtins.str] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[AppEngineFlexibleAppVersionResources, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    runtime_channel: typing.Optional[builtins.str] = None,
    runtime_main_executable_path: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    serving_status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppEngineFlexibleAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[AppEngineFlexibleAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e356b2ae56c4c12b5c10f812816282e3c38845b320c4aa61c917d3a70dde7f5a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eadd705340bc124c07d9dd7af6c0af2e86d96c8b7056e95577d8ff89c34c67e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43936e328a204423669fcc377e5250e960607d64ae1e1b5d13477e6b160108c0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3de01269a4e61bb09c9b3e83a0e4ef233fe0e2f04aa74c15eba9e39be7cf86e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842ad4b62da031d61fa2b8610807ada57dbc1116479986aae8920467556c39ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935cb89345a43ba055cbfc9325e4f805f31a43befaa961d30deb9313f76b9968(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f1cb210e4b45d91d2e1c2e79bcb2e69e39eabdd28b069c416f582010c08d54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e42b7b034ece8ea72f89a87203544303e2409e8f17044a845782117db4ef40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66baf3c26f53a1895261cea2362df893a44e8258b3a43f509ba7288eda32f87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c84b655326c0e4da77f47d2e5580b33a4dc22147b43456812881a93ac2567f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9277434eb630bf83f650924d247716ab26d315709b863041b4558885f5b00890(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afafea02b62c5ca0e3835fff1eea08b5b44d50f3dbed836ce9fa4f412b699092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58ba58195f3ea7b06a6d311bd57eb253f5a374b8974df6a04751c8b412891e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e77d29c845e8d2460d93d3631568e9d1aad90b39d902d1de8e2f39317d97be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c7a653259a27ca13dea9c36cdce953838aefaabccae9e85459a6d0ce51495f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ccac7695545e0c88c9cb0099e56ebfcc0e049620ddba9e1c8d51106515b948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663aa1aefe0081cffcc74aff636604118e98e3ce2febd709e462ae9fb0ca655a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5127f6c6cf8a14c847cd371918efae09972bd5c7a7595d71c32c0773aed09702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7226339c4cac65f79693a3d48a8c4238f1cc9e774a6876054d85dad7a9a372ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309e2aa1426ec3f78583c0932b186644dbee5a7a2024fc636f9409061e19939b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e340960f181a5b2b488acc4d868bfad10312739207d323bf1ac85a0d270aa6a(
    *,
    script: builtins.str,
    auth_fail_action: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    security_level: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa1373194e2042d8e4a3002a6d251500fbe8a43b6b8f0e70a17454735a3dee3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda7f99f7efb6cc7c9c948da8de817cacf7d3b157667969bb4b03a2b915f88e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f42230c079693f5daa9658c4ab10b5566b79e3b71123c100b1bbe9fbd0514e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43157cb358ab8b736712cd84d101f382d0fc3afb1c6bd4cec39a28e9584268cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2c57a27946e8e77e845748a11f477f78f4aa55e2f69540bc53796e988feadb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c47aeed0e6a9cd2c4bd625be74a535988449aba66a6eadd3a2bc929cf885b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9acd96a8d246ac854f77dbcf5d78e8a7ba530e1388502e0aa0de9291fa7b4f9(
    value: typing.Optional[AppEngineFlexibleAppVersionApiConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f292286440d5b53f2bac3996f50b11a5945066340b1452b28a18f6dfd269a6a(
    *,
    cpu_utilization: typing.Union[AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization, typing.Dict[builtins.str, typing.Any]],
    cool_down_period: typing.Optional[builtins.str] = None,
    disk_utilization: typing.Optional[typing.Union[AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    max_concurrent_requests: typing.Optional[jsii.Number] = None,
    max_idle_instances: typing.Optional[jsii.Number] = None,
    max_pending_latency: typing.Optional[builtins.str] = None,
    max_total_instances: typing.Optional[jsii.Number] = None,
    min_idle_instances: typing.Optional[jsii.Number] = None,
    min_pending_latency: typing.Optional[builtins.str] = None,
    min_total_instances: typing.Optional[jsii.Number] = None,
    network_utilization: typing.Optional[typing.Union[AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    request_utilization: typing.Optional[typing.Union[AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4249c050c7b6ac7898badc8cdfff5049a65e260e57428eb36ea6169ccc7fe77a(
    *,
    target_utilization: jsii.Number,
    aggregation_window_length: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1601cc0345dce1dbbfbf3837b5e1f9ce7891dbbe977dccc11b0c0ed32effcd47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bf159713491ca330604e9204a93a4972682ff387a53e23587980b215c8c512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbeae3e48b5339ebfc03b2449bd6d99b4a690b018e439fe51a59aefc507a72a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__accff91caacc593833b2f00a73e9876ad4a29c2717fc4fbdaac3bffd76927d67(
    value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingCpuUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6cb7f36ec168bf0e0db1987e8fd48b0612086f94c3e95208f887e2e612c5b19(
    *,
    target_read_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_read_ops_per_second: typing.Optional[jsii.Number] = None,
    target_write_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_write_ops_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7477868ecf60d73c6a728a346b976937949ab7ee708c420a20dce2bc41a71019(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c38a5e060028fcdf07277a12e4d299a2b080261eff0436d7feb0910d15ee00(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878b60c1b9c037bc828955fa2d7218dc308be512ee74e80aa39469bc8f489053(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe4c5065e16f13f0828f3dc61775df531119f1ba786b8d17bbeee01f8533fc3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280be15a44f4247c3fb4d465dcc25ef67576d9ce10643e29e5fa28c2a59d6a14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3aa1ad199f6203ad40f92f3ec1ce99f2295a64e0acef5e525ede34b75941620(
    value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingDiskUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd9e939069da4c6f670272f6eb16f44c2fad908d59edbf72ebe8e6508befb05(
    *,
    target_received_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_received_packets_per_second: typing.Optional[jsii.Number] = None,
    target_sent_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_sent_packets_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9c5ec3a2622ceed8a301a84f5600b693927881cc30c7542a99f56bce623120(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3932ce9b21f75d17c8f20d796b515eff587784c3daa198e50eaf80320b432c0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8027863260aa7c455bb24f3513786412899ab2ec23effc33620db2c9c0ee2c09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e37c5ff3f3db9529545b14984e2470d2de482913c39a9f41fa68a2d8a6db612(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f055b7ce0606cfcbc949106d6bdd8485e2eb22f9be3450227b75b70b8adbc5d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f856d5d7f18d99b99412d4aa391e1431ba5c7ef357ea923ec0839b2fb1fb964b(
    value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c440e2c760fceacf783f7077e22592488d50091d0c118253a5e0cb7a66531468(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03392d2466377da4e5ad2b625614c72a92d2f75d329e9b08838af87b75621f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4be6db8fafe0a26d15ff8c00bc5b195d9c386279322002b6abe331ae495f838(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91f684db00e6eb9ca23693c587b31b7a213cc7763a030f6ff7dad3fb38b6b66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a296fa73f23ebc3f6f1d6b34be9f0169060d8d4d75c96c7f1a744387b901732e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcad5d19680bba3da7f5a9bf38f6c3bf902e0939f547bd62a11fcfc799f09c13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be49b6cf8dfa907963c67c9bbe3a0864d5a393f71b265d67a3df2ac3df899df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75733115ed2e723bbe36b011bbe5d620be3c874ce402da81abd69fde8b5981f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f11f8c1a4bb0602518283e03de0f8b75f70227af933e628907f79bb68ce88d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1d3379eb51b7804205bd89b449d002e8ea6865b3e89255b350419e0eb0c745(
    value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfaf1954449d8dbc3ab6c60cf4331a39dfaaa86addf0313bd70a7e41f92a972(
    *,
    target_concurrent_requests: typing.Optional[jsii.Number] = None,
    target_request_count_per_second: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993cf687a7223b28238791fdfaddaa7e41626f6eebf94a528ee642a28f8b1673(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8a000d94dc01f639dbd2c067aedcd7c9007bf5053e2f42c0262a148de26e0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbfc99275bb97004bef724e94206928a29d88a68d00c3da98536671a54e39af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4534c63888e89a664617eccbb139af650136c189b04b52343eec0e01c8f8ff6(
    value: typing.Optional[AppEngineFlexibleAppVersionAutomaticScalingRequestUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1809754fe940e05679993049eac52967aabf82acf792de8ed99ba349f63f62(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_check: typing.Union[AppEngineFlexibleAppVersionLivenessCheck, typing.Dict[builtins.str, typing.Any]],
    readiness_check: typing.Union[AppEngineFlexibleAppVersionReadinessCheck, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    api_config: typing.Optional[typing.Union[AppEngineFlexibleAppVersionApiConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    automatic_scaling: typing.Optional[typing.Union[AppEngineFlexibleAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    default_expiration: typing.Optional[builtins.str] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment: typing.Optional[typing.Union[AppEngineFlexibleAppVersionDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoints_api_service: typing.Optional[typing.Union[AppEngineFlexibleAppVersionEndpointsApiService, typing.Dict[builtins.str, typing.Any]]] = None,
    entrypoint: typing.Optional[typing.Union[AppEngineFlexibleAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    flexible_runtime_settings: typing.Optional[typing.Union[AppEngineFlexibleAppVersionFlexibleRuntimeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    manual_scaling: typing.Optional[typing.Union[AppEngineFlexibleAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[AppEngineFlexibleAppVersionNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    nobuild_files_regex: typing.Optional[builtins.str] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[AppEngineFlexibleAppVersionResources, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    runtime_channel: typing.Optional[builtins.str] = None,
    runtime_main_executable_path: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    serving_status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppEngineFlexibleAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[AppEngineFlexibleAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cad41cf94b5d26b54ae8fe13b282b954e366f54eaac906df13d75e5b96b808(
    *,
    cloud_build_options: typing.Optional[typing.Union[AppEngineFlexibleAppVersionDeploymentCloudBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    container: typing.Optional[typing.Union[AppEngineFlexibleAppVersionDeploymentContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zip: typing.Optional[typing.Union[AppEngineFlexibleAppVersionDeploymentZip, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b42c7bde6c616abe71723c3497729f29da76ecfdb9bf6a79d45f8732bd42169(
    *,
    app_yaml_path: builtins.str,
    cloud_build_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abe9c0d4c49fe1f8a82aafc4694ca8fbed2715a89c88c35ae938dcbb251d153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03c854b922da5455ae099bef5ae2fedd7affb389cfae90c707e966a74572f4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8789a78b70ec85d21a55b4cca55784233d7768780a4129e65065e226cd3a46b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89475283d117da42ecc765877fb0370f6b23599cecfcaaad035d75d6c6ecc79(
    value: typing.Optional[AppEngineFlexibleAppVersionDeploymentCloudBuildOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30057c8255603628183d50bb74b326b5293e7f5b0c80e68ca56935c4dd679b07(
    *,
    image: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909f25812f8f3fac2b447295cf15ed18639ea1d48d152184c60f00750a5035f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddec4b6f732e219612f60d22f1d26bea656473be610735f4b98d00e6d612397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03f3f25cb95b24bbf512c60005bcd7019221e0d57ac749ccfc432f09c46b4dc(
    value: typing.Optional[AppEngineFlexibleAppVersionDeploymentContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bbabff0c673ad9df9c0ce1d8a269e91df7434b2a68cfae48be5e705715cb04(
    *,
    name: builtins.str,
    source_url: builtins.str,
    sha1_sum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4eb394a01425e4ec86d6d315e0d582654049b4e96e7b982b6bd9e3f01ce5e2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d1d45afbc87a8fd78913085a14e1e060039b4e611488fd206b7a9f2b4f71b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820b07a267fffa2eb9cd2ac2fcb59ed7fb08bc8b39c60b08ae0f37de620bcd68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160dac37cfb76fdeb56b07f58ef474871620d50cc4fcb9021122bed56b51c75b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4270b10950b8593138bc7b9d7b75a4b8173b5f6e73a925c225a194adc84ea24d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48acd37cf2b94cb4bd4b9580ba0446a8bfef82db696aab3aba522ae7888aefa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionDeploymentFiles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec22779e36378fa9e4d21ee1cfe6588cebec8aa945d61369f88f5652cbf99278(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e3e928dfed5c278caa769a891243216c228dda044f7d7e858121c9e26b93b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26bbc1cd12e268282755369cc0e75160acd9fe29be5fda6ef73b80dd4ccc1be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f186a7335a3c8c9c26b254f2c81f5277e32d90e9099f2ab4c3fa6356786cc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b0b73d4be4b745c026265829f518ef9252e6bc66f0eb5a85f39db740e4d36a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionDeploymentFiles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f8f09bb50b50b03a63d10ce8f7e4df82e08b9bb8f5e84fbe599d20dd78c801(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123699a947c23f57f36fe20628ac7b91f50339aead23fddc86e790283ee44486(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd8d2fa61c6e08d17f4c2ba392495b36b8a205b29603a6cb61b29a6152ee490(
    value: typing.Optional[AppEngineFlexibleAppVersionDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68439297c89d8937975a842ee1740bc734d54acd43b45bd21e0c975d069f6b1(
    *,
    source_url: builtins.str,
    files_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf8b7a9fa0647bacecb3daeeb562f10d9b97139ab327b232307f1ec962c8419(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defc07fe841db3786658ed06aaf0a273025dba10173c366beedf987d6613794e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1dc159009d2df176f9707da9c8cbea4ceea9bc209611b81639f1a1d91411a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db97f59adb636320a8c84f58fb2b64792117ff848a01518db199fff5499584c(
    value: typing.Optional[AppEngineFlexibleAppVersionDeploymentZip],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a8679c2e2e1ee030ea41fead9b577f32fa98edc11ec1a43133b08f0706140b(
    *,
    name: builtins.str,
    config_id: typing.Optional[builtins.str] = None,
    disable_trace_sampling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rollout_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e20194d6c15fcf539e7791a4afbdef17ad844ff1a1f13c728fa2e0db145a9ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea528667176f31bd6359f2d4c7b57a5e136d4a1fbc8263b673cbbe68caa66d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980fdf2985c9e3c24898ba53a2aebd3e75da82b59e4ada2370a34defa31021a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46beee5c56a5b96ce196811ee3ce67687f3cb66c60b394b41185a76011b44cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3ffca21766a4e199a1815b718f1af114153c9dd0714ed8454c025effbf26b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5aff6716c7d5e501a3936a26e321a54b4f1b59f662a27d3b8552db474afb9c(
    value: typing.Optional[AppEngineFlexibleAppVersionEndpointsApiService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550d177dfe0de0347a2fc3199881f27c9c28877e1282ec571b3854631e656a46(
    *,
    shell: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07611c600260835e3c544f4e875b358f52cf85d6d38582cbfe496ca7ddbbf567(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5206b86cfec1e5b110f6ef7b24bb13f98bd1c9f1dc9ebc017c7955c2989fc3cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9ae8f10d269acec70c5779ae7d754208b0e83bb2a600dba92ec61ed70ceef6(
    value: typing.Optional[AppEngineFlexibleAppVersionEntrypoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fb01e6e138973058a58f649614b8f57d7abb3c9cbedcefed8379cbc6c4fd3b(
    *,
    operating_system: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80607c306349b5c9286a1fcfe4c217b1713c69ba2bbb8137dfa890a09be42f96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670fc1558fc14a657870e58425c2f819f2862ec298cc398640f4aab00cac201e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c560aad2bbfb4c73f7302d042e0314d7f25e1cc30be5a840d6d71e4c1f6fe68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1829302a1e46c6afae1979e4d4921252a4b2c524b777bb44c05078da1efbb15a(
    value: typing.Optional[AppEngineFlexibleAppVersionFlexibleRuntimeSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb143b4d7faf50f3f36ab7ed0611d16cd654fecb5b79e8d67b3f59046a9d9799(
    *,
    auth_fail_action: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    redirect_http_response_code: typing.Optional[builtins.str] = None,
    script: typing.Optional[typing.Union[AppEngineFlexibleAppVersionHandlersScript, typing.Dict[builtins.str, typing.Any]]] = None,
    security_level: typing.Optional[builtins.str] = None,
    static_files: typing.Optional[typing.Union[AppEngineFlexibleAppVersionHandlersStaticFiles, typing.Dict[builtins.str, typing.Any]]] = None,
    url_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339c69850331de4db97b63a27a751f5b74ee21eb53995eb09c2e24fa16bdc403(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8da93fb8fd9252491575281851afecad93b71bf013f33aefce4d3a49ac32f36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cc04cd039ec0c6a4d5b64bff8b87cccf6e8da7f51f09cf7426d574e941ef2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae392cdb14576baebf4dcc500e4efad3be9ecd4bbf67a613e0947ada256d0a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067f009e4827dbca39826f1d72a33769d2b11621cc896e4abcd9cd5909702e2b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42a4777631b065a9f582ff4dab9c8551e0dc35d2430437fa13801e8ac09f812(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionHandlers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20e76bd21781abf657c6f62c8fb20ba8d944053d92a5f41788bb882aa2e2f8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758a95bc64e2af96d7bbcc3231a8f999746a495243f88528d103df463a29e42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9070b37b672cfa4244482645b693a59aa02447868ff17252acbd4313aa72e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699d3a4a93c78b56bf086080c8ecba2020c42a2180bad00bc367255de97024d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6ff79e5712cee24b5609bc017f245237d9e08dcf7f5107f87bd6bb14243d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3b5462597c847d2a4213d60ea802f136a5703aac13058f7e6a22350c57dbee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f972d4b316bb75b053f1c1016ddce499d8d735125dd8b8a921731223fcdec334(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionHandlers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4ef84ced88babff899f76fe51e026a273c47f4a5e90e8366c617ce8046d2a0(
    *,
    script_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dedaa0f72224c55e1e737c1d9611a6b0ac4e3f57848f6488b88ccf539a69e4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcebaa894b1beacb7fdddece32d1d25eb343b95bbab95b4dacdcbfa19111ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce809aa1fc276d05f3379fd773685ad11088d009297904642aa091c160c6dd3c(
    value: typing.Optional[AppEngineFlexibleAppVersionHandlersScript],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb2367fd5068af79157f1403f60cd371e0f76c860a1078e2d8de605fb791061(
    *,
    application_readable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration: typing.Optional[builtins.str] = None,
    http_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mime_type: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    require_matching_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upload_path_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbcb983dac25b7c44e27f8df60d8835ea5cbd3bedb4689f153aef0bf3e2147f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416c53b5a96f1616ec6cb58dc9f45e76ef993e79da87a2ebde0e44e055173ba8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2e13a5f86b7de829738e4426f9ef1c206257bf8a5be9ac596a728377cf15c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b82bfd25f6062a683733e976bc6a599725b83a495812316f1cf676df39815dd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d25d980a41efb6ccf3422f6576e7401585346c9e6e90a08ec35ace4b79278f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd711ef84ccd16328a7aa219d74bc976058ecac71fad44a81f29ce4608ccc601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e72a59509f7217409dc99b496fb82a8aa8032044559cc11aefaf6d05325919(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8c621f2b4476efa7e015d6e6379ebe7470a956c421b99f255c5f24c1f96126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432c7b5d4b33b7876c199ec86701c6452c5f917ae2e76ab8110125025deb58ed(
    value: typing.Optional[AppEngineFlexibleAppVersionHandlersStaticFiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934246427f811a373c77f0a5872c9155129dfdd999639fbe73c6fa87f6a6f8cf(
    *,
    path: builtins.str,
    check_interval: typing.Optional[builtins.str] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    initial_delay: typing.Optional[builtins.str] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9ff6b3e2954c31809a33acd65b4529b3a714a33657a6b45dedeb853702c02f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8963d106c7d3e03c8465431a36843f00e402d23b89aaf236c3c51be108c31453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcacd9de3f4a7ae097e4b38417d4758aabaf001c880e5e4d51b4b7b298c29260(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a6922390f4d335948fd25bacaae8cfc30ff421ae42bb583819f1f0f8edf3fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abaafa338392202c2f2dcca7cbbc39e25ef8aa2df3180e109d8ec78571fe881(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2b0627562960c4a612970278da997120d4c056bab532323cd7f53720d5912d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b770588c5a8412cc80dfa4129a02f414f88c28c62adc24480463773eaeb35ca3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecebbcf3b121c9b10799432a122dee8e665648e4cf2ae8ad4927d3703187cf26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d600d0d7f6f91930c5491263e46e5f52ec05fee5404e5dcb4672be65e82fbff0(
    value: typing.Optional[AppEngineFlexibleAppVersionLivenessCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5352a3c7c731eadb8bf8f29bb637015560ceb1fed008eab82bba24ff56cd28(
    *,
    instances: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499c18e7d2c14467097338bca06c4b81cc7dfad66e44dd3e8d1d08ac336838b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7365b4685ad7891354464ce914bf8b8ff2fa788391297f01613fff111a88efc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f66a655c5f434e542dd762f1fc8a37f1cb28fed5be71b1aa7cd4845c9a0067(
    value: typing.Optional[AppEngineFlexibleAppVersionManualScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099930e67f98b35fff6aab9482de800b73c99a228756e33a35de887d93bef718(
    *,
    name: builtins.str,
    forwarded_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_tag: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb42511a026b9d098e61119c42fe5033ef9459bd1c6facb3c9482287473989e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfe0162f79c13e7cf58c3152c966d52068516559163f9d71301ef9d8125b1d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6acf02723000d1156da882ad26394f042df0f0820e5423892b7877162b51bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960e35f3f58fde9cd0ad3d1aedbe1f76f087ef8ac98c5197425bd10bdf937bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1202113447ede38e87811fd8ea7b2e41122bbe8c092f377d4503739b67a256(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a763f8e74d5f08b91aac020c84e3b3886c3edeac02368277b1da951599454b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad3d7a1b31e938359fe9cc71dab10a82a04204a8c9f3bb00b23151b752cf772(
    value: typing.Optional[AppEngineFlexibleAppVersionNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e243a8bae05eeedf728d15c34138eb144d6d47cd2f320b4450fa321dcb6521(
    *,
    path: builtins.str,
    app_start_timeout: typing.Optional[builtins.str] = None,
    check_interval: typing.Optional[builtins.str] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2554ff77138da66e90e748425d0f5e754c61644f469c4ba375ad480e9ec5c0e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5be6d51711894d650a8ad1f2d64a68ad80b201710119cab7d87369be4684621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb0f0c4dc99cacaa6664833cb2bb8c8e73f4ea85112448966085d676c4b338f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84644d9cb6d6373bb46f3414fec47ee6f1fb318c6138e7dfd34bfa79f073b7eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccbbafcbed299d374c9e133c61c5c971d60d0d5c8db4637c2d0028725be14bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2679fc707764c45286733417b3584e05369ff9b0d08d7804ca70c64f0c96bbb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f270971ec27391ef000173d4b1981ef11c664b6a6bd96b543d41ab7042bcc30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a34c1832224046ce75de5284249540327d856829b09f74b3e0a4fa98a27089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46490c07d6efdf99eb62032898aa29477cd637b1ea131496567f23e9a584a44f(
    value: typing.Optional[AppEngineFlexibleAppVersionReadinessCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf03490cd409124774919d686e3fbb7bc9c96c9d0115c5b12960c4d3cfaca65(
    *,
    cpu: typing.Optional[jsii.Number] = None,
    disk_gb: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionResourcesVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a4a29d0b2cc0c1962d0ecf159b0457c949768c23f146b1c7d0e9181383c69d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091c6d3351ee1e80f80b99dc5562a578b93b6107c46fa3d45fea406c26cce8fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineFlexibleAppVersionResourcesVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b52215b81eb3639c81e5cfe3dc35867b6469945a151720d68288bd33ee078b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b19da1fb491cfa4bad597adce0815faea7ac7eea8f3f53a2ba4b795226bfce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f9c567314b40c83e9bcc03956a90dab07cfdb8261ebe0bf95d9bd3e49d8152(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202a187b1a90a1f3952428110ba1dfdbdcf9aba33e367758833f18d8371886dd(
    value: typing.Optional[AppEngineFlexibleAppVersionResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336b7c220fe115940c58e133a0b2d01add54108c4c59a77e779d7323dd2d935f(
    *,
    name: builtins.str,
    size_gb: jsii.Number,
    volume_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8068f524bd3dfef3ccc821e29f218e28ffc08a4cbdbb9a9a9f06feea3488aae6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cbcbe0ecf7f47ea49cc495dc1ae514c8e411efb787de9cc72068d3df5304aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5016af623a2ac6f4f1f1a2bc06b80e76949cc362c5fd9e1151b69f47627b30c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34a190144609fdb3e6367793760a21b716a116568024a91ae424f343df844e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3eea630d1f9f949bcef691fb7ecf99796f24d2462ce30b8a3983ed327af1bc6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28593493b66704bee6346920877a61478cf8d2be6c2e8881dfe50101cff07ee9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineFlexibleAppVersionResourcesVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799e05dfda4a1ba73666600a9552e4adf94306b1fa071973692b9130633473b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21b140c1ab474ab7ff5b467f31f5a64a4ed7e3de47daa033d100e22f80539cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1b4fd1cbc2ce53d7fe770df503cb7ec84e318e3072f83de23a75ec2f9c7d13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aaa2ae212a291b5dee3352c157424be854fbafb07d69052e8696c00f773abae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7655adbf738d3d021777e4a65345637a1d231500a5005a159eb3c69c3e185fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionResourcesVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23198e67c6f4a60cf948cf01fa795ddf96d36fc98efbcbc72badde100bf301d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9faf4267dc58b94a385a1caecc9fe2c8c3b9fed087511d3fcee944144411616d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f6effebb728f2d3e77c8a6cd1eaca56bb9203627798d0df796ad0f02a85932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b35c8dcae69d3b1b4c8948b6469afbc641f4247678783c55d81b9ccf60e395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7478fcf681388e7606af9fef86b581158b07619634e84f54c2b00331b00ef495(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d181c8fe3d1cc712fde25591e4fc5fc5ffee2919fd60faf60a9c990768825b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineFlexibleAppVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f32165dae6bfda366452e2c7aad099d37ac658220d757f1e293ffdae84991d(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e4d6d528e55a2405414f973592f8947a9aa1be333eb11768d631e1d44f6de5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff05a6cc15c1fa6b5e9398676f34fb29484765391529644edde2b87381b2a75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c42e8f465c4db3c81db8d327e2c43d61ab0af7f14e969d6332820e85a20a1f(
    value: typing.Optional[AppEngineFlexibleAppVersionVpcAccessConnector],
) -> None:
    """Type checking stubs"""
    pass
