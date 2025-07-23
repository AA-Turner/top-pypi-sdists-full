r'''
# `google_app_engine_standard_app_version`

Refer to the Terraform Registry for docs: [`google_app_engine_standard_app_version`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version).
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


class AppEngineStandardAppVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version google_app_engine_standard_app_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        deployment: typing.Union["AppEngineStandardAppVersionDeployment", typing.Dict[builtins.str, typing.Any]],
        entrypoint: typing.Union["AppEngineStandardAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_scaling: typing.Optional[typing.Union["AppEngineStandardAppVersionAutomaticScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_scaling: typing.Optional[typing.Union["AppEngineStandardAppVersionBasicScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionLibraries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manual_scaling: typing.Optional[typing.Union["AppEngineStandardAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AppEngineStandardAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["AppEngineStandardAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version google_app_engine_standard_app_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#deployment AppEngineStandardAppVersion#deployment}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#entrypoint AppEngineStandardAppVersion#entrypoint}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#runtime AppEngineStandardAppVersion#runtime}
        :param service: AppEngine service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#service AppEngineStandardAppVersion#service}
        :param app_engine_apis: Allows App Engine second generation runtimes to access the legacy bundled services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#app_engine_apis AppEngineStandardAppVersion#app_engine_apis}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#automatic_scaling AppEngineStandardAppVersion#automatic_scaling}
        :param basic_scaling: basic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#basic_scaling AppEngineStandardAppVersion#basic_scaling}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#delete_service_on_destroy AppEngineStandardAppVersion#delete_service_on_destroy}
        :param env_variables: Environment variables available to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#env_variables AppEngineStandardAppVersion#env_variables}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#handlers AppEngineStandardAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#id AppEngineStandardAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#inbound_services AppEngineStandardAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G BasicScaling or ManualScaling: B1, B2, B4, B4_1G, B8 Defaults to F1 for AutomaticScaling and B2 for ManualScaling and BasicScaling. If no scaling is specified, AutomaticScaling is chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#instance_class AppEngineStandardAppVersion#instance_class}
        :param libraries: libraries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#libraries AppEngineStandardAppVersion#libraries}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#manual_scaling AppEngineStandardAppVersion#manual_scaling}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#noop_on_destroy AppEngineStandardAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#project AppEngineStandardAppVersion#project}.
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#runtime_api_version AppEngineStandardAppVersion#runtime_api_version}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#service_account AppEngineStandardAppVersion#service_account}
        :param threadsafe: Whether multiple requests can be dispatched to this version at once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#threadsafe AppEngineStandardAppVersion#threadsafe}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#timeouts AppEngineStandardAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#version_id AppEngineStandardAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#vpc_access_connector AppEngineStandardAppVersion#vpc_access_connector}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c388d6369590a49add3066028495ba108e8f8ab9db3d28c144f2fcf52855a4ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppEngineStandardAppVersionConfig(
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
        '''Generates CDKTF code for importing a AppEngineStandardAppVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppEngineStandardAppVersion to import.
        :param import_from_id: The id of the existing AppEngineStandardAppVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppEngineStandardAppVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5889170f8810f2eab2b1eafb3ffd2b724c7836494d311d2ec9c48bed70f89e97)
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
        standard_scheduler_settings: typing.Optional[typing.Union["AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_concurrent_requests AppEngineStandardAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_idle_instances AppEngineStandardAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_pending_latency AppEngineStandardAppVersion#max_pending_latency}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_idle_instances AppEngineStandardAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_pending_latency AppEngineStandardAppVersion#min_pending_latency}
        :param standard_scheduler_settings: standard_scheduler_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#standard_scheduler_settings AppEngineStandardAppVersion#standard_scheduler_settings}
        '''
        value = AppEngineStandardAppVersionAutomaticScaling(
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
        :param max_instances: Maximum number of instances to create for this version. Must be in the range [1.0, 200.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_instances AppEngineStandardAppVersion#max_instances}
        :param idle_timeout: Duration of time after the last request that an instance must wait before the instance is shut down. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#idle_timeout AppEngineStandardAppVersion#idle_timeout}
        '''
        value = AppEngineStandardAppVersionBasicScaling(
            max_instances=max_instances, idle_timeout=idle_timeout
        )

        return typing.cast(None, jsii.invoke(self, "putBasicScaling", [value]))

    @jsii.member(jsii_name="putDeployment")
    def put_deployment(
        self,
        *,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["AppEngineStandardAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#files AppEngineStandardAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#zip AppEngineStandardAppVersion#zip}
        '''
        value = AppEngineStandardAppVersionDeployment(files=files, zip=zip)

        return typing.cast(None, jsii.invoke(self, "putDeployment", [value]))

    @jsii.member(jsii_name="putEntrypoint")
    def put_entrypoint(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#shell AppEngineStandardAppVersion#shell}
        '''
        value = AppEngineStandardAppVersionEntrypoint(shell=shell)

        return typing.cast(None, jsii.invoke(self, "putEntrypoint", [value]))

    @jsii.member(jsii_name="putHandlers")
    def put_handlers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d7a25da7428a9cfaeff2a05c337aeb994be5ca01c9846d0e97d59b70a9be14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHandlers", [value]))

    @jsii.member(jsii_name="putLibraries")
    def put_libraries(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionLibraries", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0799d08610e28672dbee8af98fcfc337f49c2de5b5c09e820fd71fc383309db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLibraries", [value]))

    @jsii.member(jsii_name="putManualScaling")
    def put_manual_scaling(self, *, instances: jsii.Number) -> None:
        '''
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#instances AppEngineStandardAppVersion#instances}
        '''
        value = AppEngineStandardAppVersionManualScaling(instances=instances)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#create AppEngineStandardAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#delete AppEngineStandardAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#update AppEngineStandardAppVersion#update}.
        '''
        value = AppEngineStandardAppVersionTimeouts(
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
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#name AppEngineStandardAppVersion#name}
        :param egress_setting: The egress setting for the connector, controlling what traffic is diverted through it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#egress_setting AppEngineStandardAppVersion#egress_setting}
        '''
        value = AppEngineStandardAppVersionVpcAccessConnector(
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
    ) -> "AppEngineStandardAppVersionAutomaticScalingOutputReference":
        return typing.cast("AppEngineStandardAppVersionAutomaticScalingOutputReference", jsii.get(self, "automaticScaling"))

    @builtins.property
    @jsii.member(jsii_name="basicScaling")
    def basic_scaling(self) -> "AppEngineStandardAppVersionBasicScalingOutputReference":
        return typing.cast("AppEngineStandardAppVersionBasicScalingOutputReference", jsii.get(self, "basicScaling"))

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(self) -> "AppEngineStandardAppVersionDeploymentOutputReference":
        return typing.cast("AppEngineStandardAppVersionDeploymentOutputReference", jsii.get(self, "deployment"))

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> "AppEngineStandardAppVersionEntrypointOutputReference":
        return typing.cast("AppEngineStandardAppVersionEntrypointOutputReference", jsii.get(self, "entrypoint"))

    @builtins.property
    @jsii.member(jsii_name="handlers")
    def handlers(self) -> "AppEngineStandardAppVersionHandlersList":
        return typing.cast("AppEngineStandardAppVersionHandlersList", jsii.get(self, "handlers"))

    @builtins.property
    @jsii.member(jsii_name="libraries")
    def libraries(self) -> "AppEngineStandardAppVersionLibrariesList":
        return typing.cast("AppEngineStandardAppVersionLibrariesList", jsii.get(self, "libraries"))

    @builtins.property
    @jsii.member(jsii_name="manualScaling")
    def manual_scaling(
        self,
    ) -> "AppEngineStandardAppVersionManualScalingOutputReference":
        return typing.cast("AppEngineStandardAppVersionManualScalingOutputReference", jsii.get(self, "manualScaling"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AppEngineStandardAppVersionTimeoutsOutputReference":
        return typing.cast("AppEngineStandardAppVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnector")
    def vpc_access_connector(
        self,
    ) -> "AppEngineStandardAppVersionVpcAccessConnectorOutputReference":
        return typing.cast("AppEngineStandardAppVersionVpcAccessConnectorOutputReference", jsii.get(self, "vpcAccessConnector"))

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
    ) -> typing.Optional["AppEngineStandardAppVersionAutomaticScaling"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionAutomaticScaling"], jsii.get(self, "automaticScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="basicScalingInput")
    def basic_scaling_input(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionBasicScaling"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionBasicScaling"], jsii.get(self, "basicScalingInput"))

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
    ) -> typing.Optional["AppEngineStandardAppVersionDeployment"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionDeployment"], jsii.get(self, "deploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="entrypointInput")
    def entrypoint_input(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionEntrypoint"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionEntrypoint"], jsii.get(self, "entrypointInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionHandlers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionHandlers"]]], jsii.get(self, "handlersInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionLibraries"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionLibraries"]]], jsii.get(self, "librariesInput"))

    @builtins.property
    @jsii.member(jsii_name="manualScalingInput")
    def manual_scaling_input(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionManualScaling"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionManualScaling"], jsii.get(self, "manualScalingInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppEngineStandardAppVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppEngineStandardAppVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionIdInput")
    def version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessConnectorInput")
    def vpc_access_connector_input(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionVpcAccessConnector"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionVpcAccessConnector"], jsii.get(self, "vpcAccessConnectorInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__13e1d89c7944c95953482b31f8172922d425702f96c18371a78db786d8a43dbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d03809292826bf95a79a007be3a399329879e46a36f9429e1eafb89d07b9e1b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteServiceOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envVariables")
    def env_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "envVariables"))

    @env_variables.setter
    def env_variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f64b0f489868702f7460cb09a57364273588564bfd1dff21a0471867e04ace9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408c183916158f9a414e0dda126aca5420c91a586f8f5f94a60b00699d0fe4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundServices")
    def inbound_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inboundServices"))

    @inbound_services.setter
    def inbound_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f871dd29f03a907b491bf732a6471ea20ad08e8c97fc8857a5c79802123bf1bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceClass")
    def instance_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceClass"))

    @instance_class.setter
    def instance_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60abc5a7541361c17f90b90e6491d3e09b935841baedc3def8b25bbceee4dc19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ec193471dcaeb5697fab486a026b28b8d9b88e253c0471edd8ed30061945df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noopOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ea7804311797fbd70a01ef4ee2fd8aa609359890dbe9dc2edaa7d04bec73ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec407220bfcaadd0a5a2ee6115f51fd79bf6cee13e3c3060134c96ba0152c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeApiVersion")
    def runtime_api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeApiVersion"))

    @runtime_api_version.setter
    def runtime_api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b3b044a56cfe4942a145e4b5a82539083b9f84983272eb39561568b18cdc0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea0b578ffc32b609b88d3f0ac2e7546787a1a13d54919cf030c08f28592c5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ec6e6ef1f0187ac5e7dbc0735c4ce7938c24f84d5087ffae8203fc3d6fe827)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c47c22e39589d62eb405092ac368e3ad10ca4ba2392ead4c8d3d66ac1e7a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsafe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c843bde2730dee38534635723d5a2236f401ad5fd33ae8844ed389330209c8e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionAutomaticScaling",
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
class AppEngineStandardAppVersionAutomaticScaling:
    def __init__(
        self,
        *,
        max_concurrent_requests: typing.Optional[jsii.Number] = None,
        max_idle_instances: typing.Optional[jsii.Number] = None,
        max_pending_latency: typing.Optional[builtins.str] = None,
        min_idle_instances: typing.Optional[jsii.Number] = None,
        min_pending_latency: typing.Optional[builtins.str] = None,
        standard_scheduler_settings: typing.Optional[typing.Union["AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_concurrent_requests: Number of concurrent requests an automatic scaling instance can accept before the scheduler spawns a new instance. Defaults to a runtime-specific value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_concurrent_requests AppEngineStandardAppVersion#max_concurrent_requests}
        :param max_idle_instances: Maximum number of idle instances that should be maintained for this version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_idle_instances AppEngineStandardAppVersion#max_idle_instances}
        :param max_pending_latency: Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_pending_latency AppEngineStandardAppVersion#max_pending_latency}
        :param min_idle_instances: Minimum number of idle instances that should be maintained for this version. Only applicable for the default version of a service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_idle_instances AppEngineStandardAppVersion#min_idle_instances}
        :param min_pending_latency: Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_pending_latency AppEngineStandardAppVersion#min_pending_latency}
        :param standard_scheduler_settings: standard_scheduler_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#standard_scheduler_settings AppEngineStandardAppVersion#standard_scheduler_settings}
        '''
        if isinstance(standard_scheduler_settings, dict):
            standard_scheduler_settings = AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings(**standard_scheduler_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccf027a3b78a8ef2f96cba8fe815d63a8a531e8829f7793c34c7f1d98787569)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_concurrent_requests AppEngineStandardAppVersion#max_concurrent_requests}
        '''
        result = self._values.get("max_concurrent_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle instances that should be maintained for this version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_idle_instances AppEngineStandardAppVersion#max_idle_instances}
        '''
        result = self._values.get("max_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Maximum amount of time that a request should wait in the pending queue before starting a new instance to handle it.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_pending_latency AppEngineStandardAppVersion#max_pending_latency}
        '''
        result = self._values.get("max_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_idle_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of idle instances that should be maintained for this version.

        Only applicable for the default version of a service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_idle_instances AppEngineStandardAppVersion#min_idle_instances}
        '''
        result = self._values.get("min_idle_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_pending_latency(self) -> typing.Optional[builtins.str]:
        '''Minimum amount of time a request should wait in the pending queue before starting a new instance to handle it.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_pending_latency AppEngineStandardAppVersion#min_pending_latency}
        '''
        result = self._values.get("min_pending_latency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standard_scheduler_settings(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"]:
        '''standard_scheduler_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#standard_scheduler_settings AppEngineStandardAppVersion#standard_scheduler_settings}
        '''
        result = self._values.get("standard_scheduler_settings")
        return typing.cast(typing.Optional["AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionAutomaticScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionAutomaticScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionAutomaticScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__171d2651dfeed3aa1d5c12a7276cc859b7722ed238580f86006117449e601690)
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
        :param max_instances: Maximum number of instances to run for this version. Set to zero to disable maxInstances configuration. **Note:** Starting from March 2025, App Engine sets the maxInstances default for standard environment deployments to 20. This change doesn't impact existing apps. To override the default, specify a new value between 0 and 2147483647, and deploy a new version or redeploy over an existing version. To disable the maxInstances default configuration setting, specify the maximum permitted value 2147483647. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_instances AppEngineStandardAppVersion#max_instances}
        :param min_instances: Minimum number of instances to run for this version. Set to zero to disable minInstances configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_instances AppEngineStandardAppVersion#min_instances}
        :param target_cpu_utilization: Target CPU utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#target_cpu_utilization AppEngineStandardAppVersion#target_cpu_utilization}
        :param target_throughput_utilization: Target throughput utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#target_throughput_utilization AppEngineStandardAppVersion#target_throughput_utilization}
        '''
        value = AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings(
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
    ) -> "AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference":
        return typing.cast("AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference", jsii.get(self, "standardSchedulerSettings"))

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
    ) -> typing.Optional["AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings"], jsii.get(self, "standardSchedulerSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRequests")
    def max_concurrent_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentRequests"))

    @max_concurrent_requests.setter
    def max_concurrent_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8842bbc238b483a8e7de17273d423f9349ce0abb92cd02fb21d400296f4f32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIdleInstances")
    def max_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleInstances"))

    @max_idle_instances.setter
    def max_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff7e9458e2da139d6b5b0b58d07ff090a54faacb6692b8d00121500f2d46bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingLatency")
    def max_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxPendingLatency"))

    @max_pending_latency.setter
    def max_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502a58ee873a0d1082925a4c67acaba378bbe4f9a812fda0c937cb621fcb1e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minIdleInstances")
    def min_idle_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minIdleInstances"))

    @min_idle_instances.setter
    def min_idle_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0935dc46e896662ed4a8e8308de5e60b7730532629c601264556123106dccac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minIdleInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minPendingLatency")
    def min_pending_latency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minPendingLatency"))

    @min_pending_latency.setter
    def min_pending_latency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10eb4e59ebde7f85f8e1aafe3c3a4280b99e28c9afb45835bc0eb028b5ff85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minPendingLatency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionAutomaticScaling]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionAutomaticScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionAutomaticScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa824f6e058efcf4ab9ae3464e27f191f8131932d1cef97b783cdbfa9b2752ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_instances": "maxInstances",
        "min_instances": "minInstances",
        "target_cpu_utilization": "targetCpuUtilization",
        "target_throughput_utilization": "targetThroughputUtilization",
    },
)
class AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings:
    def __init__(
        self,
        *,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        target_cpu_utilization: typing.Optional[jsii.Number] = None,
        target_throughput_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances to run for this version. Set to zero to disable maxInstances configuration. **Note:** Starting from March 2025, App Engine sets the maxInstances default for standard environment deployments to 20. This change doesn't impact existing apps. To override the default, specify a new value between 0 and 2147483647, and deploy a new version or redeploy over an existing version. To disable the maxInstances default configuration setting, specify the maximum permitted value 2147483647. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_instances AppEngineStandardAppVersion#max_instances}
        :param min_instances: Minimum number of instances to run for this version. Set to zero to disable minInstances configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_instances AppEngineStandardAppVersion#min_instances}
        :param target_cpu_utilization: Target CPU utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#target_cpu_utilization AppEngineStandardAppVersion#target_cpu_utilization}
        :param target_throughput_utilization: Target throughput utilization ratio to maintain when scaling. Should be a value in the range [0.50, 0.95], zero, or a negative value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#target_throughput_utilization AppEngineStandardAppVersion#target_throughput_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df37acd9beef70f053969b10f0c383267689c6c7f0e72212cc0b59779c889c99)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_instances AppEngineStandardAppVersion#max_instances}
        '''
        result = self._values.get("max_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of instances to run for this version. Set to zero to disable minInstances configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#min_instances AppEngineStandardAppVersion#min_instances}
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cpu_utilization(self) -> typing.Optional[jsii.Number]:
        '''Target CPU utilization ratio to maintain when scaling.

        Should be a value in the range [0.50, 0.95], zero, or a negative value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#target_cpu_utilization AppEngineStandardAppVersion#target_cpu_utilization}
        '''
        result = self._values.get("target_cpu_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_throughput_utilization(self) -> typing.Optional[jsii.Number]:
        '''Target throughput utilization ratio to maintain when scaling.

        Should be a value in the range [0.50, 0.95], zero, or a negative value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#target_throughput_utilization AppEngineStandardAppVersion#target_throughput_utilization}
        '''
        result = self._values.get("target_throughput_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a5313c974f73cd45f321fc72757a1c92019d25c04dc594b78fb0ee66af38ea3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7acbc040bc78fb9996fbd2a183c3739d2cede138e546bb9999510b0d98782e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @min_instances.setter
    def min_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e3f5e42f07b590dae6591a7b4e5da15a3d51ce709c918316fb4e97c2294444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCpuUtilization")
    def target_cpu_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetCpuUtilization"))

    @target_cpu_utilization.setter
    def target_cpu_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6a30d1aa6cb5023ea813cffb1b3fde4d54de739f41200c3962a1c5be5d093f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCpuUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetThroughputUtilization")
    def target_throughput_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetThroughputUtilization"))

    @target_throughput_utilization.setter
    def target_throughput_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0912ec3b848e478d55dbeb55d353179ee340d8c1d3b29802ad531f5b602bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetThroughputUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309923fda5e6b5f106eed6e0ced81fc1f488f4e3fceabd441cdced10aa9e849e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionBasicScaling",
    jsii_struct_bases=[],
    name_mapping={"max_instances": "maxInstances", "idle_timeout": "idleTimeout"},
)
class AppEngineStandardAppVersionBasicScaling:
    def __init__(
        self,
        *,
        max_instances: jsii.Number,
        idle_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances to create for this version. Must be in the range [1.0, 200.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_instances AppEngineStandardAppVersion#max_instances}
        :param idle_timeout: Duration of time after the last request that an instance must wait before the instance is shut down. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#idle_timeout AppEngineStandardAppVersion#idle_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ff08810f9dd0a6c813defb040a51bf94ed3f904c21aee4224559856719c1eb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#max_instances AppEngineStandardAppVersion#max_instances}
        '''
        result = self._values.get("max_instances")
        assert result is not None, "Required property 'max_instances' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional[builtins.str]:
        '''Duration of time after the last request that an instance must wait before the instance is shut down.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#idle_timeout AppEngineStandardAppVersion#idle_timeout}
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionBasicScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionBasicScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionBasicScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df252e83727680911cab35acfea55543d2e28e647a2c7791f5f1a46375509682)
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
            type_hints = typing.get_type_hints(_typecheckingstub__250b0b5b51d63920143b7b33b0f6cb22177ed83eb9ce04cf15ad3e51a90f83b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db16fa343d5628c92b37093f0d8484aef608eb188c75a51cf5753a4bd4a1e0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionBasicScaling]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionBasicScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionBasicScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b7ed06ebdae7aa72abd6b0915ab759f54f37569fc9ecad9131164255378df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionConfig",
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
class AppEngineStandardAppVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        deployment: typing.Union["AppEngineStandardAppVersionDeployment", typing.Dict[builtins.str, typing.Any]],
        entrypoint: typing.Union["AppEngineStandardAppVersionEntrypoint", typing.Dict[builtins.str, typing.Any]],
        runtime: builtins.str,
        service: builtins.str,
        app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        basic_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionBasicScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_class: typing.Optional[builtins.str] = None,
        libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionLibraries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manual_scaling: typing.Optional[typing.Union["AppEngineStandardAppVersionManualScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        runtime_api_version: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AppEngineStandardAppVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_id: typing.Optional[builtins.str] = None,
        vpc_access_connector: typing.Optional[typing.Union["AppEngineStandardAppVersionVpcAccessConnector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param deployment: deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#deployment AppEngineStandardAppVersion#deployment}
        :param entrypoint: entrypoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#entrypoint AppEngineStandardAppVersion#entrypoint}
        :param runtime: Desired runtime. Example python27. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#runtime AppEngineStandardAppVersion#runtime}
        :param service: AppEngine service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#service AppEngineStandardAppVersion#service}
        :param app_engine_apis: Allows App Engine second generation runtimes to access the legacy bundled services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#app_engine_apis AppEngineStandardAppVersion#app_engine_apis}
        :param automatic_scaling: automatic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#automatic_scaling AppEngineStandardAppVersion#automatic_scaling}
        :param basic_scaling: basic_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#basic_scaling AppEngineStandardAppVersion#basic_scaling}
        :param delete_service_on_destroy: If set to 'true', the service will be deleted if it is the last version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#delete_service_on_destroy AppEngineStandardAppVersion#delete_service_on_destroy}
        :param env_variables: Environment variables available to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#env_variables AppEngineStandardAppVersion#env_variables}
        :param handlers: handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#handlers AppEngineStandardAppVersion#handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#id AppEngineStandardAppVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inbound_services: A list of the types of messages that this application is able to receive. Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#inbound_services AppEngineStandardAppVersion#inbound_services}
        :param instance_class: Instance class that is used to run this version. Valid values are AutomaticScaling: F1, F2, F4, F4_1G BasicScaling or ManualScaling: B1, B2, B4, B4_1G, B8 Defaults to F1 for AutomaticScaling and B2 for ManualScaling and BasicScaling. If no scaling is specified, AutomaticScaling is chosen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#instance_class AppEngineStandardAppVersion#instance_class}
        :param libraries: libraries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#libraries AppEngineStandardAppVersion#libraries}
        :param manual_scaling: manual_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#manual_scaling AppEngineStandardAppVersion#manual_scaling}
        :param noop_on_destroy: If set to 'true', the application version will not be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#noop_on_destroy AppEngineStandardAppVersion#noop_on_destroy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#project AppEngineStandardAppVersion#project}.
        :param runtime_api_version: The version of the API in the given runtime environment. Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref' Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#runtime_api_version AppEngineStandardAppVersion#runtime_api_version}
        :param service_account: The identity that the deployed version will run as. Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#service_account AppEngineStandardAppVersion#service_account}
        :param threadsafe: Whether multiple requests can be dispatched to this version at once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#threadsafe AppEngineStandardAppVersion#threadsafe}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#timeouts AppEngineStandardAppVersion#timeouts}
        :param version_id: Relative name of the version within the service. For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#version_id AppEngineStandardAppVersion#version_id}
        :param vpc_access_connector: vpc_access_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#vpc_access_connector AppEngineStandardAppVersion#vpc_access_connector}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deployment, dict):
            deployment = AppEngineStandardAppVersionDeployment(**deployment)
        if isinstance(entrypoint, dict):
            entrypoint = AppEngineStandardAppVersionEntrypoint(**entrypoint)
        if isinstance(automatic_scaling, dict):
            automatic_scaling = AppEngineStandardAppVersionAutomaticScaling(**automatic_scaling)
        if isinstance(basic_scaling, dict):
            basic_scaling = AppEngineStandardAppVersionBasicScaling(**basic_scaling)
        if isinstance(manual_scaling, dict):
            manual_scaling = AppEngineStandardAppVersionManualScaling(**manual_scaling)
        if isinstance(timeouts, dict):
            timeouts = AppEngineStandardAppVersionTimeouts(**timeouts)
        if isinstance(vpc_access_connector, dict):
            vpc_access_connector = AppEngineStandardAppVersionVpcAccessConnector(**vpc_access_connector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb5624fa17adf5a25b848d18ca07910ddbcdc744ef10eeef12afc73e8ae2bdc)
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
    def deployment(self) -> "AppEngineStandardAppVersionDeployment":
        '''deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#deployment AppEngineStandardAppVersion#deployment}
        '''
        result = self._values.get("deployment")
        assert result is not None, "Required property 'deployment' is missing"
        return typing.cast("AppEngineStandardAppVersionDeployment", result)

    @builtins.property
    def entrypoint(self) -> "AppEngineStandardAppVersionEntrypoint":
        '''entrypoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#entrypoint AppEngineStandardAppVersion#entrypoint}
        '''
        result = self._values.get("entrypoint")
        assert result is not None, "Required property 'entrypoint' is missing"
        return typing.cast("AppEngineStandardAppVersionEntrypoint", result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''Desired runtime. Example python27.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#runtime AppEngineStandardAppVersion#runtime}
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''AppEngine service resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#service AppEngineStandardAppVersion#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine_apis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows App Engine second generation runtimes to access the legacy bundled services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#app_engine_apis AppEngineStandardAppVersion#app_engine_apis}
        '''
        result = self._values.get("app_engine_apis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def automatic_scaling(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionAutomaticScaling]:
        '''automatic_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#automatic_scaling AppEngineStandardAppVersion#automatic_scaling}
        '''
        result = self._values.get("automatic_scaling")
        return typing.cast(typing.Optional[AppEngineStandardAppVersionAutomaticScaling], result)

    @builtins.property
    def basic_scaling(self) -> typing.Optional[AppEngineStandardAppVersionBasicScaling]:
        '''basic_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#basic_scaling AppEngineStandardAppVersion#basic_scaling}
        '''
        result = self._values.get("basic_scaling")
        return typing.cast(typing.Optional[AppEngineStandardAppVersionBasicScaling], result)

    @builtins.property
    def delete_service_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the service will be deleted if it is the last version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#delete_service_on_destroy AppEngineStandardAppVersion#delete_service_on_destroy}
        '''
        result = self._values.get("delete_service_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def env_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables available to the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#env_variables AppEngineStandardAppVersion#env_variables}
        '''
        result = self._values.get("env_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def handlers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionHandlers"]]]:
        '''handlers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#handlers AppEngineStandardAppVersion#handlers}
        '''
        result = self._values.get("handlers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionHandlers"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#id AppEngineStandardAppVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inbound_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the types of messages that this application is able to receive.

        Possible values: ["INBOUND_SERVICE_MAIL", "INBOUND_SERVICE_MAIL_BOUNCE", "INBOUND_SERVICE_XMPP_ERROR", "INBOUND_SERVICE_XMPP_MESSAGE", "INBOUND_SERVICE_XMPP_SUBSCRIBE", "INBOUND_SERVICE_XMPP_PRESENCE", "INBOUND_SERVICE_CHANNEL_PRESENCE", "INBOUND_SERVICE_WARMUP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#inbound_services AppEngineStandardAppVersion#inbound_services}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#instance_class AppEngineStandardAppVersion#instance_class}
        '''
        result = self._values.get("instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def libraries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionLibraries"]]]:
        '''libraries block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#libraries AppEngineStandardAppVersion#libraries}
        '''
        result = self._values.get("libraries")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionLibraries"]]], result)

    @builtins.property
    def manual_scaling(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionManualScaling"]:
        '''manual_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#manual_scaling AppEngineStandardAppVersion#manual_scaling}
        '''
        result = self._values.get("manual_scaling")
        return typing.cast(typing.Optional["AppEngineStandardAppVersionManualScaling"], result)

    @builtins.property
    def noop_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the application version will not be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#noop_on_destroy AppEngineStandardAppVersion#noop_on_destroy}
        '''
        result = self._values.get("noop_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#project AppEngineStandardAppVersion#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_api_version(self) -> typing.Optional[builtins.str]:
        '''The version of the API in the given runtime environment.

        Please see the app.yaml reference for valid values at 'https://cloud.google.com/appengine/docs/standard//config/appref'
        Substitute '' with 'python', 'java', 'php', 'ruby', 'go' or 'nodejs'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#runtime_api_version AppEngineStandardAppVersion#runtime_api_version}
        '''
        result = self._values.get("runtime_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The identity that the deployed version will run as.

        Admin API will use the App Engine Appspot service account as default if this field is neither provided in app.yaml file nor through CLI flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#service_account AppEngineStandardAppVersion#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threadsafe(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether multiple requests can be dispatched to this version at once.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#threadsafe AppEngineStandardAppVersion#threadsafe}
        '''
        result = self._values.get("threadsafe")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppEngineStandardAppVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#timeouts AppEngineStandardAppVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppEngineStandardAppVersionTimeouts"], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Relative name of the version within the service.

        For example, 'v1'. Version names can contain only lowercase letters, numbers, or hyphens. Reserved names,"default", "latest", and any name with the prefix "ah-".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#version_id AppEngineStandardAppVersion#version_id}
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_access_connector(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionVpcAccessConnector"]:
        '''vpc_access_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#vpc_access_connector AppEngineStandardAppVersion#vpc_access_connector}
        '''
        result = self._values.get("vpc_access_connector")
        return typing.cast(typing.Optional["AppEngineStandardAppVersionVpcAccessConnector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionDeployment",
    jsii_struct_bases=[],
    name_mapping={"files": "files", "zip": "zip"},
)
class AppEngineStandardAppVersionDeployment:
    def __init__(
        self,
        *,
        files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppEngineStandardAppVersionDeploymentFiles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zip: typing.Optional[typing.Union["AppEngineStandardAppVersionDeploymentZip", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param files: files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#files AppEngineStandardAppVersion#files}
        :param zip: zip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#zip AppEngineStandardAppVersion#zip}
        '''
        if isinstance(zip, dict):
            zip = AppEngineStandardAppVersionDeploymentZip(**zip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d801241060561fa0e2b87da5b424a2ba4312f247867fde4af0a62a7d7f3a995)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionDeploymentFiles"]]]:
        '''files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#files AppEngineStandardAppVersion#files}
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppEngineStandardAppVersionDeploymentFiles"]]], result)

    @builtins.property
    def zip(self) -> typing.Optional["AppEngineStandardAppVersionDeploymentZip"]:
        '''zip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#zip AppEngineStandardAppVersion#zip}
        '''
        result = self._values.get("zip")
        return typing.cast(typing.Optional["AppEngineStandardAppVersionDeploymentZip"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionDeploymentFiles",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "source_url": "sourceUrl", "sha1_sum": "sha1Sum"},
)
class AppEngineStandardAppVersionDeploymentFiles:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_url: builtins.str,
        sha1_sum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#name AppEngineStandardAppVersion#name}.
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#source_url AppEngineStandardAppVersion#source_url}
        :param sha1_sum: SHA1 checksum of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#sha1_sum AppEngineStandardAppVersion#sha1_sum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37e3c4318816f9103317834d040a0217c9991be1e676bae032f287d0be26fe6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#name AppEngineStandardAppVersion#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_url(self) -> builtins.str:
        '''Source URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#source_url AppEngineStandardAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha1_sum(self) -> typing.Optional[builtins.str]:
        '''SHA1 checksum of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#sha1_sum AppEngineStandardAppVersion#sha1_sum}
        '''
        result = self._values.get("sha1_sum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionDeploymentFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionDeploymentFilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionDeploymentFilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__287c3c3a6475e559b70c53fc5f2c04ef89f5822ae2df46781d03aca2bd8d42ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppEngineStandardAppVersionDeploymentFilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edb17703bbedf261f8c1ae8124a60bdbbbea1cbd9ccfa1ee144316e01e9c2f0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppEngineStandardAppVersionDeploymentFilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f64ad0fc86bfbbbc64bf58e471e44affd159f0f187a1b87553268ce67ef7694)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faa851e34c53008cc930c6bb70e794b5579297b863e72a7019468b1f88b643e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c4c4a45aed4b01f9fd7c83c0fa133682416e6b4eabb5b2f981d6030bc620470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionDeploymentFiles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionDeploymentFiles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6caca763c39c0b86982dd479780b53acc476d5c94d607500857b23d4ac368b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineStandardAppVersionDeploymentFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionDeploymentFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d0dddf0d0859e7d854d98d54264c68e6b34a5ad8cee529125f45cec75bbb124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4524196fe047a0bd5339dc14636d7597f00b738d7e1becc5f48fcf4df5d1a051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sha1Sum")
    def sha1_sum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1Sum"))

    @sha1_sum.setter
    def sha1_sum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb96f9dd63a919f042492652d143d7178ffeca3ccb9c18e23f2f29aee1bed65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha1Sum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73dcdfcbb415e574e167eb2660c6e7ee19b6cb961787cf6f2e4d85aec33a782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionDeploymentFiles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionDeploymentFiles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionDeploymentFiles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c40879480b6777aa83d909fb5e783af4aaf44d02b6a23230742faf1acc8916e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineStandardAppVersionDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf58855ca5a8f8c08456840863102531e37878e764fbe3dda70245cc6bd6507)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFiles")
    def put_files(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152dacd05effff06082e163cf4b82c67aeacff81457cde8bd23697ec0f3b3c37)
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
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#source_url AppEngineStandardAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#files_count AppEngineStandardAppVersion#files_count}
        '''
        value = AppEngineStandardAppVersionDeploymentZip(
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
    def files(self) -> AppEngineStandardAppVersionDeploymentFilesList:
        return typing.cast(AppEngineStandardAppVersionDeploymentFilesList, jsii.get(self, "files"))

    @builtins.property
    @jsii.member(jsii_name="zip")
    def zip(self) -> "AppEngineStandardAppVersionDeploymentZipOutputReference":
        return typing.cast("AppEngineStandardAppVersionDeploymentZipOutputReference", jsii.get(self, "zip"))

    @builtins.property
    @jsii.member(jsii_name="filesInput")
    def files_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionDeploymentFiles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionDeploymentFiles]]], jsii.get(self, "filesInput"))

    @builtins.property
    @jsii.member(jsii_name="zipInput")
    def zip_input(self) -> typing.Optional["AppEngineStandardAppVersionDeploymentZip"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionDeploymentZip"], jsii.get(self, "zipInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineStandardAppVersionDeployment]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420373a518ef5bb59651d003873d589b657a375e82b9fca3267af025bcfd0e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionDeploymentZip",
    jsii_struct_bases=[],
    name_mapping={"source_url": "sourceUrl", "files_count": "filesCount"},
)
class AppEngineStandardAppVersionDeploymentZip:
    def __init__(
        self,
        *,
        source_url: builtins.str,
        files_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_url: Source URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#source_url AppEngineStandardAppVersion#source_url}
        :param files_count: files count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#files_count AppEngineStandardAppVersion#files_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e01d08e0a7156037d412cf46174570fd3cd6fd8a8b38fd1bc5fefea212fdb0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#source_url AppEngineStandardAppVersion#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def files_count(self) -> typing.Optional[jsii.Number]:
        '''files count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#files_count AppEngineStandardAppVersion#files_count}
        '''
        result = self._values.get("files_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionDeploymentZip(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionDeploymentZipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionDeploymentZipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33094ba5d052016b4368b609f1f73fd28549d62c7d1030cd171975467bb14b4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ec3c78d8c48908312fabc796b1fa57334709afd8b6387622cd59b2743999d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e22ad6b70fe5267e3bad7bc26b904ac8452b1b3aa992658be1b11bf7f028fc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionDeploymentZip]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionDeploymentZip], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionDeploymentZip],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f205b78c04b1db44966d7e6ae264e7f56da7702c55c45559d7fadb3d7d7c5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionEntrypoint",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell"},
)
class AppEngineStandardAppVersionEntrypoint:
    def __init__(self, *, shell: builtins.str) -> None:
        '''
        :param shell: The format should be a shell command that can be fed to bash -c. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#shell AppEngineStandardAppVersion#shell}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b8e3dd84635f0da6d4f46e4879d669df7d0031fa7d89cd7d065befe348f494)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "shell": shell,
        }

    @builtins.property
    def shell(self) -> builtins.str:
        '''The format should be a shell command that can be fed to bash -c.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#shell AppEngineStandardAppVersion#shell}
        '''
        result = self._values.get("shell")
        assert result is not None, "Required property 'shell' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionEntrypoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionEntrypointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionEntrypointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8eba4126415e6ab839b67cee1479ff7bc369da6b57e8971dddb9e44fec3cc3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff0773fc9ca924cd0ccb115010cf9e3e535db23ab04b2ea4b397d6d1c504c5dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineStandardAppVersionEntrypoint]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionEntrypoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionEntrypoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931f3c8c8fa0f6ff0709f741662183c4aafca07e23e89a31d262a388edf4ac97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionHandlers",
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
class AppEngineStandardAppVersionHandlers:
    def __init__(
        self,
        *,
        auth_fail_action: typing.Optional[builtins.str] = None,
        login: typing.Optional[builtins.str] = None,
        redirect_http_response_code: typing.Optional[builtins.str] = None,
        script: typing.Optional[typing.Union["AppEngineStandardAppVersionHandlersScript", typing.Dict[builtins.str, typing.Any]]] = None,
        security_level: typing.Optional[builtins.str] = None,
        static_files: typing.Optional[typing.Union["AppEngineStandardAppVersionHandlersStaticFiles", typing.Dict[builtins.str, typing.Any]]] = None,
        url_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_fail_action: Actions to take when the user is not logged in. Possible values: ["AUTH_FAIL_ACTION_REDIRECT", "AUTH_FAIL_ACTION_UNAUTHORIZED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#auth_fail_action AppEngineStandardAppVersion#auth_fail_action}
        :param login: Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#login AppEngineStandardAppVersion#login}
        :param redirect_http_response_code: 30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#redirect_http_response_code AppEngineStandardAppVersion#redirect_http_response_code}
        :param script: script block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#script AppEngineStandardAppVersion#script}
        :param security_level: Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#security_level AppEngineStandardAppVersion#security_level}
        :param static_files: static_files block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#static_files AppEngineStandardAppVersion#static_files}
        :param url_regex: URL prefix. Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings. All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#url_regex AppEngineStandardAppVersion#url_regex}
        '''
        if isinstance(script, dict):
            script = AppEngineStandardAppVersionHandlersScript(**script)
        if isinstance(static_files, dict):
            static_files = AppEngineStandardAppVersionHandlersStaticFiles(**static_files)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0344d46fb86dfab5c0a6982097fd89df44d456f87d8db76efe1e163df613e8b8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#auth_fail_action AppEngineStandardAppVersion#auth_fail_action}
        '''
        result = self._values.get("auth_fail_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login(self) -> typing.Optional[builtins.str]:
        '''Methods to restrict access to a URL based on login status. Possible values: ["LOGIN_OPTIONAL", "LOGIN_ADMIN", "LOGIN_REQUIRED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#login AppEngineStandardAppVersion#login}
        '''
        result = self._values.get("login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_http_response_code(self) -> typing.Optional[builtins.str]:
        '''30x code to use when performing redirects for the secure field. Possible values: ["REDIRECT_HTTP_RESPONSE_CODE_301", "REDIRECT_HTTP_RESPONSE_CODE_302", "REDIRECT_HTTP_RESPONSE_CODE_303", "REDIRECT_HTTP_RESPONSE_CODE_307"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#redirect_http_response_code AppEngineStandardAppVersion#redirect_http_response_code}
        '''
        result = self._values.get("redirect_http_response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional["AppEngineStandardAppVersionHandlersScript"]:
        '''script block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#script AppEngineStandardAppVersion#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional["AppEngineStandardAppVersionHandlersScript"], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''Security (HTTPS) enforcement for this URL. Possible values: ["SECURE_DEFAULT", "SECURE_NEVER", "SECURE_OPTIONAL", "SECURE_ALWAYS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#security_level AppEngineStandardAppVersion#security_level}
        '''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_files(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionHandlersStaticFiles"]:
        '''static_files block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#static_files AppEngineStandardAppVersion#static_files}
        '''
        result = self._values.get("static_files")
        return typing.cast(typing.Optional["AppEngineStandardAppVersionHandlersStaticFiles"], result)

    @builtins.property
    def url_regex(self) -> typing.Optional[builtins.str]:
        '''URL prefix.

        Uses regular expression syntax, which means regexp special characters must be escaped, but should not contain groupings.
        All URLs that begin with this prefix are handled by this handler, using the portion of the URL after the prefix as part of the file path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#url_regex AppEngineStandardAppVersion#url_regex}
        '''
        result = self._values.get("url_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionHandlers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionHandlersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionHandlersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d84db5cc92aeedc3facdb4a7f0323fd6f096e9cd41170181a49e0265547eca7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppEngineStandardAppVersionHandlersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c4ff47155422903760cde9fb83a050dc12584e761cc3dbd0f59df64fbca595)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppEngineStandardAppVersionHandlersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ad59c253bb7da977151d37c1c32942b1b0b2b273725f8c932af70ac16c6e0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70df4c095e3822116f6e1081388882c985a49ed12aeb898ba5eeaa507a5f7dda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5767407f647ad368f1e14734dceb5044e0280468916ce438bbf6477c778f8118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionHandlers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionHandlers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionHandlers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eef39c314c1b05dba2ea6f92dafdb50b02e7b1c9eec9e33ab5ed8d8be211b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineStandardAppVersionHandlersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionHandlersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1649768603894b6fa46ff9570f08df18995dadd4778df5c8a66f054ea1c48fb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putScript")
    def put_script(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#script_path AppEngineStandardAppVersion#script_path}
        '''
        value = AppEngineStandardAppVersionHandlersScript(script_path=script_path)

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
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#application_readable AppEngineStandardAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#expiration AppEngineStandardAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#http_headers AppEngineStandardAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#mime_type AppEngineStandardAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#path AppEngineStandardAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#require_matching_file AppEngineStandardAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#upload_path_regex AppEngineStandardAppVersion#upload_path_regex}
        '''
        value = AppEngineStandardAppVersionHandlersStaticFiles(
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
    def script(self) -> "AppEngineStandardAppVersionHandlersScriptOutputReference":
        return typing.cast("AppEngineStandardAppVersionHandlersScriptOutputReference", jsii.get(self, "script"))

    @builtins.property
    @jsii.member(jsii_name="staticFiles")
    def static_files(
        self,
    ) -> "AppEngineStandardAppVersionHandlersStaticFilesOutputReference":
        return typing.cast("AppEngineStandardAppVersionHandlersStaticFilesOutputReference", jsii.get(self, "staticFiles"))

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
    ) -> typing.Optional["AppEngineStandardAppVersionHandlersScript"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionHandlersScript"], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="securityLevelInput")
    def security_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="staticFilesInput")
    def static_files_input(
        self,
    ) -> typing.Optional["AppEngineStandardAppVersionHandlersStaticFiles"]:
        return typing.cast(typing.Optional["AppEngineStandardAppVersionHandlersStaticFiles"], jsii.get(self, "staticFilesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fc90d180bfe754f482706ad8ab9cbacda4e9472917fbdca7ba6c2a8956f24da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authFailAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "login"))

    @login.setter
    def login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56470968eb0eca323d4e59447c002722af653671c947881986568cc66fb566b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "login", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectHttpResponseCode")
    def redirect_http_response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectHttpResponseCode"))

    @redirect_http_response_code.setter
    def redirect_http_response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99cd4ff6b0aeeccbe87e21a703f882b6798b40b882d681e0d00133d3da213a97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectHttpResponseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @security_level.setter
    def security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c613268c5ab76f2f95461373e86b23402778400c9094e6116a4ba338aa33aae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlRegex")
    def url_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlRegex"))

    @url_regex.setter
    def url_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb695a577e7c3e7158d12a4c7fb3d348c815d7ad43a12a9b6535c2cee7fc175c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionHandlers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionHandlers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionHandlers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e031038623319ab4268912c4cc40b8ac921b63a31cc89358bfb8e8a81c04a206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionHandlersScript",
    jsii_struct_bases=[],
    name_mapping={"script_path": "scriptPath"},
)
class AppEngineStandardAppVersionHandlersScript:
    def __init__(self, *, script_path: builtins.str) -> None:
        '''
        :param script_path: Path to the script from the application root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#script_path AppEngineStandardAppVersion#script_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c12fbaa554385eed5b131055803073f2270ae9bfb6561fb8af1a9e2b7a29e6)
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script_path": script_path,
        }

    @builtins.property
    def script_path(self) -> builtins.str:
        '''Path to the script from the application root directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#script_path AppEngineStandardAppVersion#script_path}
        '''
        result = self._values.get("script_path")
        assert result is not None, "Required property 'script_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionHandlersScript(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionHandlersScriptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionHandlersScriptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc0450970996ef2117a02b131c7fb8c1e2b077784f3f24cb643675fb86173612)
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
            type_hints = typing.get_type_hints(_typecheckingstub__575e9515eda294a0bac9f93d75b4599da1720023fe103aca88d6f4c34510991b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionHandlersScript]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionHandlersScript], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionHandlersScript],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd2f22db2d090e653572b6b2f83233588420a7f8d03fbe76cd4064133bbb272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionHandlersStaticFiles",
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
class AppEngineStandardAppVersionHandlersStaticFiles:
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
        :param application_readable: Whether files should also be uploaded as code data. By default, files declared in static file handlers are uploaded as static data and are only served to end users; they cannot be read by the application. If enabled, uploads are charged against both your code and static data storage resource quotas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#application_readable AppEngineStandardAppVersion#application_readable}
        :param expiration: Time a static file served by this handler should be cached by web proxies and browsers. A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#expiration AppEngineStandardAppVersion#expiration}
        :param http_headers: HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#http_headers AppEngineStandardAppVersion#http_headers}
        :param mime_type: MIME type used to serve all files served by this handler. Defaults to file-specific MIME types, which are derived from each file's filename extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#mime_type AppEngineStandardAppVersion#mime_type}
        :param path: Path to the static files matched by the URL pattern, from the application root directory. The path can refer to text matched in groupings in the URL pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#path AppEngineStandardAppVersion#path}
        :param require_matching_file: Whether this handler should match the request if the file referenced by the handler does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#require_matching_file AppEngineStandardAppVersion#require_matching_file}
        :param upload_path_regex: Regular expression that matches the file paths for all files that should be referenced by this handler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#upload_path_regex AppEngineStandardAppVersion#upload_path_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375cc957045c8f074d165ffc0d85be6877739049440bf20dd754061e98d9cc24)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#application_readable AppEngineStandardAppVersion#application_readable}
        '''
        result = self._values.get("application_readable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Time a static file served by this handler should be cached by web proxies and browsers.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#expiration AppEngineStandardAppVersion#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP headers to use for all responses from these URLs. An object containing a list of "key:value" value pairs.".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#http_headers AppEngineStandardAppVersion#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mime_type(self) -> typing.Optional[builtins.str]:
        '''MIME type used to serve all files served by this handler.

        Defaults to file-specific MIME types, which are derived from each file's filename extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#mime_type AppEngineStandardAppVersion#mime_type}
        '''
        result = self._values.get("mime_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to the static files matched by the URL pattern, from the application root directory.

        The path can refer to text matched in groupings in the URL pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#path AppEngineStandardAppVersion#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_matching_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this handler should match the request if the file referenced by the handler does not exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#require_matching_file AppEngineStandardAppVersion#require_matching_file}
        '''
        result = self._values.get("require_matching_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upload_path_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression that matches the file paths for all files that should be referenced by this handler.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#upload_path_regex AppEngineStandardAppVersion#upload_path_regex}
        '''
        result = self._values.get("upload_path_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionHandlersStaticFiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionHandlersStaticFilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionHandlersStaticFilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cd87c1fcf47e12b9c71754fa18bef809aecc202a0a63b551ab19bbc35d2a42a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04f2baad94f5fae2ee2021ecde1f0be01244bf0caaceb14059d0b0edc27d5e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationReadable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f408a8661d2766c26bbd66ccffa32d6f8b709d7b1eae1b228aa9fddf1884e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "httpHeaders"))

    @http_headers.setter
    def http_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b33f93e6c51e99811faee6eb523d135b1dfc3a2af3f1bd64264f739132be9c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mimeType")
    def mime_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mimeType"))

    @mime_type.setter
    def mime_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548f8a445a9ca98751e4f19283812364211e176fb0270d027d82f8bf5a756fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mimeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a06b876cdfd6dd59af265c914fa6580f8265b8fa6a189445b5230873eb9660)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78041667110cc88bba220d0d5c7b52e52bb30514b8aa70845a59df7a68e541bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireMatchingFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadPathRegex")
    def upload_path_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uploadPathRegex"))

    @upload_path_regex.setter
    def upload_path_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4cd25867af493547266b5aba649a1f4883c0ac55782252b7cd31f8d92461d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadPathRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionHandlersStaticFiles]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionHandlersStaticFiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionHandlersStaticFiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc5656087a48170f8673ad5f8990ad1dcd0395a225dd5e98a5003eed09e16c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionLibraries",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "version": "version"},
)
class AppEngineStandardAppVersionLibraries:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the library. Example "django". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#name AppEngineStandardAppVersion#name}
        :param version: Version of the library to select, or "latest". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#version AppEngineStandardAppVersion#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb9069ef98909d4e0000e36e62616223eaa9b83d14e93b4cf0ff210a3dff3ec)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#name AppEngineStandardAppVersion#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the library to select, or "latest".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#version AppEngineStandardAppVersion#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionLibraries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionLibrariesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionLibrariesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26fd5ef20d35afaa5a08775621614f664cb647cbe57e06eda99eb84b4a12b640)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppEngineStandardAppVersionLibrariesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1736fc1a0d2355fe2e36f361b399fd435e84cf2deede05149e05e9488c4ae411)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppEngineStandardAppVersionLibrariesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878f70835fecff4583bbf2aa7afeba2627f81e942e29e2646914321dd3691532)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a50caf693a31ae68fdf6958af30ca565a8f44c605ca5aadbb03ff333378b54c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7c275b8a4e0e4dc0c2f141fca209c55b6f6b82e1bdc39a30149e7d8c7879af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionLibraries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionLibraries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionLibraries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6fec354c268d1d1ceca0e58e2e2ff266ce8099ffc7f4758cf6c9f55e4e63dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppEngineStandardAppVersionLibrariesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionLibrariesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__828a710ec0eebaaa7a587d33dcaf092a5464f394826189f699aeaae7ce966ef2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d362531bef705875f291c5499cef424158fc89157a67a34320cfb4c2621f0e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e702bee9aa7a11d6878b77414b8e9fa0030519274bdb72b93a5a3a3472a437a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionLibraries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionLibraries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionLibraries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89d705b4e464e04e9800f078f94c01f27451fc28bed625273cbb583dddedd64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionManualScaling",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class AppEngineStandardAppVersionManualScaling:
    def __init__(self, *, instances: jsii.Number) -> None:
        '''
        :param instances: Number of instances to assign to the service at the start. **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2 Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#instances AppEngineStandardAppVersion#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a58dccc50a06068071d593f5717910fabe5310896264e819d3cdc5b0302ca08)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instances": instances,
        }

    @builtins.property
    def instances(self) -> jsii.Number:
        '''Number of instances to assign to the service at the start.

        **Note:** When managing the number of instances at runtime through the App Engine Admin API or the (now deprecated) Python 2
        Modules API set_num_instances() you must use 'lifecycle.ignore_changes = ["manual_scaling"[0].instances]' to prevent drift detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#instances AppEngineStandardAppVersion#instances}
        '''
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionManualScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionManualScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionManualScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f00341647437369d507c33531da9dd90be6e7db2174341355b6c1adb554618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54eaaebafa9e9647f57bcb76b7d4fe593be4f87680a12be7e597f8b462dbd818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionManualScaling]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionManualScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionManualScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efcfda50ba54187f9e0dcd37c51bb3bea7fbddfcf7f1ad3864d6f9148174f704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AppEngineStandardAppVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#create AppEngineStandardAppVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#delete AppEngineStandardAppVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#update AppEngineStandardAppVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017b47b3f5bdc6b459903bfc6b6b8161c558a1ba7f12714fa7377b0e5ae012f3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#create AppEngineStandardAppVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#delete AppEngineStandardAppVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#update AppEngineStandardAppVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__880cc35f0322034a3b6118c3a8ba013b0563367ee57586b10ca2231a3ca90c0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c24ca56522d9f8163baac073ddae68bd3887339c37e54c834f13584ce0cbb0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e674b777b78d4509c079b7d966a74430ac2c64554df6214e13aa92afecc8f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398b5552790950f86acae68f8253b69bd786f76c7f653d3f23d62a7a34e4b817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3eea7e8f49e94db7b1ae03f9b1676d83080c3a9ea94b901866808cab4409c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionVpcAccessConnector",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "egress_setting": "egressSetting"},
)
class AppEngineStandardAppVersionVpcAccessConnector:
    def __init__(
        self,
        *,
        name: builtins.str,
        egress_setting: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Full Serverless VPC Access Connector name e.g. /projects/my-project/locations/us-central1/connectors/c1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#name AppEngineStandardAppVersion#name}
        :param egress_setting: The egress setting for the connector, controlling what traffic is diverted through it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#egress_setting AppEngineStandardAppVersion#egress_setting}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c94b8f8b82cf12f02e6d5e4c82c15e2002ff62a3fe8f858c95d84c47a9f205)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#name AppEngineStandardAppVersion#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def egress_setting(self) -> typing.Optional[builtins.str]:
        '''The egress setting for the connector, controlling what traffic is diverted through it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_standard_app_version#egress_setting AppEngineStandardAppVersion#egress_setting}
        '''
        result = self._values.get("egress_setting")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineStandardAppVersionVpcAccessConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineStandardAppVersionVpcAccessConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineStandardAppVersion.AppEngineStandardAppVersionVpcAccessConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1ded76584384fa3a72b5d4ddfd1cb56a641efd663b973113ed5e9e9a0dfcb05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1219580506dcb64d4fad9fdb3aff58b536ac58be1770b4007aa4d67864346ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressSetting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3101e7aa3cd4582b6da7a4672d21847eae72118f7b56e4bfb809f89a458a841f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppEngineStandardAppVersionVpcAccessConnector]:
        return typing.cast(typing.Optional[AppEngineStandardAppVersionVpcAccessConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineStandardAppVersionVpcAccessConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e7ce6b095196dd87a98fcf68ba743b38fc3946e5adf2edc8a8b836d0900321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppEngineStandardAppVersion",
    "AppEngineStandardAppVersionAutomaticScaling",
    "AppEngineStandardAppVersionAutomaticScalingOutputReference",
    "AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings",
    "AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettingsOutputReference",
    "AppEngineStandardAppVersionBasicScaling",
    "AppEngineStandardAppVersionBasicScalingOutputReference",
    "AppEngineStandardAppVersionConfig",
    "AppEngineStandardAppVersionDeployment",
    "AppEngineStandardAppVersionDeploymentFiles",
    "AppEngineStandardAppVersionDeploymentFilesList",
    "AppEngineStandardAppVersionDeploymentFilesOutputReference",
    "AppEngineStandardAppVersionDeploymentOutputReference",
    "AppEngineStandardAppVersionDeploymentZip",
    "AppEngineStandardAppVersionDeploymentZipOutputReference",
    "AppEngineStandardAppVersionEntrypoint",
    "AppEngineStandardAppVersionEntrypointOutputReference",
    "AppEngineStandardAppVersionHandlers",
    "AppEngineStandardAppVersionHandlersList",
    "AppEngineStandardAppVersionHandlersOutputReference",
    "AppEngineStandardAppVersionHandlersScript",
    "AppEngineStandardAppVersionHandlersScriptOutputReference",
    "AppEngineStandardAppVersionHandlersStaticFiles",
    "AppEngineStandardAppVersionHandlersStaticFilesOutputReference",
    "AppEngineStandardAppVersionLibraries",
    "AppEngineStandardAppVersionLibrariesList",
    "AppEngineStandardAppVersionLibrariesOutputReference",
    "AppEngineStandardAppVersionManualScaling",
    "AppEngineStandardAppVersionManualScalingOutputReference",
    "AppEngineStandardAppVersionTimeouts",
    "AppEngineStandardAppVersionTimeoutsOutputReference",
    "AppEngineStandardAppVersionVpcAccessConnector",
    "AppEngineStandardAppVersionVpcAccessConnectorOutputReference",
]

publication.publish()

def _typecheckingstub__c388d6369590a49add3066028495ba108e8f8ab9db3d28c144f2fcf52855a4ce(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    deployment: typing.Union[AppEngineStandardAppVersionDeployment, typing.Dict[builtins.str, typing.Any]],
    entrypoint: typing.Union[AppEngineStandardAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionBasicScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionLibraries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manual_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AppEngineStandardAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[AppEngineStandardAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5889170f8810f2eab2b1eafb3ffd2b724c7836494d311d2ec9c48bed70f89e97(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d7a25da7428a9cfaeff2a05c337aeb994be5ca01c9846d0e97d59b70a9be14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0799d08610e28672dbee8af98fcfc337f49c2de5b5c09e820fd71fc383309db(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionLibraries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e1d89c7944c95953482b31f8172922d425702f96c18371a78db786d8a43dbb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03809292826bf95a79a007be3a399329879e46a36f9429e1eafb89d07b9e1b0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f64b0f489868702f7460cb09a57364273588564bfd1dff21a0471867e04ace9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408c183916158f9a414e0dda126aca5420c91a586f8f5f94a60b00699d0fe4b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f871dd29f03a907b491bf732a6471ea20ad08e8c97fc8857a5c79802123bf1bd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60abc5a7541361c17f90b90e6491d3e09b935841baedc3def8b25bbceee4dc19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec193471dcaeb5697fab486a026b28b8d9b88e253c0471edd8ed30061945df3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ea7804311797fbd70a01ef4ee2fd8aa609359890dbe9dc2edaa7d04bec73ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec407220bfcaadd0a5a2ee6115f51fd79bf6cee13e3c3060134c96ba0152c91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b3b044a56cfe4942a145e4b5a82539083b9f84983272eb39561568b18cdc0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea0b578ffc32b609b88d3f0ac2e7546787a1a13d54919cf030c08f28592c5b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ec6e6ef1f0187ac5e7dbc0735c4ce7938c24f84d5087ffae8203fc3d6fe827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c47c22e39589d62eb405092ac368e3ad10ca4ba2392ead4c8d3d66ac1e7a10(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c843bde2730dee38534635723d5a2236f401ad5fd33ae8844ed389330209c8e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccf027a3b78a8ef2f96cba8fe815d63a8a531e8829f7793c34c7f1d98787569(
    *,
    max_concurrent_requests: typing.Optional[jsii.Number] = None,
    max_idle_instances: typing.Optional[jsii.Number] = None,
    max_pending_latency: typing.Optional[builtins.str] = None,
    min_idle_instances: typing.Optional[jsii.Number] = None,
    min_pending_latency: typing.Optional[builtins.str] = None,
    standard_scheduler_settings: typing.Optional[typing.Union[AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171d2651dfeed3aa1d5c12a7276cc859b7722ed238580f86006117449e601690(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8842bbc238b483a8e7de17273d423f9349ce0abb92cd02fb21d400296f4f32e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff7e9458e2da139d6b5b0b58d07ff090a54faacb6692b8d00121500f2d46bc9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502a58ee873a0d1082925a4c67acaba378bbe4f9a812fda0c937cb621fcb1e61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0935dc46e896662ed4a8e8308de5e60b7730532629c601264556123106dccac5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10eb4e59ebde7f85f8e1aafe3c3a4280b99e28c9afb45835bc0eb028b5ff85a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa824f6e058efcf4ab9ae3464e27f191f8131932d1cef97b783cdbfa9b2752ad(
    value: typing.Optional[AppEngineStandardAppVersionAutomaticScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df37acd9beef70f053969b10f0c383267689c6c7f0e72212cc0b59779c889c99(
    *,
    max_instances: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    target_cpu_utilization: typing.Optional[jsii.Number] = None,
    target_throughput_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5313c974f73cd45f321fc72757a1c92019d25c04dc594b78fb0ee66af38ea3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acbc040bc78fb9996fbd2a183c3739d2cede138e546bb9999510b0d98782e82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e3f5e42f07b590dae6591a7b4e5da15a3d51ce709c918316fb4e97c2294444(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6a30d1aa6cb5023ea813cffb1b3fde4d54de739f41200c3962a1c5be5d093f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0912ec3b848e478d55dbeb55d353179ee340d8c1d3b29802ad531f5b602bdc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309923fda5e6b5f106eed6e0ced81fc1f488f4e3fceabd441cdced10aa9e849e(
    value: typing.Optional[AppEngineStandardAppVersionAutomaticScalingStandardSchedulerSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ff08810f9dd0a6c813defb040a51bf94ed3f904c21aee4224559856719c1eb(
    *,
    max_instances: jsii.Number,
    idle_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df252e83727680911cab35acfea55543d2e28e647a2c7791f5f1a46375509682(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250b0b5b51d63920143b7b33b0f6cb22177ed83eb9ce04cf15ad3e51a90f83b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db16fa343d5628c92b37093f0d8484aef608eb188c75a51cf5753a4bd4a1e0cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b7ed06ebdae7aa72abd6b0915ab759f54f37569fc9ecad9131164255378df9(
    value: typing.Optional[AppEngineStandardAppVersionBasicScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb5624fa17adf5a25b848d18ca07910ddbcdc744ef10eeef12afc73e8ae2bdc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deployment: typing.Union[AppEngineStandardAppVersionDeployment, typing.Dict[builtins.str, typing.Any]],
    entrypoint: typing.Union[AppEngineStandardAppVersionEntrypoint, typing.Dict[builtins.str, typing.Any]],
    runtime: builtins.str,
    service: builtins.str,
    app_engine_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionAutomaticScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionBasicScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_service_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    inbound_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_class: typing.Optional[builtins.str] = None,
    libraries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionLibraries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manual_scaling: typing.Optional[typing.Union[AppEngineStandardAppVersionManualScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    noop_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    runtime_api_version: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    threadsafe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AppEngineStandardAppVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_id: typing.Optional[builtins.str] = None,
    vpc_access_connector: typing.Optional[typing.Union[AppEngineStandardAppVersionVpcAccessConnector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d801241060561fa0e2b87da5b424a2ba4312f247867fde4af0a62a7d7f3a995(
    *,
    files: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zip: typing.Optional[typing.Union[AppEngineStandardAppVersionDeploymentZip, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37e3c4318816f9103317834d040a0217c9991be1e676bae032f287d0be26fe6(
    *,
    name: builtins.str,
    source_url: builtins.str,
    sha1_sum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287c3c3a6475e559b70c53fc5f2c04ef89f5822ae2df46781d03aca2bd8d42ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edb17703bbedf261f8c1ae8124a60bdbbbea1cbd9ccfa1ee144316e01e9c2f0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f64ad0fc86bfbbbc64bf58e471e44affd159f0f187a1b87553268ce67ef7694(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa851e34c53008cc930c6bb70e794b5579297b863e72a7019468b1f88b643e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4c4a45aed4b01f9fd7c83c0fa133682416e6b4eabb5b2f981d6030bc620470(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6caca763c39c0b86982dd479780b53acc476d5c94d607500857b23d4ac368b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionDeploymentFiles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0dddf0d0859e7d854d98d54264c68e6b34a5ad8cee529125f45cec75bbb124(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4524196fe047a0bd5339dc14636d7597f00b738d7e1becc5f48fcf4df5d1a051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb96f9dd63a919f042492652d143d7178ffeca3ccb9c18e23f2f29aee1bed65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73dcdfcbb415e574e167eb2660c6e7ee19b6cb961787cf6f2e4d85aec33a782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c40879480b6777aa83d909fb5e783af4aaf44d02b6a23230742faf1acc8916e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionDeploymentFiles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf58855ca5a8f8c08456840863102531e37878e764fbe3dda70245cc6bd6507(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152dacd05effff06082e163cf4b82c67aeacff81457cde8bd23697ec0f3b3c37(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppEngineStandardAppVersionDeploymentFiles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420373a518ef5bb59651d003873d589b657a375e82b9fca3267af025bcfd0e44(
    value: typing.Optional[AppEngineStandardAppVersionDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e01d08e0a7156037d412cf46174570fd3cd6fd8a8b38fd1bc5fefea212fdb0(
    *,
    source_url: builtins.str,
    files_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33094ba5d052016b4368b609f1f73fd28549d62c7d1030cd171975467bb14b4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec3c78d8c48908312fabc796b1fa57334709afd8b6387622cd59b2743999d39(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e22ad6b70fe5267e3bad7bc26b904ac8452b1b3aa992658be1b11bf7f028fc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f205b78c04b1db44966d7e6ae264e7f56da7702c55c45559d7fadb3d7d7c5ad(
    value: typing.Optional[AppEngineStandardAppVersionDeploymentZip],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b8e3dd84635f0da6d4f46e4879d669df7d0031fa7d89cd7d065befe348f494(
    *,
    shell: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8eba4126415e6ab839b67cee1479ff7bc369da6b57e8971dddb9e44fec3cc3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0773fc9ca924cd0ccb115010cf9e3e535db23ab04b2ea4b397d6d1c504c5dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931f3c8c8fa0f6ff0709f741662183c4aafca07e23e89a31d262a388edf4ac97(
    value: typing.Optional[AppEngineStandardAppVersionEntrypoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0344d46fb86dfab5c0a6982097fd89df44d456f87d8db76efe1e163df613e8b8(
    *,
    auth_fail_action: typing.Optional[builtins.str] = None,
    login: typing.Optional[builtins.str] = None,
    redirect_http_response_code: typing.Optional[builtins.str] = None,
    script: typing.Optional[typing.Union[AppEngineStandardAppVersionHandlersScript, typing.Dict[builtins.str, typing.Any]]] = None,
    security_level: typing.Optional[builtins.str] = None,
    static_files: typing.Optional[typing.Union[AppEngineStandardAppVersionHandlersStaticFiles, typing.Dict[builtins.str, typing.Any]]] = None,
    url_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d84db5cc92aeedc3facdb4a7f0323fd6f096e9cd41170181a49e0265547eca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c4ff47155422903760cde9fb83a050dc12584e761cc3dbd0f59df64fbca595(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ad59c253bb7da977151d37c1c32942b1b0b2b273725f8c932af70ac16c6e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70df4c095e3822116f6e1081388882c985a49ed12aeb898ba5eeaa507a5f7dda(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5767407f647ad368f1e14734dceb5044e0280468916ce438bbf6477c778f8118(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eef39c314c1b05dba2ea6f92dafdb50b02e7b1c9eec9e33ab5ed8d8be211b81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionHandlers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1649768603894b6fa46ff9570f08df18995dadd4778df5c8a66f054ea1c48fb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc90d180bfe754f482706ad8ab9cbacda4e9472917fbdca7ba6c2a8956f24da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56470968eb0eca323d4e59447c002722af653671c947881986568cc66fb566b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cd4ff6b0aeeccbe87e21a703f882b6798b40b882d681e0d00133d3da213a97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c613268c5ab76f2f95461373e86b23402778400c9094e6116a4ba338aa33aae1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb695a577e7c3e7158d12a4c7fb3d348c815d7ad43a12a9b6535c2cee7fc175c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e031038623319ab4268912c4cc40b8ac921b63a31cc89358bfb8e8a81c04a206(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionHandlers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c12fbaa554385eed5b131055803073f2270ae9bfb6561fb8af1a9e2b7a29e6(
    *,
    script_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0450970996ef2117a02b131c7fb8c1e2b077784f3f24cb643675fb86173612(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575e9515eda294a0bac9f93d75b4599da1720023fe103aca88d6f4c34510991b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd2f22db2d090e653572b6b2f83233588420a7f8d03fbe76cd4064133bbb272(
    value: typing.Optional[AppEngineStandardAppVersionHandlersScript],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375cc957045c8f074d165ffc0d85be6877739049440bf20dd754061e98d9cc24(
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

def _typecheckingstub__9cd87c1fcf47e12b9c71754fa18bef809aecc202a0a63b551ab19bbc35d2a42a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f2baad94f5fae2ee2021ecde1f0be01244bf0caaceb14059d0b0edc27d5e93(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f408a8661d2766c26bbd66ccffa32d6f8b709d7b1eae1b228aa9fddf1884e74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b33f93e6c51e99811faee6eb523d135b1dfc3a2af3f1bd64264f739132be9c9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548f8a445a9ca98751e4f19283812364211e176fb0270d027d82f8bf5a756fd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a06b876cdfd6dd59af265c914fa6580f8265b8fa6a189445b5230873eb9660(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78041667110cc88bba220d0d5c7b52e52bb30514b8aa70845a59df7a68e541bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4cd25867af493547266b5aba649a1f4883c0ac55782252b7cd31f8d92461d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc5656087a48170f8673ad5f8990ad1dcd0395a225dd5e98a5003eed09e16c5(
    value: typing.Optional[AppEngineStandardAppVersionHandlersStaticFiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb9069ef98909d4e0000e36e62616223eaa9b83d14e93b4cf0ff210a3dff3ec(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fd5ef20d35afaa5a08775621614f664cb647cbe57e06eda99eb84b4a12b640(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1736fc1a0d2355fe2e36f361b399fd435e84cf2deede05149e05e9488c4ae411(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878f70835fecff4583bbf2aa7afeba2627f81e942e29e2646914321dd3691532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a50caf693a31ae68fdf6958af30ca565a8f44c605ca5aadbb03ff333378b54c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c275b8a4e0e4dc0c2f141fca209c55b6f6b82e1bdc39a30149e7d8c7879af6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6fec354c268d1d1ceca0e58e2e2ff266ce8099ffc7f4758cf6c9f55e4e63dd8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppEngineStandardAppVersionLibraries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828a710ec0eebaaa7a587d33dcaf092a5464f394826189f699aeaae7ce966ef2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d362531bef705875f291c5499cef424158fc89157a67a34320cfb4c2621f0e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e702bee9aa7a11d6878b77414b8e9fa0030519274bdb72b93a5a3a3472a437a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89d705b4e464e04e9800f078f94c01f27451fc28bed625273cbb583dddedd64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionLibraries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a58dccc50a06068071d593f5717910fabe5310896264e819d3cdc5b0302ca08(
    *,
    instances: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f00341647437369d507c33531da9dd90be6e7db2174341355b6c1adb554618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54eaaebafa9e9647f57bcb76b7d4fe593be4f87680a12be7e597f8b462dbd818(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcfda50ba54187f9e0dcd37c51bb3bea7fbddfcf7f1ad3864d6f9148174f704(
    value: typing.Optional[AppEngineStandardAppVersionManualScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017b47b3f5bdc6b459903bfc6b6b8161c558a1ba7f12714fa7377b0e5ae012f3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880cc35f0322034a3b6118c3a8ba013b0563367ee57586b10ca2231a3ca90c0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c24ca56522d9f8163baac073ddae68bd3887339c37e54c834f13584ce0cbb0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e674b777b78d4509c079b7d966a74430ac2c64554df6214e13aa92afecc8f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398b5552790950f86acae68f8253b69bd786f76c7f653d3f23d62a7a34e4b817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3eea7e8f49e94db7b1ae03f9b1676d83080c3a9ea94b901866808cab4409c0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineStandardAppVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c94b8f8b82cf12f02e6d5e4c82c15e2002ff62a3fe8f858c95d84c47a9f205(
    *,
    name: builtins.str,
    egress_setting: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ded76584384fa3a72b5d4ddfd1cb56a641efd663b973113ed5e9e9a0dfcb05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1219580506dcb64d4fad9fdb3aff58b536ac58be1770b4007aa4d67864346ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3101e7aa3cd4582b6da7a4672d21847eae72118f7b56e4bfb809f89a458a841f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e7ce6b095196dd87a98fcf68ba743b38fc3946e5adf2edc8a8b836d0900321(
    value: typing.Optional[AppEngineStandardAppVersionVpcAccessConnector],
) -> None:
    """Type checking stubs"""
    pass
