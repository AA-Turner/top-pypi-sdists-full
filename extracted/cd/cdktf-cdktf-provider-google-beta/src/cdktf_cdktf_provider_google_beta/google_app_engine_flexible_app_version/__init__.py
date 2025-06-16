r'''
# `google_app_engine_flexible_app_version`

Refer to the Terraform Registry for docs: [`google_app_engine_flexible_app_version`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version).
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


class GoogleAppEngineFlexibleAppVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version google_app_engine_flexible_app_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        liveness_check: typing.Union["GoogleAppEngineFlexibleAppVersionLivenessCheck", typing.Dict[builtins.str, typing.Any]],
        readiness_check: typing.Union["GoogleAppEngineFlexibleAppVersionReadinessCheck", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        api_config: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionApiConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        automatic_scaling: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        default_expiration: typing.Optional[builtins.str] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoints_api_service: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionEndpointsApiService", typing.Dict[builtins.str, typing.Any]]] = None,
        entrypoint: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        flexible_runtime_settings: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        manual_scaling: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        nobuild_files_regex: typing.Optional[builtins.str] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionResources", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        runtime_channel: typing.Optional[builtins.str] = None,
        runtime_main_executable_path: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        serving_status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version google_app_engine_flexible_app_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param liveness_check: liveness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#liveness_check GoogleAppEngineFlexibleAppVersion#liveness_check}
        :param readiness_check: readiness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#readiness_check GoogleAppEngineFlexibleAppVersion#readiness_check}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime GoogleAppEngineFlexibleAppVersion#runtime}
        :param service: AppEngine service resource. Can contain numbers, letters, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#service GoogleAppEngineFlexibleAppVersion#service}
        :param api_config: api_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#api_config GoogleAppEngineFlexibleAppVersion#api_config}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#automatic_scaling GoogleAppEngineFlexibleAppVersion#automatic_scaling}
        :param beta_settings: Metadata settings that are supplied to this version to enable beta runtime features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#beta_settings GoogleAppEngineFlexibleAppVersion#beta_settings}
        :param default_expiration: Duration that static files should be cached by web proxies and browsers. Only applicable if the corresponding StaticFilesHandler does not specify its own expiration time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#default_expiration GoogleAppEngineFlexibleAppVersion#default_expiration}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#delete_service_on_destroy GoogleAppEngineFlexibleAppVersion#delete_service_on_destroy}
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#deployment GoogleAppEngineFlexibleAppVersion#deployment}
        :param endpoints_api_service: endpoints_api_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#endpoints_api_service GoogleAppEngineFlexibleAppVersion#endpoints_api_service}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#entrypoint GoogleAppEngineFlexibleAppVersion#entrypoint}
        :param env_variables: Environment variables available to the application. As these are not returned in the API request, Terraform will not detect any changes made outside of the Terraform config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#env_variables GoogleAppEngineFlexibleAppVersion#env_variables}
        :param flexible_runtime_settings: flexible_runtime_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#flexible_runtime_settings GoogleAppEngineFlexibleAppVersion#flexible_runtime_settings}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#handlers GoogleAppEngineFlexibleAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#id GoogleAppEngineFlexibleAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#inbound_services GoogleAppEngineFlexibleAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G ManualScaling: B1, B2, B4, B8, B4_1G Defaults to F1 for AutomaticScaling and B1 for ManualScaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_class GoogleAppEngineFlexibleAppVersion#instance_class}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#manual_scaling GoogleAppEngineFlexibleAppVersion#manual_scaling}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#network GoogleAppEngineFlexibleAppVersion#network}
        :param nobuild_files_regex: Files that match this pattern will not be built into this version. Only applicable for Go runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#nobuild_files_regex GoogleAppEngineFlexibleAppVersion#nobuild_files_regex}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#noop_on_destroy GoogleAppEngineFlexibleAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#project GoogleAppEngineFlexibleAppVersion#project}.
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#resources GoogleAppEngineFlexibleAppVersion#resources}
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_api_version GoogleAppEngineFlexibleAppVersion#runtime_api_version}
        :param runtime_channel: The channel of the runtime to use. Only available for some runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_channel GoogleAppEngineFlexibleAppVersion#runtime_channel}
        :param runtime_main_executable_path: The path or name of the app's main executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_main_executable_path GoogleAppEngineFlexibleAppVersion#runtime_main_executable_path}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#service_account GoogleAppEngineFlexibleAppVersion#service_account}
        :param serving_status: Current serving status of this version. Only the versions with a SERVING status create instances and can be billed. Default value: "SERVING" Possible values: ["SERVING", "STOPPED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#serving_status GoogleAppEngineFlexibleAppVersion#serving_status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeouts GoogleAppEngineFlexibleAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#version_id GoogleAppEngineFlexibleAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#vpc_access_connector GoogleAppEngineFlexibleAppVersion#vpc_access_connector}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39d0c4696d5a866dcb8bacfbc4b2116aae0fba5a519d5d0a26e51f26b31c964)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleAppEngineFlexibleAppVersionConfig(
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
        '''Generates CDKTF code for importing a GoogleAppEngineFlexibleAppVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleAppEngineFlexibleAppVersion to import.
        :param import_from_id: The id of the existing GoogleAppEngineFlexibleAppVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleAppEngineFlexibleAppVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9723e7217156c902b806023d58b6e4551227b0ad886829528984ad5bcd7e27e5)
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
        :param script: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script GoogleAppEngineFlexibleAppVersion#script}
        :param auth_fail_action: Action to take when users access resources that require authentication. Default value: "AUTH_FAIL_ACTION_REDIRECT" Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#auth_fail_action GoogleAppEngineFlexibleAppVersion#auth_fail_action}
        :param login: Level of login required to access this resource. Default value: "LOGIN_OPTIONAL" Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#login GoogleAppEngineFlexibleAppVersion#login}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#security_level GoogleAppEngineFlexibleAppVersion#security_level}
        :param url: URL to serve the endpoint at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#url GoogleAppEngineFlexibleAppVersion#url}
        '''
        value = GoogleAppEngineFlexibleAppVersionApiConfig(
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
        cpu_utilization: typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization", typing.Dict[builtins.str, typing.Any]],
        cool_down_period: typing.Optional[builtins.str] = None,
        disk_utilization: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_requests: typing.Optional[jsii.Number] = None,
        max_idle_instances: typing.Optional[jsii.Number] = None,
        max_pending_latency: typing.Optional[builtins.str] = None,
        max_total_instances: typing.Optional[jsii.Number] = None,
        min_idle_instances: typing.Optional[jsii.Number] = None,
        min_pending_latency: typing.Optional[builtins.str] = None,
        min_total_instances: typing.Optional[jsii.Number] = None,
        network_utilization: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        request_utilization: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cpu_utilization GoogleAppEngineFlexibleAppVersion#cpu_utilization}
        :param cool_down_period: The time period that the Autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. Default: 120s Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cool_down_period GoogleAppEngineFlexibleAppVersion#cool_down_period}
        :param disk_utilization: disk_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disk_utilization GoogleAppEngineFlexibleAppVersion#disk_utilization}
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_concurrent_requests GoogleAppEngineFlexibleAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_idle_instances GoogleAppEngineFlexibleAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_pending_latency GoogleAppEngineFlexibleAppVersion#max_pending_latency}
        :param max_total_instances: Maximum number of instances that should be started to handle requests for this version. Default: 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_total_instances GoogleAppEngineFlexibleAppVersion#max_total_instances}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_idle_instances GoogleAppEngineFlexibleAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_pending_latency GoogleAppEngineFlexibleAppVersion#min_pending_latency}
        :param min_total_instances: Minimum number of running instances that should be maintained for this version. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_total_instances GoogleAppEngineFlexibleAppVersion#min_total_instances}
        :param network_utilization: network_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#network_utilization GoogleAppEngineFlexibleAppVersion#network_utilization}
        :param request_utilization: request_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#request_utilization GoogleAppEngineFlexibleAppVersion#request_utilization}
        '''
        value = GoogleAppEngineFlexibleAppVersionAutomaticScaling(
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
        cloud_build_options: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        container: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_build_options: cloud_build_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cloud_build_options GoogleAppEngineFlexibleAppVersion#cloud_build_options}
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#container GoogleAppEngineFlexibleAppVersion#container}
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#files GoogleAppEngineFlexibleAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#zip GoogleAppEngineFlexibleAppVersion#zip}
        '''
        value = GoogleAppEngineFlexibleAppVersionDeployment(
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
        :param name: Endpoints service name which is the name of the "service" resource in the Service Management API. For example "myapi.endpoints.myproject.cloud.goog". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        :param config_id: Endpoints service configuration ID as specified by the Service Management API. For example "2016-09-19r1". By default, the rollout strategy for Endpoints is "FIXED". This means that Endpoints starts up with a particular configuration ID. When a new configuration is rolled out, Endpoints must be given the new configuration ID. The configId field is used to give the configuration ID and is required in this case. Endpoints also has a rollout strategy called "MANAGED". When using this, Endpoints fetches the latest configuration and does not need the configuration ID. In this case, configId must be omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#config_id GoogleAppEngineFlexibleAppVersion#config_id}
        :param disable_trace_sampling: Enable or disable trace sampling. By default, this is set to false for enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disable_trace_sampling GoogleAppEngineFlexibleAppVersion#disable_trace_sampling}
        :param rollout_strategy: Endpoints rollout strategy. If FIXED, configId must be specified. If MANAGED, configId must be omitted. Default value: "FIXED" Possible values: ["FIXED", "MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#rollout_strategy GoogleAppEngineFlexibleAppVersion#rollout_strategy}
        '''
        value = GoogleAppEngineFlexibleAppVersionEndpointsApiService(
            name=name,
            config_id=config_id,
            disable_trace_sampling=disable_trace_sampling,
            rollout_strategy=rollout_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointsApiService", [value]))

    @jsii.member(jsii_name="putEntrypoint")
    def put_entrypoint(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#shell GoogleAppEngineFlexibleAppVersion#shell}
        '''
        value = GoogleAppEngineFlexibleAppVersionEntrypoint(shell=shell)

        return typing.cast(None, jsii.invoke(self, "putEntrypoint", [value]))

    @jsii.member(jsii_name="putFlexibleRuntimeSettings")
    def put_flexible_runtime_settings(
        self,
        *,
        operating_system: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operating_system: Operating System of the application runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#operating_system GoogleAppEngineFlexibleAppVersion#operating_system}
        :param runtime_version: The runtime version of an App Engine flexible application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_version GoogleAppEngineFlexibleAppVersion#runtime_version}
        '''
        value = GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings(
            operating_system=operating_system, runtime_version=runtime_version
        )

        return typing.cast(None, jsii.invoke(self, "putFlexibleRuntimeSettings", [value]))

    @jsii.member(jsii_name="putHandlers")
    def put_handlers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5ab8d02fee4f28189f8924941f740c0c063fc23fae0b2ac5c2520551464045)
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
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        :param check_interval: Interval between health checks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#check_interval GoogleAppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before considering the VM unhealthy. Default: 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#failure_threshold GoogleAppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#host GoogleAppEngineFlexibleAppVersion#host}
        :param initial_delay: The initial delay before starting to execute the checks. Default: "300s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#initial_delay GoogleAppEngineFlexibleAppVersion#initial_delay}
        :param success_threshold: Number of consecutive successful checks required before considering the VM healthy. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#success_threshold GoogleAppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeout GoogleAppEngineFlexibleAppVersion#timeout}
        '''
        value = GoogleAppEngineFlexibleAppVersionLivenessCheck(
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
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instances GoogleAppEngineFlexibleAppVersion#instances}
        '''
        value = GoogleAppEngineFlexibleAppVersionManualScaling(instances=instances)

        return typing.cast(None, jsii.invoke(self, "putManualScaling", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        *,
        name: builtins.str,
        forwarded_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_ip_mode: typing.Optional[builtins.str] = None,
        instance_tag: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Google Compute Engine network where the virtual machines are created. Specify the short name, not the resource path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        :param forwarded_ports: List of ports, or port pairs, to forward from the virtual machine to the application container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#forwarded_ports GoogleAppEngineFlexibleAppVersion#forwarded_ports}
        :param instance_ip_mode: Prevent instances from receiving an ephemeral external IP address. Possible values: ["EXTERNAL", "INTERNAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_ip_mode GoogleAppEngineFlexibleAppVersion#instance_ip_mode}
        :param instance_tag: Tag to apply to the instance during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_tag GoogleAppEngineFlexibleAppVersion#instance_tag}
        :param session_affinity: Enable session affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#session_affinity GoogleAppEngineFlexibleAppVersion#session_affinity}
        :param subnetwork: Google Cloud Platform sub-network where the virtual machines are created. Specify the short name, not the resource path. If the network that the instance is being created in is a Legacy network, then the IP address is allocated from the IPv4Range. If the network that the instance is being created in is an auto Subnet Mode Network, then only network name should be specified (not the subnetworkName) and the IP address is created from the IPCidrRange of the subnetwork that exists in that zone for that network. If the network that the instance is being created in is a custom Subnet Mode Network, then the subnetworkName must be specified and the IP address is created from the IPCidrRange of the subnetwork. If specified, the subnetwork must exist in the same region as the App Engine flexible environment application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#subnetwork GoogleAppEngineFlexibleAppVersion#subnetwork}
        '''
        value = GoogleAppEngineFlexibleAppVersionNetwork(
            name=name,
            forwarded_ports=forwarded_ports,
            instance_ip_mode=instance_ip_mode,
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
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        :param app_start_timeout: A maximum time limit on application initialization, measured from moment the application successfully replies to a healthcheck until it is ready to serve traffic. Default: "300s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#app_start_timeout GoogleAppEngineFlexibleAppVersion#app_start_timeout}
        :param check_interval: Interval between health checks. Default: "5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#check_interval GoogleAppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before removing traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#failure_threshold GoogleAppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#host GoogleAppEngineFlexibleAppVersion#host}
        :param success_threshold: Number of consecutive successful checks required before receiving traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#success_threshold GoogleAppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeout GoogleAppEngineFlexibleAppVersion#timeout}
        '''
        value = GoogleAppEngineFlexibleAppVersionReadinessCheck(
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
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionResourcesVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cpu: Number of CPU cores needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cpu GoogleAppEngineFlexibleAppVersion#cpu}
        :param disk_gb: Disk size (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disk_gb GoogleAppEngineFlexibleAppVersion#disk_gb}
        :param memory_gb: Memory (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#memory_gb GoogleAppEngineFlexibleAppVersion#memory_gb}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#volumes GoogleAppEngineFlexibleAppVersion#volumes}
        '''
        value = GoogleAppEngineFlexibleAppVersionResources(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#create GoogleAppEngineFlexibleAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#delete GoogleAppEngineFlexibleAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#update GoogleAppEngineFlexibleAppVersion#update}.
        '''
        value = GoogleAppEngineFlexibleAppVersionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcAccessConnector")
    def put_vpc_access_connector(self, *, name: builtins.str) -> None:
        '''
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        '''
        value = GoogleAppEngineFlexibleAppVersionVpcAccessConnector(name=name)

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
    def api_config(self) -> "GoogleAppEngineFlexibleAppVersionApiConfigOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionApiConfigOutputReference", jsii.get(self, "apiConfig"))

    @builtins.property
    @jsii.member(jsii_name="automaticScaling")
    def automatic_scaling(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionAutomaticScalingOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionAutomaticScalingOutputReference", jsii.get(self, "automaticScaling"))

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionDeploymentOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionDeploymentOutputReference", jsii.get(self, "deployment"))

    @builtins.property
    @jsii.member(jsii_name="endpointsApiService")
    def endpoints_api_service(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionEndpointsApiServiceOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionEndpointsApiServiceOutputReference", jsii.get(self, "endpointsApiService"))

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionEntrypointOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionEntrypointOutputReference", jsii.get(self, "entrypoint"))

    @builtins.property
    @jsii.member(jsii_name="flexibleRuntimeSettings")
    def flexible_runtime_settings(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference", jsii.get(self, "flexibleRuntimeSettings"))

    @builtins.property
    @jsii.member(jsii_name="handlers")
    def handlers(self) -> "GoogleAppEngineFlexibleAppVersionHandlersList":
        return typing.cast("GoogleAppEngineFlexibleAppVersionHandlersList", jsii.get(self, "handlers"))

    @builtins.property
    @jsii.member(jsii_name="livenessCheck")
    def liveness_check(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionLivenessCheckOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionLivenessCheckOutputReference", jsii.get(self, "livenessCheck"))

    @builtins.property
    @jsii.member(jsii_name="manualScaling")
    def manual_scaling(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionManualScalingOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionManualScalingOutputReference", jsii.get(self, "manualScaling"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "GoogleAppEngineFlexibleAppVersionNetworkOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="readinessCheck")
    def readiness_check(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionReadinessCheckOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionReadinessCheckOutputReference", jsii.get(self, "readinessCheck"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "GoogleAppEngineFlexibleAppVersionResourcesOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleAppEngineFlexibleAppVersionTimeoutsOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnector")
    def vpc_access_connector(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionVpcAccessConnectorOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionVpcAccessConnectorOutputReference", jsii.get(self, "vpcAccessConnector"))

    @builtins.property
    @jsii.member(jsii_name="apiConfigInput")
    def api_config_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionApiConfig"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionApiConfig"], jsii.get(self, "apiConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticScalingInput")
    def automatic_scaling_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScaling"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScaling"], jsii.get(self, "automaticScalingInput"))

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
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionDeployment"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionDeployment"], jsii.get(self, "deploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsApiServiceInput")
    def endpoints_api_service_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionEndpointsApiService"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionEndpointsApiService"], jsii.get(self, "endpointsApiServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="entrypointInput")
    def entrypoint_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionEntrypoint"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionEntrypoint"], jsii.get(self, "entrypointInput"))

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
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings"], jsii.get(self, "flexibleRuntimeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="handlersInput")
    def handlers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionHandlers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionHandlers"]]], jsii.get(self, "handlersInput"))

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
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionLivenessCheck"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionLivenessCheck"], jsii.get(self, "livenessCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="manualScalingInput")
    def manual_scaling_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionManualScaling"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionManualScaling"], jsii.get(self, "manualScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionNetwork"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionNetwork"], jsii.get(self, "networkInput"))

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
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionReadinessCheck"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionReadinessCheck"], jsii.get(self, "readinessCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionResources"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionResources"], jsii.get(self, "resourcesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAppEngineFlexibleAppVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAppEngineFlexibleAppVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionIdInput")
    def version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnectorInput")
    def vpc_access_connector_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionVpcAccessConnector"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionVpcAccessConnector"], jsii.get(self, "vpcAccessConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="betaSettings")
    def beta_settings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "betaSettings"))

    @beta_settings.setter
    def beta_settings(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bba4932ea51688eeb51f873771bba7aed5d18f262ee4d0d7692fe4c309cbf45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "betaSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultExpiration")
    def default_expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultExpiration"))

    @default_expiration.setter
    def default_expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f564f79c5bacb31970886fb54267181c9a495594e042c295810da6a22dd26f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed5cb37b5b9b5f105ba273ae35c05029f198b5c5e1fdfd050d12f331a731245f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteServiceOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envVariables")
    def env_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "envVariables"))

    @env_variables.setter
    def env_variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbbb235b8c6c05cd31c473d4522b686f89386221b798ee6870aff4c28781b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bade06fc724aa62e438af77f9b6ab754fb06be949651b1ca01b02609228278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundServices")
    def inbound_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inboundServices"))

    @inbound_services.setter
    def inbound_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3798850755556f5cef875cee0534604ca09b50ebba04c88111db762c3d973b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceClass")
    def instance_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceClass"))

    @instance_class.setter
    def instance_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec721cd624f688ef8317b355700003e7a492bd77799f530b11b72b46d3c73cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nobuildFilesRegex")
    def nobuild_files_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nobuildFilesRegex"))

    @nobuild_files_regex.setter
    def nobuild_files_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56130e1f9bb942eb2a19943b70519049c3ad785d6d13e06c9bb6a90b087aef41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f9fab893734b79c8dca848d9e6e718b24ee4f680ffd0de2209699d77b0a7392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noopOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c1fbd79e1104926ccfff6b6204e8de3eb3a3e989a50d9d1164c9773e3a3a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce80908d444e58f5490d588914d4bae5ec8238d2a0e8e392487a142e8595f9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeApiVersion")
    def runtime_api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeApiVersion"))

    @runtime_api_version.setter
    def runtime_api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122720b5252aa55dbe9307977d1fe08d9ca276078993abe1287fba17785b777a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeChannel")
    def runtime_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeChannel"))

    @runtime_channel.setter
    def runtime_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d417f9489b8a13710e0820a456bb64b846135acbac4e3f567a8f191e75b73e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeMainExecutablePath")
    def runtime_main_executable_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeMainExecutablePath"))

    @runtime_main_executable_path.setter
    def runtime_main_executable_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6df1838ab801486ab7313dd3a67bd550650383baccad00cfb0fb63a1235630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeMainExecutablePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49a68e30f8254c407b80b1771e594ae81f340637837cca603759de02abbae12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a176c9425b02ac1879024003072b98b2219f78bd4fe0894a6b6313d4ec95f9b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servingStatus")
    def serving_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servingStatus"))

    @serving_status.setter
    def serving_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a26e3be121d76558c233839fe0bc117b814ed6ce538559e14c3a1dbd5f79db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servingStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d71b32f80615d1a3b9b9475bd380756faabf5c490a51fbd8ae3c5bd59f9001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionApiConfig",
    jsii_struct_bases=[],
    name_mapping={
        "script": "script",
        "auth_fail_action": "authFailAction",
        "login": "login",
        "security_level": "securityLevel",
        "url": "url",
    },
)
class GoogleAppEngineFlexibleAppVersionApiConfig:
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
        :param script: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script GoogleAppEngineFlexibleAppVersion#script}
        :param auth_fail_action: Action to take when users access resources that require authentication. Default value: "AUTH_FAIL_ACTION_REDIRECT" Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#auth_fail_action GoogleAppEngineFlexibleAppVersion#auth_fail_action}
        :param login: Level of login required to access this resource. Default value: "LOGIN_OPTIONAL" Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#login GoogleAppEngineFlexibleAppVersion#login}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#security_level GoogleAppEngineFlexibleAppVersion#security_level}
        :param url: URL to serve the endpoint at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#url GoogleAppEngineFlexibleAppVersion#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f76cafcf9a26e5cae0bef668fdd1817354a3d06150f22dcb4b0862502e570e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script GoogleAppEngineFlexibleAppVersion#script}
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_fail_action(self) -> typing.Optional[builtins.str]:
        '''Action to take when users access resources that require authentication. Default value: "AUTH_FAIL_ACTION_REDIRECT" Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#auth_fail_action GoogleAppEngineFlexibleAppVersion#auth_fail_action}
        '''
        result = self._values.get("auth_fail_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login(self) -> typing.Optional[builtins.str]:
        '''Level of login required to access this resource. Default value: "LOGIN_OPTIONAL" Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#login GoogleAppEngineFlexibleAppVersion#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#security_level GoogleAppEngineFlexibleAppVersion#security_level}
        '''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''URL to serve the endpoint at.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#url GoogleAppEngineFlexibleAppVersion#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionApiConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionApiConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionApiConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5976f435131d3d6adea3caeea117d0292dd461e52fe5bb6642128632d76c65c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1a0a5b2506b679c79c4d17998a967a2e66e974c68ef3e60d8f23cafa398e7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authFailAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "login"))

    @login.setter
    def login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc61d807b1fb633a98940dc70870d1e656697cc164c18ee4416670ea3844583f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "login", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f591455e75c06ca31d6e1bfb23c08675f94e3767a848b90152924e7ddff4889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @security_level.setter
    def security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41173b19f51698e2f24cab89e60da9671b8f6186cfa5e9064bd0b06c786c9b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d3bf84808966ec83b56f406859e6d6586ce0153b7594f0fedec26c68beceed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionApiConfig]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionApiConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionApiConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0453e574addd32f993b867e19a46935f3b3fd11a9e88713d25322dfac14c1a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScaling",
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
class GoogleAppEngineFlexibleAppVersionAutomaticScaling:
    def __init__(
        self,
        *,
        cpu_utilization: typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization", typing.Dict[builtins.str, typing.Any]],
        cool_down_period: typing.Optional[builtins.str] = None,
        disk_utilization: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_requests: typing.Optional[jsii.Number] = None,
        max_idle_instances: typing.Optional[jsii.Number] = None,
        max_pending_latency: typing.Optional[builtins.str] = None,
        max_total_instances: typing.Optional[jsii.Number] = None,
        min_idle_instances: typing.Optional[jsii.Number] = None,
        min_pending_latency: typing.Optional[builtins.str] = None,
        min_total_instances: typing.Optional[jsii.Number] = None,
        network_utilization: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        request_utilization: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cpu_utilization GoogleAppEngineFlexibleAppVersion#cpu_utilization}
        :param cool_down_period: The time period that the Autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. Default: 120s Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cool_down_period GoogleAppEngineFlexibleAppVersion#cool_down_period}
        :param disk_utilization: disk_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disk_utilization GoogleAppEngineFlexibleAppVersion#disk_utilization}
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_concurrent_requests GoogleAppEngineFlexibleAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_idle_instances GoogleAppEngineFlexibleAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_pending_latency GoogleAppEngineFlexibleAppVersion#max_pending_latency}
        :param max_total_instances: Maximum number of instances that should be started to handle requests for this version. Default: 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_total_instances GoogleAppEngineFlexibleAppVersion#max_total_instances}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_idle_instances GoogleAppEngineFlexibleAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_pending_latency GoogleAppEngineFlexibleAppVersion#min_pending_latency}
        :param min_total_instances: Minimum number of running instances that should be maintained for this version. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_total_instances GoogleAppEngineFlexibleAppVersion#min_total_instances}
        :param network_utilization: network_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#network_utilization GoogleAppEngineFlexibleAppVersion#network_utilization}
        :param request_utilization: request_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#request_utilization GoogleAppEngineFlexibleAppVersion#request_utilization}
        '''
        if isinstance(cpu_utilization, dict):
            cpu_utilization = GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization(**cpu_utilization)
        if isinstance(disk_utilization, dict):
            disk_utilization = GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization(**disk_utilization)
        if isinstance(network_utilization, dict):
            network_utilization = GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization(**network_utilization)
        if isinstance(request_utilization, dict):
            request_utilization = GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization(**request_utilization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b985d564dc4e8b7b9d8b1422305166c5083c08a29789f81e703e5a6691da96b0)
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
    ) -> "GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization":
        '''cpu_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cpu_utilization GoogleAppEngineFlexibleAppVersion#cpu_utilization}
        '''
        result = self._values.get("cpu_utilization")
        assert result is not None, "Required property 'cpu_utilization' is missing"
        return typing.cast("GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization", result)

    @builtins.property
    def cool_down_period(self) -> typing.Optional[builtins.str]:
        '''The time period that the Autoscaler should wait before it starts collecting information from a new instance.

        This prevents the autoscaler from collecting information when the instance is initializing,
        during which the collected usage would not be reliable. Default: 120s

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cool_down_period GoogleAppEngineFlexibleAppVersion#cool_down_period}
        '''
        result = self._values.get("cool_down_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_utilization(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization"]:
        '''disk_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disk_utilization GoogleAppEngineFlexibleAppVersion#disk_utilization}
        '''
        result = self._values.get("disk_utilization")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization"], result)

    @builtins.property
    def max_concurrent_requests(self) -> typing.Optional[jsii.Number]:
        '''Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance.

        Defaults to a runtime-specific value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_concurrent_requests GoogleAppEngineFlexibleAppVersion#max_concurrent_requests}
        '''
        result = self._values.get("max_concurrent_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle instances that should be maintained for this version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_idle_instances GoogleAppEngineFlexibleAppVersion#max_idle_instances}
        '''
        result = self._values.get("max_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_pending_latency GoogleAppEngineFlexibleAppVersion#max_pending_latency}
        '''
        result = self._values.get("max_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_total_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of instances that should be started to handle requests for this version. Default: 20.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#max_total_instances GoogleAppEngineFlexibleAppVersion#max_total_instances}
        '''
        result = self._values.get("max_total_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of idle instances that should be maintained for this version.

        Only applicable for the default version of a service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_idle_instances GoogleAppEngineFlexibleAppVersion#min_idle_instances}
        '''
        result = self._values.get("min_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_pending_latency GoogleAppEngineFlexibleAppVersion#min_pending_latency}
        '''
        result = self._values.get("min_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_total_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of running instances that should be maintained for this version. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#min_total_instances GoogleAppEngineFlexibleAppVersion#min_total_instances}
        '''
        result = self._values.get("min_total_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_utilization(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization"]:
        '''network_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#network_utilization GoogleAppEngineFlexibleAppVersion#network_utilization}
        '''
        result = self._values.get("network_utilization")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization"], result)

    @builtins.property
    def request_utilization(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"]:
        '''request_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#request_utilization GoogleAppEngineFlexibleAppVersion#request_utilization}
        '''
        result = self._values.get("request_utilization")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionAutomaticScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_utilization": "targetUtilization",
        "aggregation_window_length": "aggregationWindowLength",
    },
)
class GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization:
    def __init__(
        self,
        *,
        target_utilization: jsii.Number,
        aggregation_window_length: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_utilization: Target CPU utilization ratio to maintain when scaling. Must be between 0 and 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_utilization GoogleAppEngineFlexibleAppVersion#target_utilization}
        :param aggregation_window_length: Period of time over which CPU utilization is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#aggregation_window_length GoogleAppEngineFlexibleAppVersion#aggregation_window_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14470f1b001c3130ae62f49ae3171aa86927334e92c838eef1038fbfba79367)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_utilization GoogleAppEngineFlexibleAppVersion#target_utilization}
        '''
        result = self._values.get("target_utilization")
        assert result is not None, "Required property 'target_utilization' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def aggregation_window_length(self) -> typing.Optional[builtins.str]:
        '''Period of time over which CPU utilization is calculated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#aggregation_window_length GoogleAppEngineFlexibleAppVersion#aggregation_window_length}
        '''
        result = self._values.get("aggregation_window_length")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b522c72a17cbf9097abc4629b9b5c572bf0fad30f6dad0b828068af606e72ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0590b61246b21a615ba429ba6cdd3a33cd7872c0a6ab4aa5d8f6ecdd0088e199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationWindowLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetUtilization")
    def target_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetUtilization"))

    @target_utilization.setter
    def target_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9610ddb1f8e2b9cfbfe25ecd683075077a37dc183dc895998ee96b163c7170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41fc8b497af0f4738b1887d0860af246460e8aea51c4895f84cfa78e86b0d6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_read_bytes_per_second": "targetReadBytesPerSecond",
        "target_read_ops_per_second": "targetReadOpsPerSecond",
        "target_write_bytes_per_second": "targetWriteBytesPerSecond",
        "target_write_ops_per_second": "targetWriteOpsPerSecond",
    },
)
class GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization:
    def __init__(
        self,
        *,
        target_read_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_read_ops_per_second: typing.Optional[jsii.Number] = None,
        target_write_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_write_ops_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_read_bytes_per_second: Target bytes read per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_read_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_read_bytes_per_second}
        :param target_read_ops_per_second: Target ops read per seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_read_ops_per_second GoogleAppEngineFlexibleAppVersion#target_read_ops_per_second}
        :param target_write_bytes_per_second: Target bytes written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_write_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_write_bytes_per_second}
        :param target_write_ops_per_second: Target ops written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_write_ops_per_second GoogleAppEngineFlexibleAppVersion#target_write_ops_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032867d97978fad13840e98f4a5ec1634ad82dc400cc45cd1a14c647e553a700)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_read_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_read_bytes_per_second}
        '''
        result = self._values.get("target_read_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_read_ops_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target ops read per seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_read_ops_per_second GoogleAppEngineFlexibleAppVersion#target_read_ops_per_second}
        '''
        result = self._values.get("target_read_ops_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_write_bytes_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target bytes written per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_write_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_write_bytes_per_second}
        '''
        result = self._values.get("target_write_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_write_ops_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target ops written per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_write_ops_per_second GoogleAppEngineFlexibleAppVersion#target_write_ops_per_second}
        '''
        result = self._values.get("target_write_ops_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c59f7b4dbbaa3cb4e566377372a2169d8d4bf251f31da30651c2b8f953228a96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__065fb2adbfa876675d32627b255775d263bb73aac244b83c42c4ed153615c8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReadBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetReadOpsPerSecond")
    def target_read_ops_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReadOpsPerSecond"))

    @target_read_ops_per_second.setter
    def target_read_ops_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc02b3136d509bf27e435381447862b529a62642ab7706a4c15ee077720ea5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReadOpsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetWriteBytesPerSecond")
    def target_write_bytes_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetWriteBytesPerSecond"))

    @target_write_bytes_per_second.setter
    def target_write_bytes_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8528a433db6b592e7a2e9391205dfce2198b8ba65fc4d49db4f7335d89b0927e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetWriteBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetWriteOpsPerSecond")
    def target_write_ops_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetWriteOpsPerSecond"))

    @target_write_ops_per_second.setter
    def target_write_ops_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c240a65ce2f32af9e81564f0d3f2e097c88cffa4847c9b42e519b6d89cc6c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetWriteOpsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61450b64e99a420030f5aae3f60f9f48e840aee2efea7ee9fed2564fe1734077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_received_bytes_per_second": "targetReceivedBytesPerSecond",
        "target_received_packets_per_second": "targetReceivedPacketsPerSecond",
        "target_sent_bytes_per_second": "targetSentBytesPerSecond",
        "target_sent_packets_per_second": "targetSentPacketsPerSecond",
    },
)
class GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization:
    def __init__(
        self,
        *,
        target_received_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_received_packets_per_second: typing.Optional[jsii.Number] = None,
        target_sent_bytes_per_second: typing.Optional[jsii.Number] = None,
        target_sent_packets_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_received_bytes_per_second: Target bytes received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_received_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_received_bytes_per_second}
        :param target_received_packets_per_second: Target packets received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_received_packets_per_second GoogleAppEngineFlexibleAppVersion#target_received_packets_per_second}
        :param target_sent_bytes_per_second: Target bytes sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_sent_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_sent_bytes_per_second}
        :param target_sent_packets_per_second: Target packets sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_sent_packets_per_second GoogleAppEngineFlexibleAppVersion#target_sent_packets_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec826b8b024f270411c8530001e5fa80a984e67f568e7cecfb0da1b209efe19)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_received_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_received_bytes_per_second}
        '''
        result = self._values.get("target_received_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_received_packets_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target packets received per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_received_packets_per_second GoogleAppEngineFlexibleAppVersion#target_received_packets_per_second}
        '''
        result = self._values.get("target_received_packets_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_sent_bytes_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target bytes sent per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_sent_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_sent_bytes_per_second}
        '''
        result = self._values.get("target_sent_bytes_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_sent_packets_per_second(self) -> typing.Optional[jsii.Number]:
        '''Target packets sent per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_sent_packets_per_second GoogleAppEngineFlexibleAppVersion#target_sent_packets_per_second}
        '''
        result = self._values.get("target_sent_packets_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59aca59f956798f46f7230751d46b76f8dad3e8a2855fd46d83fb12dec87dc40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c60b7831d3a26080dbe03adb8917e8ee5467090751918c9250033b1043b4c4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReceivedBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetReceivedPacketsPerSecond")
    def target_received_packets_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReceivedPacketsPerSecond"))

    @target_received_packets_per_second.setter
    def target_received_packets_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a242803b3534fc6ee8b6a9b7494430e283e0049083ad10e707cdb0f56a971b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetReceivedPacketsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSentBytesPerSecond")
    def target_sent_bytes_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSentBytesPerSecond"))

    @target_sent_bytes_per_second.setter
    def target_sent_bytes_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6e41ae868451d95cb093ca2fc10e47ee31eb7a35f070476122abd414dc0983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSentBytesPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetSentPacketsPerSecond")
    def target_sent_packets_per_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetSentPacketsPerSecond"))

    @target_sent_packets_per_second.setter
    def target_sent_packets_per_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec412ae7f0431139defceec5e47e059215639ca7aef8f5219f02df84000cfb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSentPacketsPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb6608181593e4e3702c80b82cbbb1add24de508b935311e9a28e37a0d86e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineFlexibleAppVersionAutomaticScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__407b3691f96a7779517badcb3f2fcbc44ba171ebc9fb834955822d025c6fbfff)
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
        :param target_utilization: Target CPU utilization ratio to maintain when scaling. Must be between 0 and 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_utilization GoogleAppEngineFlexibleAppVersion#target_utilization}
        :param aggregation_window_length: Period of time over which CPU utilization is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#aggregation_window_length GoogleAppEngineFlexibleAppVersion#aggregation_window_length}
        '''
        value = GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization(
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
        :param target_read_bytes_per_second: Target bytes read per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_read_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_read_bytes_per_second}
        :param target_read_ops_per_second: Target ops read per seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_read_ops_per_second GoogleAppEngineFlexibleAppVersion#target_read_ops_per_second}
        :param target_write_bytes_per_second: Target bytes written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_write_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_write_bytes_per_second}
        :param target_write_ops_per_second: Target ops written per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_write_ops_per_second GoogleAppEngineFlexibleAppVersion#target_write_ops_per_second}
        '''
        value = GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization(
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
        :param target_received_bytes_per_second: Target bytes received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_received_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_received_bytes_per_second}
        :param target_received_packets_per_second: Target packets received per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_received_packets_per_second GoogleAppEngineFlexibleAppVersion#target_received_packets_per_second}
        :param target_sent_bytes_per_second: Target bytes sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_sent_bytes_per_second GoogleAppEngineFlexibleAppVersion#target_sent_bytes_per_second}
        :param target_sent_packets_per_second: Target packets sent per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_sent_packets_per_second GoogleAppEngineFlexibleAppVersion#target_sent_packets_per_second}
        '''
        value = GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization(
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
        :param target_concurrent_requests: Target number of concurrent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_concurrent_requests GoogleAppEngineFlexibleAppVersion#target_concurrent_requests}
        :param target_request_count_per_second: Target requests per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_request_count_per_second GoogleAppEngineFlexibleAppVersion#target_request_count_per_second}
        '''
        value = GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization(
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
    ) -> GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference:
        return typing.cast(GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference, jsii.get(self, "cpuUtilization"))

    @builtins.property
    @jsii.member(jsii_name="diskUtilization")
    def disk_utilization(
        self,
    ) -> GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference:
        return typing.cast(GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference, jsii.get(self, "diskUtilization"))

    @builtins.property
    @jsii.member(jsii_name="networkUtilization")
    def network_utilization(
        self,
    ) -> GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference:
        return typing.cast(GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference, jsii.get(self, "networkUtilization"))

    @builtins.property
    @jsii.member(jsii_name="requestUtilization")
    def request_utilization(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference", jsii.get(self, "requestUtilization"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriodInput")
    def cool_down_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coolDownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationInput")
    def cpu_utilization_input(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization], jsii.get(self, "cpuUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="diskUtilizationInput")
    def disk_utilization_input(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization], jsii.get(self, "diskUtilizationInput"))

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
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization], jsii.get(self, "networkUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUtilizationInput")
    def request_utilization_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization"], jsii.get(self, "requestUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriod")
    def cool_down_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coolDownPeriod"))

    @cool_down_period.setter
    def cool_down_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6800cbf738045625d061b45ab23e70f1cc338618d332e64a9c5f93af9fff102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRequests")
    def max_concurrent_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentRequests"))

    @max_concurrent_requests.setter
    def max_concurrent_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4ffa52567e43082817ead8928914c311506153cf2be5a63d504444d623fb3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIdleInstances")
    def max_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleInstances"))

    @max_idle_instances.setter
    def max_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316d701ccb9921e26e5eafe5d846d15b3be35c4962a3ce15c9270f569008a419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingLatency")
    def max_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxPendingLatency"))

    @max_pending_latency.setter
    def max_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f610cb9af4075e9f855b4c6af3156d1db3871ea8ca60daa543fec9a3e5427858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTotalInstances")
    def max_total_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTotalInstances"))

    @max_total_instances.setter
    def max_total_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b324df0e550d76a818657fdf19dfa09b9db5c4ac6b51d4841c95121a9c7cf89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTotalInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minIdleInstances")
    def min_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minIdleInstances"))

    @min_idle_instances.setter
    def min_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f20a7864b159f51fb5a802843c5dcd064a444ddc0910a9be7d71bcb4034fae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minPendingLatency")
    def min_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minPendingLatency"))

    @min_pending_latency.setter
    def min_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b235165c060c1b8deb7c0a0242c7a4457e95e0a99a5706861ec766adc4625de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTotalInstances")
    def min_total_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minTotalInstances"))

    @min_total_instances.setter
    def min_total_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465cce2b7d929f7933fef159b529d2dfb9fdfedc18bbe75d64f3f0eb376f4aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTotalInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScaling]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94878956e37eb684dbdf8fc50b8b02bd03e19d84bbf7aef9bd8bf61b9eda850c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization",
    jsii_struct_bases=[],
    name_mapping={
        "target_concurrent_requests": "targetConcurrentRequests",
        "target_request_count_per_second": "targetRequestCountPerSecond",
    },
)
class GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization:
    def __init__(
        self,
        *,
        target_concurrent_requests: typing.Optional[jsii.Number] = None,
        target_request_count_per_second: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_concurrent_requests: Target number of concurrent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_concurrent_requests GoogleAppEngineFlexibleAppVersion#target_concurrent_requests}
        :param target_request_count_per_second: Target requests per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_request_count_per_second GoogleAppEngineFlexibleAppVersion#target_request_count_per_second}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba555b0506e67bb74c1e55b384ac25f3bb983ea5fbc84817a8b6cb51fc81257)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_concurrent_requests GoogleAppEngineFlexibleAppVersion#target_concurrent_requests}
        '''
        result = self._values.get("target_concurrent_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_request_count_per_second(self) -> typing.Optional[builtins.str]:
        '''Target requests per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#target_request_count_per_second GoogleAppEngineFlexibleAppVersion#target_request_count_per_second}
        '''
        result = self._values.get("target_request_count_per_second")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed3092507c6987380458c4bc9d0d4fa3b19f21524d1cfe36cce95ae2134915db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83bfa6aa5c602eb2f8d85e81d98179a3cfdfee057e661e81be86df132ab26815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetConcurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRequestCountPerSecond")
    def target_request_count_per_second(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRequestCountPerSecond"))

    @target_request_count_per_second.setter
    def target_request_count_per_second(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b50f66ee392d6b300f21e20fe8e70b50d6ddb1e1ce4db20aa49ee181e4993b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRequestCountPerSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815a6eecd70f2f6af7d9247de9cb6c1f1d1512bebaaa6719544cb925eac0bee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionConfig",
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
class GoogleAppEngineFlexibleAppVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        liveness_check: typing.Union["GoogleAppEngineFlexibleAppVersionLivenessCheck", typing.Dict[builtins.str, typing.Any]],
        readiness_check: typing.Union["GoogleAppEngineFlexibleAppVersionReadinessCheck", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        api_config: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionApiConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        automatic_scaling: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        default_expiration: typing.Optional[builtins.str] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoints_api_service: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionEndpointsApiService", typing.Dict[builtins.str, typing.Any]]] = None,
        entrypoint: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        flexible_runtime_settings: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        manual_scaling: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        nobuild_files_regex: typing.Optional[builtins.str] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionResources", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        runtime_channel: typing.Optional[builtins.str] = None,
        runtime_main_executable_path: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        serving_status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param liveness_check: liveness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#liveness_check GoogleAppEngineFlexibleAppVersion#liveness_check}
        :param readiness_check: readiness_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#readiness_check GoogleAppEngineFlexibleAppVersion#readiness_check}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime GoogleAppEngineFlexibleAppVersion#runtime}
        :param service: AppEngine service resource. Can contain numbers, letters, and hyphens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#service GoogleAppEngineFlexibleAppVersion#service}
        :param api_config: api_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#api_config GoogleAppEngineFlexibleAppVersion#api_config}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#automatic_scaling GoogleAppEngineFlexibleAppVersion#automatic_scaling}
        :param beta_settings: Metadata settings that are supplied to this version to enable beta runtime features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#beta_settings GoogleAppEngineFlexibleAppVersion#beta_settings}
        :param default_expiration: Duration that static files should be cached by web proxies and browsers. Only applicable if the corresponding StaticFilesHandler does not specify its own expiration time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#default_expiration GoogleAppEngineFlexibleAppVersion#default_expiration}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#delete_service_on_destroy GoogleAppEngineFlexibleAppVersion#delete_service_on_destroy}
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#deployment GoogleAppEngineFlexibleAppVersion#deployment}
        :param endpoints_api_service: endpoints_api_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#endpoints_api_service GoogleAppEngineFlexibleAppVersion#endpoints_api_service}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#entrypoint GoogleAppEngineFlexibleAppVersion#entrypoint}
        :param env_variables: Environment variables available to the application. As these are not returned in the API request, Terraform will not detect any changes made outside of the Terraform config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#env_variables GoogleAppEngineFlexibleAppVersion#env_variables}
        :param flexible_runtime_settings: flexible_runtime_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#flexible_runtime_settings GoogleAppEngineFlexibleAppVersion#flexible_runtime_settings}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#handlers GoogleAppEngineFlexibleAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#id GoogleAppEngineFlexibleAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#inbound_services GoogleAppEngineFlexibleAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G ManualScaling: B1, B2, B4, B8, B4_1G Defaults to F1 for AutomaticScaling and B1 for ManualScaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_class GoogleAppEngineFlexibleAppVersion#instance_class}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#manual_scaling GoogleAppEngineFlexibleAppVersion#manual_scaling}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#network GoogleAppEngineFlexibleAppVersion#network}
        :param nobuild_files_regex: Files that match this pattern will not be built into this version. Only applicable for Go runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#nobuild_files_regex GoogleAppEngineFlexibleAppVersion#nobuild_files_regex}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#noop_on_destroy GoogleAppEngineFlexibleAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#project GoogleAppEngineFlexibleAppVersion#project}.
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#resources GoogleAppEngineFlexibleAppVersion#resources}
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_api_version GoogleAppEngineFlexibleAppVersion#runtime_api_version}
        :param runtime_channel: The channel of the runtime to use. Only available for some runtimes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_channel GoogleAppEngineFlexibleAppVersion#runtime_channel}
        :param runtime_main_executable_path: The path or name of the app's main executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_main_executable_path GoogleAppEngineFlexibleAppVersion#runtime_main_executable_path}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#service_account GoogleAppEngineFlexibleAppVersion#service_account}
        :param serving_status: Current serving status of this version. Only the versions with a SERVING status create instances and can be billed. Default value: "SERVING" Possible values: ["SERVING", "STOPPED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#serving_status GoogleAppEngineFlexibleAppVersion#serving_status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeouts GoogleAppEngineFlexibleAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#version_id GoogleAppEngineFlexibleAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#vpc_access_connector GoogleAppEngineFlexibleAppVersion#vpc_access_connector}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(liveness_check, dict):
            liveness_check = GoogleAppEngineFlexibleAppVersionLivenessCheck(**liveness_check)
        if isinstance(readiness_check, dict):
            readiness_check = GoogleAppEngineFlexibleAppVersionReadinessCheck(**readiness_check)
        if isinstance(api_config, dict):
            api_config = GoogleAppEngineFlexibleAppVersionApiConfig(**api_config)
        if isinstance(automatic_scaling, dict):
            automatic_scaling = GoogleAppEngineFlexibleAppVersionAutomaticScaling(**automatic_scaling)
        if isinstance(deployment, dict):
            deployment = GoogleAppEngineFlexibleAppVersionDeployment(**deployment)
        if isinstance(endpoints_api_service, dict):
            endpoints_api_service = GoogleAppEngineFlexibleAppVersionEndpointsApiService(**endpoints_api_service)
        if isinstance(entrypoint, dict):
            entrypoint = GoogleAppEngineFlexibleAppVersionEntrypoint(**entrypoint)
        if isinstance(flexible_runtime_settings, dict):
            flexible_runtime_settings = GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings(**flexible_runtime_settings)
        if isinstance(manual_scaling, dict):
            manual_scaling = GoogleAppEngineFlexibleAppVersionManualScaling(**manual_scaling)
        if isinstance(network, dict):
            network = GoogleAppEngineFlexibleAppVersionNetwork(**network)
        if isinstance(resources, dict):
            resources = GoogleAppEngineFlexibleAppVersionResources(**resources)
        if isinstance(timeouts, dict):
            timeouts = GoogleAppEngineFlexibleAppVersionTimeouts(**timeouts)
        if isinstance(vpc_access_connector, dict):
            vpc_access_connector = GoogleAppEngineFlexibleAppVersionVpcAccessConnector(**vpc_access_connector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b81a57febdaaaa747dbba7963f12f7dca4767b1455ca959f554492756652db)
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
    def liveness_check(self) -> "GoogleAppEngineFlexibleAppVersionLivenessCheck":
        '''liveness_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#liveness_check GoogleAppEngineFlexibleAppVersion#liveness_check}
        '''
        result = self._values.get("liveness_check")
        assert result is not None, "Required property 'liveness_check' is missing"
        return typing.cast("GoogleAppEngineFlexibleAppVersionLivenessCheck", result)

    @builtins.property
    def readiness_check(self) -> "GoogleAppEngineFlexibleAppVersionReadinessCheck":
        '''readiness_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#readiness_check GoogleAppEngineFlexibleAppVersion#readiness_check}
        '''
        result = self._values.get("readiness_check")
        assert result is not None, "Required property 'readiness_check' is missing"
        return typing.cast("GoogleAppEngineFlexibleAppVersionReadinessCheck", result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''Desired runtime. Example python27.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime GoogleAppEngineFlexibleAppVersion#runtime}
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''AppEngine service resource. Can contain numbers, letters, and hyphens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#service GoogleAppEngineFlexibleAppVersion#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_config(self) -> typing.Optional[GoogleAppEngineFlexibleAppVersionApiConfig]:
        '''api_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#api_config GoogleAppEngineFlexibleAppVersion#api_config}
        '''
        result = self._values.get("api_config")
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionApiConfig], result)

    @builtins.property
    def automatic_scaling(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScaling]:
        '''automatic_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#automatic_scaling GoogleAppEngineFlexibleAppVersion#automatic_scaling}
        '''
        result = self._values.get("automatic_scaling")
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScaling], result)

    @builtins.property
    def beta_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata settings that are supplied to this version to enable beta runtime features.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#beta_settings GoogleAppEngineFlexibleAppVersion#beta_settings}
        '''
        result = self._values.get("beta_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def default_expiration(self) -> typing.Optional[builtins.str]:
        '''Duration that static files should be cached by web proxies and browsers.

        Only applicable if the corresponding StaticFilesHandler does not specify its own expiration time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#default_expiration GoogleAppEngineFlexibleAppVersion#default_expiration}
        '''
        result = self._values.get("default_expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_service_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the service will be deleted if it is the last version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#delete_service_on_destroy GoogleAppEngineFlexibleAppVersion#delete_service_on_destroy}
        '''
        result = self._values.get("delete_service_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deployment(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionDeployment"]:
        '''deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#deployment GoogleAppEngineFlexibleAppVersion#deployment}
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionDeployment"], result)

    @builtins.property
    def endpoints_api_service(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionEndpointsApiService"]:
        '''endpoints_api_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#endpoints_api_service GoogleAppEngineFlexibleAppVersion#endpoints_api_service}
        '''
        result = self._values.get("endpoints_api_service")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionEndpointsApiService"], result)

    @builtins.property
    def entrypoint(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionEntrypoint"]:
        '''entrypoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#entrypoint GoogleAppEngineFlexibleAppVersion#entrypoint}
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionEntrypoint"], result)

    @builtins.property
    def env_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables available to the application.

        As these are not returned in the API request, Terraform will not detect any changes made outside of the Terraform config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#env_variables GoogleAppEngineFlexibleAppVersion#env_variables}
        '''
        result = self._values.get("env_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def flexible_runtime_settings(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings"]:
        '''flexible_runtime_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#flexible_runtime_settings GoogleAppEngineFlexibleAppVersion#flexible_runtime_settings}
        '''
        result = self._values.get("flexible_runtime_settings")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings"], result)

    @builtins.property
    def handlers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionHandlers"]]]:
        '''handlers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#handlers GoogleAppEngineFlexibleAppVersion#handlers}
        '''
        result = self._values.get("handlers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionHandlers"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#id GoogleAppEngineFlexibleAppVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inbound_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the types of messages that this application is able to receive.

        Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#inbound_services GoogleAppEngineFlexibleAppVersion#inbound_services}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_class GoogleAppEngineFlexibleAppVersion#instance_class}
        '''
        result = self._values.get("instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_scaling(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionManualScaling"]:
        '''manual_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#manual_scaling GoogleAppEngineFlexibleAppVersion#manual_scaling}
        '''
        result = self._values.get("manual_scaling")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionManualScaling"], result)

    @builtins.property
    def network(self) -> typing.Optional["GoogleAppEngineFlexibleAppVersionNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#network GoogleAppEngineFlexibleAppVersion#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionNetwork"], result)

    @builtins.property
    def nobuild_files_regex(self) -> typing.Optional[builtins.str]:
        '''Files that match this pattern will not be built into this version. Only applicable for Go runtimes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#nobuild_files_regex GoogleAppEngineFlexibleAppVersion#nobuild_files_regex}
        '''
        result = self._values.get("nobuild_files_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noop_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the application version will not be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#noop_on_destroy GoogleAppEngineFlexibleAppVersion#noop_on_destroy}
        '''
        result = self._values.get("noop_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#project GoogleAppEngineFlexibleAppVersion#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#resources GoogleAppEngineFlexibleAppVersion#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionResources"], result)

    @builtins.property
    def runtime_api_version(self) -> typing.Optional[builtins.str]:
        '''The version of the API in the given runtime environment.

        Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref'
        Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_api_version GoogleAppEngineFlexibleAppVersion#runtime_api_version}
        '''
        result = self._values.get("runtime_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_channel(self) -> typing.Optional[builtins.str]:
        '''The channel of the runtime to use. Only available for some runtimes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_channel GoogleAppEngineFlexibleAppVersion#runtime_channel}
        '''
        result = self._values.get("runtime_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_main_executable_path(self) -> typing.Optional[builtins.str]:
        '''The path or name of the app's main executable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_main_executable_path GoogleAppEngineFlexibleAppVersion#runtime_main_executable_path}
        '''
        result = self._values.get("runtime_main_executable_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The identity that the deployed version will run as.

        Admin API will use the App Engine Appspot service account as
        default if this field is neither provided in app.yaml file nor through CLI flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#service_account GoogleAppEngineFlexibleAppVersion#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serving_status(self) -> typing.Optional[builtins.str]:
        '''Current serving status of this version.

        Only the versions with a SERVING status create instances and can be billed. Default value: "SERVING" Possible values: ["SERVING", "STOPPED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#serving_status GoogleAppEngineFlexibleAppVersion#serving_status}
        '''
        result = self._values.get("serving_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleAppEngineFlexibleAppVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeouts GoogleAppEngineFlexibleAppVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionTimeouts"], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Relative name of the version within the service.

        For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens.
        Reserved names,"default", "latest", and any name with the prefix "ah-".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#version_id GoogleAppEngineFlexibleAppVersion#version_id}
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_access_connector(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionVpcAccessConnector"]:
        '''vpc_access_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#vpc_access_connector GoogleAppEngineFlexibleAppVersion#vpc_access_connector}
        '''
        result = self._values.get("vpc_access_connector")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionVpcAccessConnector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_build_options": "cloudBuildOptions",
        "container": "container",
        "files": "files",
        "zip": "zip",
    },
)
class GoogleAppEngineFlexibleAppVersionDeployment:
    def __init__(
        self,
        *,
        cloud_build_options: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        container: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_build_options: cloud_build_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cloud_build_options GoogleAppEngineFlexibleAppVersion#cloud_build_options}
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#container GoogleAppEngineFlexibleAppVersion#container}
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#files GoogleAppEngineFlexibleAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#zip GoogleAppEngineFlexibleAppVersion#zip}
        '''
        if isinstance(cloud_build_options, dict):
            cloud_build_options = GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions(**cloud_build_options)
        if isinstance(container, dict):
            container = GoogleAppEngineFlexibleAppVersionDeploymentContainer(**container)
        if isinstance(zip, dict):
            zip = GoogleAppEngineFlexibleAppVersionDeploymentZip(**zip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1685d935397eb1ad852973e788ea74d57a6ae0707b39f733a5b410049092a8f4)
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
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions"]:
        '''cloud_build_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cloud_build_options GoogleAppEngineFlexibleAppVersion#cloud_build_options}
        '''
        result = self._values.get("cloud_build_options")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions"], result)

    @builtins.property
    def container(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentContainer"]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#container GoogleAppEngineFlexibleAppVersion#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentContainer"], result)

    @builtins.property
    def files(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionDeploymentFiles"]]]:
        '''files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#files GoogleAppEngineFlexibleAppVersion#files}
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionDeploymentFiles"]]], result)

    @builtins.property
    def zip(self) -> typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentZip"]:
        '''zip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#zip GoogleAppEngineFlexibleAppVersion#zip}
        '''
        result = self._values.get("zip")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentZip"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions",
    jsii_struct_bases=[],
    name_mapping={
        "app_yaml_path": "appYamlPath",
        "cloud_build_timeout": "cloudBuildTimeout",
    },
)
class GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions:
    def __init__(
        self,
        *,
        app_yaml_path: builtins.str,
        cloud_build_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_yaml_path: Path to the yaml file used in deployment, used to determine runtime configuration details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#app_yaml_path GoogleAppEngineFlexibleAppVersion#app_yaml_path}
        :param cloud_build_timeout: The Cloud Build timeout used as part of any dependent builds performed by version creation. Defaults to 10 minutes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cloud_build_timeout GoogleAppEngineFlexibleAppVersion#cloud_build_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4385fae4b5bf166063b525d35a05418bad4efb895e308d512824d41d8d3c70c7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#app_yaml_path GoogleAppEngineFlexibleAppVersion#app_yaml_path}
        '''
        result = self._values.get("app_yaml_path")
        assert result is not None, "Required property 'app_yaml_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_build_timeout(self) -> typing.Optional[builtins.str]:
        '''The Cloud Build timeout used as part of any dependent builds performed by version creation. Defaults to 10 minutes.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cloud_build_timeout GoogleAppEngineFlexibleAppVersion#cloud_build_timeout}
        '''
        result = self._values.get("cloud_build_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f074e6d6b5bc63da4f33130261b9c25a67bd4843af86b96834f3fe82e756b4fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ce7c8e94b356b0d172a04a527a6a6c9e18cc4012a7f1b659efaaef9b0459c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appYamlPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudBuildTimeout")
    def cloud_build_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudBuildTimeout"))

    @cloud_build_timeout.setter
    def cloud_build_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c53c61fab55bfe9c75239eed21631d288033953a28af806e92064f0a5134c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudBuildTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7931390e9f855821d4be4184ed46969baf53f3ea9eecd9e382213be42d6d12e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentContainer",
    jsii_struct_bases=[],
    name_mapping={"image": "image"},
)
class GoogleAppEngineFlexibleAppVersionDeploymentContainer:
    def __init__(self, *, image: builtins.str) -> None:
        '''
        :param image: URI to the hosted container image in Google Container Registry. The URI must be fully qualified and include a tag or digest. Examples: "gcr.io/my-project/image:tag" or "gcr.io/my-project/image@digest" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#image GoogleAppEngineFlexibleAppVersion#image}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725097de818a4e723d5c1cb5f92a4900f2a0856f66f95c17aad0a6d52b2e3ac1)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }

    @builtins.property
    def image(self) -> builtins.str:
        '''URI to the hosted container image in Google Container Registry.

        The URI must be fully qualified and include a tag or digest.
        Examples: "gcr.io/my-project/image:tag" or "gcr.io/my-project/image@digest"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#image GoogleAppEngineFlexibleAppVersion#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionDeploymentContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionDeploymentContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d65fe9d96d0ea7a6082b2d546033f942e97e52cca094c99d306165225166811)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a6adb8e636903b83eed8496d1ca3d1383da3e9d98a8a817ad4fc33afe673795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentContainer]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad673daae5c81eac1e8c39d45fc338268f58f4bfe45f2421c3e35f5c4f2bbc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentFiles",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "source_url": "sourceUrl", "sha1_sum": "sha1Sum"},
)
class GoogleAppEngineFlexibleAppVersionDeploymentFiles:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_url: builtins.str,
        sha1_sum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}.
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#source_url GoogleAppEngineFlexibleAppVersion#source_url}
        :param sha1_sum: SHA1 checksum of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#sha1_sum GoogleAppEngineFlexibleAppVersion#sha1_sum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35556212b7b3e7ff06e9fe9b3899265bb16eb67e324169b54ec59fc1eac92849)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_url(self) -> builtins.str:
        '''Source URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#source_url GoogleAppEngineFlexibleAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha1_sum(self) -> typing.Optional[builtins.str]:
        '''SHA1 checksum of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#sha1_sum GoogleAppEngineFlexibleAppVersion#sha1_sum}
        '''
        result = self._values.get("sha1_sum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionDeploymentFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionDeploymentFilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentFilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__358cf449257210f85795ea223f8922c70da5401c6eaae5b0ce36dae1eef036c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAppEngineFlexibleAppVersionDeploymentFilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896598fc46cdfae22a1162fb8375a1f114a0bf94c262286d8a8a72d99bb4f372)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAppEngineFlexibleAppVersionDeploymentFilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e26f704b630fb9689e7db66eec551f3795f45f331b3ed89c8889908af8916b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aefa53a00887588e7bcaa57f581e3c1bc11868f11f53ef512ff21d5d50716698)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31836eead46d6b733d85a3115fa3fba25ec3e688abbc37500a0e1df8b5f88be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionDeploymentFiles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionDeploymentFiles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33639714e2548505ffbb2f3b31c0fec7b6b08c721b546c5d8893a85a757b58b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineFlexibleAppVersionDeploymentFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ecd1eb0f48dd9904a2b699a8aed3472603544fe0bd5611c42e200bf235f613)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01a71f1a70cbe1da4873e7977128f6e590361268c17e692dad0266498f04b5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sha1Sum")
    def sha1_sum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1Sum"))

    @sha1_sum.setter
    def sha1_sum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7cea4c658ca8e62d608df93b0ef0238a999072cc604980c5d7f30bf2540e96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha1Sum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c928c6ebc1c56de692377ba128b0816469073fe22be80bd3a6c19b9ff4f7cbe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionDeploymentFiles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionDeploymentFiles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionDeploymentFiles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621daf0430f5d1305aab2d2d848813ff765f0c1b67cc29a770e232103a484f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineFlexibleAppVersionDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__053ff44a9130a4d0cee6a3eca76ebcc980f2a889e16822d926d0975e23fa9879)
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
        :param app_yaml_path: Path to the yaml file used in deployment, used to determine runtime configuration details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#app_yaml_path GoogleAppEngineFlexibleAppVersion#app_yaml_path}
        :param cloud_build_timeout: The Cloud Build timeout used as part of any dependent builds performed by version creation. Defaults to 10 minutes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cloud_build_timeout GoogleAppEngineFlexibleAppVersion#cloud_build_timeout}
        '''
        value = GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions(
            app_yaml_path=app_yaml_path, cloud_build_timeout=cloud_build_timeout
        )

        return typing.cast(None, jsii.invoke(self, "putCloudBuildOptions", [value]))

    @jsii.member(jsii_name="putContainer")
    def put_container(self, *, image: builtins.str) -> None:
        '''
        :param image: URI to the hosted container image in Google Container Registry. The URI must be fully qualified and include a tag or digest. Examples: "gcr.io/my-project/image:tag" or "gcr.io/my-project/image@digest" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#image GoogleAppEngineFlexibleAppVersion#image}
        '''
        value = GoogleAppEngineFlexibleAppVersionDeploymentContainer(image=image)

        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putFiles")
    def put_files(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ebc0cadcb456e85147da94ff9376d4593ce3282b800c3f9df363326fbc8562)
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
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#source_url GoogleAppEngineFlexibleAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#files_count GoogleAppEngineFlexibleAppVersion#files_count}
        '''
        value = GoogleAppEngineFlexibleAppVersionDeploymentZip(
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
    ) -> GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference:
        return typing.cast(GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference, jsii.get(self, "cloudBuildOptions"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(
        self,
    ) -> GoogleAppEngineFlexibleAppVersionDeploymentContainerOutputReference:
        return typing.cast(GoogleAppEngineFlexibleAppVersionDeploymentContainerOutputReference, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> GoogleAppEngineFlexibleAppVersionDeploymentFilesList:
        return typing.cast(GoogleAppEngineFlexibleAppVersionDeploymentFilesList, jsii.get(self, "files"))

    @builtins.property
    @jsii.member(jsii_name="zip")
    def zip(self) -> "GoogleAppEngineFlexibleAppVersionDeploymentZipOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionDeploymentZipOutputReference", jsii.get(self, "zip"))

    @builtins.property
    @jsii.member(jsii_name="cloudBuildOptionsInput")
    def cloud_build_options_input(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions], jsii.get(self, "cloudBuildOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentContainer]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentContainer], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="filesInput")
    def files_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionDeploymentFiles]]], jsii.get(self, "filesInput"))

    @builtins.property
    @jsii.member(jsii_name="zipInput")
    def zip_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentZip"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionDeploymentZip"], jsii.get(self, "zipInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionDeployment]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e8023d394dcd9c40ec287e18d34f4100d970c5420d02e87db6ed7cc7adbdcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentZip",
    jsii_struct_bases=[],
    name_mapping={"source_url": "sourceUrl", "files_count": "filesCount"},
)
class GoogleAppEngineFlexibleAppVersionDeploymentZip:
    def __init__(
        self,
        *,
        source_url: builtins.str,
        files_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#source_url GoogleAppEngineFlexibleAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#files_count GoogleAppEngineFlexibleAppVersion#files_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca10d35f230e8f0bf8c2dac0aa1342b8c0f8723f329ef986a63933588f4eaf05)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#source_url GoogleAppEngineFlexibleAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def files_count(self) -> typing.Optional[jsii.Number]:
        '''files count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#files_count GoogleAppEngineFlexibleAppVersion#files_count}
        '''
        result = self._values.get("files_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionDeploymentZip(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionDeploymentZipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionDeploymentZipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15a3776177d36f912984457a55a22ccb30e222f8e7ebfe0535bd18ced42fd50d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1274f28d73d0fc2094f053d55304f6f0545a228b60587f155ff09ef163c19e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2289db8537277a155bffb3945c8e8f0aabbd5c84a9f1918b2a816db5301a2935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentZip]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentZip], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentZip],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28aaf290c6f2aa94bb12d998bcd0ccff3e59ca23f50da81c244ca3306aa87263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionEndpointsApiService",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "config_id": "configId",
        "disable_trace_sampling": "disableTraceSampling",
        "rollout_strategy": "rolloutStrategy",
    },
)
class GoogleAppEngineFlexibleAppVersionEndpointsApiService:
    def __init__(
        self,
        *,
        name: builtins.str,
        config_id: typing.Optional[builtins.str] = None,
        disable_trace_sampling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rollout_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Endpoints service name which is the name of the "service" resource in the Service Management API. For example "myapi.endpoints.myproject.cloud.goog". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        :param config_id: Endpoints service configuration ID as specified by the Service Management API. For example "2016-09-19r1". By default, the rollout strategy for Endpoints is "FIXED". This means that Endpoints starts up with a particular configuration ID. When a new configuration is rolled out, Endpoints must be given the new configuration ID. The configId field is used to give the configuration ID and is required in this case. Endpoints also has a rollout strategy called "MANAGED". When using this, Endpoints fetches the latest configuration and does not need the configuration ID. In this case, configId must be omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#config_id GoogleAppEngineFlexibleAppVersion#config_id}
        :param disable_trace_sampling: Enable or disable trace sampling. By default, this is set to false for enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disable_trace_sampling GoogleAppEngineFlexibleAppVersion#disable_trace_sampling}
        :param rollout_strategy: Endpoints rollout strategy. If FIXED, configId must be specified. If MANAGED, configId must be omitted. Default value: "FIXED" Possible values: ["FIXED", "MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#rollout_strategy GoogleAppEngineFlexibleAppVersion#rollout_strategy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9681ca3c2839d67e3fae757d39baf11b8c39d3728763801240ca65b80664b9a9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#config_id GoogleAppEngineFlexibleAppVersion#config_id}
        '''
        result = self._values.get("config_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_trace_sampling(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable trace sampling. By default, this is set to false for enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disable_trace_sampling GoogleAppEngineFlexibleAppVersion#disable_trace_sampling}
        '''
        result = self._values.get("disable_trace_sampling")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rollout_strategy(self) -> typing.Optional[builtins.str]:
        '''Endpoints rollout strategy.

        If FIXED, configId must be specified. If MANAGED, configId must be omitted. Default value: "FIXED" Possible values: ["FIXED", "MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#rollout_strategy GoogleAppEngineFlexibleAppVersion#rollout_strategy}
        '''
        result = self._values.get("rollout_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionEndpointsApiService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionEndpointsApiServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionEndpointsApiServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d313d0c1281a193f521b460d33379bdaf6e7546ee2f889a3c6c45abbc4122145)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd0eb2375bca6d4a0514b66cdf33c810e4418a13d8c37884f6b356f670e1fcc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74b01578f3060200d57e686121bf82fe1872c8d67a22a0522567b2f726a624bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTraceSampling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f16774708e79196c7594035028460a4dc246c5ceef6c042a3083c06b011bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rolloutStrategy")
    def rollout_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutStrategy"))

    @rollout_strategy.setter
    def rollout_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991a25f50df6e08ce77da5c097b79008375f1b60adf2bc61093b390be888c7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionEndpointsApiService]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionEndpointsApiService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionEndpointsApiService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54bdb641311958614166c4e5a2d15db12218c55dd030ecb3e366faca57c88088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionEntrypoint",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell"},
)
class GoogleAppEngineFlexibleAppVersionEntrypoint:
    def __init__(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#shell GoogleAppEngineFlexibleAppVersion#shell}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb2f7d2f951c80672751202e34da09a6dfe066782520202f1f927b7d25806d1)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "shell": shell,
        }

    @builtins.property
    def shell(self) -> builtins.str:
        '''The format should be a shell command that can be fed to bash -c.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#shell GoogleAppEngineFlexibleAppVersion#shell}
        '''
        result = self._values.get("shell")
        assert result is not None, "Required property 'shell' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionEntrypoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionEntrypointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionEntrypointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e27fe1c961ac0772cd5e877056074db67dc54e3e61eb1b853f45de9a0f6a9cf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67a2328ae3d8ed31e053a90f1c5f1f06355a63e29b859bd8615185429a2bf26c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionEntrypoint]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionEntrypoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionEntrypoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f1eb791d0cc10263a655f25e6594ce2fc6bd8de9c49e0f4df902d4b012082d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings",
    jsii_struct_bases=[],
    name_mapping={
        "operating_system": "operatingSystem",
        "runtime_version": "runtimeVersion",
    },
)
class GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings:
    def __init__(
        self,
        *,
        operating_system: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operating_system: Operating System of the application runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#operating_system GoogleAppEngineFlexibleAppVersion#operating_system}
        :param runtime_version: The runtime version of an App Engine flexible application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_version GoogleAppEngineFlexibleAppVersion#runtime_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4897273ff7cbfc1b7620d18facde392346d6ea8a309c7109aadd55883f952f4b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#operating_system GoogleAppEngineFlexibleAppVersion#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''The runtime version of an App Engine flexible application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#runtime_version GoogleAppEngineFlexibleAppVersion#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4eb497fd446522cceded4df1252c29b0bb3887734180812899b440176903f45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f1c3cc9a980dd93c06106fe6d23654f9b1372a618a6d6b45b956e251964e508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ff22005eeef9cdc326a5ea21c7084927d948ccb99d8dbd1310cac8b27506ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94baeb4d98cf178405e9f00fbd0ef41cacc0d7705d74ef332ce21433cdd596e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionHandlers",
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
class GoogleAppEngineFlexibleAppVersionHandlers:
    def __init__(
        self,
        *,
        auth_fail_action: typing.Optional[builtins.str] = None,
        login: typing.Optional[builtins.str] = None,
        redirect_http_response_code: typing.Optional[builtins.str] = None,
        script: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionHandlersScript", typing.Dict[builtins.str, typing.Any]]] = None,
        security_level: typing.Optional[builtins.str] = None,
        static_files: typing.Optional[typing.Union["GoogleAppEngineFlexibleAppVersionHandlersStaticFiles", typing.Dict[builtins.str, typing.Any]]] = None,
        url_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_fail_action: Actions to take when the user is not logged in. Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#auth_fail_action GoogleAppEngineFlexibleAppVersion#auth_fail_action}
        :param login: Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#login GoogleAppEngineFlexibleAppVersion#login}
        :param redirect_http_response_code: 30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#redirect_http_response_code GoogleAppEngineFlexibleAppVersion#redirect_http_response_code}
        :param script: script block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script GoogleAppEngineFlexibleAppVersion#script}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#security_level GoogleAppEngineFlexibleAppVersion#security_level}
        :param static_files: static_files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#static_files GoogleAppEngineFlexibleAppVersion#static_files}
        :param url_regex: URL prefix. Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings. All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#url_regex GoogleAppEngineFlexibleAppVersion#url_regex}
        '''
        if isinstance(script, dict):
            script = GoogleAppEngineFlexibleAppVersionHandlersScript(**script)
        if isinstance(static_files, dict):
            static_files = GoogleAppEngineFlexibleAppVersionHandlersStaticFiles(**static_files)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d86d927c5febb409a0069a21f7191b104fe54db33e5789688f93bb44b8a389b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#auth_fail_action GoogleAppEngineFlexibleAppVersion#auth_fail_action}
        '''
        result = self._values.get("auth_fail_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login(self) -> typing.Optional[builtins.str]:
        '''Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#login GoogleAppEngineFlexibleAppVersion#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_http_response_code(self) -> typing.Optional[builtins.str]:
        '''30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#redirect_http_response_code GoogleAppEngineFlexibleAppVersion#redirect_http_response_code}
        '''
        result = self._values.get("redirect_http_response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersScript"]:
        '''script block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script GoogleAppEngineFlexibleAppVersion#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersScript"], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#security_level GoogleAppEngineFlexibleAppVersion#security_level}
        '''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_files(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersStaticFiles"]:
        '''static_files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#static_files GoogleAppEngineFlexibleAppVersion#static_files}
        '''
        result = self._values.get("static_files")
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersStaticFiles"], result)

    @builtins.property
    def url_regex(self) -> typing.Optional[builtins.str]:
        '''URL prefix.

        Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings.
        All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#url_regex GoogleAppEngineFlexibleAppVersion#url_regex}
        '''
        result = self._values.get("url_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionHandlers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionHandlersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionHandlersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b7f471e28f818c8659b793f4b39bdf582792d1c6e8d7e5e14fa91d708fb4a1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAppEngineFlexibleAppVersionHandlersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf56923ab0c19767733f0debbb7e3ae6cdbec45bcb34818ac4701af05071bf82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAppEngineFlexibleAppVersionHandlersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4df062c70b96edf2bd009825c1bb2d664410923f49411ceae3da40eb92fcc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff172f122591d5ddb6e301e0c975ad70b64549f470cb305b2e6730600786e698)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2116ad016ab8fd770a8d61c9fc4fb4709a74a443b1dc6363831c0c2104f01220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionHandlers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionHandlers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionHandlers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053017905e1d26f7ef516d3241b61b90540d158064cfb7765cb8dd377970febd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineFlexibleAppVersionHandlersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionHandlersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c2369897a149014481bb0d11c6cdd4047269d6417209cf0535fecf3aa27a7f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putScript")
    def put_script(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script_path GoogleAppEngineFlexibleAppVersion#script_path}
        '''
        value = GoogleAppEngineFlexibleAppVersionHandlersScript(
            script_path=script_path
        )

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
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#application_readable GoogleAppEngineFlexibleAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Default is '0s' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#expiration GoogleAppEngineFlexibleAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#http_headers GoogleAppEngineFlexibleAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#mime_type GoogleAppEngineFlexibleAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#require_matching_file GoogleAppEngineFlexibleAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#upload_path_regex GoogleAppEngineFlexibleAppVersion#upload_path_regex}
        '''
        value = GoogleAppEngineFlexibleAppVersionHandlersStaticFiles(
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
    def script(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionHandlersScriptOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionHandlersScriptOutputReference", jsii.get(self, "script"))

    @builtins.property
    @jsii.member(jsii_name="staticFiles")
    def static_files(
        self,
    ) -> "GoogleAppEngineFlexibleAppVersionHandlersStaticFilesOutputReference":
        return typing.cast("GoogleAppEngineFlexibleAppVersionHandlersStaticFilesOutputReference", jsii.get(self, "staticFiles"))

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
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersScript"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersScript"], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="securityLevelInput")
    def security_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="staticFilesInput")
    def static_files_input(
        self,
    ) -> typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersStaticFiles"]:
        return typing.cast(typing.Optional["GoogleAppEngineFlexibleAppVersionHandlersStaticFiles"], jsii.get(self, "staticFilesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__08862dbafa55579242ae7950fceba3653edd57c4a65f248bb2ef3b5e2fc7ee58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authFailAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "login"))

    @login.setter
    def login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5763930a7a5debf520132251728e2f03542fa41bb2d4813f71676f774d992489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "login", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectHttpResponseCode")
    def redirect_http_response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectHttpResponseCode"))

    @redirect_http_response_code.setter
    def redirect_http_response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c43ce9e1af2c3485da6ab4c145368009baa92767626564b8499097923417409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectHttpResponseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @security_level.setter
    def security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f653bcf792dc887a41bce4e4d4790cb84d5c46d62d11542371e0aa15a1ad4b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlRegex")
    def url_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlRegex"))

    @url_regex.setter
    def url_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559e0ea64226c1795dab7e612582066e032a5ae47ad7d9fbdd7c9ce95f6a3d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionHandlers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionHandlers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionHandlers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0a948e0ce32a6ce2f58cb33da9c91eaada70fe084467b8be611ca816e0afa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionHandlersScript",
    jsii_struct_bases=[],
    name_mapping={"script_path": "scriptPath"},
)
class GoogleAppEngineFlexibleAppVersionHandlersScript:
    def __init__(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script_path GoogleAppEngineFlexibleAppVersion#script_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c0f5d348f94eec538a83445d3cf336752207298d92880dba21f99138dc2c94)
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script_path": script_path,
        }

    @builtins.property
    def script_path(self) -> builtins.str:
        '''Path to the script from the application root directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#script_path GoogleAppEngineFlexibleAppVersion#script_path}
        '''
        result = self._values.get("script_path")
        assert result is not None, "Required property 'script_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionHandlersScript(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionHandlersScriptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionHandlersScriptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e5f50e1548ae443508d70dfc3424ddf1150e16386d7bedc6a615d7ab306b1af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b67c9aeb53c02af547f92eafc646f366cddf1cb6e2d08e1e4130ac7a46549c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersScript]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersScript], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersScript],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf22b62d5210b911ecd5b9efc072b2ee1c8704fd1ffdeee313f2adff3738b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionHandlersStaticFiles",
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
class GoogleAppEngineFlexibleAppVersionHandlersStaticFiles:
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
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#application_readable GoogleAppEngineFlexibleAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Default is '0s' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#expiration GoogleAppEngineFlexibleAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#http_headers GoogleAppEngineFlexibleAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#mime_type GoogleAppEngineFlexibleAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#require_matching_file GoogleAppEngineFlexibleAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#upload_path_regex GoogleAppEngineFlexibleAppVersion#upload_path_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d906cce3c50cdbf1f35aac0fb0163eaf6b2cfc45b4128ac383c8f5511e44f91e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#application_readable GoogleAppEngineFlexibleAppVersion#application_readable}
        '''
        result = self._values.get("application_readable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Time a static file served by this handler should be cached by web proxies and browsers.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s".
        Default is '0s'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#expiration GoogleAppEngineFlexibleAppVersion#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#http_headers GoogleAppEngineFlexibleAppVersion#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mime_type(self) -> typing.Optional[builtins.str]:
        '''MIME type used to serve all files served by this handler.

        Defaults to file-specific MIME types, which are derived from each file's filename extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#mime_type GoogleAppEngineFlexibleAppVersion#mime_type}
        '''
        result = self._values.get("mime_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to the static files matched by the URL pattern, from the application root directory.

        The path can refer to text matched in groupings in the URL pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_matching_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this handler should match the request if the file referenced by the handler does not exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#require_matching_file GoogleAppEngineFlexibleAppVersion#require_matching_file}
        '''
        result = self._values.get("require_matching_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upload_path_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression that matches the file paths for all files that should be referenced by this handler.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#upload_path_regex GoogleAppEngineFlexibleAppVersion#upload_path_regex}
        '''
        result = self._values.get("upload_path_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionHandlersStaticFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionHandlersStaticFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionHandlersStaticFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1edd52a2e5d2ce74958d2c933113f5f18895f12bd8e6eea680d2721ed905c12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90ae67d78452a95d009782b3815aa2e3860ffca9c9e01e95c39ce6b1d4385bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationReadable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecc3b258834043c52e1f51149e311519f558daa534dcda94eeff7c87b6b4744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "httpHeaders"))

    @http_headers.setter
    def http_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a14452b5cab3113e2f6911c66230ad66410d22810f987c775cac436733a3db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mimeType")
    def mime_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mimeType"))

    @mime_type.setter
    def mime_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afe3e14a486d8a3b610c54d1ace88057d17892d16f0e178304e3e9a64b18b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mimeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9878c747e7b021f06ccdeb145a45f6bc24ac03324f4a8c99a9977fb5a7a3a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb536baccd3d965a0a953bfd8866b35a795026afa57e8cd23839ef0446ed736c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireMatchingFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadPathRegex")
    def upload_path_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uploadPathRegex"))

    @upload_path_regex.setter
    def upload_path_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491cd83e1ee16865ebb302279299212b1093f07200ba099a6ad1f0f4c8c053c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadPathRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersStaticFiles]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersStaticFiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersStaticFiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6d669cbb9d543ea08f1050b362595a85070032ee3f9a8b6e6c20197a2530402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionLivenessCheck",
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
class GoogleAppEngineFlexibleAppVersionLivenessCheck:
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
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        :param check_interval: Interval between health checks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#check_interval GoogleAppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before considering the VM unhealthy. Default: 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#failure_threshold GoogleAppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#host GoogleAppEngineFlexibleAppVersion#host}
        :param initial_delay: The initial delay before starting to execute the checks. Default: "300s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#initial_delay GoogleAppEngineFlexibleAppVersion#initial_delay}
        :param success_threshold: Number of consecutive successful checks required before considering the VM healthy. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#success_threshold GoogleAppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeout GoogleAppEngineFlexibleAppVersion#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818f150e5790cf8f86bc6217811b6fba5f0dfe4470206b79a502c7cefd6f949a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def check_interval(self) -> typing.Optional[builtins.str]:
        '''Interval between health checks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#check_interval GoogleAppEngineFlexibleAppVersion#check_interval}
        '''
        result = self._values.get("check_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failed checks required before considering the VM unhealthy. Default: 4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#failure_threshold GoogleAppEngineFlexibleAppVersion#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#host GoogleAppEngineFlexibleAppVersion#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[builtins.str]:
        '''The initial delay before starting to execute the checks. Default: "300s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#initial_delay GoogleAppEngineFlexibleAppVersion#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successful checks required before considering the VM healthy. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#success_threshold GoogleAppEngineFlexibleAppVersion#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Time before the check is considered failed. Default: "4s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeout GoogleAppEngineFlexibleAppVersion#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionLivenessCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionLivenessCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionLivenessCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5560d62c618e0b4fbee6e54ff5b04b13ab4c63d443cd96241a0a939fa07cee29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__adb08ecdf7617408e32dcbda8fcc61e56d71708ee35b6b4c726f831d554b8bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e780e1d91292b14a0fae70a2797fe70c1cb5573b36310894d2ce7a28c904b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10f6fd1b3e8510867ef5f6bd2172adb619bfd419b7621573742b796dcc37796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b80f9fa46c2844c274cd6dfb509c412d8ff22eee00aa6e84c049d368f527a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d233467d4b979cc2c50e688fc9bec8b7f107061e5a4ad85b814199aaff5a15e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7137561f69e95bbc3beba9b2fe65a42bd8871105521de568b718dcc84f16e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce39f22ec9a31abeef99bc6c798c743fdebc0d2c448e02fe2afdb353c286dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionLivenessCheck]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionLivenessCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionLivenessCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28980ba3b28b7c7aca5dc817c698fcb4725ae1c2a7b060a7ad3cf2c7f022a7d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionManualScaling",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class GoogleAppEngineFlexibleAppVersionManualScaling:
    def __init__(self, *, instances: jsii.Number) -> None:
        '''
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instances GoogleAppEngineFlexibleAppVersion#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37589790062fb96fba0eacc227ef512dc3466f0af9d9c27e78ddfb069e744a76)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instances": instances,
        }

    @builtins.property
    def instances(self) -> jsii.Number:
        '''Number of instances to assign to the service at the start.

        **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2
        Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instances GoogleAppEngineFlexibleAppVersion#instances}
        '''
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionManualScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionManualScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionManualScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89e47905630928487bb0eebb3eec88710b252c92b4dc89a21a1446c2ad2679e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dce4e9338d7ec820248e9580bd9adfe64743009c5212268226d417d2bbec9d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionManualScaling]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionManualScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionManualScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce81ea4c026e723b62e4ee6424e5c79785daec667fcbcba697ab0f9df6647aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "forwarded_ports": "forwardedPorts",
        "instance_ip_mode": "instanceIpMode",
        "instance_tag": "instanceTag",
        "session_affinity": "sessionAffinity",
        "subnetwork": "subnetwork",
    },
)
class GoogleAppEngineFlexibleAppVersionNetwork:
    def __init__(
        self,
        *,
        name: builtins.str,
        forwarded_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_ip_mode: typing.Optional[builtins.str] = None,
        instance_tag: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Google Compute Engine network where the virtual machines are created. Specify the short name, not the resource path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        :param forwarded_ports: List of ports, or port pairs, to forward from the virtual machine to the application container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#forwarded_ports GoogleAppEngineFlexibleAppVersion#forwarded_ports}
        :param instance_ip_mode: Prevent instances from receiving an ephemeral external IP address. Possible values: ["EXTERNAL", "INTERNAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_ip_mode GoogleAppEngineFlexibleAppVersion#instance_ip_mode}
        :param instance_tag: Tag to apply to the instance during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_tag GoogleAppEngineFlexibleAppVersion#instance_tag}
        :param session_affinity: Enable session affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#session_affinity GoogleAppEngineFlexibleAppVersion#session_affinity}
        :param subnetwork: Google Cloud Platform sub-network where the virtual machines are created. Specify the short name, not the resource path. If the network that the instance is being created in is a Legacy network, then the IP address is allocated from the IPv4Range. If the network that the instance is being created in is an auto Subnet Mode Network, then only network name should be specified (not the subnetworkName) and the IP address is created from the IPCidrRange of the subnetwork that exists in that zone for that network. If the network that the instance is being created in is a custom Subnet Mode Network, then the subnetworkName must be specified and the IP address is created from the IPCidrRange of the subnetwork. If specified, the subnetwork must exist in the same region as the App Engine flexible environment application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#subnetwork GoogleAppEngineFlexibleAppVersion#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d3431197cd2c91add70c0df23df4cb6172a38abe2ecc76dd64fac0b303595d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument forwarded_ports", value=forwarded_ports, expected_type=type_hints["forwarded_ports"])
            check_type(argname="argument instance_ip_mode", value=instance_ip_mode, expected_type=type_hints["instance_ip_mode"])
            check_type(argname="argument instance_tag", value=instance_tag, expected_type=type_hints["instance_tag"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if forwarded_ports is not None:
            self._values["forwarded_ports"] = forwarded_ports
        if instance_ip_mode is not None:
            self._values["instance_ip_mode"] = instance_ip_mode
        if instance_tag is not None:
            self._values["instance_tag"] = instance_tag
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork

    @builtins.property
    def name(self) -> builtins.str:
        '''Google Compute Engine network where the virtual machines are created. Specify the short name, not the resource path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forwarded_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of ports, or port pairs, to forward from the virtual machine to the application container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#forwarded_ports GoogleAppEngineFlexibleAppVersion#forwarded_ports}
        '''
        result = self._values.get("forwarded_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_ip_mode(self) -> typing.Optional[builtins.str]:
        '''Prevent instances from receiving an ephemeral external IP address. Possible values: ["EXTERNAL", "INTERNAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_ip_mode GoogleAppEngineFlexibleAppVersion#instance_ip_mode}
        '''
        result = self._values.get("instance_ip_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_tag(self) -> typing.Optional[builtins.str]:
        '''Tag to apply to the instance during creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#instance_tag GoogleAppEngineFlexibleAppVersion#instance_tag}
        '''
        result = self._values.get("instance_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable session affinity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#session_affinity GoogleAppEngineFlexibleAppVersion#session_affinity}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#subnetwork GoogleAppEngineFlexibleAppVersion#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8253f58436093059c20f29f7c8b953478a504393e6ec56f8662ba78142137358)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetForwardedPorts")
    def reset_forwarded_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedPorts", []))

    @jsii.member(jsii_name="resetInstanceIpMode")
    def reset_instance_ip_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceIpMode", []))

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
    @jsii.member(jsii_name="instanceIpModeInput")
    def instance_ip_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIpModeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5849de554c5962fd90205d37fc733ffe3cfda64a7e0ddee37da8e4b896e26d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardedPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceIpMode")
    def instance_ip_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceIpMode"))

    @instance_ip_mode.setter
    def instance_ip_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4065880e0480c7a0d279bfc72837eaba6eb69099e944f6d5ee26ad6149cdb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceIpMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTag")
    def instance_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTag"))

    @instance_tag.setter
    def instance_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273fcd24225c56bcdae62f4179532a3c910ab8f219749c2c1b782076bfb32895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b702d9327708ebbc7fef36c7ccf9791b0830587328e8b087d5cdbdb9f20fe07e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d93d4e549b1cdbeebcc28e5d64e97f8971b16eb407bdb744babb1c2a198ee769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0aee2dda6ef05513739c1d08daafa2168767447ddc39c074badfc141ac7528f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionNetwork]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993f45e569f136d9c38f409316b385d3655de1caf5a17a4cd906029dce957fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionReadinessCheck",
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
class GoogleAppEngineFlexibleAppVersionReadinessCheck:
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
        :param path: The request path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        :param app_start_timeout: A maximum time limit on application initialization, measured from moment the application successfully replies to a healthcheck until it is ready to serve traffic. Default: "300s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#app_start_timeout GoogleAppEngineFlexibleAppVersion#app_start_timeout}
        :param check_interval: Interval between health checks. Default: "5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#check_interval GoogleAppEngineFlexibleAppVersion#check_interval}
        :param failure_threshold: Number of consecutive failed checks required before removing traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#failure_threshold GoogleAppEngineFlexibleAppVersion#failure_threshold}
        :param host: Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#host GoogleAppEngineFlexibleAppVersion#host}
        :param success_threshold: Number of consecutive successful checks required before receiving traffic. Default: 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#success_threshold GoogleAppEngineFlexibleAppVersion#success_threshold}
        :param timeout: Time before the check is considered failed. Default: "4s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeout GoogleAppEngineFlexibleAppVersion#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf260d42bcd39ad625e109d7d8a2a31b1d29918af596fe774917b5d99e97b78)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#path GoogleAppEngineFlexibleAppVersion#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_start_timeout(self) -> typing.Optional[builtins.str]:
        '''A maximum time limit on application initialization, measured from moment the application successfully replies to a healthcheck until it is ready to serve traffic.

        Default: "300s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#app_start_timeout GoogleAppEngineFlexibleAppVersion#app_start_timeout}
        '''
        result = self._values.get("app_start_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_interval(self) -> typing.Optional[builtins.str]:
        '''Interval between health checks.  Default: "5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#check_interval GoogleAppEngineFlexibleAppVersion#check_interval}
        '''
        result = self._values.get("check_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failed checks required before removing traffic. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#failure_threshold GoogleAppEngineFlexibleAppVersion#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host header to send when performing a HTTP Readiness check. Example: "myapp.appspot.com".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#host GoogleAppEngineFlexibleAppVersion#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successful checks required before receiving traffic. Default: 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#success_threshold GoogleAppEngineFlexibleAppVersion#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Time before the check is considered failed. Default: "4s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#timeout GoogleAppEngineFlexibleAppVersion#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionReadinessCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionReadinessCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionReadinessCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b890ffa0b4fd044b129c1ab81875bffaba66c910fe33f3ca3aa98b98cb7043b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55e3e6259ff0b49e9c34f13f379d4eeb670705df267ac29088cf94702698f29b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appStartTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="checkInterval")
    def check_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkInterval"))

    @check_interval.setter
    def check_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48c6df09662f8ee874ff198ad55d736489aaf63bf5f23ceb0822ac8b96c05c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08362366b81bbd619fe6c2d644c9a43a90bed96b43b972979f7554fe51a275cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cf11178fee91d7b6452d56e462b3924a40e70029f893c4450419e9e9725c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec28a827d652f72e1f9e799c227cc603a2ffa8415b8c65438dcc7975270f244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2dc2c3b23306f0166513a10e839ebe05be5aedce3732c34b28934d4efe0c1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf467620bb294df873e4d383e42e8549f9cb5ba726eeaf3d5a8684b86040a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionReadinessCheck]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionReadinessCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionReadinessCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287de96397183aa1a9e99486701299c202c337481cca88176f9d9e893d7badd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionResources",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "disk_gb": "diskGb",
        "memory_gb": "memoryGb",
        "volumes": "volumes",
    },
)
class GoogleAppEngineFlexibleAppVersionResources:
    def __init__(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        disk_gb: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionResourcesVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cpu: Number of CPU cores needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cpu GoogleAppEngineFlexibleAppVersion#cpu}
        :param disk_gb: Disk size (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disk_gb GoogleAppEngineFlexibleAppVersion#disk_gb}
        :param memory_gb: Memory (GB) needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#memory_gb GoogleAppEngineFlexibleAppVersion#memory_gb}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#volumes GoogleAppEngineFlexibleAppVersion#volumes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7173859d8329c561587249226d66a139da020046ea1bde1c143fe55431aa96f9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#cpu GoogleAppEngineFlexibleAppVersion#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_gb(self) -> typing.Optional[jsii.Number]:
        '''Disk size (GB) needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#disk_gb GoogleAppEngineFlexibleAppVersion#disk_gb}
        '''
        result = self._values.get("disk_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#memory_gb GoogleAppEngineFlexibleAppVersion#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionResourcesVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#volumes GoogleAppEngineFlexibleAppVersion#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionResourcesVolumes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__010f49d95f3dfbb537a80706c304675b97b9c900f5dd231d65d3ec68047eff86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineFlexibleAppVersionResourcesVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99706bf11f7ce5d8607e222cdc594a0c89f77815439028d9f270eca11c2ac4ff)
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
    def volumes(self) -> "GoogleAppEngineFlexibleAppVersionResourcesVolumesList":
        return typing.cast("GoogleAppEngineFlexibleAppVersionResourcesVolumesList", jsii.get(self, "volumes"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionResourcesVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineFlexibleAppVersionResourcesVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a539a2d6106bae8bd6c1d2c24fce91adcf3b58885d80fe68345df17a54ce7945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskGb")
    def disk_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskGb"))

    @disk_gb.setter
    def disk_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2766e2e42e350cfba722fd32e55eec026d657658fc314609905487d763f11c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9830c6637cbd874cacd53814f95b9f04360ac27db76e1cbc7be824620c26ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionResources]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487eff5278a9929186258191e6bfc1fff2dc18821a6629b3a16d17f8c4717945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionResourcesVolumes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "size_gb": "sizeGb", "volume_type": "volumeType"},
)
class GoogleAppEngineFlexibleAppVersionResourcesVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        size_gb: jsii.Number,
        volume_type: builtins.str,
    ) -> None:
        '''
        :param name: Unique name for the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        :param size_gb: Volume size in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#size_gb GoogleAppEngineFlexibleAppVersion#size_gb}
        :param volume_type: Underlying volume type, e.g. 'tmpfs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#volume_type GoogleAppEngineFlexibleAppVersion#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a90a1d32cbba74826b27dc1aab5ed2fea0aaae24cc1c64e1e4808e0cbffaa7a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_gb(self) -> jsii.Number:
        '''Volume size in gigabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#size_gb GoogleAppEngineFlexibleAppVersion#size_gb}
        '''
        result = self._values.get("size_gb")
        assert result is not None, "Required property 'size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_type(self) -> builtins.str:
        '''Underlying volume type, e.g. 'tmpfs'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#volume_type GoogleAppEngineFlexibleAppVersion#volume_type}
        '''
        result = self._values.get("volume_type")
        assert result is not None, "Required property 'volume_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionResourcesVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionResourcesVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionResourcesVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__910061867ad9b1bb5f9daee0b2d116c411c086d28f7dbe7fe1ec5f1deada6628)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAppEngineFlexibleAppVersionResourcesVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb8eb345b1dbe2b088e452e7a6b30fdf26bf739b22a1bb52a9d5abe14396aaa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAppEngineFlexibleAppVersionResourcesVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9193be3b1e0b9e08b60c52f0077999cd277e5a28d88ad84d396b9a68ef35c23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c48074faa25519184a89f324a64541afb17cb862afefb19af69bdc5b204b6d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a2f0a62c02c1881dcbd170b0b5005ff5c34ff292c725a14b0cbf385be1be37f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionResourcesVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionResourcesVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionResourcesVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422f9fc9b4e968eb24bf864ff85cdb1be75bd20a829127bc96029579034350c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineFlexibleAppVersionResourcesVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionResourcesVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aa97421f7b6e1097c17d8e2e938a93ec9ad722c726fa9f792da5976b45409a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5430c77fa637ed598d3e3e6071e3506c21e0019bac08e15bc8a890012c80a193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @size_gb.setter
    def size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820e493be2efd867ea51dc3b9595490ab3d4ac673f5eba86d4d88e575542fc7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d8dc71bea8b8b13b988b5c9467d3e02b405097d56b4fd0ca2462eb3a284162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionResourcesVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionResourcesVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionResourcesVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce982b617cc3141167d214a19f8396bec240c426cf196040c4eebe506d20176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleAppEngineFlexibleAppVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#create GoogleAppEngineFlexibleAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#delete GoogleAppEngineFlexibleAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#update GoogleAppEngineFlexibleAppVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec3c3a3df5a093f8fbc41e87304e8ea93d502ff964869e09fcd06cc3357f385)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#create GoogleAppEngineFlexibleAppVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#delete GoogleAppEngineFlexibleAppVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#update GoogleAppEngineFlexibleAppVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12d51e13215dce077ac6461dd7a3794a780f9d9d1257382379c4303740a20516)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6c65605f55ec3ce8b6f4f345000c42d479e4e56708726793f70636d1af930c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962f7bdf3f4c8e12e9e8833e9fc38ec6b7605f537f2240dd4285eafb7e10cef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96117eaf1c6ce9f21bfc196653ec9ff30e04ad7994d4b7f6552ac83722452a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4058cc2a52e6923da39e0d14e020b6736fc1259238842c2e4ec36a7b1a3cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionVpcAccessConnector",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleAppEngineFlexibleAppVersionVpcAccessConnector:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ccb6b8075c7107e6bc795149de976f36b0e94ec3795bb755d87ac27e0f4a03)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_flexible_app_version#name GoogleAppEngineFlexibleAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineFlexibleAppVersionVpcAccessConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineFlexibleAppVersionVpcAccessConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineFlexibleAppVersion.GoogleAppEngineFlexibleAppVersionVpcAccessConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de50a76764b325c4ba75ce6976175ee8eb01553a9e45175b7dd88ba7c926ad09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ce0ecc6e1c3f131e2ab38a25f328dd16b4148e46cc5e670492ba0c23abe2ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineFlexibleAppVersionVpcAccessConnector]:
        return typing.cast(typing.Optional[GoogleAppEngineFlexibleAppVersionVpcAccessConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineFlexibleAppVersionVpcAccessConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ff4629204f9ef4b25c1e587f5d5921d3b3f34d826a563b105e590a91156048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleAppEngineFlexibleAppVersion",
    "GoogleAppEngineFlexibleAppVersionApiConfig",
    "GoogleAppEngineFlexibleAppVersionApiConfigOutputReference",
    "GoogleAppEngineFlexibleAppVersionAutomaticScaling",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilizationOutputReference",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilizationOutputReference",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilizationOutputReference",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingOutputReference",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization",
    "GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilizationOutputReference",
    "GoogleAppEngineFlexibleAppVersionConfig",
    "GoogleAppEngineFlexibleAppVersionDeployment",
    "GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions",
    "GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptionsOutputReference",
    "GoogleAppEngineFlexibleAppVersionDeploymentContainer",
    "GoogleAppEngineFlexibleAppVersionDeploymentContainerOutputReference",
    "GoogleAppEngineFlexibleAppVersionDeploymentFiles",
    "GoogleAppEngineFlexibleAppVersionDeploymentFilesList",
    "GoogleAppEngineFlexibleAppVersionDeploymentFilesOutputReference",
    "GoogleAppEngineFlexibleAppVersionDeploymentOutputReference",
    "GoogleAppEngineFlexibleAppVersionDeploymentZip",
    "GoogleAppEngineFlexibleAppVersionDeploymentZipOutputReference",
    "GoogleAppEngineFlexibleAppVersionEndpointsApiService",
    "GoogleAppEngineFlexibleAppVersionEndpointsApiServiceOutputReference",
    "GoogleAppEngineFlexibleAppVersionEntrypoint",
    "GoogleAppEngineFlexibleAppVersionEntrypointOutputReference",
    "GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings",
    "GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettingsOutputReference",
    "GoogleAppEngineFlexibleAppVersionHandlers",
    "GoogleAppEngineFlexibleAppVersionHandlersList",
    "GoogleAppEngineFlexibleAppVersionHandlersOutputReference",
    "GoogleAppEngineFlexibleAppVersionHandlersScript",
    "GoogleAppEngineFlexibleAppVersionHandlersScriptOutputReference",
    "GoogleAppEngineFlexibleAppVersionHandlersStaticFiles",
    "GoogleAppEngineFlexibleAppVersionHandlersStaticFilesOutputReference",
    "GoogleAppEngineFlexibleAppVersionLivenessCheck",
    "GoogleAppEngineFlexibleAppVersionLivenessCheckOutputReference",
    "GoogleAppEngineFlexibleAppVersionManualScaling",
    "GoogleAppEngineFlexibleAppVersionManualScalingOutputReference",
    "GoogleAppEngineFlexibleAppVersionNetwork",
    "GoogleAppEngineFlexibleAppVersionNetworkOutputReference",
    "GoogleAppEngineFlexibleAppVersionReadinessCheck",
    "GoogleAppEngineFlexibleAppVersionReadinessCheckOutputReference",
    "GoogleAppEngineFlexibleAppVersionResources",
    "GoogleAppEngineFlexibleAppVersionResourcesOutputReference",
    "GoogleAppEngineFlexibleAppVersionResourcesVolumes",
    "GoogleAppEngineFlexibleAppVersionResourcesVolumesList",
    "GoogleAppEngineFlexibleAppVersionResourcesVolumesOutputReference",
    "GoogleAppEngineFlexibleAppVersionTimeouts",
    "GoogleAppEngineFlexibleAppVersionTimeoutsOutputReference",
    "GoogleAppEngineFlexibleAppVersionVpcAccessConnector",
    "GoogleAppEngineFlexibleAppVersionVpcAccessConnectorOutputReference",
]

publication.publish()

def _typecheckingstub__a39d0c4696d5a866dcb8bacfbc4b2116aae0fba5a519d5d0a26e51f26b31c964(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    liveness_check: typing.Union[GoogleAppEngineFlexibleAppVersionLivenessCheck, typing.Dict[builtins.str, typing.Any]],
    readiness_check: typing.Union[GoogleAppEngineFlexibleAppVersionReadinessCheck, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    api_config: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionApiConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    automatic_scaling: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    default_expiration: typing.Optional[builtins.str] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoints_api_service: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionEndpointsApiService, typing.Dict[builtins.str, typing.Any]]] = None,
    entrypoint: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    flexible_runtime_settings: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    manual_scaling: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    nobuild_files_regex: typing.Optional[builtins.str] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionResources, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    runtime_channel: typing.Optional[builtins.str] = None,
    runtime_main_executable_path: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    serving_status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9723e7217156c902b806023d58b6e4551227b0ad886829528984ad5bcd7e27e5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5ab8d02fee4f28189f8924941f740c0c063fc23fae0b2ac5c2520551464045(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bba4932ea51688eeb51f873771bba7aed5d18f262ee4d0d7692fe4c309cbf45(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f564f79c5bacb31970886fb54267181c9a495594e042c295810da6a22dd26f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5cb37b5b9b5f105ba273ae35c05029f198b5c5e1fdfd050d12f331a731245f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbbb235b8c6c05cd31c473d4522b686f89386221b798ee6870aff4c28781b07(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bade06fc724aa62e438af77f9b6ab754fb06be949651b1ca01b02609228278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3798850755556f5cef875cee0534604ca09b50ebba04c88111db762c3d973b66(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec721cd624f688ef8317b355700003e7a492bd77799f530b11b72b46d3c73cad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56130e1f9bb942eb2a19943b70519049c3ad785d6d13e06c9bb6a90b087aef41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9fab893734b79c8dca848d9e6e718b24ee4f680ffd0de2209699d77b0a7392(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c1fbd79e1104926ccfff6b6204e8de3eb3a3e989a50d9d1164c9773e3a3a26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce80908d444e58f5490d588914d4bae5ec8238d2a0e8e392487a142e8595f9cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122720b5252aa55dbe9307977d1fe08d9ca276078993abe1287fba17785b777a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d417f9489b8a13710e0820a456bb64b846135acbac4e3f567a8f191e75b73e29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6df1838ab801486ab7313dd3a67bd550650383baccad00cfb0fb63a1235630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49a68e30f8254c407b80b1771e594ae81f340637837cca603759de02abbae12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a176c9425b02ac1879024003072b98b2219f78bd4fe0894a6b6313d4ec95f9b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a26e3be121d76558c233839fe0bc117b814ed6ce538559e14c3a1dbd5f79db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d71b32f80615d1a3b9b9475bd380756faabf5c490a51fbd8ae3c5bd59f9001(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f76cafcf9a26e5cae0bef668fdd1817354a3d06150f22dcb4b0862502e570e(
    *,
    script: builtins.str,
    auth_fail_action: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    security_level: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5976f435131d3d6adea3caeea117d0292dd461e52fe5bb6642128632d76c65c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a0a5b2506b679c79c4d17998a967a2e66e974c68ef3e60d8f23cafa398e7ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc61d807b1fb633a98940dc70870d1e656697cc164c18ee4416670ea3844583f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f591455e75c06ca31d6e1bfb23c08675f94e3767a848b90152924e7ddff4889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41173b19f51698e2f24cab89e60da9671b8f6186cfa5e9064bd0b06c786c9b5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d3bf84808966ec83b56f406859e6d6586ce0153b7594f0fedec26c68beceed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0453e574addd32f993b867e19a46935f3b3fd11a9e88713d25322dfac14c1a33(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionApiConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b985d564dc4e8b7b9d8b1422305166c5083c08a29789f81e703e5a6691da96b0(
    *,
    cpu_utilization: typing.Union[GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization, typing.Dict[builtins.str, typing.Any]],
    cool_down_period: typing.Optional[builtins.str] = None,
    disk_utilization: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    max_concurrent_requests: typing.Optional[jsii.Number] = None,
    max_idle_instances: typing.Optional[jsii.Number] = None,
    max_pending_latency: typing.Optional[builtins.str] = None,
    max_total_instances: typing.Optional[jsii.Number] = None,
    min_idle_instances: typing.Optional[jsii.Number] = None,
    min_pending_latency: typing.Optional[builtins.str] = None,
    min_total_instances: typing.Optional[jsii.Number] = None,
    network_utilization: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    request_utilization: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14470f1b001c3130ae62f49ae3171aa86927334e92c838eef1038fbfba79367(
    *,
    target_utilization: jsii.Number,
    aggregation_window_length: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b522c72a17cbf9097abc4629b9b5c572bf0fad30f6dad0b828068af606e72ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0590b61246b21a615ba429ba6cdd3a33cd7872c0a6ab4aa5d8f6ecdd0088e199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9610ddb1f8e2b9cfbfe25ecd683075077a37dc183dc895998ee96b163c7170(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41fc8b497af0f4738b1887d0860af246460e8aea51c4895f84cfa78e86b0d6b6(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingCpuUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032867d97978fad13840e98f4a5ec1634ad82dc400cc45cd1a14c647e553a700(
    *,
    target_read_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_read_ops_per_second: typing.Optional[jsii.Number] = None,
    target_write_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_write_ops_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59f7b4dbbaa3cb4e566377372a2169d8d4bf251f31da30651c2b8f953228a96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065fb2adbfa876675d32627b255775d263bb73aac244b83c42c4ed153615c8fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc02b3136d509bf27e435381447862b529a62642ab7706a4c15ee077720ea5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8528a433db6b592e7a2e9391205dfce2198b8ba65fc4d49db4f7335d89b0927e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c240a65ce2f32af9e81564f0d3f2e097c88cffa4847c9b42e519b6d89cc6c60(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61450b64e99a420030f5aae3f60f9f48e840aee2efea7ee9fed2564fe1734077(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingDiskUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec826b8b024f270411c8530001e5fa80a984e67f568e7cecfb0da1b209efe19(
    *,
    target_received_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_received_packets_per_second: typing.Optional[jsii.Number] = None,
    target_sent_bytes_per_second: typing.Optional[jsii.Number] = None,
    target_sent_packets_per_second: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59aca59f956798f46f7230751d46b76f8dad3e8a2855fd46d83fb12dec87dc40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60b7831d3a26080dbe03adb8917e8ee5467090751918c9250033b1043b4c4eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a242803b3534fc6ee8b6a9b7494430e283e0049083ad10e707cdb0f56a971b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6e41ae868451d95cb093ca2fc10e47ee31eb7a35f070476122abd414dc0983(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec412ae7f0431139defceec5e47e059215639ca7aef8f5219f02df84000cfb0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb6608181593e4e3702c80b82cbbb1add24de508b935311e9a28e37a0d86e49(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingNetworkUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407b3691f96a7779517badcb3f2fcbc44ba171ebc9fb834955822d025c6fbfff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6800cbf738045625d061b45ab23e70f1cc338618d332e64a9c5f93af9fff102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4ffa52567e43082817ead8928914c311506153cf2be5a63d504444d623fb3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316d701ccb9921e26e5eafe5d846d15b3be35c4962a3ce15c9270f569008a419(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f610cb9af4075e9f855b4c6af3156d1db3871ea8ca60daa543fec9a3e5427858(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b324df0e550d76a818657fdf19dfa09b9db5c4ac6b51d4841c95121a9c7cf89(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f20a7864b159f51fb5a802843c5dcd064a444ddc0910a9be7d71bcb4034fae7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b235165c060c1b8deb7c0a0242c7a4457e95e0a99a5706861ec766adc4625de8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465cce2b7d929f7933fef159b529d2dfb9fdfedc18bbe75d64f3f0eb376f4aee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94878956e37eb684dbdf8fc50b8b02bd03e19d84bbf7aef9bd8bf61b9eda850c(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba555b0506e67bb74c1e55b384ac25f3bb983ea5fbc84817a8b6cb51fc81257(
    *,
    target_concurrent_requests: typing.Optional[jsii.Number] = None,
    target_request_count_per_second: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3092507c6987380458c4bc9d0d4fa3b19f21524d1cfe36cce95ae2134915db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bfa6aa5c602eb2f8d85e81d98179a3cfdfee057e661e81be86df132ab26815(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b50f66ee392d6b300f21e20fe8e70b50d6ddb1e1ce4db20aa49ee181e4993b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815a6eecd70f2f6af7d9247de9cb6c1f1d1512bebaaa6719544cb925eac0bee5(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionAutomaticScalingRequestUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b81a57febdaaaa747dbba7963f12f7dca4767b1455ca959f554492756652db(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_check: typing.Union[GoogleAppEngineFlexibleAppVersionLivenessCheck, typing.Dict[builtins.str, typing.Any]],
    readiness_check: typing.Union[GoogleAppEngineFlexibleAppVersionReadinessCheck, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    api_config: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionApiConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    automatic_scaling: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    beta_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    default_expiration: typing.Optional[builtins.str] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoints_api_service: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionEndpointsApiService, typing.Dict[builtins.str, typing.Any]]] = None,
    entrypoint: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    flexible_runtime_settings: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    manual_scaling: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    nobuild_files_regex: typing.Optional[builtins.str] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionResources, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    runtime_channel: typing.Optional[builtins.str] = None,
    runtime_main_executable_path: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    serving_status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1685d935397eb1ad852973e788ea74d57a6ae0707b39f733a5b410049092a8f4(
    *,
    cloud_build_options: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    container: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionDeploymentContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zip: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionDeploymentZip, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4385fae4b5bf166063b525d35a05418bad4efb895e308d512824d41d8d3c70c7(
    *,
    app_yaml_path: builtins.str,
    cloud_build_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f074e6d6b5bc63da4f33130261b9c25a67bd4843af86b96834f3fe82e756b4fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce7c8e94b356b0d172a04a527a6a6c9e18cc4012a7f1b659efaaef9b0459c24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c53c61fab55bfe9c75239eed21631d288033953a28af806e92064f0a5134c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7931390e9f855821d4be4184ed46969baf53f3ea9eecd9e382213be42d6d12e1(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentCloudBuildOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725097de818a4e723d5c1cb5f92a4900f2a0856f66f95c17aad0a6d52b2e3ac1(
    *,
    image: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d65fe9d96d0ea7a6082b2d546033f942e97e52cca094c99d306165225166811(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6adb8e636903b83eed8496d1ca3d1383da3e9d98a8a817ad4fc33afe673795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad673daae5c81eac1e8c39d45fc338268f58f4bfe45f2421c3e35f5c4f2bbc7(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35556212b7b3e7ff06e9fe9b3899265bb16eb67e324169b54ec59fc1eac92849(
    *,
    name: builtins.str,
    source_url: builtins.str,
    sha1_sum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358cf449257210f85795ea223f8922c70da5401c6eaae5b0ce36dae1eef036c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896598fc46cdfae22a1162fb8375a1f114a0bf94c262286d8a8a72d99bb4f372(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e26f704b630fb9689e7db66eec551f3795f45f331b3ed89c8889908af8916b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefa53a00887588e7bcaa57f581e3c1bc11868f11f53ef512ff21d5d50716698(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31836eead46d6b733d85a3115fa3fba25ec3e688abbc37500a0e1df8b5f88be9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33639714e2548505ffbb2f3b31c0fec7b6b08c721b546c5d8893a85a757b58b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionDeploymentFiles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ecd1eb0f48dd9904a2b699a8aed3472603544fe0bd5611c42e200bf235f613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a71f1a70cbe1da4873e7977128f6e590361268c17e692dad0266498f04b5f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cea4c658ca8e62d608df93b0ef0238a999072cc604980c5d7f30bf2540e96f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c928c6ebc1c56de692377ba128b0816469073fe22be80bd3a6c19b9ff4f7cbe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621daf0430f5d1305aab2d2d848813ff765f0c1b67cc29a770e232103a484f20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionDeploymentFiles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053ff44a9130a4d0cee6a3eca76ebcc980f2a889e16822d926d0975e23fa9879(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ebc0cadcb456e85147da94ff9376d4593ce3282b800c3f9df363326fbc8562(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e8023d394dcd9c40ec287e18d34f4100d970c5420d02e87db6ed7cc7adbdcb(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca10d35f230e8f0bf8c2dac0aa1342b8c0f8723f329ef986a63933588f4eaf05(
    *,
    source_url: builtins.str,
    files_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a3776177d36f912984457a55a22ccb30e222f8e7ebfe0535bd18ced42fd50d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1274f28d73d0fc2094f053d55304f6f0545a228b60587f155ff09ef163c19e4d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2289db8537277a155bffb3945c8e8f0aabbd5c84a9f1918b2a816db5301a2935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aaf290c6f2aa94bb12d998bcd0ccff3e59ca23f50da81c244ca3306aa87263(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionDeploymentZip],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9681ca3c2839d67e3fae757d39baf11b8c39d3728763801240ca65b80664b9a9(
    *,
    name: builtins.str,
    config_id: typing.Optional[builtins.str] = None,
    disable_trace_sampling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rollout_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d313d0c1281a193f521b460d33379bdaf6e7546ee2f889a3c6c45abbc4122145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0eb2375bca6d4a0514b66cdf33c810e4418a13d8c37884f6b356f670e1fcc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b01578f3060200d57e686121bf82fe1872c8d67a22a0522567b2f726a624bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f16774708e79196c7594035028460a4dc246c5ceef6c042a3083c06b011bb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991a25f50df6e08ce77da5c097b79008375f1b60adf2bc61093b390be888c7eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bdb641311958614166c4e5a2d15db12218c55dd030ecb3e366faca57c88088(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionEndpointsApiService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb2f7d2f951c80672751202e34da09a6dfe066782520202f1f927b7d25806d1(
    *,
    shell: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27fe1c961ac0772cd5e877056074db67dc54e3e61eb1b853f45de9a0f6a9cf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a2328ae3d8ed31e053a90f1c5f1f06355a63e29b859bd8615185429a2bf26c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f1eb791d0cc10263a655f25e6594ce2fc6bd8de9c49e0f4df902d4b012082d(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionEntrypoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4897273ff7cbfc1b7620d18facde392346d6ea8a309c7109aadd55883f952f4b(
    *,
    operating_system: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4eb497fd446522cceded4df1252c29b0bb3887734180812899b440176903f45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1c3cc9a980dd93c06106fe6d23654f9b1372a618a6d6b45b956e251964e508(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ff22005eeef9cdc326a5ea21c7084927d948ccb99d8dbd1310cac8b27506ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94baeb4d98cf178405e9f00fbd0ef41cacc0d7705d74ef332ce21433cdd596e(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionFlexibleRuntimeSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d86d927c5febb409a0069a21f7191b104fe54db33e5789688f93bb44b8a389b(
    *,
    auth_fail_action: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    redirect_http_response_code: typing.Optional[builtins.str] = None,
    script: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionHandlersScript, typing.Dict[builtins.str, typing.Any]]] = None,
    security_level: typing.Optional[builtins.str] = None,
    static_files: typing.Optional[typing.Union[GoogleAppEngineFlexibleAppVersionHandlersStaticFiles, typing.Dict[builtins.str, typing.Any]]] = None,
    url_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7f471e28f818c8659b793f4b39bdf582792d1c6e8d7e5e14fa91d708fb4a1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf56923ab0c19767733f0debbb7e3ae6cdbec45bcb34818ac4701af05071bf82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4df062c70b96edf2bd009825c1bb2d664410923f49411ceae3da40eb92fcc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff172f122591d5ddb6e301e0c975ad70b64549f470cb305b2e6730600786e698(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2116ad016ab8fd770a8d61c9fc4fb4709a74a443b1dc6363831c0c2104f01220(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053017905e1d26f7ef516d3241b61b90540d158064cfb7765cb8dd377970febd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionHandlers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2369897a149014481bb0d11c6cdd4047269d6417209cf0535fecf3aa27a7f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08862dbafa55579242ae7950fceba3653edd57c4a65f248bb2ef3b5e2fc7ee58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5763930a7a5debf520132251728e2f03542fa41bb2d4813f71676f774d992489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c43ce9e1af2c3485da6ab4c145368009baa92767626564b8499097923417409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f653bcf792dc887a41bce4e4d4790cb84d5c46d62d11542371e0aa15a1ad4b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559e0ea64226c1795dab7e612582066e032a5ae47ad7d9fbdd7c9ce95f6a3d60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0a948e0ce32a6ce2f58cb33da9c91eaada70fe084467b8be611ca816e0afa9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionHandlers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c0f5d348f94eec538a83445d3cf336752207298d92880dba21f99138dc2c94(
    *,
    script_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5f50e1548ae443508d70dfc3424ddf1150e16386d7bedc6a615d7ab306b1af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b67c9aeb53c02af547f92eafc646f366cddf1cb6e2d08e1e4130ac7a46549c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf22b62d5210b911ecd5b9efc072b2ee1c8704fd1ffdeee313f2adff3738b9b(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersScript],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d906cce3c50cdbf1f35aac0fb0163eaf6b2cfc45b4128ac383c8f5511e44f91e(
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

def _typecheckingstub__f1edd52a2e5d2ce74958d2c933113f5f18895f12bd8e6eea680d2721ed905c12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ae67d78452a95d009782b3815aa2e3860ffca9c9e01e95c39ce6b1d4385bfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecc3b258834043c52e1f51149e311519f558daa534dcda94eeff7c87b6b4744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a14452b5cab3113e2f6911c66230ad66410d22810f987c775cac436733a3db(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afe3e14a486d8a3b610c54d1ace88057d17892d16f0e178304e3e9a64b18b57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9878c747e7b021f06ccdeb145a45f6bc24ac03324f4a8c99a9977fb5a7a3a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb536baccd3d965a0a953bfd8866b35a795026afa57e8cd23839ef0446ed736c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491cd83e1ee16865ebb302279299212b1093f07200ba099a6ad1f0f4c8c053c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d669cbb9d543ea08f1050b362595a85070032ee3f9a8b6e6c20197a2530402(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionHandlersStaticFiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818f150e5790cf8f86bc6217811b6fba5f0dfe4470206b79a502c7cefd6f949a(
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

def _typecheckingstub__5560d62c618e0b4fbee6e54ff5b04b13ab4c63d443cd96241a0a939fa07cee29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb08ecdf7617408e32dcbda8fcc61e56d71708ee35b6b4c726f831d554b8bd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e780e1d91292b14a0fae70a2797fe70c1cb5573b36310894d2ce7a28c904b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10f6fd1b3e8510867ef5f6bd2172adb619bfd419b7621573742b796dcc37796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b80f9fa46c2844c274cd6dfb509c412d8ff22eee00aa6e84c049d368f527a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d233467d4b979cc2c50e688fc9bec8b7f107061e5a4ad85b814199aaff5a15e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7137561f69e95bbc3beba9b2fe65a42bd8871105521de568b718dcc84f16e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce39f22ec9a31abeef99bc6c798c743fdebc0d2c448e02fe2afdb353c286dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28980ba3b28b7c7aca5dc817c698fcb4725ae1c2a7b060a7ad3cf2c7f022a7d7(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionLivenessCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37589790062fb96fba0eacc227ef512dc3466f0af9d9c27e78ddfb069e744a76(
    *,
    instances: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e47905630928487bb0eebb3eec88710b252c92b4dc89a21a1446c2ad2679e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce4e9338d7ec820248e9580bd9adfe64743009c5212268226d417d2bbec9d4f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce81ea4c026e723b62e4ee6424e5c79785daec667fcbcba697ab0f9df6647aa(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionManualScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d3431197cd2c91add70c0df23df4cb6172a38abe2ecc76dd64fac0b303595d(
    *,
    name: builtins.str,
    forwarded_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_ip_mode: typing.Optional[builtins.str] = None,
    instance_tag: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8253f58436093059c20f29f7c8b953478a504393e6ec56f8662ba78142137358(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5849de554c5962fd90205d37fc733ffe3cfda64a7e0ddee37da8e4b896e26d0f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4065880e0480c7a0d279bfc72837eaba6eb69099e944f6d5ee26ad6149cdb8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273fcd24225c56bcdae62f4179532a3c910ab8f219749c2c1b782076bfb32895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b702d9327708ebbc7fef36c7ccf9791b0830587328e8b087d5cdbdb9f20fe07e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93d4e549b1cdbeebcc28e5d64e97f8971b16eb407bdb744babb1c2a198ee769(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0aee2dda6ef05513739c1d08daafa2168767447ddc39c074badfc141ac7528f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993f45e569f136d9c38f409316b385d3655de1caf5a17a4cd906029dce957fc6(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf260d42bcd39ad625e109d7d8a2a31b1d29918af596fe774917b5d99e97b78(
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

def _typecheckingstub__6b890ffa0b4fd044b129c1ab81875bffaba66c910fe33f3ca3aa98b98cb7043b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e3e6259ff0b49e9c34f13f379d4eeb670705df267ac29088cf94702698f29b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48c6df09662f8ee874ff198ad55d736489aaf63bf5f23ceb0822ac8b96c05c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08362366b81bbd619fe6c2d644c9a43a90bed96b43b972979f7554fe51a275cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cf11178fee91d7b6452d56e462b3924a40e70029f893c4450419e9e9725c6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec28a827d652f72e1f9e799c227cc603a2ffa8415b8c65438dcc7975270f244(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dc2c3b23306f0166513a10e839ebe05be5aedce3732c34b28934d4efe0c1fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf467620bb294df873e4d383e42e8549f9cb5ba726eeaf3d5a8684b86040a21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287de96397183aa1a9e99486701299c202c337481cca88176f9d9e893d7badd2(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionReadinessCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7173859d8329c561587249226d66a139da020046ea1bde1c143fe55431aa96f9(
    *,
    cpu: typing.Optional[jsii.Number] = None,
    disk_gb: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionResourcesVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010f49d95f3dfbb537a80706c304675b97b9c900f5dd231d65d3ec68047eff86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99706bf11f7ce5d8607e222cdc594a0c89f77815439028d9f270eca11c2ac4ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineFlexibleAppVersionResourcesVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a539a2d6106bae8bd6c1d2c24fce91adcf3b58885d80fe68345df17a54ce7945(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2766e2e42e350cfba722fd32e55eec026d657658fc314609905487d763f11c06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9830c6637cbd874cacd53814f95b9f04360ac27db76e1cbc7be824620c26ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487eff5278a9929186258191e6bfc1fff2dc18821a6629b3a16d17f8c4717945(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a90a1d32cbba74826b27dc1aab5ed2fea0aaae24cc1c64e1e4808e0cbffaa7a(
    *,
    name: builtins.str,
    size_gb: jsii.Number,
    volume_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910061867ad9b1bb5f9daee0b2d116c411c086d28f7dbe7fe1ec5f1deada6628(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb8eb345b1dbe2b088e452e7a6b30fdf26bf739b22a1bb52a9d5abe14396aaa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9193be3b1e0b9e08b60c52f0077999cd277e5a28d88ad84d396b9a68ef35c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c48074faa25519184a89f324a64541afb17cb862afefb19af69bdc5b204b6d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2f0a62c02c1881dcbd170b0b5005ff5c34ff292c725a14b0cbf385be1be37f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422f9fc9b4e968eb24bf864ff85cdb1be75bd20a829127bc96029579034350c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineFlexibleAppVersionResourcesVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa97421f7b6e1097c17d8e2e938a93ec9ad722c726fa9f792da5976b45409a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5430c77fa637ed598d3e3e6071e3506c21e0019bac08e15bc8a890012c80a193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820e493be2efd867ea51dc3b9595490ab3d4ac673f5eba86d4d88e575542fc7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d8dc71bea8b8b13b988b5c9467d3e02b405097d56b4fd0ca2462eb3a284162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce982b617cc3141167d214a19f8396bec240c426cf196040c4eebe506d20176(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionResourcesVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec3c3a3df5a093f8fbc41e87304e8ea93d502ff964869e09fcd06cc3357f385(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d51e13215dce077ac6461dd7a3794a780f9d9d1257382379c4303740a20516(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c65605f55ec3ce8b6f4f345000c42d479e4e56708726793f70636d1af930c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962f7bdf3f4c8e12e9e8833e9fc38ec6b7605f537f2240dd4285eafb7e10cef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96117eaf1c6ce9f21bfc196653ec9ff30e04ad7994d4b7f6552ac83722452a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4058cc2a52e6923da39e0d14e020b6736fc1259238842c2e4ec36a7b1a3cf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineFlexibleAppVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ccb6b8075c7107e6bc795149de976f36b0e94ec3795bb755d87ac27e0f4a03(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de50a76764b325c4ba75ce6976175ee8eb01553a9e45175b7dd88ba7c926ad09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce0ecc6e1c3f131e2ab38a25f328dd16b4148e46cc5e670492ba0c23abe2ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ff4629204f9ef4b25c1e587f5d5921d3b3f34d826a563b105e590a91156048(
    value: typing.Optional[GoogleAppEngineFlexibleAppVersionVpcAccessConnector],
) -> None:
    """Type checking stubs"""
    pass
