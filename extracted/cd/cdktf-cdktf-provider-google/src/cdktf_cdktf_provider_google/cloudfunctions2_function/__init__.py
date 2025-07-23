r'''
# `google_cloudfunctions2_function`

Refer to the Terraform Registry for docs: [`google_cloudfunctions2_function`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function).
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


class Cloudfunctions2Function(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2Function",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function google_cloudfunctions2_function}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        build_config: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_trigger: typing.Optional[typing.Union["Cloudfunctions2FunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_config: typing.Optional[typing.Union["Cloudfunctions2FunctionServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["Cloudfunctions2FunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function google_cloudfunctions2_function} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of this cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#location Cloudfunctions2Function#location}
        :param name: A user-defined name of the function. Function names must be unique globally and match pattern 'projects/* /locations/* /functions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#name Cloudfunctions2Function#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#build_config Cloudfunctions2Function#build_config}
        :param description: User-provided description of a function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#description Cloudfunctions2Function#description}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_trigger Cloudfunctions2Function#event_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#id Cloudfunctions2Function#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. It must match the pattern projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#kms_key_name Cloudfunctions2Function#kms_key_name}
        :param labels: A set of key/value label pairs associated with this Cloud Function. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#labels Cloudfunctions2Function#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project Cloudfunctions2Function#project}.
        :param service_config: service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_config Cloudfunctions2Function#service_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#timeouts Cloudfunctions2Function#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a777d2c5993a68750b427cb9c1964136fd03b455d25300e773248687decad6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Cloudfunctions2FunctionConfig(
            location=location,
            name=name,
            build_config=build_config,
            description=description,
            event_trigger=event_trigger,
            id=id,
            kms_key_name=kms_key_name,
            labels=labels,
            project=project,
            service_config=service_config,
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
        '''Generates CDKTF code for importing a Cloudfunctions2Function resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Cloudfunctions2Function to import.
        :param import_from_id: The id of the existing Cloudfunctions2Function that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Cloudfunctions2Function to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e7def9eb26d06376f569ab86d0e52a8f23a2b2f693e8a4ab148a67e3bd8ab9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBuildConfig")
    def put_build_config(
        self,
        *,
        automatic_update_policy: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_repository: typing.Optional[builtins.str] = None,
        entry_point: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_deploy_update_policy: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigSource", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_update_policy: automatic_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#automatic_update_policy Cloudfunctions2Function#automatic_update_policy}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#docker_repository Cloudfunctions2Function#docker_repository}
        :param entry_point: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". For Node.js this is name of a function exported by the module specified in source_location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#entry_point Cloudfunctions2Function#entry_point}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#environment_variables Cloudfunctions2Function#environment_variables}
        :param on_deploy_update_policy: on_deploy_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#on_deploy_update_policy Cloudfunctions2Function#on_deploy_update_policy}
        :param runtime: The runtime in which to run the function. Required when deploying a new function, optional when updating an existing function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#runtime Cloudfunctions2Function#runtime}
        :param service_account: The fully-qualified name of the service account to be used for building the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account Cloudfunctions2Function#service_account}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#source Cloudfunctions2Function#source}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#worker_pool Cloudfunctions2Function#worker_pool}
        '''
        value = Cloudfunctions2FunctionBuildConfig(
            automatic_update_policy=automatic_update_policy,
            docker_repository=docker_repository,
            entry_point=entry_point,
            environment_variables=environment_variables,
            on_deploy_update_policy=on_deploy_update_policy,
            runtime=runtime,
            service_account=service_account,
            source=source,
            worker_pool=worker_pool,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildConfig", [value]))

    @jsii.member(jsii_name="putEventTrigger")
    def put_event_trigger(
        self,
        *,
        event_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionEventTriggerEventFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_type: typing.Optional[builtins.str] = None,
        pubsub_topic: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        trigger_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_filters: event_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_filters Cloudfunctions2Function#event_filters}
        :param event_type: Required. The type of event to observe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_type Cloudfunctions2Function#event_type}
        :param pubsub_topic: The name of a Pub/Sub topic in the same project that will be used as the transport topic for the event delivery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#pubsub_topic Cloudfunctions2Function#pubsub_topic}
        :param retry_policy: Describes the retry policy in case of function's execution failure. Retried execution is charged as any other execution. Possible values: ["RETRY_POLICY_UNSPECIFIED", "RETRY_POLICY_DO_NOT_RETRY", "RETRY_POLICY_RETRY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#retry_policy Cloudfunctions2Function#retry_policy}
        :param service_account_email: Optional. The email of the trigger's service account. The service account must have permission to invoke Cloud Run services. If empty, defaults to the Compute Engine default service account: {project_number}-compute@developer.gserviceaccount.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account_email Cloudfunctions2Function#service_account_email}
        :param trigger_region: The region that the trigger will be in. The trigger will only receive events originating in this region. It can be the same region as the function, a different region or multi-region, or the global region. If not provided, defaults to the same region as the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#trigger_region Cloudfunctions2Function#trigger_region}
        '''
        value = Cloudfunctions2FunctionEventTrigger(
            event_filters=event_filters,
            event_type=event_type,
            pubsub_topic=pubsub_topic,
            retry_policy=retry_policy,
            service_account_email=service_account_email,
            trigger_region=trigger_region,
        )

        return typing.cast(None, jsii.invoke(self, "putEventTrigger", [value]))

    @jsii.member(jsii_name="putServiceConfig")
    def put_service_config(
        self,
        *,
        all_traffic_on_latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        available_cpu: typing.Optional[builtins.str] = None,
        available_memory: typing.Optional[builtins.str] = None,
        binary_authorization_policy: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ingress_settings: typing.Optional[builtins.str] = None,
        max_instance_count: typing.Optional[jsii.Number] = None,
        max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        vpc_connector: typing.Optional[builtins.str] = None,
        vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_traffic_on_latest_revision: Whether 100% of traffic is routed to the latest revision. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#all_traffic_on_latest_revision Cloudfunctions2Function#all_traffic_on_latest_revision}
        :param available_cpu: The number of CPUs used in a single container instance. Default value is calculated from available memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#available_cpu Cloudfunctions2Function#available_cpu}
        :param available_memory: The amount of memory available for a function. Defaults to 256M. Supported units are k, M, G, Mi, Gi. If no unit is supplied the value is interpreted as bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#available_memory Cloudfunctions2Function#available_memory}
        :param binary_authorization_policy: The binary authorization policy to be checked when deploying the Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#binary_authorization_policy Cloudfunctions2Function#binary_authorization_policy}
        :param environment_variables: Environment variables that shall be available during function execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#environment_variables Cloudfunctions2Function#environment_variables}
        :param ingress_settings: Available ingress settings. Defaults to "ALLOW_ALL" if unspecified. Default value: "ALLOW_ALL" Possible values: ["ALLOW_ALL", "ALLOW_INTERNAL_ONLY", "ALLOW_INTERNAL_AND_GCLB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#ingress_settings Cloudfunctions2Function#ingress_settings}
        :param max_instance_count: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#max_instance_count Cloudfunctions2Function#max_instance_count}
        :param max_instance_request_concurrency: Sets the maximum number of concurrent requests that each instance can receive. Defaults to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#max_instance_request_concurrency Cloudfunctions2Function#max_instance_request_concurrency}
        :param min_instance_count: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#min_instance_count Cloudfunctions2Function#min_instance_count}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret_environment_variables Cloudfunctions2Function#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret_volumes Cloudfunctions2Function#secret_volumes}
        :param service: Name of the service associated with a Function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service Cloudfunctions2Function#service}
        :param service_account_email: The email of the service account for this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account_email Cloudfunctions2Function#service_account_email}
        :param timeout_seconds: The function execution timeout. Execution is considered failed and can be terminated if the function is not completed at the end of the timeout period. Defaults to 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#timeout_seconds Cloudfunctions2Function#timeout_seconds}
        :param vpc_connector: The Serverless VPC Access connector that this cloud function can connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#vpc_connector Cloudfunctions2Function#vpc_connector}
        :param vpc_connector_egress_settings: Available egress settings. Possible values: ["VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED", "PRIVATE_RANGES_ONLY", "ALL_TRAFFIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#vpc_connector_egress_settings Cloudfunctions2Function#vpc_connector_egress_settings}
        '''
        value = Cloudfunctions2FunctionServiceConfig(
            all_traffic_on_latest_revision=all_traffic_on_latest_revision,
            available_cpu=available_cpu,
            available_memory=available_memory,
            binary_authorization_policy=binary_authorization_policy,
            environment_variables=environment_variables,
            ingress_settings=ingress_settings,
            max_instance_count=max_instance_count,
            max_instance_request_concurrency=max_instance_request_concurrency,
            min_instance_count=min_instance_count,
            secret_environment_variables=secret_environment_variables,
            secret_volumes=secret_volumes,
            service=service,
            service_account_email=service_account_email,
            timeout_seconds=timeout_seconds,
            vpc_connector=vpc_connector,
            vpc_connector_egress_settings=vpc_connector_egress_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putServiceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#create Cloudfunctions2Function#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#delete Cloudfunctions2Function#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#update Cloudfunctions2Function#update}.
        '''
        value = Cloudfunctions2FunctionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBuildConfig")
    def reset_build_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEventTrigger")
    def reset_event_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventTrigger", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServiceConfig")
    def reset_service_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceConfig", []))

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
    @jsii.member(jsii_name="buildConfig")
    def build_config(self) -> "Cloudfunctions2FunctionBuildConfigOutputReference":
        return typing.cast("Cloudfunctions2FunctionBuildConfigOutputReference", jsii.get(self, "buildConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="eventTrigger")
    def event_trigger(self) -> "Cloudfunctions2FunctionEventTriggerOutputReference":
        return typing.cast("Cloudfunctions2FunctionEventTriggerOutputReference", jsii.get(self, "eventTrigger"))

    @builtins.property
    @jsii.member(jsii_name="serviceConfig")
    def service_config(self) -> "Cloudfunctions2FunctionServiceConfigOutputReference":
        return typing.cast("Cloudfunctions2FunctionServiceConfigOutputReference", jsii.get(self, "serviceConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "Cloudfunctions2FunctionTimeoutsOutputReference":
        return typing.cast("Cloudfunctions2FunctionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="buildConfigInput")
    def build_config_input(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfig"]:
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfig"], jsii.get(self, "buildConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTriggerInput")
    def event_trigger_input(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionEventTrigger"]:
        return typing.cast(typing.Optional["Cloudfunctions2FunctionEventTrigger"], jsii.get(self, "eventTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

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
    @jsii.member(jsii_name="serviceConfigInput")
    def service_config_input(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionServiceConfig"]:
        return typing.cast(typing.Optional["Cloudfunctions2FunctionServiceConfig"], jsii.get(self, "serviceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Cloudfunctions2FunctionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Cloudfunctions2FunctionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713870acfc9b7fb30ad998b0f7fe9ab1bcf745fdb1946c35750f7dc0119c8e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8802628b4d0287f8dd7a987c8022b0b52958524b31ccbf02d69dcc032bdf8452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec03652374e41a82e31a3501c9f05293b4b038de4126c346585a675afa23d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767472f67ab5cbaf7db7c7f8dbcae02f5b426e904a0d13ba32a360bfa289981b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a181b391428b173a48bb69e7543e53d3b0a557a23941bc3ef5b70235ff2c250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b287877cb788ea7c873569bb8672b443601c0c28bc793d5572434e39804587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc08b5f8962eaecf6a7db6164983cac3b623483931626d80578b4f559e456e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfig",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_update_policy": "automaticUpdatePolicy",
        "docker_repository": "dockerRepository",
        "entry_point": "entryPoint",
        "environment_variables": "environmentVariables",
        "on_deploy_update_policy": "onDeployUpdatePolicy",
        "runtime": "runtime",
        "service_account": "serviceAccount",
        "source": "source",
        "worker_pool": "workerPool",
    },
)
class Cloudfunctions2FunctionBuildConfig:
    def __init__(
        self,
        *,
        automatic_update_policy: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_repository: typing.Optional[builtins.str] = None,
        entry_point: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_deploy_update_policy: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigSource", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_update_policy: automatic_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#automatic_update_policy Cloudfunctions2Function#automatic_update_policy}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#docker_repository Cloudfunctions2Function#docker_repository}
        :param entry_point: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". For Node.js this is name of a function exported by the module specified in source_location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#entry_point Cloudfunctions2Function#entry_point}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#environment_variables Cloudfunctions2Function#environment_variables}
        :param on_deploy_update_policy: on_deploy_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#on_deploy_update_policy Cloudfunctions2Function#on_deploy_update_policy}
        :param runtime: The runtime in which to run the function. Required when deploying a new function, optional when updating an existing function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#runtime Cloudfunctions2Function#runtime}
        :param service_account: The fully-qualified name of the service account to be used for building the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account Cloudfunctions2Function#service_account}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#source Cloudfunctions2Function#source}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#worker_pool Cloudfunctions2Function#worker_pool}
        '''
        if isinstance(automatic_update_policy, dict):
            automatic_update_policy = Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy(**automatic_update_policy)
        if isinstance(on_deploy_update_policy, dict):
            on_deploy_update_policy = Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy(**on_deploy_update_policy)
        if isinstance(source, dict):
            source = Cloudfunctions2FunctionBuildConfigSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7940f8ec199aa5c02f491ad4099d1f2c2463f9ade32984778ad84d5dea62b383)
            check_type(argname="argument automatic_update_policy", value=automatic_update_policy, expected_type=type_hints["automatic_update_policy"])
            check_type(argname="argument docker_repository", value=docker_repository, expected_type=type_hints["docker_repository"])
            check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument on_deploy_update_policy", value=on_deploy_update_policy, expected_type=type_hints["on_deploy_update_policy"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument worker_pool", value=worker_pool, expected_type=type_hints["worker_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic_update_policy is not None:
            self._values["automatic_update_policy"] = automatic_update_policy
        if docker_repository is not None:
            self._values["docker_repository"] = docker_repository
        if entry_point is not None:
            self._values["entry_point"] = entry_point
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if on_deploy_update_policy is not None:
            self._values["on_deploy_update_policy"] = on_deploy_update_policy
        if runtime is not None:
            self._values["runtime"] = runtime
        if service_account is not None:
            self._values["service_account"] = service_account
        if source is not None:
            self._values["source"] = source
        if worker_pool is not None:
            self._values["worker_pool"] = worker_pool

    @builtins.property
    def automatic_update_policy(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy"]:
        '''automatic_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#automatic_update_policy Cloudfunctions2Function#automatic_update_policy}
        '''
        result = self._values.get("automatic_update_policy")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy"], result)

    @builtins.property
    def docker_repository(self) -> typing.Optional[builtins.str]:
        '''User managed repository created in Artifact Registry optionally with a customer managed encryption key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#docker_repository Cloudfunctions2Function#docker_repository}
        '''
        result = self._values.get("docker_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry_point(self) -> typing.Optional[builtins.str]:
        '''The name of the function (as defined in source code) that will be executed.

        Defaults to the resource name suffix, if not specified. For backward
        compatibility, if function with given name is not found, then the system
        will try to use function named "function". For Node.js this is name of a
        function exported by the module specified in source_location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#entry_point Cloudfunctions2Function#entry_point}
        '''
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-provided build-time environment variables for the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#environment_variables Cloudfunctions2Function#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_deploy_update_policy(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy"]:
        '''on_deploy_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#on_deploy_update_policy Cloudfunctions2Function#on_deploy_update_policy}
        '''
        result = self._values.get("on_deploy_update_policy")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy"], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''The runtime in which to run the function. Required when deploying a new function, optional when updating an existing function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#runtime Cloudfunctions2Function#runtime}
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified name of the service account to be used for building the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account Cloudfunctions2Function#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional["Cloudfunctions2FunctionBuildConfigSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#source Cloudfunctions2Function#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigSource"], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Build Custom Worker Pool that should be used to build the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#worker_pool Cloudfunctions2Function#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionBuildConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__197528e0a99b9521e1f1ac8e970c8f8ca5aebf7eb86be01a963b856f99784c75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95998965b4c9b8a9cc52d3dcab40fa80bcbd4df7ccc5d83cc8b975520081ee3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__238d6db85291ccd211e14eadf2c44ce1c75f4794d3c0c18a9a3179192ebe8cf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212f824208852be85ceb636c38671cb8458f389878539210743e2ede7d05170e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudfunctions2FunctionBuildConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c055ffb2ce67c0fcac6fb22d6a9af1b680960956b42fb03d9f8118ca238ae73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutomaticUpdatePolicy")
    def put_automatic_update_policy(self) -> None:
        value = Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy()

        return typing.cast(None, jsii.invoke(self, "putAutomaticUpdatePolicy", [value]))

    @jsii.member(jsii_name="putOnDeployUpdatePolicy")
    def put_on_deploy_update_policy(self) -> None:
        value = Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy()

        return typing.cast(None, jsii.invoke(self, "putOnDeployUpdatePolicy", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        repo_source: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#repo_source Cloudfunctions2Function#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#storage_source Cloudfunctions2Function#storage_source}
        '''
        value = Cloudfunctions2FunctionBuildConfigSource(
            repo_source=repo_source, storage_source=storage_source
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetAutomaticUpdatePolicy")
    def reset_automatic_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticUpdatePolicy", []))

    @jsii.member(jsii_name="resetDockerRepository")
    def reset_docker_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerRepository", []))

    @jsii.member(jsii_name="resetEntryPoint")
    def reset_entry_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntryPoint", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetOnDeployUpdatePolicy")
    def reset_on_deploy_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDeployUpdatePolicy", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetWorkerPool")
    def reset_worker_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerPool", []))

    @builtins.property
    @jsii.member(jsii_name="automaticUpdatePolicy")
    def automatic_update_policy(
        self,
    ) -> Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference:
        return typing.cast(Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference, jsii.get(self, "automaticUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildAttribute"))

    @builtins.property
    @jsii.member(jsii_name="onDeployUpdatePolicy")
    def on_deploy_update_policy(
        self,
    ) -> Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference:
        return typing.cast(Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference, jsii.get(self, "onDeployUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Cloudfunctions2FunctionBuildConfigSourceOutputReference":
        return typing.cast("Cloudfunctions2FunctionBuildConfigSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="automaticUpdatePolicyInput")
    def automatic_update_policy_input(
        self,
    ) -> typing.Optional[Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy], jsii.get(self, "automaticUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerRepositoryInput")
    def docker_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="entryPointInput")
    def entry_point_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entryPointInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="onDeployUpdatePolicyInput")
    def on_deploy_update_policy_input(
        self,
    ) -> typing.Optional[Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy], jsii.get(self, "onDeployUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfigSource"]:
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="workerPoolInput")
    def worker_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerRepository")
    def docker_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerRepository"))

    @docker_repository.setter
    def docker_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5332428eba0ac891375b228a482c48a6acc9051509c63dd292c13ab39a1e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryPoint")
    def entry_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryPoint"))

    @entry_point.setter
    def entry_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3649bd8f31625dc419b24ade40f6b0732104a3fec5fd057ca1314f58c9963d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entryPoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e61700dffa0037ab5e125776c38175703607fcd1ebda55f71ae2d345814631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ec82512490726edbc265b5c55f4978cda03a34b6a8262cf8789a054f29c48c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b1bf9ecfd6302b62e240ef80c80e54254457721bdc32884160cfebf9f79de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43009103601218ad110c603a961248b5ab8600b25aef084908fd5bb8aff51fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Cloudfunctions2FunctionBuildConfig]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionBuildConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee0bd14fec5dad8669b25d87a3b57673fe6ceb906b00deb033c0f6b97ff15be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigSource",
    jsii_struct_bases=[],
    name_mapping={"repo_source": "repoSource", "storage_source": "storageSource"},
)
class Cloudfunctions2FunctionBuildConfigSource:
    def __init__(
        self,
        *,
        repo_source: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["Cloudfunctions2FunctionBuildConfigSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#repo_source Cloudfunctions2Function#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#storage_source Cloudfunctions2Function#storage_source}
        '''
        if isinstance(repo_source, dict):
            repo_source = Cloudfunctions2FunctionBuildConfigSourceRepoSource(**repo_source)
        if isinstance(storage_source, dict):
            storage_source = Cloudfunctions2FunctionBuildConfigSourceStorageSource(**storage_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd2eaa666b4a8dfcd42cbee89adf2352e689fb33f783938842293be30a494ee)
            check_type(argname="argument repo_source", value=repo_source, expected_type=type_hints["repo_source"])
            check_type(argname="argument storage_source", value=storage_source, expected_type=type_hints["storage_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if repo_source is not None:
            self._values["repo_source"] = repo_source
        if storage_source is not None:
            self._values["storage_source"] = storage_source

    @builtins.property
    def repo_source(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfigSourceRepoSource"]:
        '''repo_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#repo_source Cloudfunctions2Function#repo_source}
        '''
        result = self._values.get("repo_source")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigSourceRepoSource"], result)

    @builtins.property
    def storage_source(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfigSourceStorageSource"]:
        '''storage_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#storage_source Cloudfunctions2Function#storage_source}
        '''
        result = self._values.get("storage_source")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigSourceStorageSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionBuildConfigSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionBuildConfigSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b86c5179e83cb148a33f0d753d7b159e1256ece8cf0a7baa687264516f5b6c14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepoSource")
    def put_repo_source(
        self,
        *,
        branch_name: typing.Optional[builtins.str] = None,
        commit_sha: typing.Optional[builtins.str] = None,
        dir: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_id: typing.Optional[builtins.str] = None,
        repo_name: typing.Optional[builtins.str] = None,
        tag_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch_name: Regex matching branches to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#branch_name Cloudfunctions2Function#branch_name}
        :param commit_sha: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#commit_sha Cloudfunctions2Function#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#dir Cloudfunctions2Function#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#invert_regex Cloudfunctions2Function#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project_id Cloudfunctions2Function#project_id}
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#repo_name Cloudfunctions2Function#repo_name}
        :param tag_name: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#tag_name Cloudfunctions2Function#tag_name}
        '''
        value = Cloudfunctions2FunctionBuildConfigSourceRepoSource(
            branch_name=branch_name,
            commit_sha=commit_sha,
            dir=dir,
            invert_regex=invert_regex,
            project_id=project_id,
            repo_name=repo_name,
            tag_name=tag_name,
        )

        return typing.cast(None, jsii.invoke(self, "putRepoSource", [value]))

    @jsii.member(jsii_name="putStorageSource")
    def put_storage_source(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        generation: typing.Optional[jsii.Number] = None,
        object: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#bucket Cloudfunctions2Function#bucket}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#generation Cloudfunctions2Function#generation}
        :param object: Google Cloud Storage object containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#object Cloudfunctions2Function#object}
        '''
        value = Cloudfunctions2FunctionBuildConfigSourceStorageSource(
            bucket=bucket, generation=generation, object=object
        )

        return typing.cast(None, jsii.invoke(self, "putStorageSource", [value]))

    @jsii.member(jsii_name="resetRepoSource")
    def reset_repo_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepoSource", []))

    @jsii.member(jsii_name="resetStorageSource")
    def reset_storage_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageSource", []))

    @builtins.property
    @jsii.member(jsii_name="repoSource")
    def repo_source(
        self,
    ) -> "Cloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference":
        return typing.cast("Cloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference", jsii.get(self, "repoSource"))

    @builtins.property
    @jsii.member(jsii_name="storageSource")
    def storage_source(
        self,
    ) -> "Cloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference":
        return typing.cast("Cloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference", jsii.get(self, "storageSource"))

    @builtins.property
    @jsii.member(jsii_name="repoSourceInput")
    def repo_source_input(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfigSourceRepoSource"]:
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigSourceRepoSource"], jsii.get(self, "repoSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSourceInput")
    def storage_source_input(
        self,
    ) -> typing.Optional["Cloudfunctions2FunctionBuildConfigSourceStorageSource"]:
        return typing.cast(typing.Optional["Cloudfunctions2FunctionBuildConfigSourceStorageSource"], jsii.get(self, "storageSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudfunctions2FunctionBuildConfigSource]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfigSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionBuildConfigSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917f63c51170eb2d199243789f93537f46d62572211ac66ff7aa7d53d190d2c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigSourceRepoSource",
    jsii_struct_bases=[],
    name_mapping={
        "branch_name": "branchName",
        "commit_sha": "commitSha",
        "dir": "dir",
        "invert_regex": "invertRegex",
        "project_id": "projectId",
        "repo_name": "repoName",
        "tag_name": "tagName",
    },
)
class Cloudfunctions2FunctionBuildConfigSourceRepoSource:
    def __init__(
        self,
        *,
        branch_name: typing.Optional[builtins.str] = None,
        commit_sha: typing.Optional[builtins.str] = None,
        dir: typing.Optional[builtins.str] = None,
        invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_id: typing.Optional[builtins.str] = None,
        repo_name: typing.Optional[builtins.str] = None,
        tag_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch_name: Regex matching branches to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#branch_name Cloudfunctions2Function#branch_name}
        :param commit_sha: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#commit_sha Cloudfunctions2Function#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#dir Cloudfunctions2Function#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#invert_regex Cloudfunctions2Function#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project_id Cloudfunctions2Function#project_id}
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#repo_name Cloudfunctions2Function#repo_name}
        :param tag_name: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#tag_name Cloudfunctions2Function#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e63e09f6ab13d39ff1d6980a3a296b231a5ee13eb6b33c1e3765eb6ed72571)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument commit_sha", value=commit_sha, expected_type=type_hints["commit_sha"])
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument invert_regex", value=invert_regex, expected_type=type_hints["invert_regex"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if commit_sha is not None:
            self._values["commit_sha"] = commit_sha
        if dir is not None:
            self._values["dir"] = dir
        if invert_regex is not None:
            self._values["invert_regex"] = invert_regex
        if project_id is not None:
            self._values["project_id"] = project_id
        if repo_name is not None:
            self._values["repo_name"] = repo_name
        if tag_name is not None:
            self._values["tag_name"] = tag_name

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''Regex matching branches to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#branch_name Cloudfunctions2Function#branch_name}
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''Regex matching tags to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#commit_sha Cloudfunctions2Function#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''Directory, relative to the source root, in which to run the build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#dir Cloudfunctions2Function#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger a build if the revision regex does NOT match the revision regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#invert_regex Cloudfunctions2Function#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project_id Cloudfunctions2Function#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Source Repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#repo_name Cloudfunctions2Function#repo_name}
        '''
        result = self._values.get("repo_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''Regex matching tags to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#tag_name Cloudfunctions2Function#tag_name}
        '''
        result = self._values.get("tag_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionBuildConfigSourceRepoSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a68742dc8dabdb5b95f539618c56fa2f9593709dd18e6e0ad8d84162049ad449)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranchName")
    def reset_branch_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchName", []))

    @jsii.member(jsii_name="resetCommitSha")
    def reset_commit_sha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitSha", []))

    @jsii.member(jsii_name="resetDir")
    def reset_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDir", []))

    @jsii.member(jsii_name="resetInvertRegex")
    def reset_invert_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertRegex", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRepoName")
    def reset_repo_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepoName", []))

    @jsii.member(jsii_name="resetTagName")
    def reset_tag_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagName", []))

    @builtins.property
    @jsii.member(jsii_name="branchNameInput")
    def branch_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameInput"))

    @builtins.property
    @jsii.member(jsii_name="commitShaInput")
    def commit_sha_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitShaInput"))

    @builtins.property
    @jsii.member(jsii_name="dirInput")
    def dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dirInput"))

    @builtins.property
    @jsii.member(jsii_name="invertRegexInput")
    def invert_regex_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="repoNameInput")
    def repo_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNameInput")
    def tag_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagNameInput"))

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377814d7f612715b9777fa4675d5dfe2e0656c50fb6601624caf065e9ee8d26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c6e3a9ed5cc0519a1a18dbcf21efb708e7c13c906b78a96d1e4e02f91f6aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740b561db72fc2b2fad9b91746442ee2eadc3f6228fc7fc19d2b67dbec8757c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertRegex")
    def invert_regex(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertRegex"))

    @invert_regex.setter
    def invert_regex(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c7f9bf502d364d8f0bf0db7e3476386f5f87dea4d12d580d6044e725ccf158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf2d566afbcb05bdcdc243571f24e1832509b50580fc6f17d21b0b96d713c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @repo_name.setter
    def repo_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebaaade49f6bee6b30609cb5a47283a0c6e37fac44b2c130d1070705b13cf80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba4f0213d4b774844c779c11e0ef323394d40f0786897f1301ca3c7b06a7677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudfunctions2FunctionBuildConfigSourceRepoSource]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfigSourceRepoSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionBuildConfigSourceRepoSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82341577dca62f7c68cba874c2da341c93f9f0d9a87cad0d8ee23b1f66f382a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigSourceStorageSource",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "generation": "generation", "object": "object"},
)
class Cloudfunctions2FunctionBuildConfigSourceStorageSource:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        generation: typing.Optional[jsii.Number] = None,
        object: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#bucket Cloudfunctions2Function#bucket}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#generation Cloudfunctions2Function#generation}
        :param object: Google Cloud Storage object containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#object Cloudfunctions2Function#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1626ca35445566696f8b53661fdc82339a4bd5e2608fdb9b724687c4cb9c38)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if generation is not None:
            self._values["generation"] = generation
        if object is not None:
            self._values["object"] = object

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage bucket containing the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#bucket Cloudfunctions2Function#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#generation Cloudfunctions2Function#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def object(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage object containing the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#object Cloudfunctions2Function#object}
        '''
        result = self._values.get("object")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionBuildConfigSourceStorageSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a46cfec4d33b81b19ffbdc4ef045c2f430808e37b95a49757da5ddd057cab56d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @jsii.member(jsii_name="resetObject")
    def reset_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObject", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c857a7fa5f4d12351dd978d1890c21ce27fd562738993cf66f4333576d5c941e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c008b3c92ede38b6423940b9ec32bbcccab6a8a95a0b67c356e5087ac3525e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb79e162e5e457b6412278b6da53713c28129eba25a2a90fd8b6032d0ac3046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudfunctions2FunctionBuildConfigSourceStorageSource]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfigSourceStorageSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionBuildConfigSourceStorageSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df33685277bb5ff4a858e9ab45861791e1f82841340beeb42ed69f653de4ce36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionConfig",
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
        "name": "name",
        "build_config": "buildConfig",
        "description": "description",
        "event_trigger": "eventTrigger",
        "id": "id",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "project": "project",
        "service_config": "serviceConfig",
        "timeouts": "timeouts",
    },
)
class Cloudfunctions2FunctionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        build_config: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_trigger: typing.Optional[typing.Union["Cloudfunctions2FunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_config: typing.Optional[typing.Union["Cloudfunctions2FunctionServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["Cloudfunctions2FunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of this cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#location Cloudfunctions2Function#location}
        :param name: A user-defined name of the function. Function names must be unique globally and match pattern 'projects/* /locations/* /functions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#name Cloudfunctions2Function#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#build_config Cloudfunctions2Function#build_config}
        :param description: User-provided description of a function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#description Cloudfunctions2Function#description}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_trigger Cloudfunctions2Function#event_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#id Cloudfunctions2Function#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. It must match the pattern projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#kms_key_name Cloudfunctions2Function#kms_key_name}
        :param labels: A set of key/value label pairs associated with this Cloud Function. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#labels Cloudfunctions2Function#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project Cloudfunctions2Function#project}.
        :param service_config: service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_config Cloudfunctions2Function#service_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#timeouts Cloudfunctions2Function#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(build_config, dict):
            build_config = Cloudfunctions2FunctionBuildConfig(**build_config)
        if isinstance(event_trigger, dict):
            event_trigger = Cloudfunctions2FunctionEventTrigger(**event_trigger)
        if isinstance(service_config, dict):
            service_config = Cloudfunctions2FunctionServiceConfig(**service_config)
        if isinstance(timeouts, dict):
            timeouts = Cloudfunctions2FunctionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e210f0d04f5e59c6d64faa63e9cf52d3e8fd2a215b24089a5f24200cf0e64e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument build_config", value=build_config, expected_type=type_hints["build_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_trigger", value=event_trigger, expected_type=type_hints["event_trigger"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument service_config", value=service_config, expected_type=type_hints["service_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if build_config is not None:
            self._values["build_config"] = build_config
        if description is not None:
            self._values["description"] = description
        if event_trigger is not None:
            self._values["event_trigger"] = event_trigger
        if id is not None:
            self._values["id"] = id
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if service_config is not None:
            self._values["service_config"] = service_config
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
        '''The location of this cloud function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#location Cloudfunctions2Function#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A user-defined name of the function. Function names must be unique globally and match pattern 'projects/* /locations/* /functions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#name Cloudfunctions2Function#name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_config(self) -> typing.Optional[Cloudfunctions2FunctionBuildConfig]:
        '''build_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#build_config Cloudfunctions2Function#build_config}
        '''
        result = self._values.get("build_config")
        return typing.cast(typing.Optional[Cloudfunctions2FunctionBuildConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description of a function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#description Cloudfunctions2Function#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_trigger(self) -> typing.Optional["Cloudfunctions2FunctionEventTrigger"]:
        '''event_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_trigger Cloudfunctions2Function#event_trigger}
        '''
        result = self._values.get("event_trigger")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionEventTrigger"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#id Cloudfunctions2Function#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources.

        It must match the pattern projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#kms_key_name Cloudfunctions2Function#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs associated with this Cloud Function.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#labels Cloudfunctions2Function#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project Cloudfunctions2Function#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_config(self) -> typing.Optional["Cloudfunctions2FunctionServiceConfig"]:
        '''service_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_config Cloudfunctions2Function#service_config}
        '''
        result = self._values.get("service_config")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionServiceConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["Cloudfunctions2FunctionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#timeouts Cloudfunctions2Function#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["Cloudfunctions2FunctionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionEventTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "event_filters": "eventFilters",
        "event_type": "eventType",
        "pubsub_topic": "pubsubTopic",
        "retry_policy": "retryPolicy",
        "service_account_email": "serviceAccountEmail",
        "trigger_region": "triggerRegion",
    },
)
class Cloudfunctions2FunctionEventTrigger:
    def __init__(
        self,
        *,
        event_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionEventTriggerEventFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_type: typing.Optional[builtins.str] = None,
        pubsub_topic: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        trigger_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_filters: event_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_filters Cloudfunctions2Function#event_filters}
        :param event_type: Required. The type of event to observe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_type Cloudfunctions2Function#event_type}
        :param pubsub_topic: The name of a Pub/Sub topic in the same project that will be used as the transport topic for the event delivery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#pubsub_topic Cloudfunctions2Function#pubsub_topic}
        :param retry_policy: Describes the retry policy in case of function's execution failure. Retried execution is charged as any other execution. Possible values: ["RETRY_POLICY_UNSPECIFIED", "RETRY_POLICY_DO_NOT_RETRY", "RETRY_POLICY_RETRY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#retry_policy Cloudfunctions2Function#retry_policy}
        :param service_account_email: Optional. The email of the trigger's service account. The service account must have permission to invoke Cloud Run services. If empty, defaults to the Compute Engine default service account: {project_number}-compute@developer.gserviceaccount.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account_email Cloudfunctions2Function#service_account_email}
        :param trigger_region: The region that the trigger will be in. The trigger will only receive events originating in this region. It can be the same region as the function, a different region or multi-region, or the global region. If not provided, defaults to the same region as the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#trigger_region Cloudfunctions2Function#trigger_region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1162c899938b8426ca10cc3fee5e93d327c75161152cb1ad357f00f4fae877ae)
            check_type(argname="argument event_filters", value=event_filters, expected_type=type_hints["event_filters"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument trigger_region", value=trigger_region, expected_type=type_hints["trigger_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_filters is not None:
            self._values["event_filters"] = event_filters
        if event_type is not None:
            self._values["event_type"] = event_type
        if pubsub_topic is not None:
            self._values["pubsub_topic"] = pubsub_topic
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email
        if trigger_region is not None:
            self._values["trigger_region"] = trigger_region

    @builtins.property
    def event_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionEventTriggerEventFilters"]]]:
        '''event_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_filters Cloudfunctions2Function#event_filters}
        '''
        result = self._values.get("event_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionEventTriggerEventFilters"]]], result)

    @builtins.property
    def event_type(self) -> typing.Optional[builtins.str]:
        '''Required. The type of event to observe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#event_type Cloudfunctions2Function#event_type}
        '''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_topic(self) -> typing.Optional[builtins.str]:
        '''The name of a Pub/Sub topic in the same project that will be used as the transport topic for the event delivery.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#pubsub_topic Cloudfunctions2Function#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional[builtins.str]:
        '''Describes the retry policy in case of function's execution failure.

        Retried execution is charged as any other execution. Possible values: ["RETRY_POLICY_UNSPECIFIED", "RETRY_POLICY_DO_NOT_RETRY", "RETRY_POLICY_RETRY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#retry_policy Cloudfunctions2Function#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The email of the trigger's service account. The service account
        must have permission to invoke Cloud Run services. If empty, defaults to the
        Compute Engine default service account: {project_number}-compute@developer.gserviceaccount.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account_email Cloudfunctions2Function#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_region(self) -> typing.Optional[builtins.str]:
        '''The region that the trigger will be in.

        The trigger will only receive
        events originating in this region. It can be the same
        region as the function, a different region or multi-region, or the global
        region. If not provided, defaults to the same region as the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#trigger_region Cloudfunctions2Function#trigger_region}
        '''
        result = self._values.get("trigger_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionEventTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionEventTriggerEventFilters",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute", "value": "value", "operator": "operator"},
)
class Cloudfunctions2FunctionEventTriggerEventFilters:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        value: builtins.str,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute: 'Required. The name of a CloudEvents attribute. Currently, only a subset of attributes are supported for filtering. Use the 'gcloud eventarc providers describe' command to learn more about events and their attributes. Do not filter for the 'type' attribute here, as this is already achieved by the resource's 'event_type' attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#attribute Cloudfunctions2Function#attribute}
        :param value: Required. The value for the attribute. If the operator field is set as 'match-path-pattern', this value can be a path pattern instead of an exact value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#value Cloudfunctions2Function#value}
        :param operator: Optional. The operator used for matching the events with the value of the filter. If not specified, only events that have an exact key-value pair specified in the filter are matched. The only allowed value is 'match-path-pattern'. `See documentation on path patterns here <https://cloud.google.com/eventarc/docs/path-patterns>`_' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#operator Cloudfunctions2Function#operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3585d1936ea407b4c3ba523eebc75939cb951cbc3389973902f05a494dcb3d5)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute": attribute,
            "value": value,
        }
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def attribute(self) -> builtins.str:
        ''''Required.

        The name of a CloudEvents attribute.
        Currently, only a subset of attributes are supported for filtering. Use the 'gcloud eventarc providers describe' command to learn more about events and their attributes.
        Do not filter for the 'type' attribute here, as this is already achieved by the resource's 'event_type' attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#attribute Cloudfunctions2Function#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Required.

        The value for the attribute.
        If the operator field is set as 'match-path-pattern', this value can be a path pattern instead of an exact value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#value Cloudfunctions2Function#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The operator used for matching the events with the value of
        the filter. If not specified, only events that have an exact key-value
        pair specified in the filter are matched.
        The only allowed value is 'match-path-pattern'.
        `See documentation on path patterns here <https://cloud.google.com/eventarc/docs/path-patterns>`_'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#operator Cloudfunctions2Function#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionEventTriggerEventFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionEventTriggerEventFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionEventTriggerEventFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df306a7040a9b390d9bb0edb45ea30e43aa307fedb216a87c5bf4acc199d41df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Cloudfunctions2FunctionEventTriggerEventFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7decc67899845de74039ce3396c5dd55868ea4baf647df234a33034760333fdb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Cloudfunctions2FunctionEventTriggerEventFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0263542882b6ed768bfca263588ae5f4d84cdbb55ba320eab4d01a26c9e85174)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69d8605d6cebf0578947ced8b0bda312c61a79925796da0ef7f25d7e15fe2cdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77a85dfb249f23aa477d15cf96aae3829452a93452111cb59472036492593c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionEventTriggerEventFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionEventTriggerEventFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionEventTriggerEventFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa80e55d07e99a932491b8dceb9b2e377da8142fd78a265cd27754645d485b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudfunctions2FunctionEventTriggerEventFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionEventTriggerEventFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51a052ab74b2e90ca1477ef65774ede0d113ae9e967d9c03fda1d4d81a057236)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05fb6abd53281af7d00858fb201e81da7a98ee38cfd23feb9664e72b9dd5f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f686082191a9380a0453a4481c13b587ae09a15ca127267dde58732d6f6681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909ff68de7e501b677ce4b146f565ef8505c0e992eee2cbf7cc66210b050ccfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionEventTriggerEventFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionEventTriggerEventFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionEventTriggerEventFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a960e24f9c9ee82eecffeb44c76860fcd8c094f68830dff801609016e676ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudfunctions2FunctionEventTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionEventTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60a71e78df6e9106bfa9c86499ca448129e5407b4371bcea009c275ff3cbbc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEventFilters")
    def put_event_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionEventTriggerEventFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7dc415caccc02183624ce11d7e32b2766a350b3a5719298efddc8a80fc23b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventFilters", [value]))

    @jsii.member(jsii_name="resetEventFilters")
    def reset_event_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventFilters", []))

    @jsii.member(jsii_name="resetEventType")
    def reset_event_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventType", []))

    @jsii.member(jsii_name="resetPubsubTopic")
    def reset_pubsub_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubTopic", []))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @jsii.member(jsii_name="resetTriggerRegion")
    def reset_trigger_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerRegion", []))

    @builtins.property
    @jsii.member(jsii_name="eventFilters")
    def event_filters(self) -> Cloudfunctions2FunctionEventTriggerEventFiltersList:
        return typing.cast(Cloudfunctions2FunctionEventTriggerEventFiltersList, jsii.get(self, "eventFilters"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="eventFiltersInput")
    def event_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionEventTriggerEventFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionEventTriggerEventFilters]]], jsii.get(self, "eventFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerRegionInput")
    def trigger_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992b29476494b7bd33a437d49992162a2edb5ae76e6922e93b7a7c760091913f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb77e63496ba41777326d523c94c9cec4e7947b51b57243d32a3eaeff1cc1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retryPolicy"))

    @retry_policy.setter
    def retry_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c5b591cc97575b042f962ad461a99592b18a02e23e792194b41b34311e17fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817f0d86933ae8576808cdc232681378ca556309b90001e1aafbb06c79fb28b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerRegion")
    def trigger_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerRegion"))

    @trigger_region.setter
    def trigger_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d32eef71797c87e9832b0b04c2da15e2d8365e626a70cdeaedf05d2894a910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Cloudfunctions2FunctionEventTrigger]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionEventTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionEventTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b96c24cca60c5aab94e8aca1dfda19d476d4716b656d1a05941f632a5720c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "all_traffic_on_latest_revision": "allTrafficOnLatestRevision",
        "available_cpu": "availableCpu",
        "available_memory": "availableMemory",
        "binary_authorization_policy": "binaryAuthorizationPolicy",
        "environment_variables": "environmentVariables",
        "ingress_settings": "ingressSettings",
        "max_instance_count": "maxInstanceCount",
        "max_instance_request_concurrency": "maxInstanceRequestConcurrency",
        "min_instance_count": "minInstanceCount",
        "secret_environment_variables": "secretEnvironmentVariables",
        "secret_volumes": "secretVolumes",
        "service": "service",
        "service_account_email": "serviceAccountEmail",
        "timeout_seconds": "timeoutSeconds",
        "vpc_connector": "vpcConnector",
        "vpc_connector_egress_settings": "vpcConnectorEgressSettings",
    },
)
class Cloudfunctions2FunctionServiceConfig:
    def __init__(
        self,
        *,
        all_traffic_on_latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        available_cpu: typing.Optional[builtins.str] = None,
        available_memory: typing.Optional[builtins.str] = None,
        binary_authorization_policy: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ingress_settings: typing.Optional[builtins.str] = None,
        max_instance_count: typing.Optional[jsii.Number] = None,
        max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        vpc_connector: typing.Optional[builtins.str] = None,
        vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_traffic_on_latest_revision: Whether 100% of traffic is routed to the latest revision. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#all_traffic_on_latest_revision Cloudfunctions2Function#all_traffic_on_latest_revision}
        :param available_cpu: The number of CPUs used in a single container instance. Default value is calculated from available memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#available_cpu Cloudfunctions2Function#available_cpu}
        :param available_memory: The amount of memory available for a function. Defaults to 256M. Supported units are k, M, G, Mi, Gi. If no unit is supplied the value is interpreted as bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#available_memory Cloudfunctions2Function#available_memory}
        :param binary_authorization_policy: The binary authorization policy to be checked when deploying the Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#binary_authorization_policy Cloudfunctions2Function#binary_authorization_policy}
        :param environment_variables: Environment variables that shall be available during function execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#environment_variables Cloudfunctions2Function#environment_variables}
        :param ingress_settings: Available ingress settings. Defaults to "ALLOW_ALL" if unspecified. Default value: "ALLOW_ALL" Possible values: ["ALLOW_ALL", "ALLOW_INTERNAL_ONLY", "ALLOW_INTERNAL_AND_GCLB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#ingress_settings Cloudfunctions2Function#ingress_settings}
        :param max_instance_count: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#max_instance_count Cloudfunctions2Function#max_instance_count}
        :param max_instance_request_concurrency: Sets the maximum number of concurrent requests that each instance can receive. Defaults to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#max_instance_request_concurrency Cloudfunctions2Function#max_instance_request_concurrency}
        :param min_instance_count: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#min_instance_count Cloudfunctions2Function#min_instance_count}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret_environment_variables Cloudfunctions2Function#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret_volumes Cloudfunctions2Function#secret_volumes}
        :param service: Name of the service associated with a Function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service Cloudfunctions2Function#service}
        :param service_account_email: The email of the service account for this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account_email Cloudfunctions2Function#service_account_email}
        :param timeout_seconds: The function execution timeout. Execution is considered failed and can be terminated if the function is not completed at the end of the timeout period. Defaults to 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#timeout_seconds Cloudfunctions2Function#timeout_seconds}
        :param vpc_connector: The Serverless VPC Access connector that this cloud function can connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#vpc_connector Cloudfunctions2Function#vpc_connector}
        :param vpc_connector_egress_settings: Available egress settings. Possible values: ["VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED", "PRIVATE_RANGES_ONLY", "ALL_TRAFFIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#vpc_connector_egress_settings Cloudfunctions2Function#vpc_connector_egress_settings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807a23d3bf0bc0ec04d3dabccfcdf2faf540ef9ddb229c817c2ff5ee90a1f773)
            check_type(argname="argument all_traffic_on_latest_revision", value=all_traffic_on_latest_revision, expected_type=type_hints["all_traffic_on_latest_revision"])
            check_type(argname="argument available_cpu", value=available_cpu, expected_type=type_hints["available_cpu"])
            check_type(argname="argument available_memory", value=available_memory, expected_type=type_hints["available_memory"])
            check_type(argname="argument binary_authorization_policy", value=binary_authorization_policy, expected_type=type_hints["binary_authorization_policy"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument ingress_settings", value=ingress_settings, expected_type=type_hints["ingress_settings"])
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument max_instance_request_concurrency", value=max_instance_request_concurrency, expected_type=type_hints["max_instance_request_concurrency"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument secret_environment_variables", value=secret_environment_variables, expected_type=type_hints["secret_environment_variables"])
            check_type(argname="argument secret_volumes", value=secret_volumes, expected_type=type_hints["secret_volumes"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
            check_type(argname="argument vpc_connector", value=vpc_connector, expected_type=type_hints["vpc_connector"])
            check_type(argname="argument vpc_connector_egress_settings", value=vpc_connector_egress_settings, expected_type=type_hints["vpc_connector_egress_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_traffic_on_latest_revision is not None:
            self._values["all_traffic_on_latest_revision"] = all_traffic_on_latest_revision
        if available_cpu is not None:
            self._values["available_cpu"] = available_cpu
        if available_memory is not None:
            self._values["available_memory"] = available_memory
        if binary_authorization_policy is not None:
            self._values["binary_authorization_policy"] = binary_authorization_policy
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if ingress_settings is not None:
            self._values["ingress_settings"] = ingress_settings
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if max_instance_request_concurrency is not None:
            self._values["max_instance_request_concurrency"] = max_instance_request_concurrency
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if secret_environment_variables is not None:
            self._values["secret_environment_variables"] = secret_environment_variables
        if secret_volumes is not None:
            self._values["secret_volumes"] = secret_volumes
        if service is not None:
            self._values["service"] = service
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds
        if vpc_connector is not None:
            self._values["vpc_connector"] = vpc_connector
        if vpc_connector_egress_settings is not None:
            self._values["vpc_connector_egress_settings"] = vpc_connector_egress_settings

    @builtins.property
    def all_traffic_on_latest_revision(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether 100% of traffic is routed to the latest revision. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#all_traffic_on_latest_revision Cloudfunctions2Function#all_traffic_on_latest_revision}
        '''
        result = self._values.get("all_traffic_on_latest_revision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def available_cpu(self) -> typing.Optional[builtins.str]:
        '''The number of CPUs used in a single container instance. Default value is calculated from available memory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#available_cpu Cloudfunctions2Function#available_cpu}
        '''
        result = self._values.get("available_cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def available_memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory available for a function.

        Defaults to 256M. Supported units are k, M, G, Mi, Gi. If no unit is
        supplied the value is interpreted as bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#available_memory Cloudfunctions2Function#available_memory}
        '''
        result = self._values.get("available_memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_authorization_policy(self) -> typing.Optional[builtins.str]:
        '''The binary authorization policy to be checked when deploying the Cloud Run service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#binary_authorization_policy Cloudfunctions2Function#binary_authorization_policy}
        '''
        result = self._values.get("binary_authorization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables that shall be available during function execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#environment_variables Cloudfunctions2Function#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def ingress_settings(self) -> typing.Optional[builtins.str]:
        '''Available ingress settings. Defaults to "ALLOW_ALL" if unspecified. Default value: "ALLOW_ALL" Possible values: ["ALLOW_ALL", "ALLOW_INTERNAL_ONLY", "ALLOW_INTERNAL_AND_GCLB"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#ingress_settings Cloudfunctions2Function#ingress_settings}
        '''
        result = self._values.get("ingress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The limit on the maximum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#max_instance_count Cloudfunctions2Function#max_instance_count}
        '''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_instance_request_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Sets the maximum number of concurrent requests that each instance can receive. Defaults to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#max_instance_request_concurrency Cloudfunctions2Function#max_instance_request_concurrency}
        '''
        result = self._values.get("max_instance_request_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The limit on the minimum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#min_instance_count Cloudfunctions2Function#min_instance_count}
        '''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]]:
        '''secret_environment_variables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret_environment_variables Cloudfunctions2Function#secret_environment_variables}
        '''
        result = self._values.get("secret_environment_variables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]], result)

    @builtins.property
    def secret_volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumes"]]]:
        '''secret_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret_volumes Cloudfunctions2Function#secret_volumes}
        '''
        result = self._values.get("secret_volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumes"]]], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Name of the service associated with a Function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service Cloudfunctions2Function#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The email of the service account for this function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#service_account_email Cloudfunctions2Function#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''The function execution timeout.

        Execution is considered failed and
        can be terminated if the function is not completed at the end of the
        timeout period. Defaults to 60 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#timeout_seconds Cloudfunctions2Function#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_connector(self) -> typing.Optional[builtins.str]:
        '''The Serverless VPC Access connector that this cloud function can connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#vpc_connector Cloudfunctions2Function#vpc_connector}
        '''
        result = self._values.get("vpc_connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_connector_egress_settings(self) -> typing.Optional[builtins.str]:
        '''Available egress settings. Possible values: ["VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED", "PRIVATE_RANGES_ONLY", "ALL_TRAFFIC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#vpc_connector_egress_settings Cloudfunctions2Function#vpc_connector_egress_settings}
        '''
        result = self._values.get("vpc_connector_egress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionServiceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8603dad00eaa0fc8cb2b6e3b6243a0a156e976b66d64e73f7e6fe30911f3c4a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretEnvironmentVariables")
    def put_secret_environment_variables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8f0a045e3df9e863f3abb053e69b761665688e100edc8f8862482bd05c2351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretEnvironmentVariables", [value]))

    @jsii.member(jsii_name="putSecretVolumes")
    def put_secret_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbce29608560061a08d2dae726eff64f7fc72e709e5103130192fefedfa2016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretVolumes", [value]))

    @jsii.member(jsii_name="resetAllTrafficOnLatestRevision")
    def reset_all_traffic_on_latest_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllTrafficOnLatestRevision", []))

    @jsii.member(jsii_name="resetAvailableCpu")
    def reset_available_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableCpu", []))

    @jsii.member(jsii_name="resetAvailableMemory")
    def reset_available_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableMemory", []))

    @jsii.member(jsii_name="resetBinaryAuthorizationPolicy")
    def reset_binary_authorization_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorizationPolicy", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetIngressSettings")
    def reset_ingress_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressSettings", []))

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMaxInstanceRequestConcurrency")
    def reset_max_instance_request_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceRequestConcurrency", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @jsii.member(jsii_name="resetSecretEnvironmentVariables")
    def reset_secret_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretEnvironmentVariables", []))

    @jsii.member(jsii_name="resetSecretVolumes")
    def reset_secret_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVolumes", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @jsii.member(jsii_name="resetVpcConnector")
    def reset_vpc_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConnector", []))

    @jsii.member(jsii_name="resetVpcConnectorEgressSettings")
    def reset_vpc_connector_egress_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConnectorEgressSettings", []))

    @builtins.property
    @jsii.member(jsii_name="gcfUri")
    def gcf_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcfUri"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvironmentVariables")
    def secret_environment_variables(
        self,
    ) -> "Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList":
        return typing.cast("Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList", jsii.get(self, "secretEnvironmentVariables"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumes")
    def secret_volumes(self) -> "Cloudfunctions2FunctionServiceConfigSecretVolumesList":
        return typing.cast("Cloudfunctions2FunctionServiceConfigSecretVolumesList", jsii.get(self, "secretVolumes"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="allTrafficOnLatestRevisionInput")
    def all_traffic_on_latest_revision_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allTrafficOnLatestRevisionInput"))

    @builtins.property
    @jsii.member(jsii_name="availableCpuInput")
    def available_cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availableCpuInput"))

    @builtins.property
    @jsii.member(jsii_name="availableMemoryInput")
    def available_memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availableMemoryInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationPolicyInput")
    def binary_authorization_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryAuthorizationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressSettingsInput")
    def ingress_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingressSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceRequestConcurrencyInput")
    def max_instance_request_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceRequestConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvironmentVariablesInput")
    def secret_environment_variables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]], jsii.get(self, "secretEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumesInput")
    def secret_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumes"]]], jsii.get(self, "secretVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorEgressSettingsInput")
    def vpc_connector_egress_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectorEgressSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorInput")
    def vpc_connector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="allTrafficOnLatestRevision")
    def all_traffic_on_latest_revision(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allTrafficOnLatestRevision"))

    @all_traffic_on_latest_revision.setter
    def all_traffic_on_latest_revision(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45ac857ee8e339e7265a39e624da189f4e49fe5dafc0b10cc9137f2b2a290c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allTrafficOnLatestRevision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableCpu")
    def available_cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availableCpu"))

    @available_cpu.setter
    def available_cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9066dc07a7bea5176d2baf9c499b0f51897fb237608932192b478ce744d4b0a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableCpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableMemory")
    def available_memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availableMemory"))

    @available_memory.setter
    def available_memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9c1a745f724e865096d079e424214d14c36d0b86dec9bc9efe3c58baf6399e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableMemory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationPolicy")
    def binary_authorization_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryAuthorizationPolicy"))

    @binary_authorization_policy.setter
    def binary_authorization_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde243c473b184714d8de47ac6fcaa906ee53cd561dedd5535817d982867cecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryAuthorizationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0052b66801444e5a919969f73ed4b3bfe3e862c87fd33b6a6891612f0c8973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressSettings")
    def ingress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressSettings"))

    @ingress_settings.setter
    def ingress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ba65fa3aed93f80bb0d093cb1c49e32e3c624ea722ec38a59322771b5d252e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fdf4835c53a31de2e3b37198d4943b4ffa8bd530a72d05111c7ec1500e0bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceRequestConcurrency")
    def max_instance_request_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceRequestConcurrency"))

    @max_instance_request_concurrency.setter
    def max_instance_request_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da43f0fdf18cbf0111f04dde3f8f0872502921788d60ed56ca72502a3a16f946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceRequestConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade2e50bcc4c119b2c7bf7de2ebff7269bff67d489fabb266146cfc91be28c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cc0e9f57b9b19324da9a95e6d09f250ec48afaf02982f61f7fcd14a9f02751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbc2b7cd3cb70c00b04ceb214cb5c797918f9855613e9ac2757319c1f6abfb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950e17596eeb4b42dff38e5d97040ddc933a579658eefcf8aea4d8d84a99c7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnector")
    def vpc_connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnector"))

    @vpc_connector.setter
    def vpc_connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676032ed2bd94753061dd41234575edf798ec518213a8ef9961de96c36d5909e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorEgressSettings")
    def vpc_connector_egress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorEgressSettings"))

    @vpc_connector_egress_settings.setter
    def vpc_connector_egress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abf894f6ca45ebd76646b6a6368b870d3c712f67dd832c6cf06fd14cd607ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectorEgressSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Cloudfunctions2FunctionServiceConfig]:
        return typing.cast(typing.Optional[Cloudfunctions2FunctionServiceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudfunctions2FunctionServiceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7088aca922ac3ade2e890b9bb67a72fad0d889095a10223722c1733cec54a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "project_id": "projectId",
        "secret": "secret",
        "version": "version",
    },
)
class Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables:
    def __init__(
        self,
        *,
        key: builtins.str,
        project_id: builtins.str,
        secret: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param key: Name of the environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#key Cloudfunctions2Function#key}
        :param project_id: Project identifier (preferably project number but can also be the project ID) of the project that contains the secret. If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project_id Cloudfunctions2Function#project_id}
        :param secret: Name of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret Cloudfunctions2Function#secret}
        :param version: Version of the secret (version number or the string 'latest'). It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new instances start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#version Cloudfunctions2Function#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3005b66de5b7f1d33370f0003ae480a60f3556cd00bcb11e6a732af6ae8b18cf)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "project_id": project_id,
            "secret": secret,
            "version": version,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Name of the environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#key Cloudfunctions2Function#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Project identifier (preferably project number but can also be the project ID) of the project that contains the secret.

        If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project_id Cloudfunctions2Function#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''Name of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret Cloudfunctions2Function#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string 'latest').

        It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new instances start.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#version Cloudfunctions2Function#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__235f4d36e493e93f43b03e592a9b06d7b48c7af279d8c69ab0ca1651a4932fe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62b470980230c991596dc0921fc3ecba622a4be2e9c1d8bf80129853a2af2ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f99d3b2cd3ef8a03730bf3c8286d27bf17c95103bf6a0fea57253f80516cd2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56d0dfbeb022a3f200eb380ae316be15b341090badb190cbed6d00035ae2395b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c409fb0ebaa0bb3d399dd0176c50d91a5b640920b24561288d8c68435e61272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720b9d992a293a01bcff625cd4f7ecfdc149b17f3bf96d30a6324c92318fffe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed00b3e18350d94d25dac55d4c767c3f42ca72cc02e4876827d05fca05d28fae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286866150f47c7263e8817279ccf78501855f35f8bf88a5351d4370f533d6cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0244acf62e3fea9b2a73691a5d46fa0d152f96e60d2544d7f5fd43f7d91018d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f21247d551519ce904b5d22a2287e226f903f73074a2d25b4e2c32541dcf0d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b976dab196d68b7288d3044ffa1be49a7f3cc95b90c429b31ebe7908571e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdbc1075b92dfe670c3dcc69f20c7c47f4a07d95850c2589cb93f7dcc5d7cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "mount_path": "mountPath",
        "project_id": "projectId",
        "secret": "secret",
        "versions": "versions",
    },
)
class Cloudfunctions2FunctionServiceConfigSecretVolumes:
    def __init__(
        self,
        *,
        mount_path: builtins.str,
        project_id: builtins.str,
        secret: builtins.str,
        versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mount_path: The path within the container to mount the secret volume. For example, setting the mountPath as /etc/secrets would mount the secret value files under the /etc/secrets directory. This directory will also be completely shadowed and unavailable to mount any other secrets. Recommended mount path: /etc/secrets Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#mount_path Cloudfunctions2Function#mount_path}
        :param project_id: Project identifier (preferably project number but can also be the project ID) of the project that contains the secret. If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project_id Cloudfunctions2Function#project_id}
        :param secret: Name of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret Cloudfunctions2Function#secret}
        :param versions: versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#versions Cloudfunctions2Function#versions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ee4fb75549b70cdb5a65c5fb14fe872e34c87860a73525af7a3d75f72a066d)
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument versions", value=versions, expected_type=type_hints["versions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mount_path": mount_path,
            "project_id": project_id,
            "secret": secret,
        }
        if versions is not None:
            self._values["versions"] = versions

    @builtins.property
    def mount_path(self) -> builtins.str:
        '''The path within the container to mount the secret volume.

        For example, setting the mountPath as /etc/secrets would mount the secret value files under the /etc/secrets directory. This directory will also be completely shadowed and unavailable to mount any other secrets. Recommended mount path: /etc/secrets

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#mount_path Cloudfunctions2Function#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Project identifier (preferably project number but can also be the project ID) of the project that contains the secret.

        If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#project_id Cloudfunctions2Function#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''Name of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#secret Cloudfunctions2Function#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def versions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]]:
        '''versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#versions Cloudfunctions2Function#versions}
        '''
        result = self._values.get("versions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionServiceConfigSecretVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionServiceConfigSecretVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e756681ff7fc39c0db15c1d515753333a08352a891294cb8e20cb66dc8fe310)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Cloudfunctions2FunctionServiceConfigSecretVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e28a001e99cd41c454430ad39fcd95f55b008887bacaa836141af23ad092e93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Cloudfunctions2FunctionServiceConfigSecretVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43117bb144c1f8ea8b5f3636abea8c6bf2efbd3c0863e0f8cb1d23c9fb79b18a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b385026048eeeb5b22145434b0adbe09446065ad8fd1637ccebedb2cdeda5029)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3b5c20fea46d926d18823d468f0cd572932671233e99a71e90a72d917edde28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec24b0b8fa88b2f986ac4e2d87f22038b7ecaa3cfdea46076b60c094646d4359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudfunctions2FunctionServiceConfigSecretVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__024c3a9f5f66095eec1f19cdf8b2b73741fdd637be29a1399a818d25975e7951)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVersions")
    def put_versions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Cloudfunctions2FunctionServiceConfigSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a548601f7414c8f0ec2b124d2c16d5b4bee1bf03598bacb122cd88a10918eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVersions", [value]))

    @jsii.member(jsii_name="resetVersions")
    def reset_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersions", []))

    @builtins.property
    @jsii.member(jsii_name="versions")
    def versions(
        self,
    ) -> "Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsList":
        return typing.cast("Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsList", jsii.get(self, "versions"))

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="versionsInput")
    def versions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Cloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]], jsii.get(self, "versionsInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac13b72757f78b1bef9eb439f5f9a0240ebbfbabd2aa92f3e0b2f856a80df71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0a2ff2b5e04eff5572ed9442379ff7ab384eb697819950c5aa89175c9dddc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa81d309290fb479affbb7d833b70040952199f59819d833c9a54a2c1a83530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214f9e799d17909a0caa472288cf1f9021178c19c3b31b89550c0c7370382fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretVolumesVersions",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "version": "version"},
)
class Cloudfunctions2FunctionServiceConfigSecretVolumesVersions:
    def __init__(self, *, path: builtins.str, version: builtins.str) -> None:
        '''
        :param path: Relative path of the file under the mount path where the secret value for this version will be fetched and made available. For example, setting the mountPath as '/etc/secrets' and path as secret_foo would mount the secret value file at /etc/secrets/secret_foo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#path Cloudfunctions2Function#path}
        :param version: Version of the secret (version number or the string 'latest'). It is preferable to use latest version with secret volumes as secret value changes are reflected immediately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#version Cloudfunctions2Function#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf446b0dfa1b4b5e84b81ab1fb45f88fdd1b32e938ca2825c2fe4f68cb78867)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "version": version,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Relative path of the file under the mount path where the secret value for this version will be fetched and made available.

        For example, setting the mountPath as '/etc/secrets' and path as secret_foo would mount the secret value file at /etc/secrets/secret_foo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#path Cloudfunctions2Function#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string 'latest').

        It is preferable to use latest version with secret volumes as secret value changes are reflected immediately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#version Cloudfunctions2Function#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionServiceConfigSecretVolumesVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__205c99943ded842b963391414ceae2bcfb12e02ee9f6dc2057b283daecc1a742)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c678ad1ecb8c8e044fa92b68c7bb2204c1df2dc24ed5e12e0c809242d6cc78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d8c854bd8002000e1a45fcc2d438ea5931067867e9a659b61a5f93ced15b25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3b05d43827f426bacbadb7ea87b928a8f7b8b0356cf72ce5cbf6adc8c5f31b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85aa6532a0f7e394ad137fbe7f18cf2198a6e33cf2508e82c2f332d0c9f7e931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b924b2867cb791c5b7e7b475a6ef6b7cc2511ef74f8acb9b13cf70edabbe61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcca59999774223b65e894e44f5593f716f2a42996daa141c777022d579cbd35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fc2504355cc36d4405d5373be575734a58d8416f4442dc71cf308f9e64411e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eaa377ed9bbbab1aa419c166d75e2cf41a24c4ad25b8f68447c293df437539a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98cb119925925c9f2e4153ba16796b0c3536fb86812b65f29d9ea0f64070dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class Cloudfunctions2FunctionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#create Cloudfunctions2Function#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#delete Cloudfunctions2Function#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#update Cloudfunctions2Function#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8877efaebe8c58393c111562c18ae0c8f48bf4e720c5f08620a017d8c1a40fa5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#create Cloudfunctions2Function#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#delete Cloudfunctions2Function#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions2_function#update Cloudfunctions2Function#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudfunctions2FunctionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudfunctions2FunctionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctions2Function.Cloudfunctions2FunctionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7228ff4b085328c7654f77cb4ba755efa8d0c730f6fe4e4a821e30e02db1df5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1b77903f6fc51fd765263331e326c05a64f8305e19076239879eb7be8a28b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea515a934791712cb45d9f7c5f63df73184bc5ad1cf714985e1be8aa77b4ea84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc7751e9272eaf01426ee03db9f722ebf759f2ef1c7b65d12810763d5138aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f661db0d82bf39400ca859ce349176dc63622d246df21fec05b27980ec9f1021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Cloudfunctions2Function",
    "Cloudfunctions2FunctionBuildConfig",
    "Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy",
    "Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference",
    "Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy",
    "Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference",
    "Cloudfunctions2FunctionBuildConfigOutputReference",
    "Cloudfunctions2FunctionBuildConfigSource",
    "Cloudfunctions2FunctionBuildConfigSourceOutputReference",
    "Cloudfunctions2FunctionBuildConfigSourceRepoSource",
    "Cloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference",
    "Cloudfunctions2FunctionBuildConfigSourceStorageSource",
    "Cloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference",
    "Cloudfunctions2FunctionConfig",
    "Cloudfunctions2FunctionEventTrigger",
    "Cloudfunctions2FunctionEventTriggerEventFilters",
    "Cloudfunctions2FunctionEventTriggerEventFiltersList",
    "Cloudfunctions2FunctionEventTriggerEventFiltersOutputReference",
    "Cloudfunctions2FunctionEventTriggerOutputReference",
    "Cloudfunctions2FunctionServiceConfig",
    "Cloudfunctions2FunctionServiceConfigOutputReference",
    "Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables",
    "Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList",
    "Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference",
    "Cloudfunctions2FunctionServiceConfigSecretVolumes",
    "Cloudfunctions2FunctionServiceConfigSecretVolumesList",
    "Cloudfunctions2FunctionServiceConfigSecretVolumesOutputReference",
    "Cloudfunctions2FunctionServiceConfigSecretVolumesVersions",
    "Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsList",
    "Cloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference",
    "Cloudfunctions2FunctionTimeouts",
    "Cloudfunctions2FunctionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f0a777d2c5993a68750b427cb9c1964136fd03b455d25300e773248687decad6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    build_config: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_trigger: typing.Optional[typing.Union[Cloudfunctions2FunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_config: typing.Optional[typing.Union[Cloudfunctions2FunctionServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[Cloudfunctions2FunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b2e7def9eb26d06376f569ab86d0e52a8f23a2b2f693e8a4ab148a67e3bd8ab9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713870acfc9b7fb30ad998b0f7fe9ab1bcf745fdb1946c35750f7dc0119c8e34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8802628b4d0287f8dd7a987c8022b0b52958524b31ccbf02d69dcc032bdf8452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec03652374e41a82e31a3501c9f05293b4b038de4126c346585a675afa23d7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767472f67ab5cbaf7db7c7f8dbcae02f5b426e904a0d13ba32a360bfa289981b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a181b391428b173a48bb69e7543e53d3b0a557a23941bc3ef5b70235ff2c250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b287877cb788ea7c873569bb8672b443601c0c28bc793d5572434e39804587(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc08b5f8962eaecf6a7db6164983cac3b623483931626d80578b4f559e456e98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7940f8ec199aa5c02f491ad4099d1f2c2463f9ade32984778ad84d5dea62b383(
    *,
    automatic_update_policy: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_repository: typing.Optional[builtins.str] = None,
    entry_point: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    on_deploy_update_policy: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfigSource, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197528e0a99b9521e1f1ac8e970c8f8ca5aebf7eb86be01a963b856f99784c75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95998965b4c9b8a9cc52d3dcab40fa80bcbd4df7ccc5d83cc8b975520081ee3b(
    value: typing.Optional[Cloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238d6db85291ccd211e14eadf2c44ce1c75f4794d3c0c18a9a3179192ebe8cf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212f824208852be85ceb636c38671cb8458f389878539210743e2ede7d05170e(
    value: typing.Optional[Cloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c055ffb2ce67c0fcac6fb22d6a9af1b680960956b42fb03d9f8118ca238ae73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5332428eba0ac891375b228a482c48a6acc9051509c63dd292c13ab39a1e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3649bd8f31625dc419b24ade40f6b0732104a3fec5fd057ca1314f58c9963d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e61700dffa0037ab5e125776c38175703607fcd1ebda55f71ae2d345814631(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ec82512490726edbc265b5c55f4978cda03a34b6a8262cf8789a054f29c48c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b1bf9ecfd6302b62e240ef80c80e54254457721bdc32884160cfebf9f79de7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43009103601218ad110c603a961248b5ab8600b25aef084908fd5bb8aff51fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee0bd14fec5dad8669b25d87a3b57673fe6ceb906b00deb033c0f6b97ff15be(
    value: typing.Optional[Cloudfunctions2FunctionBuildConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd2eaa666b4a8dfcd42cbee89adf2352e689fb33f783938842293be30a494ee(
    *,
    repo_source: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfigSourceRepoSource, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_source: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfigSourceStorageSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86c5179e83cb148a33f0d753d7b159e1256ece8cf0a7baa687264516f5b6c14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917f63c51170eb2d199243789f93537f46d62572211ac66ff7aa7d53d190d2c3(
    value: typing.Optional[Cloudfunctions2FunctionBuildConfigSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e63e09f6ab13d39ff1d6980a3a296b231a5ee13eb6b33c1e3765eb6ed72571(
    *,
    branch_name: typing.Optional[builtins.str] = None,
    commit_sha: typing.Optional[builtins.str] = None,
    dir: typing.Optional[builtins.str] = None,
    invert_regex: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_id: typing.Optional[builtins.str] = None,
    repo_name: typing.Optional[builtins.str] = None,
    tag_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68742dc8dabdb5b95f539618c56fa2f9593709dd18e6e0ad8d84162049ad449(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377814d7f612715b9777fa4675d5dfe2e0656c50fb6601624caf065e9ee8d26a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c6e3a9ed5cc0519a1a18dbcf21efb708e7c13c906b78a96d1e4e02f91f6aa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740b561db72fc2b2fad9b91746442ee2eadc3f6228fc7fc19d2b67dbec8757c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c7f9bf502d364d8f0bf0db7e3476386f5f87dea4d12d580d6044e725ccf158(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf2d566afbcb05bdcdc243571f24e1832509b50580fc6f17d21b0b96d713c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebaaade49f6bee6b30609cb5a47283a0c6e37fac44b2c130d1070705b13cf80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba4f0213d4b774844c779c11e0ef323394d40f0786897f1301ca3c7b06a7677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82341577dca62f7c68cba874c2da341c93f9f0d9a87cad0d8ee23b1f66f382a(
    value: typing.Optional[Cloudfunctions2FunctionBuildConfigSourceRepoSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1626ca35445566696f8b53661fdc82339a4bd5e2608fdb9b724687c4cb9c38(
    *,
    bucket: typing.Optional[builtins.str] = None,
    generation: typing.Optional[jsii.Number] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46cfec4d33b81b19ffbdc4ef045c2f430808e37b95a49757da5ddd057cab56d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c857a7fa5f4d12351dd978d1890c21ce27fd562738993cf66f4333576d5c941e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c008b3c92ede38b6423940b9ec32bbcccab6a8a95a0b67c356e5087ac3525e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb79e162e5e457b6412278b6da53713c28129eba25a2a90fd8b6032d0ac3046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df33685277bb5ff4a858e9ab45861791e1f82841340beeb42ed69f653de4ce36(
    value: typing.Optional[Cloudfunctions2FunctionBuildConfigSourceStorageSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e210f0d04f5e59c6d64faa63e9cf52d3e8fd2a215b24089a5f24200cf0e64e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    build_config: typing.Optional[typing.Union[Cloudfunctions2FunctionBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_trigger: typing.Optional[typing.Union[Cloudfunctions2FunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_config: typing.Optional[typing.Union[Cloudfunctions2FunctionServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[Cloudfunctions2FunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1162c899938b8426ca10cc3fee5e93d327c75161152cb1ad357f00f4fae877ae(
    *,
    event_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionEventTriggerEventFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_type: typing.Optional[builtins.str] = None,
    pubsub_topic: typing.Optional[builtins.str] = None,
    retry_policy: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    trigger_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3585d1936ea407b4c3ba523eebc75939cb951cbc3389973902f05a494dcb3d5(
    *,
    attribute: builtins.str,
    value: builtins.str,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df306a7040a9b390d9bb0edb45ea30e43aa307fedb216a87c5bf4acc199d41df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7decc67899845de74039ce3396c5dd55868ea4baf647df234a33034760333fdb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0263542882b6ed768bfca263588ae5f4d84cdbb55ba320eab4d01a26c9e85174(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d8605d6cebf0578947ced8b0bda312c61a79925796da0ef7f25d7e15fe2cdf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a85dfb249f23aa477d15cf96aae3829452a93452111cb59472036492593c93(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa80e55d07e99a932491b8dceb9b2e377da8142fd78a265cd27754645d485b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionEventTriggerEventFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a052ab74b2e90ca1477ef65774ede0d113ae9e967d9c03fda1d4d81a057236(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05fb6abd53281af7d00858fb201e81da7a98ee38cfd23feb9664e72b9dd5f93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f686082191a9380a0453a4481c13b587ae09a15ca127267dde58732d6f6681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909ff68de7e501b677ce4b146f565ef8505c0e992eee2cbf7cc66210b050ccfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a960e24f9c9ee82eecffeb44c76860fcd8c094f68830dff801609016e676ff0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionEventTriggerEventFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60a71e78df6e9106bfa9c86499ca448129e5407b4371bcea009c275ff3cbbc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7dc415caccc02183624ce11d7e32b2766a350b3a5719298efddc8a80fc23b1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionEventTriggerEventFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992b29476494b7bd33a437d49992162a2edb5ae76e6922e93b7a7c760091913f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb77e63496ba41777326d523c94c9cec4e7947b51b57243d32a3eaeff1cc1e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c5b591cc97575b042f962ad461a99592b18a02e23e792194b41b34311e17fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817f0d86933ae8576808cdc232681378ca556309b90001e1aafbb06c79fb28b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d32eef71797c87e9832b0b04c2da15e2d8365e626a70cdeaedf05d2894a910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b96c24cca60c5aab94e8aca1dfda19d476d4716b656d1a05941f632a5720c5a(
    value: typing.Optional[Cloudfunctions2FunctionEventTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807a23d3bf0bc0ec04d3dabccfcdf2faf540ef9ddb229c817c2ff5ee90a1f773(
    *,
    all_traffic_on_latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    available_cpu: typing.Optional[builtins.str] = None,
    available_memory: typing.Optional[builtins.str] = None,
    binary_authorization_policy: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ingress_settings: typing.Optional[builtins.str] = None,
    max_instance_count: typing.Optional[jsii.Number] = None,
    max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionServiceConfigSecretVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
    vpc_connector: typing.Optional[builtins.str] = None,
    vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8603dad00eaa0fc8cb2b6e3b6243a0a156e976b66d64e73f7e6fe30911f3c4a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8f0a045e3df9e863f3abb053e69b761665688e100edc8f8862482bd05c2351(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbce29608560061a08d2dae726eff64f7fc72e709e5103130192fefedfa2016(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionServiceConfigSecretVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45ac857ee8e339e7265a39e624da189f4e49fe5dafc0b10cc9137f2b2a290c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9066dc07a7bea5176d2baf9c499b0f51897fb237608932192b478ce744d4b0a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9c1a745f724e865096d079e424214d14c36d0b86dec9bc9efe3c58baf6399e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde243c473b184714d8de47ac6fcaa906ee53cd561dedd5535817d982867cecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0052b66801444e5a919969f73ed4b3bfe3e862c87fd33b6a6891612f0c8973(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ba65fa3aed93f80bb0d093cb1c49e32e3c624ea722ec38a59322771b5d252e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fdf4835c53a31de2e3b37198d4943b4ffa8bd530a72d05111c7ec1500e0bbb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da43f0fdf18cbf0111f04dde3f8f0872502921788d60ed56ca72502a3a16f946(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade2e50bcc4c119b2c7bf7de2ebff7269bff67d489fabb266146cfc91be28c24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cc0e9f57b9b19324da9a95e6d09f250ec48afaf02982f61f7fcd14a9f02751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbc2b7cd3cb70c00b04ceb214cb5c797918f9855613e9ac2757319c1f6abfb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950e17596eeb4b42dff38e5d97040ddc933a579658eefcf8aea4d8d84a99c7af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676032ed2bd94753061dd41234575edf798ec518213a8ef9961de96c36d5909e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abf894f6ca45ebd76646b6a6368b870d3c712f67dd832c6cf06fd14cd607ba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7088aca922ac3ade2e890b9bb67a72fad0d889095a10223722c1733cec54a84(
    value: typing.Optional[Cloudfunctions2FunctionServiceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3005b66de5b7f1d33370f0003ae480a60f3556cd00bcb11e6a732af6ae8b18cf(
    *,
    key: builtins.str,
    project_id: builtins.str,
    secret: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235f4d36e493e93f43b03e592a9b06d7b48c7af279d8c69ab0ca1651a4932fe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62b470980230c991596dc0921fc3ecba622a4be2e9c1d8bf80129853a2af2ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f99d3b2cd3ef8a03730bf3c8286d27bf17c95103bf6a0fea57253f80516cd2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d0dfbeb022a3f200eb380ae316be15b341090badb190cbed6d00035ae2395b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c409fb0ebaa0bb3d399dd0176c50d91a5b640920b24561288d8c68435e61272(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720b9d992a293a01bcff625cd4f7ecfdc149b17f3bf96d30a6324c92318fffe1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed00b3e18350d94d25dac55d4c767c3f42ca72cc02e4876827d05fca05d28fae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286866150f47c7263e8817279ccf78501855f35f8bf88a5351d4370f533d6cb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0244acf62e3fea9b2a73691a5d46fa0d152f96e60d2544d7f5fd43f7d91018d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f21247d551519ce904b5d22a2287e226f903f73074a2d25b4e2c32541dcf0d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b976dab196d68b7288d3044ffa1be49a7f3cc95b90c429b31ebe7908571e2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdbc1075b92dfe670c3dcc69f20c7c47f4a07d95850c2589cb93f7dcc5d7cbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ee4fb75549b70cdb5a65c5fb14fe872e34c87860a73525af7a3d75f72a066d(
    *,
    mount_path: builtins.str,
    project_id: builtins.str,
    secret: builtins.str,
    versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionServiceConfigSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e756681ff7fc39c0db15c1d515753333a08352a891294cb8e20cb66dc8fe310(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e28a001e99cd41c454430ad39fcd95f55b008887bacaa836141af23ad092e93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43117bb144c1f8ea8b5f3636abea8c6bf2efbd3c0863e0f8cb1d23c9fb79b18a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b385026048eeeb5b22145434b0adbe09446065ad8fd1637ccebedb2cdeda5029(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b5c20fea46d926d18823d468f0cd572932671233e99a71e90a72d917edde28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec24b0b8fa88b2f986ac4e2d87f22038b7ecaa3cfdea46076b60c094646d4359(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024c3a9f5f66095eec1f19cdf8b2b73741fdd637be29a1399a818d25975e7951(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a548601f7414c8f0ec2b124d2c16d5b4bee1bf03598bacb122cd88a10918eb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Cloudfunctions2FunctionServiceConfigSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac13b72757f78b1bef9eb439f5f9a0240ebbfbabd2aa92f3e0b2f856a80df71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0a2ff2b5e04eff5572ed9442379ff7ab384eb697819950c5aa89175c9dddc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa81d309290fb479affbb7d833b70040952199f59819d833c9a54a2c1a83530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214f9e799d17909a0caa472288cf1f9021178c19c3b31b89550c0c7370382fbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf446b0dfa1b4b5e84b81ab1fb45f88fdd1b32e938ca2825c2fe4f68cb78867(
    *,
    path: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205c99943ded842b963391414ceae2bcfb12e02ee9f6dc2057b283daecc1a742(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c678ad1ecb8c8e044fa92b68c7bb2204c1df2dc24ed5e12e0c809242d6cc78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d8c854bd8002000e1a45fcc2d438ea5931067867e9a659b61a5f93ced15b25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b05d43827f426bacbadb7ea87b928a8f7b8b0356cf72ce5cbf6adc8c5f31b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85aa6532a0f7e394ad137fbe7f18cf2198a6e33cf2508e82c2f332d0c9f7e931(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b924b2867cb791c5b7e7b475a6ef6b7cc2511ef74f8acb9b13cf70edabbe61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcca59999774223b65e894e44f5593f716f2a42996daa141c777022d579cbd35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fc2504355cc36d4405d5373be575734a58d8416f4442dc71cf308f9e64411e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eaa377ed9bbbab1aa419c166d75e2cf41a24c4ad25b8f68447c293df437539a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98cb119925925c9f2e4153ba16796b0c3536fb86812b65f29d9ea0f64070dfd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionServiceConfigSecretVolumesVersions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8877efaebe8c58393c111562c18ae0c8f48bf4e720c5f08620a017d8c1a40fa5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7228ff4b085328c7654f77cb4ba755efa8d0c730f6fe4e4a821e30e02db1df5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b77903f6fc51fd765263331e326c05a64f8305e19076239879eb7be8a28b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea515a934791712cb45d9f7c5f63df73184bc5ad1cf714985e1be8aa77b4ea84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc7751e9272eaf01426ee03db9f722ebf759f2ef1c7b65d12810763d5138aa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f661db0d82bf39400ca859ce349176dc63622d246df21fec05b27980ec9f1021(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudfunctions2FunctionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
