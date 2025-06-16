r'''
# `google_app_engine_standard_app_version`

Refer to the Terraform Registry for docs: [`google_app_engine_standard_app_version`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version).
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


class GoogleAppEngineStandardAppVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version google_app_engine_standard_app_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        deployment: typing.Union["GoogleAppEngineStandardAppVersionDeployment", typing.Dict[builtins.str, typing.Any]],
        entrypoint: typing.Union["GoogleAppEngineStandardAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_scaling: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionAutomaticScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_scaling: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionBasicScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionLibraries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manual_scaling: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version google_app_engine_standard_app_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#deployment GoogleAppEngineStandardAppVersion#deployment}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#entrypoint GoogleAppEngineStandardAppVersion#entrypoint}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#runtime GoogleAppEngineStandardAppVersion#runtime}
        :param service: AppEngine service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#service GoogleAppEngineStandardAppVersion#service}
        :param app_engine_apis: Allows App Engine second generation runtimes to access the legacy bundled services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#app_engine_apis GoogleAppEngineStandardAppVersion#app_engine_apis}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#automatic_scaling GoogleAppEngineStandardAppVersion#automatic_scaling}
        :param basic_scaling: basic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#basic_scaling GoogleAppEngineStandardAppVersion#basic_scaling}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#delete_service_on_destroy GoogleAppEngineStandardAppVersion#delete_service_on_destroy}
        :param env_variables: Environment variables available to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#env_variables GoogleAppEngineStandardAppVersion#env_variables}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#handlers GoogleAppEngineStandardAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#id GoogleAppEngineStandardAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#inbound_services GoogleAppEngineStandardAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G BasicScaling or ManualScaling: B1, B2, B4, B4_1G, B8 Defaults to F1 for AutomaticScaling and B2 for ManualScaling and BasicScaling. If no scaling is specified, AutomaticScaling is chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#instance_class GoogleAppEngineStandardAppVersion#instance_class}
        :param libraries: libraries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#libraries GoogleAppEngineStandardAppVersion#libraries}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#manual_scaling GoogleAppEngineStandardAppVersion#manual_scaling}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#noop_on_destroy GoogleAppEngineStandardAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#project GoogleAppEngineStandardAppVersion#project}.
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#runtime_api_version GoogleAppEngineStandardAppVersion#runtime_api_version}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#service_account GoogleAppEngineStandardAppVersion#service_account}
        :param threadsafe: Whether multiple requests can be dispatched to this version at once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#threadsafe GoogleAppEngineStandardAppVersion#threadsafe}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#timeouts GoogleAppEngineStandardAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#version_id GoogleAppEngineStandardAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#vpc_access_connector GoogleAppEngineStandardAppVersion#vpc_access_connector}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03999203be11fc8ddef0f75d3463eab226b445b4b2364918672c366917a7c0e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleAppEngineStandardAppVersionConfig(
            deployment=deployment,
            entrypoint=entrypoint,
            runtime=runtime,
            service=service,
            app_engine_apis=app_engine_apis,
            automatic_scaling=automatic_scaling,
            basic_scaling=basic_scaling,
            delete_service_on_destroy=delete_service_on_destroy,
            env_variables=env_variables,
            handlers=handlers,
            id=id,
            inbound_services=inbound_services,
            instance_class=instance_class,
            libraries=libraries,
            manual_scaling=manual_scaling,
            noop_on_destroy=noop_on_destroy,
            project=project,
            runtime_api_version=runtime_api_version,
            service_account=service_account,
            threadsafe=threadsafe,
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
        '''Generates CDKTF code for importing a GoogleAppEngineStandardAppVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleAppEngineStandardAppVersion to import.
        :param import_from_id: The id of the existing GoogleAppEngineStandardAppVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleAppEngineStandardAppVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f57b8e3a51eccfd37090cb3294549dadc2eaf99f442266c9f4733cd7e97a73c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomaticScaling")
    def put_automatic_scaling(
        self,
        *,
        max_concurrent_requests: typing.Optional[jsii.Number] = None,
        max_idle_instances: typing.Optional[jsii.Number] = None,
        max_pending_latency: typing.Optional[builtins.str] = None,
        min_idle_instances: typing.Optional[jsii.Number] = None,
        min_pending_latency: typing.Optional[builtins.str] = None,
        standard_scheduler_settings: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_concurrent_requests GoogleAppEngineStandardAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_idle_instances GoogleAppEngineStandardAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_pending_latency GoogleAppEngineStandardAppVersion#max_pending_latency}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_idle_instances GoogleAppEngineStandardAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_pending_latency GoogleAppEngineStandardAppVersion#min_pending_latency}
        :param standard_scheduler_settings: standard_scheduler_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#standard_scheduler_settings GoogleAppEngineStandardAppVersion#standard_scheduler_settings}
        '''
        value = GoogleAppEngineStandardAppVersionAutomaticScaling(
            max_concurrent_requests=max_concurrent_requests,
            max_idle_instances=max_idle_instances,
            max_pending_latency=max_pending_latency,
            min_idle_instances=min_idle_instances,
            min_pending_latency=min_pending_latency,
            standard_scheduler_settings=standard_scheduler_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAutomaticScaling", [value]))

    @jsii.member(jsii_name="putBasicScaling")
    def put_basic_scaling(
        self,
        *,
        max_instances: jsii.Number,
        idle_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances to create for this version. Must be in the range [1.0, 200.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_instances GoogleAppEngineStandardAppVersion#max_instances}
        :param idle_timeout: Duration of time after the last request that an instance must wait before the instance is shut down. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#idle_timeout GoogleAppEngineStandardAppVersion#idle_timeout}
        '''
        value = GoogleAppEngineStandardAppVersionBasicScaling(
            max_instances=max_instances, idle_timeout=idle_timeout
        )

        return typing.cast(None, jsii.invoke(self, "putBasicScaling", [value]))

    @jsii.member(jsii_name="putDeployment")
    def put_deployment(
        self,
        *,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#files GoogleAppEngineStandardAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#zip GoogleAppEngineStandardAppVersion#zip}
        '''
        value = GoogleAppEngineStandardAppVersionDeployment(files=files, zip=zip)

        return typing.cast(None, jsii.invoke(self, "putDeployment", [value]))

    @jsii.member(jsii_name="putEntrypoint")
    def put_entrypoint(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#shell GoogleAppEngineStandardAppVersion#shell}
        '''
        value = GoogleAppEngineStandardAppVersionEntrypoint(shell=shell)

        return typing.cast(None, jsii.invoke(self, "putEntrypoint", [value]))

    @jsii.member(jsii_name="putHandlers")
    def put_handlers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78842e2bfb3434758aa06b565ce432fe0229f19c41a0fe56776c27b4ff4f5914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHandlers", [value]))

    @jsii.member(jsii_name="putLibraries")
    def put_libraries(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionLibraries", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f88e489700bcd5c1de434e034594c4200aa3041b9494fb28324a23b4c3da1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLibraries", [value]))

    @jsii.member(jsii_name="putManualScaling")
    def put_manual_scaling(self, *, instances: jsii.Number) -> None:
        '''
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#instances GoogleAppEngineStandardAppVersion#instances}
        '''
        value = GoogleAppEngineStandardAppVersionManualScaling(instances=instances)

        return typing.cast(None, jsii.invoke(self, "putManualScaling", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#create GoogleAppEngineStandardAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#delete GoogleAppEngineStandardAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#update GoogleAppEngineStandardAppVersion#update}.
        '''
        value = GoogleAppEngineStandardAppVersionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcAccessConnector")
    def put_vpc_access_connector(
        self,
        *,
        name: builtins.str,
        egress_setting: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#name GoogleAppEngineStandardAppVersion#name}
        :param egress_setting: The egress setting for the connector, controlling what traffic is diverted through it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#egress_setting GoogleAppEngineStandardAppVersion#egress_setting}
        '''
        value = GoogleAppEngineStandardAppVersionVpcAccessConnector(
            name=name, egress_setting=egress_setting
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccessConnector", [value]))

    @jsii.member(jsii_name="resetAppEngineApis")
    def reset_app_engine_apis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineApis", []))

    @jsii.member(jsii_name="resetAutomaticScaling")
    def reset_automatic_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticScaling", []))

    @jsii.member(jsii_name="resetBasicScaling")
    def reset_basic_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicScaling", []))

    @jsii.member(jsii_name="resetDeleteServiceOnDestroy")
    def reset_delete_service_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteServiceOnDestroy", []))

    @jsii.member(jsii_name="resetEnvVariables")
    def reset_env_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvVariables", []))

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

    @jsii.member(jsii_name="resetLibraries")
    def reset_libraries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLibraries", []))

    @jsii.member(jsii_name="resetManualScaling")
    def reset_manual_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualScaling", []))

    @jsii.member(jsii_name="resetNoopOnDestroy")
    def reset_noop_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoopOnDestroy", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRuntimeApiVersion")
    def reset_runtime_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeApiVersion", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetThreadsafe")
    def reset_threadsafe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreadsafe", []))

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
    @jsii.member(jsii_name="automaticScaling")
    def automatic_scaling(
        self,
    ) -> "GoogleAppEngineStandardAppVersionAutomaticScalingOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionAutomaticScalingOutputReference", jsii.get(self, "automaticScaling"))

    @builtins.property
    @jsii.member(jsii_name="basicScaling")
    def basic_scaling(
        self,
    ) -> "GoogleAppEngineStandardAppVersionBasicScalingOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionBasicScalingOutputReference", jsii.get(self, "basicScaling"))

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(
        self,
    ) -> "GoogleAppEngineStandardAppVersionDeploymentOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionDeploymentOutputReference", jsii.get(self, "deployment"))

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(
        self,
    ) -> "GoogleAppEngineStandardAppVersionEntrypointOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionEntrypointOutputReference", jsii.get(self, "entrypoint"))

    @builtins.property
    @jsii.member(jsii_name="handlers")
    def handlers(self) -> "GoogleAppEngineStandardAppVersionHandlersList":
        return typing.cast("GoogleAppEngineStandardAppVersionHandlersList", jsii.get(self, "handlers"))

    @builtins.property
    @jsii.member(jsii_name="libraries")
    def libraries(self) -> "GoogleAppEngineStandardAppVersionLibrariesList":
        return typing.cast("GoogleAppEngineStandardAppVersionLibrariesList", jsii.get(self, "libraries"))

    @builtins.property
    @jsii.member(jsii_name="manualScaling")
    def manual_scaling(
        self,
    ) -> "GoogleAppEngineStandardAppVersionManualScalingOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionManualScalingOutputReference", jsii.get(self, "manualScaling"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleAppEngineStandardAppVersionTimeoutsOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnector")
    def vpc_access_connector(
        self,
    ) -> "GoogleAppEngineStandardAppVersionVpcAccessConnectorOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionVpcAccessConnectorOutputReference", jsii.get(self, "vpcAccessConnector"))

    @builtins.property
    @jsii.member(jsii_name="appEngineApisInput")
    def app_engine_apis_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "appEngineApisInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticScalingInput")
    def automatic_scaling_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionAutomaticScaling"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionAutomaticScaling"], jsii.get(self, "automaticScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="basicScalingInput")
    def basic_scaling_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionBasicScaling"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionBasicScaling"], jsii.get(self, "basicScalingInput"))

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
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionDeployment"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionDeployment"], jsii.get(self, "deploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="entrypointInput")
    def entrypoint_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionEntrypoint"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionEntrypoint"], jsii.get(self, "entrypointInput"))

    @builtins.property
    @jsii.member(jsii_name="envVariablesInput")
    def env_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="handlersInput")
    def handlers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionHandlers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionHandlers"]]], jsii.get(self, "handlersInput"))

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
    @jsii.member(jsii_name="librariesInput")
    def libraries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionLibraries"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionLibraries"]]], jsii.get(self, "librariesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualScalingInput")
    def manual_scaling_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionManualScaling"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionManualScaling"], jsii.get(self, "manualScalingInput"))

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
    @jsii.member(jsii_name="runtimeApiVersionInput")
    def runtime_api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeApiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="threadsafeInput")
    def threadsafe_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "threadsafeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAppEngineStandardAppVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAppEngineStandardAppVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionIdInput")
    def version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnectorInput")
    def vpc_access_connector_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionVpcAccessConnector"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionVpcAccessConnector"], jsii.get(self, "vpcAccessConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="appEngineApis")
    def app_engine_apis(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "appEngineApis"))

    @app_engine_apis.setter
    def app_engine_apis(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18183043ad9723c7b22589d5cdd1db7e0ee7de16538f98dc2d4e4ded0ef9541f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appEngineApis", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__05c0890a90980b289fd97dafb012245f95ac8d03e105b833826fcac9ce02041a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteServiceOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envVariables")
    def env_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "envVariables"))

    @env_variables.setter
    def env_variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b5eb93396b25e2123c166ea34e0568cddcf094a2683f955518b5557f6af8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed758c2094aea6cfe13c58fced71de5cc14b5017427b6dcbbf384ee62317203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundServices")
    def inbound_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inboundServices"))

    @inbound_services.setter
    def inbound_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c60b2d0d7afcaa9f150e647f3804fc5ba71bd64d23762d351cfe903f89f442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceClass")
    def instance_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceClass"))

    @instance_class.setter
    def instance_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab7ce3352e06e3049542a8b8ee02f02c87527a73e3536c6107b73d6a67e9cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceClass", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__8d10e449cf16c243e464ea16c9ffbd135de74eeb4fb70445174872d0fc04c13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noopOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9076c90200e919b2ed6b1f7ecee3218955e1ec7dd6c6f312ebc118e370827b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f59b1cd43529e0b0a169ec5e99c2f09f32da10ebebe92cf936a76008986cff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeApiVersion")
    def runtime_api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeApiVersion"))

    @runtime_api_version.setter
    def runtime_api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb6603b939010a42dc170dfec311e2fd12e3dd78ac6f18d28882522bdadf65c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d603a1f75ed147e193080323b93f7c85ce5aec22c8324e05a760c1e8f802807d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010eae1d08236e80dde272bebc105ae37e7e21b80a687a0ffbb4b3c3e4f69ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadsafe")
    def threadsafe(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "threadsafe"))

    @threadsafe.setter
    def threadsafe(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3953ad308ea11ca7bdf2ded2b551a7ce8c8ba61f1cbfe7a93930dc065c9aa4c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsafe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7777b3fedbcf43ec7a123fb5cea93022862883ce9719f857676d6cb925c7f540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionAutomaticScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_requests": "maxConcurrentRequests",
        "max_idle_instances": "maxIdleInstances",
        "max_pending_latency": "maxPendingLatency",
        "min_idle_instances": "minIdleInstances",
        "min_pending_latency": "minPendingLatency",
        "standard_scheduler_settings": "standardSchedulerSettings",
    },
)
class GoogleAppEngineStandardAppVersionAutomaticScaling:
    def __init__(
        self,
        *,
        max_concurrent_requests: typing.Optional[jsii.Number] = None,
        max_idle_instances: typing.Optional[jsii.Number] = None,
        max_pending_latency: typing.Optional[builtins.str] = None,
        min_idle_instances: typing.Optional[jsii.Number] = None,
        min_pending_latency: typing.Optional[builtins.str] = None,
        standard_scheduler_settings: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_concurrent_requests GoogleAppEngineStandardAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_idle_instances GoogleAppEngineStandardAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_pending_latency GoogleAppEngineStandardAppVersion#max_pending_latency}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_idle_instances GoogleAppEngineStandardAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_pending_latency GoogleAppEngineStandardAppVersion#min_pending_latency}
        :param standard_scheduler_settings: standard_scheduler_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#standard_scheduler_settings GoogleAppEngineStandardAppVersion#standard_scheduler_settings}
        '''
        if isinstance(standard_scheduler_settings, dict):
            standard_scheduler_settings = GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings(**standard_scheduler_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3f8af2cb7b730c973998babff1584a5e940cc5834da9d90f95709c8b2ebb03)
            check_type(argname="argument max_concurrent_requests", value=max_concurrent_requests, expected_type=type_hints["max_concurrent_requests"])
            check_type(argname="argument max_idle_instances", value=max_idle_instances, expected_type=type_hints["max_idle_instances"])
            check_type(argname="argument max_pending_latency", value=max_pending_latency, expected_type=type_hints["max_pending_latency"])
            check_type(argname="argument min_idle_instances", value=min_idle_instances, expected_type=type_hints["min_idle_instances"])
            check_type(argname="argument min_pending_latency", value=min_pending_latency, expected_type=type_hints["min_pending_latency"])
            check_type(argname="argument standard_scheduler_settings", value=standard_scheduler_settings, expected_type=type_hints["standard_scheduler_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_requests is not None:
            self._values["max_concurrent_requests"] = max_concurrent_requests
        if max_idle_instances is not None:
            self._values["max_idle_instances"] = max_idle_instances
        if max_pending_latency is not None:
            self._values["max_pending_latency"] = max_pending_latency
        if min_idle_instances is not None:
            self._values["min_idle_instances"] = min_idle_instances
        if min_pending_latency is not None:
            self._values["min_pending_latency"] = min_pending_latency
        if standard_scheduler_settings is not None:
            self._values["standard_scheduler_settings"] = standard_scheduler_settings

    @builtins.property
    def max_concurrent_requests(self) -> typing.Optional[jsii.Number]:
        '''Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance.

        Defaults to a runtime-specific value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_concurrent_requests GoogleAppEngineStandardAppVersion#max_concurrent_requests}
        '''
        result = self._values.get("max_concurrent_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle instances that should be maintained for this version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_idle_instances GoogleAppEngineStandardAppVersion#max_idle_instances}
        '''
        result = self._values.get("max_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_pending_latency GoogleAppEngineStandardAppVersion#max_pending_latency}
        '''
        result = self._values.get("max_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of idle instances that should be maintained for this version.

        Only applicable for the default version of a service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_idle_instances GoogleAppEngineStandardAppVersion#min_idle_instances}
        '''
        result = self._values.get("min_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_pending_latency GoogleAppEngineStandardAppVersion#min_pending_latency}
        '''
        result = self._values.get("min_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standard_scheduler_settings(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"]:
        '''standard_scheduler_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#standard_scheduler_settings GoogleAppEngineStandardAppVersion#standard_scheduler_settings}
        '''
        result = self._values.get("standard_scheduler_settings")
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionAutomaticScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionAutomaticScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionAutomaticScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe2bd8f2de4db5d331196d492efceb61c4c5506cf9ae7d5c698a125fe241b16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStandardSchedulerSettings")
    def put_standard_scheduler_settings(
        self,
        *,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        target_cpu_utilization: typing.Optional[jsii.Number] = None,
        target_throughput_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances to run for this version. Set to zero to disable maxInstances configuration. **Note:** Starting from March 2025, App Engine sets the maxInstances default for standard environment deployments to 20. This change doesn't impact existing apps. To override the default, specify a new value between 0 and 2147483647, and deploy a new version or redeploy over an existing version. To disable the maxInstances default configuration setting, specify the maximum permitted value 2147483647. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_instances GoogleAppEngineStandardAppVersion#max_instances}
        :param min_instances: Minimum number of instances to run for this version. Set to zero to disable minInstances configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_instances GoogleAppEngineStandardAppVersion#min_instances}
        :param target_cpu_utilization: Target CPU utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#target_cpu_utilization GoogleAppEngineStandardAppVersion#target_cpu_utilization}
        :param target_throughput_utilization: Target throughput utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#target_throughput_utilization GoogleAppEngineStandardAppVersion#target_throughput_utilization}
        '''
        value = GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings(
            max_instances=max_instances,
            min_instances=min_instances,
            target_cpu_utilization=target_cpu_utilization,
            target_throughput_utilization=target_throughput_utilization,
        )

        return typing.cast(None, jsii.invoke(self, "putStandardSchedulerSettings", [value]))

    @jsii.member(jsii_name="resetMaxConcurrentRequests")
    def reset_max_concurrent_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentRequests", []))

    @jsii.member(jsii_name="resetMaxIdleInstances")
    def reset_max_idle_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleInstances", []))

    @jsii.member(jsii_name="resetMaxPendingLatency")
    def reset_max_pending_latency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPendingLatency", []))

    @jsii.member(jsii_name="resetMinIdleInstances")
    def reset_min_idle_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinIdleInstances", []))

    @jsii.member(jsii_name="resetMinPendingLatency")
    def reset_min_pending_latency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinPendingLatency", []))

    @jsii.member(jsii_name="resetStandardSchedulerSettings")
    def reset_standard_scheduler_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandardSchedulerSettings", []))

    @builtins.property
    @jsii.member(jsii_name="standardSchedulerSettings")
    def standard_scheduler_settings(
        self,
    ) -> "GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference", jsii.get(self, "standardSchedulerSettings"))

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
    @jsii.member(jsii_name="minIdleInstancesInput")
    def min_idle_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minIdleInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minPendingLatencyInput")
    def min_pending_latency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minPendingLatencyInput"))

    @builtins.property
    @jsii.member(jsii_name="standardSchedulerSettingsInput")
    def standard_scheduler_settings_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"], jsii.get(self, "standardSchedulerSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRequests")
    def max_concurrent_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentRequests"))

    @max_concurrent_requests.setter
    def max_concurrent_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82f297e48a4fe40872e8bf6c1db35ac6904a732c6ffceaf44c0e9d3170ef1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIdleInstances")
    def max_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleInstances"))

    @max_idle_instances.setter
    def max_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1b8f8b13eea87622b051a4a70f284c755441179edcc4e35e603f08448605d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingLatency")
    def max_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxPendingLatency"))

    @max_pending_latency.setter
    def max_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fe7c2a7194bcd7e16b37f764daac3c1000d1d9dc37593ea2705d23ad0159d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minIdleInstances")
    def min_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minIdleInstances"))

    @min_idle_instances.setter
    def min_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce52b7232774ccc894d6788e512abccedf7c2092e9a9e53329b86aa757100c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minPendingLatency")
    def min_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minPendingLatency"))

    @min_pending_latency.setter
    def min_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07296faa7480333a153ce7963007b1f1d767fd0d64e2e3ae6aac9f4bab3420db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScaling]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba79f5a87df4e08555b11a5920bb60abb14eba9b92f8b0f1b46fae3a0811c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_instances": "maxInstances",
        "min_instances": "minInstances",
        "target_cpu_utilization": "targetCpuUtilization",
        "target_throughput_utilization": "targetThroughputUtilization",
    },
)
class GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings:
    def __init__(
        self,
        *,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        target_cpu_utilization: typing.Optional[jsii.Number] = None,
        target_throughput_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances to run for this version. Set to zero to disable maxInstances configuration. **Note:** Starting from March 2025, App Engine sets the maxInstances default for standard environment deployments to 20. This change doesn't impact existing apps. To override the default, specify a new value between 0 and 2147483647, and deploy a new version or redeploy over an existing version. To disable the maxInstances default configuration setting, specify the maximum permitted value 2147483647. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_instances GoogleAppEngineStandardAppVersion#max_instances}
        :param min_instances: Minimum number of instances to run for this version. Set to zero to disable minInstances configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_instances GoogleAppEngineStandardAppVersion#min_instances}
        :param target_cpu_utilization: Target CPU utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#target_cpu_utilization GoogleAppEngineStandardAppVersion#target_cpu_utilization}
        :param target_throughput_utilization: Target throughput utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#target_throughput_utilization GoogleAppEngineStandardAppVersion#target_throughput_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb577d2ea0a79dc40c0bc69455794e2057ce63bf2d7f1e1ab6c14abd6d35213)
            check_type(argname="argument max_instances", value=max_instances, expected_type=type_hints["max_instances"])
            check_type(argname="argument min_instances", value=min_instances, expected_type=type_hints["min_instances"])
            check_type(argname="argument target_cpu_utilization", value=target_cpu_utilization, expected_type=type_hints["target_cpu_utilization"])
            check_type(argname="argument target_throughput_utilization", value=target_throughput_utilization, expected_type=type_hints["target_throughput_utilization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instances is not None:
            self._values["max_instances"] = max_instances
        if min_instances is not None:
            self._values["min_instances"] = min_instances
        if target_cpu_utilization is not None:
            self._values["target_cpu_utilization"] = target_cpu_utilization
        if target_throughput_utilization is not None:
            self._values["target_throughput_utilization"] = target_throughput_utilization

    @builtins.property
    def max_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of instances to run for this version. Set to zero to disable maxInstances configuration.

        **Note:** Starting from March 2025, App Engine sets the maxInstances default for standard environment deployments to 20. This change doesn't impact existing apps. To override the default, specify a new value between 0 and 2147483647, and deploy a new version or redeploy over an existing version. To disable the maxInstances default configuration setting, specify the maximum permitted value 2147483647.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_instances GoogleAppEngineStandardAppVersion#max_instances}
        '''
        result = self._values.get("max_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of instances to run for this version. Set to zero to disable minInstances configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#min_instances GoogleAppEngineStandardAppVersion#min_instances}
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cpu_utilization(self) -> typing.Optional[jsii.Number]:
        '''Target CPU utilization ratio to maintain when scaling.

        Should be a value in the range [0.50, 0.95], zero, or a negative value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#target_cpu_utilization GoogleAppEngineStandardAppVersion#target_cpu_utilization}
        '''
        result = self._values.get("target_cpu_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_throughput_utilization(self) -> typing.Optional[jsii.Number]:
        '''Target throughput utilization ratio to maintain when scaling.

        Should be a value in the range [0.50, 0.95], zero, or a negative value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#target_throughput_utilization GoogleAppEngineStandardAppVersion#target_throughput_utilization}
        '''
        result = self._values.get("target_throughput_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df8c6cc892a48ccf25dc88613e174887546d955f571d9291cc084ed9efe3cc93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstances")
    def reset_max_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstances", []))

    @jsii.member(jsii_name="resetMinInstances")
    def reset_min_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstances", []))

    @jsii.member(jsii_name="resetTargetCpuUtilization")
    def reset_target_cpu_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCpuUtilization", []))

    @jsii.member(jsii_name="resetTargetThroughputUtilization")
    def reset_target_throughput_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetThroughputUtilization", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstancesInput")
    def max_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstancesInput")
    def min_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCpuUtilizationInput")
    def target_cpu_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetCpuUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="targetThroughputUtilizationInput")
    def target_throughput_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetThroughputUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db72d8f7a633e502aec939f4a55bc0fa7598c4d3bb0624ffc9b6b905fa9466a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @min_instances.setter
    def min_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ce56663695fb3e0ea2a9951ff40642f71a439f2626087872da8b9fdb47bcaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCpuUtilization")
    def target_cpu_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetCpuUtilization"))

    @target_cpu_utilization.setter
    def target_cpu_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39234659a64627aa317e44dc0381b3c12df709525e57fbc8f54daea383b1270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCpuUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetThroughputUtilization")
    def target_throughput_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetThroughputUtilization"))

    @target_throughput_utilization.setter
    def target_throughput_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c260ac704cb6af08fd1ae1ba656c4039b897d5c807b757678274f9e7b9e1e671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetThroughputUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c454b93c09ac34ec049df2d1d8eeed8562ef33b1842f899e79db3cc57281fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionBasicScaling",
    jsii_struct_bases=[],
    name_mapping={"max_instances": "maxInstances", "idle_timeout": "idleTimeout"},
)
class GoogleAppEngineStandardAppVersionBasicScaling:
    def __init__(
        self,
        *,
        max_instances: jsii.Number,
        idle_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances to create for this version. Must be in the range [1.0, 200.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_instances GoogleAppEngineStandardAppVersion#max_instances}
        :param idle_timeout: Duration of time after the last request that an instance must wait before the instance is shut down. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#idle_timeout GoogleAppEngineStandardAppVersion#idle_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a47614e1d315f0dbe3e92013e8ca888e35ee68f848700874b942b236cb7b9fcf)
            check_type(argname="argument max_instances", value=max_instances, expected_type=type_hints["max_instances"])
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_instances": max_instances,
        }
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout

    @builtins.property
    def max_instances(self) -> jsii.Number:
        '''Maximum number of instances to create for this version. Must be in the range [1.0, 200.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#max_instances GoogleAppEngineStandardAppVersion#max_instances}
        '''
        result = self._values.get("max_instances")
        assert result is not None, "Required property 'max_instances' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional[builtins.str]:
        '''Duration of time after the last request that an instance must wait before the instance is shut down.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#idle_timeout GoogleAppEngineStandardAppVersion#idle_timeout}
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionBasicScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionBasicScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionBasicScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__749e7b1e6bdd637f591f5b9f70b02f975cd77cc526c884ff7fed28bc6c13c852)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdleTimeout")
    def reset_idle_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInput")
    def idle_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idleTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstancesInput")
    def max_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeout")
    def idle_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleTimeout"))

    @idle_timeout.setter
    def idle_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ae6cd8e6d1d6593370c0011568bd9383186f411fd8f6272126d4d4f6c62952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc2e4536b1fdd7e05a987baf91e2cc0b88626d35ce2928a1538e082727749ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionBasicScaling]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionBasicScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionBasicScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd726a15c0d43c960285d313ba1420fd7a652352b2b1306ced95a77dff179cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "deployment": "deployment",
        "entrypoint": "entrypoint",
        "runtime": "runtime",
        "service": "service",
        "app_engine_apis": "appEngineApis",
        "automatic_scaling": "automaticScaling",
        "basic_scaling": "basicScaling",
        "delete_service_on_destroy": "deleteServiceOnDestroy",
        "env_variables": "envVariables",
        "handlers": "handlers",
        "id": "id",
        "inbound_services": "inboundServices",
        "instance_class": "instanceClass",
        "libraries": "libraries",
        "manual_scaling": "manualScaling",
        "noop_on_destroy": "noopOnDestroy",
        "project": "project",
        "runtime_api_version": "runtimeApiVersion",
        "service_account": "serviceAccount",
        "threadsafe": "threadsafe",
        "timeouts": "timeouts",
        "version_id": "versionId",
        "vpc_access_connector": "vpcAccessConnector",
    },
)
class GoogleAppEngineStandardAppVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        deployment: typing.Union["GoogleAppEngineStandardAppVersionDeployment", typing.Dict[builtins.str, typing.Any]],
        entrypoint: typing.Union["GoogleAppEngineStandardAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        basic_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionBasicScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionLibraries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manual_scaling: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#deployment GoogleAppEngineStandardAppVersion#deployment}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#entrypoint GoogleAppEngineStandardAppVersion#entrypoint}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#runtime GoogleAppEngineStandardAppVersion#runtime}
        :param service: AppEngine service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#service GoogleAppEngineStandardAppVersion#service}
        :param app_engine_apis: Allows App Engine second generation runtimes to access the legacy bundled services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#app_engine_apis GoogleAppEngineStandardAppVersion#app_engine_apis}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#automatic_scaling GoogleAppEngineStandardAppVersion#automatic_scaling}
        :param basic_scaling: basic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#basic_scaling GoogleAppEngineStandardAppVersion#basic_scaling}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#delete_service_on_destroy GoogleAppEngineStandardAppVersion#delete_service_on_destroy}
        :param env_variables: Environment variables available to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#env_variables GoogleAppEngineStandardAppVersion#env_variables}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#handlers GoogleAppEngineStandardAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#id GoogleAppEngineStandardAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#inbound_services GoogleAppEngineStandardAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G BasicScaling or ManualScaling: B1, B2, B4, B4_1G, B8 Defaults to F1 for AutomaticScaling and B2 for ManualScaling and BasicScaling. If no scaling is specified, AutomaticScaling is chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#instance_class GoogleAppEngineStandardAppVersion#instance_class}
        :param libraries: libraries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#libraries GoogleAppEngineStandardAppVersion#libraries}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#manual_scaling GoogleAppEngineStandardAppVersion#manual_scaling}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#noop_on_destroy GoogleAppEngineStandardAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#project GoogleAppEngineStandardAppVersion#project}.
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#runtime_api_version GoogleAppEngineStandardAppVersion#runtime_api_version}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#service_account GoogleAppEngineStandardAppVersion#service_account}
        :param threadsafe: Whether multiple requests can be dispatched to this version at once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#threadsafe GoogleAppEngineStandardAppVersion#threadsafe}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#timeouts GoogleAppEngineStandardAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#version_id GoogleAppEngineStandardAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#vpc_access_connector GoogleAppEngineStandardAppVersion#vpc_access_connector}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deployment, dict):
            deployment = GoogleAppEngineStandardAppVersionDeployment(**deployment)
        if isinstance(entrypoint, dict):
            entrypoint = GoogleAppEngineStandardAppVersionEntrypoint(**entrypoint)
        if isinstance(automatic_scaling, dict):
            automatic_scaling = GoogleAppEngineStandardAppVersionAutomaticScaling(**automatic_scaling)
        if isinstance(basic_scaling, dict):
            basic_scaling = GoogleAppEngineStandardAppVersionBasicScaling(**basic_scaling)
        if isinstance(manual_scaling, dict):
            manual_scaling = GoogleAppEngineStandardAppVersionManualScaling(**manual_scaling)
        if isinstance(timeouts, dict):
            timeouts = GoogleAppEngineStandardAppVersionTimeouts(**timeouts)
        if isinstance(vpc_access_connector, dict):
            vpc_access_connector = GoogleAppEngineStandardAppVersionVpcAccessConnector(**vpc_access_connector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb5bb527fc5f4092681ddd7656417f24224f25ddee38eaece1fbb71c75ef5f5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument app_engine_apis", value=app_engine_apis, expected_type=type_hints["app_engine_apis"])
            check_type(argname="argument automatic_scaling", value=automatic_scaling, expected_type=type_hints["automatic_scaling"])
            check_type(argname="argument basic_scaling", value=basic_scaling, expected_type=type_hints["basic_scaling"])
            check_type(argname="argument delete_service_on_destroy", value=delete_service_on_destroy, expected_type=type_hints["delete_service_on_destroy"])
            check_type(argname="argument env_variables", value=env_variables, expected_type=type_hints["env_variables"])
            check_type(argname="argument handlers", value=handlers, expected_type=type_hints["handlers"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inbound_services", value=inbound_services, expected_type=type_hints["inbound_services"])
            check_type(argname="argument instance_class", value=instance_class, expected_type=type_hints["instance_class"])
            check_type(argname="argument libraries", value=libraries, expected_type=type_hints["libraries"])
            check_type(argname="argument manual_scaling", value=manual_scaling, expected_type=type_hints["manual_scaling"])
            check_type(argname="argument noop_on_destroy", value=noop_on_destroy, expected_type=type_hints["noop_on_destroy"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument runtime_api_version", value=runtime_api_version, expected_type=type_hints["runtime_api_version"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument threadsafe", value=threadsafe, expected_type=type_hints["threadsafe"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument vpc_access_connector", value=vpc_access_connector, expected_type=type_hints["vpc_access_connector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment": deployment,
            "entrypoint": entrypoint,
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
        if app_engine_apis is not None:
            self._values["app_engine_apis"] = app_engine_apis
        if automatic_scaling is not None:
            self._values["automatic_scaling"] = automatic_scaling
        if basic_scaling is not None:
            self._values["basic_scaling"] = basic_scaling
        if delete_service_on_destroy is not None:
            self._values["delete_service_on_destroy"] = delete_service_on_destroy
        if env_variables is not None:
            self._values["env_variables"] = env_variables
        if handlers is not None:
            self._values["handlers"] = handlers
        if id is not None:
            self._values["id"] = id
        if inbound_services is not None:
            self._values["inbound_services"] = inbound_services
        if instance_class is not None:
            self._values["instance_class"] = instance_class
        if libraries is not None:
            self._values["libraries"] = libraries
        if manual_scaling is not None:
            self._values["manual_scaling"] = manual_scaling
        if noop_on_destroy is not None:
            self._values["noop_on_destroy"] = noop_on_destroy
        if project is not None:
            self._values["project"] = project
        if runtime_api_version is not None:
            self._values["runtime_api_version"] = runtime_api_version
        if service_account is not None:
            self._values["service_account"] = service_account
        if threadsafe is not None:
            self._values["threadsafe"] = threadsafe
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
    def deployment(self) -> "GoogleAppEngineStandardAppVersionDeployment":
        '''deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#deployment GoogleAppEngineStandardAppVersion#deployment}
        '''
        result = self._values.get("deployment")
        assert result is not None, "Required property 'deployment' is missing"
        return typing.cast("GoogleAppEngineStandardAppVersionDeployment", result)

    @builtins.property
    def entrypoint(self) -> "GoogleAppEngineStandardAppVersionEntrypoint":
        '''entrypoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#entrypoint GoogleAppEngineStandardAppVersion#entrypoint}
        '''
        result = self._values.get("entrypoint")
        assert result is not None, "Required property 'entrypoint' is missing"
        return typing.cast("GoogleAppEngineStandardAppVersionEntrypoint", result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''Desired runtime. Example python27.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#runtime GoogleAppEngineStandardAppVersion#runtime}
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''AppEngine service resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#service GoogleAppEngineStandardAppVersion#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_apis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows App Engine second generation runtimes to access the legacy bundled services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#app_engine_apis GoogleAppEngineStandardAppVersion#app_engine_apis}
        '''
        result = self._values.get("app_engine_apis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def automatic_scaling(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScaling]:
        '''automatic_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#automatic_scaling GoogleAppEngineStandardAppVersion#automatic_scaling}
        '''
        result = self._values.get("automatic_scaling")
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScaling], result)

    @builtins.property
    def basic_scaling(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionBasicScaling]:
        '''basic_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#basic_scaling GoogleAppEngineStandardAppVersion#basic_scaling}
        '''
        result = self._values.get("basic_scaling")
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionBasicScaling], result)

    @builtins.property
    def delete_service_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the service will be deleted if it is the last version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#delete_service_on_destroy GoogleAppEngineStandardAppVersion#delete_service_on_destroy}
        '''
        result = self._values.get("delete_service_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def env_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables available to the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#env_variables GoogleAppEngineStandardAppVersion#env_variables}
        '''
        result = self._values.get("env_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def handlers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionHandlers"]]]:
        '''handlers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#handlers GoogleAppEngineStandardAppVersion#handlers}
        '''
        result = self._values.get("handlers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionHandlers"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#id GoogleAppEngineStandardAppVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inbound_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the types of messages that this application is able to receive.

        Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#inbound_services GoogleAppEngineStandardAppVersion#inbound_services}
        '''
        result = self._values.get("inbound_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_class(self) -> typing.Optional[builtins.str]:
        '''Instance class that is used to run this version.

        Valid values are
        AutomaticScaling: F1, F2, F4, F4_1G
        BasicScaling or ManualScaling: B1, B2, B4, B4_1G, B8
        Defaults to F1 for AutomaticScaling and B2 for ManualScaling and BasicScaling. If no scaling is specified, AutomaticScaling is chosen.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#instance_class GoogleAppEngineStandardAppVersion#instance_class}
        '''
        result = self._values.get("instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def libraries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionLibraries"]]]:
        '''libraries block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#libraries GoogleAppEngineStandardAppVersion#libraries}
        '''
        result = self._values.get("libraries")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionLibraries"]]], result)

    @builtins.property
    def manual_scaling(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionManualScaling"]:
        '''manual_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#manual_scaling GoogleAppEngineStandardAppVersion#manual_scaling}
        '''
        result = self._values.get("manual_scaling")
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionManualScaling"], result)

    @builtins.property
    def noop_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the application version will not be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#noop_on_destroy GoogleAppEngineStandardAppVersion#noop_on_destroy}
        '''
        result = self._values.get("noop_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#project GoogleAppEngineStandardAppVersion#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_api_version(self) -> typing.Optional[builtins.str]:
        '''The version of the API in the given runtime environment.

        Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref'
        Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#runtime_api_version GoogleAppEngineStandardAppVersion#runtime_api_version}
        '''
        result = self._values.get("runtime_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The identity that the deployed version will run as.

        Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#service_account GoogleAppEngineStandardAppVersion#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threadsafe(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether multiple requests can be dispatched to this version at once.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#threadsafe GoogleAppEngineStandardAppVersion#threadsafe}
        '''
        result = self._values.get("threadsafe")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleAppEngineStandardAppVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#timeouts GoogleAppEngineStandardAppVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionTimeouts"], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Relative name of the version within the service.

        For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#version_id GoogleAppEngineStandardAppVersion#version_id}
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_access_connector(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionVpcAccessConnector"]:
        '''vpc_access_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#vpc_access_connector GoogleAppEngineStandardAppVersion#vpc_access_connector}
        '''
        result = self._values.get("vpc_access_connector")
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionVpcAccessConnector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionDeployment",
    jsii_struct_bases=[],
    name_mapping={"files": "files", "zip": "zip"},
)
class GoogleAppEngineStandardAppVersionDeployment:
    def __init__(
        self,
        *,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAppEngineStandardAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#files GoogleAppEngineStandardAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#zip GoogleAppEngineStandardAppVersion#zip}
        '''
        if isinstance(zip, dict):
            zip = GoogleAppEngineStandardAppVersionDeploymentZip(**zip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b65780657d5c9e3722546e781eba68b74d24d6f7100cd7e3c719380753e73c)
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument zip", value=zip, expected_type=type_hints["zip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if files is not None:
            self._values["files"] = files
        if zip is not None:
            self._values["zip"] = zip

    @builtins.property
    def files(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionDeploymentFiles"]]]:
        '''files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#files GoogleAppEngineStandardAppVersion#files}
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAppEngineStandardAppVersionDeploymentFiles"]]], result)

    @builtins.property
    def zip(self) -> typing.Optional["GoogleAppEngineStandardAppVersionDeploymentZip"]:
        '''zip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#zip GoogleAppEngineStandardAppVersion#zip}
        '''
        result = self._values.get("zip")
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionDeploymentZip"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionDeploymentFiles",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "source_url": "sourceUrl", "sha1_sum": "sha1Sum"},
)
class GoogleAppEngineStandardAppVersionDeploymentFiles:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_url: builtins.str,
        sha1_sum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#name GoogleAppEngineStandardAppVersion#name}.
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#source_url GoogleAppEngineStandardAppVersion#source_url}
        :param sha1_sum: SHA1 checksum of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#sha1_sum GoogleAppEngineStandardAppVersion#sha1_sum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e92dedc442f2bc6d97a4d228b5aff52cba40210cc85e65576ab3949cc408d2b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#name GoogleAppEngineStandardAppVersion#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_url(self) -> builtins.str:
        '''Source URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#source_url GoogleAppEngineStandardAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha1_sum(self) -> typing.Optional[builtins.str]:
        '''SHA1 checksum of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#sha1_sum GoogleAppEngineStandardAppVersion#sha1_sum}
        '''
        result = self._values.get("sha1_sum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionDeploymentFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionDeploymentFilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionDeploymentFilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9512cf9fc5b770af2c4303ede555b35b9957fd500ce077b7394ed7cb27611357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAppEngineStandardAppVersionDeploymentFilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b127000f820a5c11cde24f55045ef3b11e0bcada629c72cf95746ba7f4fea0b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAppEngineStandardAppVersionDeploymentFilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f52a2bc6accceb0cb269eb43b2ae4bfa3529e3421c47ff58f6802bc3fcaecf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f0f1040ca3da3ed523d0d0da4be6349ef2c50e851d97ec26d2d9175dbd95a0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7358e1534bb300237deca3aafdf5a41353cd350aafe9cb024ae92f19e796bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionDeploymentFiles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionDeploymentFiles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b7cedb9ca0d710d2749c1a161930f9ce2c43d887bb1453c444010e761270d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineStandardAppVersionDeploymentFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionDeploymentFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__801173fb73a42324fdd6c155e7f3409bd0935bcc899b5e600592b673367b6ad9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__812b0d27449e59c8c16784226fbaf3af47851381f3045cf646a7e16fd791ee8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sha1Sum")
    def sha1_sum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1Sum"))

    @sha1_sum.setter
    def sha1_sum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a7280bbef721e890954524e8fa4893ed404635aa1a5df4be79010cb758fac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha1Sum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02de84fbb18793195b0abc3498053d0a5897913d3f569908dfe7bdf6c4799e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionDeploymentFiles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionDeploymentFiles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionDeploymentFiles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8e78da9df261b0c4da4eb0db0605e20cd2e25c37b82266fb1ed8742bedfa6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineStandardAppVersionDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b7d809649a5fe006325ba526298aacc029a893a8c1245348125fdc505249e30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFiles")
    def put_files(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b6f91216c81e369ac18f1a143f65b224eae1665c36299c3213d09932929bd4)
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
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#source_url GoogleAppEngineStandardAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#files_count GoogleAppEngineStandardAppVersion#files_count}
        '''
        value = GoogleAppEngineStandardAppVersionDeploymentZip(
            source_url=source_url, files_count=files_count
        )

        return typing.cast(None, jsii.invoke(self, "putZip", [value]))

    @jsii.member(jsii_name="resetFiles")
    def reset_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFiles", []))

    @jsii.member(jsii_name="resetZip")
    def reset_zip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZip", []))

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> GoogleAppEngineStandardAppVersionDeploymentFilesList:
        return typing.cast(GoogleAppEngineStandardAppVersionDeploymentFilesList, jsii.get(self, "files"))

    @builtins.property
    @jsii.member(jsii_name="zip")
    def zip(self) -> "GoogleAppEngineStandardAppVersionDeploymentZipOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionDeploymentZipOutputReference", jsii.get(self, "zip"))

    @builtins.property
    @jsii.member(jsii_name="filesInput")
    def files_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionDeploymentFiles]]], jsii.get(self, "filesInput"))

    @builtins.property
    @jsii.member(jsii_name="zipInput")
    def zip_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionDeploymentZip"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionDeploymentZip"], jsii.get(self, "zipInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionDeployment]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ab679dab946d23c5de28dc47d31aa01243d07dcf4abdcb639fdeb44b3efe95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionDeploymentZip",
    jsii_struct_bases=[],
    name_mapping={"source_url": "sourceUrl", "files_count": "filesCount"},
)
class GoogleAppEngineStandardAppVersionDeploymentZip:
    def __init__(
        self,
        *,
        source_url: builtins.str,
        files_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#source_url GoogleAppEngineStandardAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#files_count GoogleAppEngineStandardAppVersion#files_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55dad9ac6442fd05a7431bd709eb79b73bbc224e173a07ac9987959115bab056)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#source_url GoogleAppEngineStandardAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def files_count(self) -> typing.Optional[jsii.Number]:
        '''files count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#files_count GoogleAppEngineStandardAppVersion#files_count}
        '''
        result = self._values.get("files_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionDeploymentZip(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionDeploymentZipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionDeploymentZipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae83819ba3840179a031e991e4b9f9513d399aa42fc7e42cbc4d8f2f2c2b966)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b11edfca10c2cb2c377738882b8474e278486861bf89e3a30271e0b59aab794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181876e3d345cd6c1783cf5d0804b02cdc49ebaf32c74fd35e0714c4bf8cbaa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionDeploymentZip]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionDeploymentZip], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionDeploymentZip],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7176871c7983535f84876ae1550d3a6b611e6c01a4f334702ac08cc82140608b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionEntrypoint",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell"},
)
class GoogleAppEngineStandardAppVersionEntrypoint:
    def __init__(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#shell GoogleAppEngineStandardAppVersion#shell}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf93da80859e556c5b2468ba7da6ead38b105e41991b5e147c77ae7e75f6b0f7)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "shell": shell,
        }

    @builtins.property
    def shell(self) -> builtins.str:
        '''The format should be a shell command that can be fed to bash -c.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#shell GoogleAppEngineStandardAppVersion#shell}
        '''
        result = self._values.get("shell")
        assert result is not None, "Required property 'shell' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionEntrypoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionEntrypointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionEntrypointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a35c443be5385cfaee0b7bd5c239c17af44325d9b45300fbeb830071d97e31d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cedbb57060ef3e53024e4f4e796de5cbeecae67322a6e38ea2bb119dbb5aee76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionEntrypoint]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionEntrypoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionEntrypoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb16ab6fb78f51e41da66f61fd89eacb5bb076fcfd33dce5311777bb80ec7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionHandlers",
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
class GoogleAppEngineStandardAppVersionHandlers:
    def __init__(
        self,
        *,
        auth_fail_action: typing.Optional[builtins.str] = None,
        login: typing.Optional[builtins.str] = None,
        redirect_http_response_code: typing.Optional[builtins.str] = None,
        script: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionHandlersScript", typing.Dict[builtins.str, typing.Any]]] = None,
        security_level: typing.Optional[builtins.str] = None,
        static_files: typing.Optional[typing.Union["GoogleAppEngineStandardAppVersionHandlersStaticFiles", typing.Dict[builtins.str, typing.Any]]] = None,
        url_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_fail_action: Actions to take when the user is not logged in. Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#auth_fail_action GoogleAppEngineStandardAppVersion#auth_fail_action}
        :param login: Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#login GoogleAppEngineStandardAppVersion#login}
        :param redirect_http_response_code: 30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#redirect_http_response_code GoogleAppEngineStandardAppVersion#redirect_http_response_code}
        :param script: script block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#script GoogleAppEngineStandardAppVersion#script}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#security_level GoogleAppEngineStandardAppVersion#security_level}
        :param static_files: static_files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#static_files GoogleAppEngineStandardAppVersion#static_files}
        :param url_regex: URL prefix. Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings. All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#url_regex GoogleAppEngineStandardAppVersion#url_regex}
        '''
        if isinstance(script, dict):
            script = GoogleAppEngineStandardAppVersionHandlersScript(**script)
        if isinstance(static_files, dict):
            static_files = GoogleAppEngineStandardAppVersionHandlersStaticFiles(**static_files)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5836dc214c579532e82b74b7bbf216671ac2a4a7db8bb02853b1600267b9f4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#auth_fail_action GoogleAppEngineStandardAppVersion#auth_fail_action}
        '''
        result = self._values.get("auth_fail_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login(self) -> typing.Optional[builtins.str]:
        '''Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#login GoogleAppEngineStandardAppVersion#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_http_response_code(self) -> typing.Optional[builtins.str]:
        '''30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#redirect_http_response_code GoogleAppEngineStandardAppVersion#redirect_http_response_code}
        '''
        result = self._values.get("redirect_http_response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionHandlersScript"]:
        '''script block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#script GoogleAppEngineStandardAppVersion#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionHandlersScript"], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#security_level GoogleAppEngineStandardAppVersion#security_level}
        '''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_files(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionHandlersStaticFiles"]:
        '''static_files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#static_files GoogleAppEngineStandardAppVersion#static_files}
        '''
        result = self._values.get("static_files")
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionHandlersStaticFiles"], result)

    @builtins.property
    def url_regex(self) -> typing.Optional[builtins.str]:
        '''URL prefix.

        Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings.
        All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#url_regex GoogleAppEngineStandardAppVersion#url_regex}
        '''
        result = self._values.get("url_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionHandlers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionHandlersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionHandlersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__464e0954637cb47f53ff017f9cc51c53cc164193574209bb342030eda0a2604d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAppEngineStandardAppVersionHandlersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5d30b9d6bd1c97b76d87af17be81ff16943b05a99c763a38e9a4465af4abe2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAppEngineStandardAppVersionHandlersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7364cbfbc354105da5a9db5d4e12422ca463d7d4e609964bb64b90b480538cb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5ec1e9ae625b33e8f46d104d673c746872629b9ed3188a896082ab93fe7408)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4640b22d55fffa55e6b7ce129d2918ef4e2f457cd4e001f6a192f553c82059f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionHandlers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionHandlers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionHandlers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc176a48230bba25dd0b0225bb74385712593f1219233803f392594bc707b3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineStandardAppVersionHandlersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionHandlersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7be34501de3c4dc9682d78e4da2979a15e4c90312a8d7ba1f96d99ba334f7d2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putScript")
    def put_script(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#script_path GoogleAppEngineStandardAppVersion#script_path}
        '''
        value = GoogleAppEngineStandardAppVersionHandlersScript(
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
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#application_readable GoogleAppEngineStandardAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#expiration GoogleAppEngineStandardAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#http_headers GoogleAppEngineStandardAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#mime_type GoogleAppEngineStandardAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#path GoogleAppEngineStandardAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#require_matching_file GoogleAppEngineStandardAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#upload_path_regex GoogleAppEngineStandardAppVersion#upload_path_regex}
        '''
        value = GoogleAppEngineStandardAppVersionHandlersStaticFiles(
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
    ) -> "GoogleAppEngineStandardAppVersionHandlersScriptOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionHandlersScriptOutputReference", jsii.get(self, "script"))

    @builtins.property
    @jsii.member(jsii_name="staticFiles")
    def static_files(
        self,
    ) -> "GoogleAppEngineStandardAppVersionHandlersStaticFilesOutputReference":
        return typing.cast("GoogleAppEngineStandardAppVersionHandlersStaticFilesOutputReference", jsii.get(self, "staticFiles"))

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
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionHandlersScript"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionHandlersScript"], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="securityLevelInput")
    def security_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="staticFilesInput")
    def static_files_input(
        self,
    ) -> typing.Optional["GoogleAppEngineStandardAppVersionHandlersStaticFiles"]:
        return typing.cast(typing.Optional["GoogleAppEngineStandardAppVersionHandlersStaticFiles"], jsii.get(self, "staticFilesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ebb45c42fe2fdfca2cb2a50fd4a12eb343d851001dfc4a31d9a8585afbc6a447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authFailAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "login"))

    @login.setter
    def login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8188301026c3d5930a901b08a3c8693427b476e6908e1a0786e6ca98ba11a939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "login", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectHttpResponseCode")
    def redirect_http_response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectHttpResponseCode"))

    @redirect_http_response_code.setter
    def redirect_http_response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c38d8f94c07d9dd77265f9663faac185b46781ede7f4896730a5d181094368c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectHttpResponseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @security_level.setter
    def security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c00784aab7e4b7ca5bd23c7ca49b97dbe6964137ead558be7bc5ff55cfcc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlRegex")
    def url_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlRegex"))

    @url_regex.setter
    def url_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49873257cadebb10327bdfbf5435f723e1d7d0a5f025b43ec5b09fe77829ac5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionHandlers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionHandlers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionHandlers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350a3fadc45d5c3d7822c1c4798f0639d0008df6afeb1bcd812ce4f1431bfbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionHandlersScript",
    jsii_struct_bases=[],
    name_mapping={"script_path": "scriptPath"},
)
class GoogleAppEngineStandardAppVersionHandlersScript:
    def __init__(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#script_path GoogleAppEngineStandardAppVersion#script_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a712c55c184629f47691e539b5b78d50fe01de6f1a61c7cc2a18a0ed48984c9)
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script_path": script_path,
        }

    @builtins.property
    def script_path(self) -> builtins.str:
        '''Path to the script from the application root directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#script_path GoogleAppEngineStandardAppVersion#script_path}
        '''
        result = self._values.get("script_path")
        assert result is not None, "Required property 'script_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionHandlersScript(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionHandlersScriptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionHandlersScriptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67a5a8b86f08fd901c91376dfb7ec270198a652e19ed7e8c20da11a697bab2c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11881269acfc9e9f475ea8445e5b927b10b5b8eca188fe1e99d757c9966e9ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionHandlersScript]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionHandlersScript], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionHandlersScript],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37e2af3d66bd75854f9c82f6dfe25a971465701b391a0e100eff784d114df4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionHandlersStaticFiles",
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
class GoogleAppEngineStandardAppVersionHandlersStaticFiles:
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
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#application_readable GoogleAppEngineStandardAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#expiration GoogleAppEngineStandardAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#http_headers GoogleAppEngineStandardAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#mime_type GoogleAppEngineStandardAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#path GoogleAppEngineStandardAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#require_matching_file GoogleAppEngineStandardAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#upload_path_regex GoogleAppEngineStandardAppVersion#upload_path_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba273e4db4a533e63c005058ce8de5d411e5ba9a4a3bc256acb8c046660fd9fa)
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

        By default, files declared in static file handlers are uploaded as
        static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged
        against both your code and static data storage resource quotas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#application_readable GoogleAppEngineStandardAppVersion#application_readable}
        '''
        result = self._values.get("application_readable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Time a static file served by this handler should be cached by web proxies and browsers.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#expiration GoogleAppEngineStandardAppVersion#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#http_headers GoogleAppEngineStandardAppVersion#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mime_type(self) -> typing.Optional[builtins.str]:
        '''MIME type used to serve all files served by this handler.

        Defaults to file-specific MIME types, which are derived from each file's filename extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#mime_type GoogleAppEngineStandardAppVersion#mime_type}
        '''
        result = self._values.get("mime_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to the static files matched by the URL pattern, from the application root directory.

        The path can refer to text matched in groupings in the URL pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#path GoogleAppEngineStandardAppVersion#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_matching_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this handler should match the request if the file referenced by the handler does not exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#require_matching_file GoogleAppEngineStandardAppVersion#require_matching_file}
        '''
        result = self._values.get("require_matching_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upload_path_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression that matches the file paths for all files that should be referenced by this handler.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#upload_path_regex GoogleAppEngineStandardAppVersion#upload_path_regex}
        '''
        result = self._values.get("upload_path_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionHandlersStaticFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionHandlersStaticFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionHandlersStaticFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46a7021df4244f69a865378cc322daf453435a6b6bc5b77ed5769f69f07284cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab495ae828148b197809b1a7d7af5180f39d1bd35d2a6b7e0e1c170535132348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationReadable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0424c12131fbc20ba65596326f4c04d59a6e21cee445c337b3b71fb6645a6dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "httpHeaders"))

    @http_headers.setter
    def http_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4508539c295b117e94960528599d1e02adb41a8f11b3d71a74994defb814944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mimeType")
    def mime_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mimeType"))

    @mime_type.setter
    def mime_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5afda7c7dd4ed408d41686a88df6e0f4a8303f9e91cdc6716b30be2985e4355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mimeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad9a21725b331b266abb08153e38a940c6640453d3afe665f4d84dd7865ffce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8868479680becab8ffae286d8c98a65d3b5714707b924e6b812194265ba1d948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireMatchingFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadPathRegex")
    def upload_path_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uploadPathRegex"))

    @upload_path_regex.setter
    def upload_path_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2d849ac5013333a315fe66bd5079ae0be717ef0c46ea4e9e18a940f4ffdc97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadPathRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionHandlersStaticFiles]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionHandlersStaticFiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionHandlersStaticFiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0504b152e9ba212a65e9c78e2a4882f6b76d59e06a4c9e281d761a1a2340ab9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionLibraries",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "version": "version"},
)
class GoogleAppEngineStandardAppVersionLibraries:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the library. Example "django". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#name GoogleAppEngineStandardAppVersion#name}
        :param version: Version of the library to select, or "latest". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#version GoogleAppEngineStandardAppVersion#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e25717bdc96214774b1953d9740eaf1955debfb992734081b53c1ec65772332)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the library. Example "django".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#name GoogleAppEngineStandardAppVersion#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the library to select, or "latest".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#version GoogleAppEngineStandardAppVersion#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionLibraries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionLibrariesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionLibrariesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c1ef1b2fb3dd94ef97dca86c68943f3bbedfcf358eb076a648d6c25cc97f71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAppEngineStandardAppVersionLibrariesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ea0451286b102fcbdfe3628338015e3aeb266d52d8487813aee427864aa1a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAppEngineStandardAppVersionLibrariesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ed8428483fcfec42a67ba7f0295b3ca435ac2ed7bbd85d858f25b2529ba007)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5aba63e0b3e4d8c11d62813e62b2daeebf6fc05e3acc6546ec08b29246f0cca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__661b19ced123f52fc632cefd29793bbe4aa564b83fd832aba82a6c536fe9c9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionLibraries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionLibraries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionLibraries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9c38900f0208578bc02176386df770ae8c92d7f68431254eea17bfba8c075e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAppEngineStandardAppVersionLibrariesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionLibrariesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78472ed57cda20284a7ac503de07aff82b073ad491085ba95000bcbd00abefb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a8546ddfa20fd92f17f13ac1fc7738e6097542985f7a6d2eb5801afc4065c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6f048eb8e9fe1079f73df0621e66446bebf6185bceace09987598717002018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionLibraries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionLibraries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionLibraries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8b9d9e289154a32784aeb6354d8e3ce04df4938f000d14c664ee100972cc89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionManualScaling",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class GoogleAppEngineStandardAppVersionManualScaling:
    def __init__(self, *, instances: jsii.Number) -> None:
        '''
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#instances GoogleAppEngineStandardAppVersion#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b4065e241a8f2c45965069408e4a377713e76d19410bc9327bb20a98def396)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instances": instances,
        }

    @builtins.property
    def instances(self) -> jsii.Number:
        '''Number of instances to assign to the service at the start.

        **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2
        Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#instances GoogleAppEngineStandardAppVersion#instances}
        '''
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionManualScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionManualScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionManualScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80f75ec8bbd75c79d592b3490e89c237c7c899a07ecd3f514b1061ba736c0ac4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b987a259cb363ebce93d23003d4a0bba0e0d45d8fe5415c530e33fd049052b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionManualScaling]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionManualScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionManualScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacec0071265488971fbf6e9b5c8421c555ec51114007c803b5e709e2fb6801f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleAppEngineStandardAppVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#create GoogleAppEngineStandardAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#delete GoogleAppEngineStandardAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#update GoogleAppEngineStandardAppVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cdcd547d41b165a899106c850f82dee61c2d8e7e8c50ec5bbd295827d2f7a8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#create GoogleAppEngineStandardAppVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#delete GoogleAppEngineStandardAppVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#update GoogleAppEngineStandardAppVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a5dc9bb99181de19821f5c9de43241e595619372a3b693ecfadb62a1169b068)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7047e0e89db973f875cfcbb079854ac190ac411e9ad0104c5ddb96b88539d9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158aaa0df08b1edfaa65d7aeec2a9ba24d6c9ebd12087f7b5dfdb1760e7b9046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e3e3d78ba8b28d68dc1c8d484bccff08ae3d3d9127f2f0dcc3e22d65b397f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3d45a1392981446d7d068b66b4106342bd14d23c56d11703605a77feeb9228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionVpcAccessConnector",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "egress_setting": "egressSetting"},
)
class GoogleAppEngineStandardAppVersionVpcAccessConnector:
    def __init__(
        self,
        *,
        name: builtins.str,
        egress_setting: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#name GoogleAppEngineStandardAppVersion#name}
        :param egress_setting: The egress setting for the connector, controlling what traffic is diverted through it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#egress_setting GoogleAppEngineStandardAppVersion#egress_setting}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fd9df19b081824425b67964b9f7484bec959ddb463ff8980ba6ea1390e6842)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument egress_setting", value=egress_setting, expected_type=type_hints["egress_setting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if egress_setting is not None:
            self._values["egress_setting"] = egress_setting

    @builtins.property
    def name(self) -> builtins.str:
        '''Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#name GoogleAppEngineStandardAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def egress_setting(self) -> typing.Optional[builtins.str]:
        '''The egress setting for the connector, controlling what traffic is diverted through it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_app_engine_standard_app_version#egress_setting GoogleAppEngineStandardAppVersion#egress_setting}
        '''
        result = self._values.get("egress_setting")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAppEngineStandardAppVersionVpcAccessConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAppEngineStandardAppVersionVpcAccessConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAppEngineStandardAppVersion.GoogleAppEngineStandardAppVersionVpcAccessConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91315812617ec825f174d33f444fd17435480e888c3eebee70b6f43b095381f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEgressSetting")
    def reset_egress_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressSetting", []))

    @builtins.property
    @jsii.member(jsii_name="egressSettingInput")
    def egress_setting_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "egressSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="egressSetting")
    def egress_setting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egressSetting"))

    @egress_setting.setter
    def egress_setting(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c34b294661663e5d0e5d0b34d348578a6344ad7da4c1e395d1047ddde133264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressSetting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce80b11541a1ee97a284c08fc8348cff554cf907e57c18164f5cafbf1d61d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAppEngineStandardAppVersionVpcAccessConnector]:
        return typing.cast(typing.Optional[GoogleAppEngineStandardAppVersionVpcAccessConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAppEngineStandardAppVersionVpcAccessConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8de8eb8b5228b859f8752d8c59002c81e293de4e2bb99ce25b2cd1478f4cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleAppEngineStandardAppVersion",
    "GoogleAppEngineStandardAppVersionAutomaticScaling",
    "GoogleAppEngineStandardAppVersionAutomaticScalingOutputReference",
    "GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings",
    "GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference",
    "GoogleAppEngineStandardAppVersionBasicScaling",
    "GoogleAppEngineStandardAppVersionBasicScalingOutputReference",
    "GoogleAppEngineStandardAppVersionConfig",
    "GoogleAppEngineStandardAppVersionDeployment",
    "GoogleAppEngineStandardAppVersionDeploymentFiles",
    "GoogleAppEngineStandardAppVersionDeploymentFilesList",
    "GoogleAppEngineStandardAppVersionDeploymentFilesOutputReference",
    "GoogleAppEngineStandardAppVersionDeploymentOutputReference",
    "GoogleAppEngineStandardAppVersionDeploymentZip",
    "GoogleAppEngineStandardAppVersionDeploymentZipOutputReference",
    "GoogleAppEngineStandardAppVersionEntrypoint",
    "GoogleAppEngineStandardAppVersionEntrypointOutputReference",
    "GoogleAppEngineStandardAppVersionHandlers",
    "GoogleAppEngineStandardAppVersionHandlersList",
    "GoogleAppEngineStandardAppVersionHandlersOutputReference",
    "GoogleAppEngineStandardAppVersionHandlersScript",
    "GoogleAppEngineStandardAppVersionHandlersScriptOutputReference",
    "GoogleAppEngineStandardAppVersionHandlersStaticFiles",
    "GoogleAppEngineStandardAppVersionHandlersStaticFilesOutputReference",
    "GoogleAppEngineStandardAppVersionLibraries",
    "GoogleAppEngineStandardAppVersionLibrariesList",
    "GoogleAppEngineStandardAppVersionLibrariesOutputReference",
    "GoogleAppEngineStandardAppVersionManualScaling",
    "GoogleAppEngineStandardAppVersionManualScalingOutputReference",
    "GoogleAppEngineStandardAppVersionTimeouts",
    "GoogleAppEngineStandardAppVersionTimeoutsOutputReference",
    "GoogleAppEngineStandardAppVersionVpcAccessConnector",
    "GoogleAppEngineStandardAppVersionVpcAccessConnectorOutputReference",
]

publication.publish()

def _typecheckingstub__03999203be11fc8ddef0f75d3463eab226b445b4b2364918672c366917a7c0e7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    deployment: typing.Union[GoogleAppEngineStandardAppVersionDeployment, typing.Dict[builtins.str, typing.Any]],
    entrypoint: typing.Union[GoogleAppEngineStandardAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionBasicScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionLibraries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manual_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2f57b8e3a51eccfd37090cb3294549dadc2eaf99f442266c9f4733cd7e97a73c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78842e2bfb3434758aa06b565ce432fe0229f19c41a0fe56776c27b4ff4f5914(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f88e489700bcd5c1de434e034594c4200aa3041b9494fb28324a23b4c3da1d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionLibraries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18183043ad9723c7b22589d5cdd1db7e0ee7de16538f98dc2d4e4ded0ef9541f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c0890a90980b289fd97dafb012245f95ac8d03e105b833826fcac9ce02041a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b5eb93396b25e2123c166ea34e0568cddcf094a2683f955518b5557f6af8f4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed758c2094aea6cfe13c58fced71de5cc14b5017427b6dcbbf384ee62317203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c60b2d0d7afcaa9f150e647f3804fc5ba71bd64d23762d351cfe903f89f442(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab7ce3352e06e3049542a8b8ee02f02c87527a73e3536c6107b73d6a67e9cd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d10e449cf16c243e464ea16c9ffbd135de74eeb4fb70445174872d0fc04c13a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9076c90200e919b2ed6b1f7ecee3218955e1ec7dd6c6f312ebc118e370827b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f59b1cd43529e0b0a169ec5e99c2f09f32da10ebebe92cf936a76008986cff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb6603b939010a42dc170dfec311e2fd12e3dd78ac6f18d28882522bdadf65c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d603a1f75ed147e193080323b93f7c85ce5aec22c8324e05a760c1e8f802807d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010eae1d08236e80dde272bebc105ae37e7e21b80a687a0ffbb4b3c3e4f69ef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3953ad308ea11ca7bdf2ded2b551a7ce8c8ba61f1cbfe7a93930dc065c9aa4c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7777b3fedbcf43ec7a123fb5cea93022862883ce9719f857676d6cb925c7f540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3f8af2cb7b730c973998babff1584a5e940cc5834da9d90f95709c8b2ebb03(
    *,
    max_concurrent_requests: typing.Optional[jsii.Number] = None,
    max_idle_instances: typing.Optional[jsii.Number] = None,
    max_pending_latency: typing.Optional[builtins.str] = None,
    min_idle_instances: typing.Optional[jsii.Number] = None,
    min_pending_latency: typing.Optional[builtins.str] = None,
    standard_scheduler_settings: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe2bd8f2de4db5d331196d492efceb61c4c5506cf9ae7d5c698a125fe241b16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82f297e48a4fe40872e8bf6c1db35ac6904a732c6ffceaf44c0e9d3170ef1b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1b8f8b13eea87622b051a4a70f284c755441179edcc4e35e603f08448605d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fe7c2a7194bcd7e16b37f764daac3c1000d1d9dc37593ea2705d23ad0159d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce52b7232774ccc894d6788e512abccedf7c2092e9a9e53329b86aa757100c9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07296faa7480333a153ce7963007b1f1d767fd0d64e2e3ae6aac9f4bab3420db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba79f5a87df4e08555b11a5920bb60abb14eba9b92f8b0f1b46fae3a0811c5c(
    value: typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb577d2ea0a79dc40c0bc69455794e2057ce63bf2d7f1e1ab6c14abd6d35213(
    *,
    max_instances: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    target_cpu_utilization: typing.Optional[jsii.Number] = None,
    target_throughput_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8c6cc892a48ccf25dc88613e174887546d955f571d9291cc084ed9efe3cc93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db72d8f7a633e502aec939f4a55bc0fa7598c4d3bb0624ffc9b6b905fa9466a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ce56663695fb3e0ea2a9951ff40642f71a439f2626087872da8b9fdb47bcaf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39234659a64627aa317e44dc0381b3c12df709525e57fbc8f54daea383b1270(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c260ac704cb6af08fd1ae1ba656c4039b897d5c807b757678274f9e7b9e1e671(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c454b93c09ac34ec049df2d1d8eeed8562ef33b1842f899e79db3cc57281fa5(
    value: typing.Optional[GoogleAppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47614e1d315f0dbe3e92013e8ca888e35ee68f848700874b942b236cb7b9fcf(
    *,
    max_instances: jsii.Number,
    idle_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749e7b1e6bdd637f591f5b9f70b02f975cd77cc526c884ff7fed28bc6c13c852(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ae6cd8e6d1d6593370c0011568bd9383186f411fd8f6272126d4d4f6c62952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc2e4536b1fdd7e05a987baf91e2cc0b88626d35ce2928a1538e082727749ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd726a15c0d43c960285d313ba1420fd7a652352b2b1306ced95a77dff179cd(
    value: typing.Optional[GoogleAppEngineStandardAppVersionBasicScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb5bb527fc5f4092681ddd7656417f24224f25ddee38eaece1fbb71c75ef5f5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deployment: typing.Union[GoogleAppEngineStandardAppVersionDeployment, typing.Dict[builtins.str, typing.Any]],
    entrypoint: typing.Union[GoogleAppEngineStandardAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionBasicScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionLibraries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manual_scaling: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b65780657d5c9e3722546e781eba68b74d24d6f7100cd7e3c719380753e73c(
    *,
    files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zip: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionDeploymentZip, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e92dedc442f2bc6d97a4d228b5aff52cba40210cc85e65576ab3949cc408d2b(
    *,
    name: builtins.str,
    source_url: builtins.str,
    sha1_sum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9512cf9fc5b770af2c4303ede555b35b9957fd500ce077b7394ed7cb27611357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b127000f820a5c11cde24f55045ef3b11e0bcada629c72cf95746ba7f4fea0b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f52a2bc6accceb0cb269eb43b2ae4bfa3529e3421c47ff58f6802bc3fcaecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0f1040ca3da3ed523d0d0da4be6349ef2c50e851d97ec26d2d9175dbd95a0f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7358e1534bb300237deca3aafdf5a41353cd350aafe9cb024ae92f19e796bab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b7cedb9ca0d710d2749c1a161930f9ce2c43d887bb1453c444010e761270d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionDeploymentFiles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801173fb73a42324fdd6c155e7f3409bd0935bcc899b5e600592b673367b6ad9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812b0d27449e59c8c16784226fbaf3af47851381f3045cf646a7e16fd791ee8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a7280bbef721e890954524e8fa4893ed404635aa1a5df4be79010cb758fac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02de84fbb18793195b0abc3498053d0a5897913d3f569908dfe7bdf6c4799e69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8e78da9df261b0c4da4eb0db0605e20cd2e25c37b82266fb1ed8742bedfa6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionDeploymentFiles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7d809649a5fe006325ba526298aacc029a893a8c1245348125fdc505249e30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b6f91216c81e369ac18f1a143f65b224eae1665c36299c3213d09932929bd4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAppEngineStandardAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ab679dab946d23c5de28dc47d31aa01243d07dcf4abdcb639fdeb44b3efe95(
    value: typing.Optional[GoogleAppEngineStandardAppVersionDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55dad9ac6442fd05a7431bd709eb79b73bbc224e173a07ac9987959115bab056(
    *,
    source_url: builtins.str,
    files_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae83819ba3840179a031e991e4b9f9513d399aa42fc7e42cbc4d8f2f2c2b966(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b11edfca10c2cb2c377738882b8474e278486861bf89e3a30271e0b59aab794(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181876e3d345cd6c1783cf5d0804b02cdc49ebaf32c74fd35e0714c4bf8cbaa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7176871c7983535f84876ae1550d3a6b611e6c01a4f334702ac08cc82140608b(
    value: typing.Optional[GoogleAppEngineStandardAppVersionDeploymentZip],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf93da80859e556c5b2468ba7da6ead38b105e41991b5e147c77ae7e75f6b0f7(
    *,
    shell: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35c443be5385cfaee0b7bd5c239c17af44325d9b45300fbeb830071d97e31d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedbb57060ef3e53024e4f4e796de5cbeecae67322a6e38ea2bb119dbb5aee76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb16ab6fb78f51e41da66f61fd89eacb5bb076fcfd33dce5311777bb80ec7f8(
    value: typing.Optional[GoogleAppEngineStandardAppVersionEntrypoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5836dc214c579532e82b74b7bbf216671ac2a4a7db8bb02853b1600267b9f4(
    *,
    auth_fail_action: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    redirect_http_response_code: typing.Optional[builtins.str] = None,
    script: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionHandlersScript, typing.Dict[builtins.str, typing.Any]]] = None,
    security_level: typing.Optional[builtins.str] = None,
    static_files: typing.Optional[typing.Union[GoogleAppEngineStandardAppVersionHandlersStaticFiles, typing.Dict[builtins.str, typing.Any]]] = None,
    url_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464e0954637cb47f53ff017f9cc51c53cc164193574209bb342030eda0a2604d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5d30b9d6bd1c97b76d87af17be81ff16943b05a99c763a38e9a4465af4abe2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7364cbfbc354105da5a9db5d4e12422ca463d7d4e609964bb64b90b480538cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5ec1e9ae625b33e8f46d104d673c746872629b9ed3188a896082ab93fe7408(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4640b22d55fffa55e6b7ce129d2918ef4e2f457cd4e001f6a192f553c82059f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc176a48230bba25dd0b0225bb74385712593f1219233803f392594bc707b3b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionHandlers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be34501de3c4dc9682d78e4da2979a15e4c90312a8d7ba1f96d99ba334f7d2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb45c42fe2fdfca2cb2a50fd4a12eb343d851001dfc4a31d9a8585afbc6a447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8188301026c3d5930a901b08a3c8693427b476e6908e1a0786e6ca98ba11a939(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c38d8f94c07d9dd77265f9663faac185b46781ede7f4896730a5d181094368c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c00784aab7e4b7ca5bd23c7ca49b97dbe6964137ead558be7bc5ff55cfcc20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49873257cadebb10327bdfbf5435f723e1d7d0a5f025b43ec5b09fe77829ac5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350a3fadc45d5c3d7822c1c4798f0639d0008df6afeb1bcd812ce4f1431bfbe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionHandlers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a712c55c184629f47691e539b5b78d50fe01de6f1a61c7cc2a18a0ed48984c9(
    *,
    script_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a5a8b86f08fd901c91376dfb7ec270198a652e19ed7e8c20da11a697bab2c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11881269acfc9e9f475ea8445e5b927b10b5b8eca188fe1e99d757c9966e9ba8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37e2af3d66bd75854f9c82f6dfe25a971465701b391a0e100eff784d114df4d(
    value: typing.Optional[GoogleAppEngineStandardAppVersionHandlersScript],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba273e4db4a533e63c005058ce8de5d411e5ba9a4a3bc256acb8c046660fd9fa(
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

def _typecheckingstub__46a7021df4244f69a865378cc322daf453435a6b6bc5b77ed5769f69f07284cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab495ae828148b197809b1a7d7af5180f39d1bd35d2a6b7e0e1c170535132348(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0424c12131fbc20ba65596326f4c04d59a6e21cee445c337b3b71fb6645a6dd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4508539c295b117e94960528599d1e02adb41a8f11b3d71a74994defb814944(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5afda7c7dd4ed408d41686a88df6e0f4a8303f9e91cdc6716b30be2985e4355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad9a21725b331b266abb08153e38a940c6640453d3afe665f4d84dd7865ffce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8868479680becab8ffae286d8c98a65d3b5714707b924e6b812194265ba1d948(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2d849ac5013333a315fe66bd5079ae0be717ef0c46ea4e9e18a940f4ffdc97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0504b152e9ba212a65e9c78e2a4882f6b76d59e06a4c9e281d761a1a2340ab9a(
    value: typing.Optional[GoogleAppEngineStandardAppVersionHandlersStaticFiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e25717bdc96214774b1953d9740eaf1955debfb992734081b53c1ec65772332(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c1ef1b2fb3dd94ef97dca86c68943f3bbedfcf358eb076a648d6c25cc97f71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ea0451286b102fcbdfe3628338015e3aeb266d52d8487813aee427864aa1a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ed8428483fcfec42a67ba7f0295b3ca435ac2ed7bbd85d858f25b2529ba007(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5aba63e0b3e4d8c11d62813e62b2daeebf6fc05e3acc6546ec08b29246f0cca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661b19ced123f52fc632cefd29793bbe4aa564b83fd832aba82a6c536fe9c9fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9c38900f0208578bc02176386df770ae8c92d7f68431254eea17bfba8c075e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAppEngineStandardAppVersionLibraries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78472ed57cda20284a7ac503de07aff82b073ad491085ba95000bcbd00abefb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a8546ddfa20fd92f17f13ac1fc7738e6097542985f7a6d2eb5801afc4065c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6f048eb8e9fe1079f73df0621e66446bebf6185bceace09987598717002018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8b9d9e289154a32784aeb6354d8e3ce04df4938f000d14c664ee100972cc89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionLibraries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b4065e241a8f2c45965069408e4a377713e76d19410bc9327bb20a98def396(
    *,
    instances: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f75ec8bbd75c79d592b3490e89c237c7c899a07ecd3f514b1061ba736c0ac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b987a259cb363ebce93d23003d4a0bba0e0d45d8fe5415c530e33fd049052b5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacec0071265488971fbf6e9b5c8421c555ec51114007c803b5e709e2fb6801f(
    value: typing.Optional[GoogleAppEngineStandardAppVersionManualScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cdcd547d41b165a899106c850f82dee61c2d8e7e8c50ec5bbd295827d2f7a8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5dc9bb99181de19821f5c9de43241e595619372a3b693ecfadb62a1169b068(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7047e0e89db973f875cfcbb079854ac190ac411e9ad0104c5ddb96b88539d9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158aaa0df08b1edfaa65d7aeec2a9ba24d6c9ebd12087f7b5dfdb1760e7b9046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e3e3d78ba8b28d68dc1c8d484bccff08ae3d3d9127f2f0dcc3e22d65b397f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3d45a1392981446d7d068b66b4106342bd14d23c56d11703605a77feeb9228(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAppEngineStandardAppVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fd9df19b081824425b67964b9f7484bec959ddb463ff8980ba6ea1390e6842(
    *,
    name: builtins.str,
    egress_setting: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91315812617ec825f174d33f444fd17435480e888c3eebee70b6f43b095381f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c34b294661663e5d0e5d0b34d348578a6344ad7da4c1e395d1047ddde133264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce80b11541a1ee97a284c08fc8348cff554cf907e57c18164f5cafbf1d61d89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8de8eb8b5228b859f8752d8c59002c81e293de4e2bb99ce25b2cd1478f4cc6(
    value: typing.Optional[GoogleAppEngineStandardAppVersionVpcAccessConnector],
) -> None:
    """Type checking stubs"""
    pass
