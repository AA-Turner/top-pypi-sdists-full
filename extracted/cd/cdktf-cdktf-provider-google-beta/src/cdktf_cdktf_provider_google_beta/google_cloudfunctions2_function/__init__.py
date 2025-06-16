r'''
# `google_cloudfunctions2_function`

Refer to the Terraform Registry for docs: [`google_cloudfunctions2_function`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function).
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


class GoogleCloudfunctions2Function(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2Function",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function google_cloudfunctions2_function}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        build_config: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_trigger: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_config: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function google_cloudfunctions2_function} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of this cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#location GoogleCloudfunctions2Function#location}
        :param name: A user-defined name of the function. Function names must be unique globally and match pattern 'projects/* /locations/* /functions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#name GoogleCloudfunctions2Function#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#build_config GoogleCloudfunctions2Function#build_config}
        :param description: User-provided description of a function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#description GoogleCloudfunctions2Function#description}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_trigger GoogleCloudfunctions2Function#event_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#id GoogleCloudfunctions2Function#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. It must match the pattern projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#kms_key_name GoogleCloudfunctions2Function#kms_key_name}
        :param labels: A set of key/value label pairs associated with this Cloud Function. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#labels GoogleCloudfunctions2Function#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project GoogleCloudfunctions2Function#project}.
        :param service_config: service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_config GoogleCloudfunctions2Function#service_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#timeouts GoogleCloudfunctions2Function#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bef043b215fc2370a92aa5f04d946c9339441ddb18e11e817e32bbb52ea87e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudfunctions2FunctionConfig(
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
        '''Generates CDKTF code for importing a GoogleCloudfunctions2Function resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudfunctions2Function to import.
        :param import_from_id: The id of the existing GoogleCloudfunctions2Function that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudfunctions2Function to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf828c5158b5dd228a569f0d658aaecb8185fd3169a99d209f16a09f0b9af293)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBuildConfig")
    def put_build_config(
        self,
        *,
        automatic_update_policy: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_repository: typing.Optional[builtins.str] = None,
        entry_point: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_deploy_update_policy: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigSource", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_update_policy: automatic_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#automatic_update_policy GoogleCloudfunctions2Function#automatic_update_policy}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#docker_repository GoogleCloudfunctions2Function#docker_repository}
        :param entry_point: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". For Node.js this is name of a function exported by the module specified in source_location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#entry_point GoogleCloudfunctions2Function#entry_point}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#environment_variables GoogleCloudfunctions2Function#environment_variables}
        :param on_deploy_update_policy: on_deploy_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#on_deploy_update_policy GoogleCloudfunctions2Function#on_deploy_update_policy}
        :param runtime: The runtime in which to run the function. Required when deploying a new function, optional when updating an existing function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#runtime GoogleCloudfunctions2Function#runtime}
        :param service_account: The fully-qualified name of the service account to be used for building the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account GoogleCloudfunctions2Function#service_account}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#source GoogleCloudfunctions2Function#source}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#worker_pool GoogleCloudfunctions2Function#worker_pool}
        '''
        value = GoogleCloudfunctions2FunctionBuildConfig(
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
        event_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionEventTriggerEventFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_type: typing.Optional[builtins.str] = None,
        pubsub_topic: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        trigger_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_filters: event_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_filters GoogleCloudfunctions2Function#event_filters}
        :param event_type: Required. The type of event to observe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_type GoogleCloudfunctions2Function#event_type}
        :param pubsub_topic: The name of a Pub/Sub topic in the same project that will be used as the transport topic for the event delivery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#pubsub_topic GoogleCloudfunctions2Function#pubsub_topic}
        :param retry_policy: Describes the retry policy in case of function's execution failure. Retried execution is charged as any other execution. Possible values: ["RETRY_POLICY_UNSPECIFIED", "RETRY_POLICY_DO_NOT_RETRY", "RETRY_POLICY_RETRY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#retry_policy GoogleCloudfunctions2Function#retry_policy}
        :param service_account_email: Optional. The email of the trigger's service account. The service account must have permission to invoke Cloud Run services. If empty, defaults to the Compute Engine default service account: {project_number}-compute@developer.gserviceaccount.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account_email GoogleCloudfunctions2Function#service_account_email}
        :param trigger_region: The region that the trigger will be in. The trigger will only receive events originating in this region. It can be the same region as the function, a different region or multi-region, or the global region. If not provided, defaults to the same region as the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#trigger_region GoogleCloudfunctions2Function#trigger_region}
        '''
        value = GoogleCloudfunctions2FunctionEventTrigger(
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
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        vpc_connector: typing.Optional[builtins.str] = None,
        vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_traffic_on_latest_revision: Whether 100% of traffic is routed to the latest revision. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#all_traffic_on_latest_revision GoogleCloudfunctions2Function#all_traffic_on_latest_revision}
        :param available_cpu: The number of CPUs used in a single container instance. Default value is calculated from available memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#available_cpu GoogleCloudfunctions2Function#available_cpu}
        :param available_memory: The amount of memory available for a function. Defaults to 256M. Supported units are k, M, G, Mi, Gi. If no unit is supplied the value is interpreted as bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#available_memory GoogleCloudfunctions2Function#available_memory}
        :param binary_authorization_policy: The binary authorization policy to be checked when deploying the Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#binary_authorization_policy GoogleCloudfunctions2Function#binary_authorization_policy}
        :param environment_variables: Environment variables that shall be available during function execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#environment_variables GoogleCloudfunctions2Function#environment_variables}
        :param ingress_settings: Available ingress settings. Defaults to "ALLOW_ALL" if unspecified. Default value: "ALLOW_ALL" Possible values: ["ALLOW_ALL", "ALLOW_INTERNAL_ONLY", "ALLOW_INTERNAL_AND_GCLB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#ingress_settings GoogleCloudfunctions2Function#ingress_settings}
        :param max_instance_count: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#max_instance_count GoogleCloudfunctions2Function#max_instance_count}
        :param max_instance_request_concurrency: Sets the maximum number of concurrent requests that each instance can receive. Defaults to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#max_instance_request_concurrency GoogleCloudfunctions2Function#max_instance_request_concurrency}
        :param min_instance_count: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#min_instance_count GoogleCloudfunctions2Function#min_instance_count}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret_environment_variables GoogleCloudfunctions2Function#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret_volumes GoogleCloudfunctions2Function#secret_volumes}
        :param service: Name of the service associated with a Function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service GoogleCloudfunctions2Function#service}
        :param service_account_email: The email of the service account for this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account_email GoogleCloudfunctions2Function#service_account_email}
        :param timeout_seconds: The function execution timeout. Execution is considered failed and can be terminated if the function is not completed at the end of the timeout period. Defaults to 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#timeout_seconds GoogleCloudfunctions2Function#timeout_seconds}
        :param vpc_connector: The Serverless VPC Access connector that this cloud function can connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#vpc_connector GoogleCloudfunctions2Function#vpc_connector}
        :param vpc_connector_egress_settings: Available egress settings. Possible values: ["VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED", "PRIVATE_RANGES_ONLY", "ALL_TRAFFIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#vpc_connector_egress_settings GoogleCloudfunctions2Function#vpc_connector_egress_settings}
        '''
        value = GoogleCloudfunctions2FunctionServiceConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#create GoogleCloudfunctions2Function#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#delete GoogleCloudfunctions2Function#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#update GoogleCloudfunctions2Function#update}.
        '''
        value = GoogleCloudfunctions2FunctionTimeouts(
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
    def build_config(self) -> "GoogleCloudfunctions2FunctionBuildConfigOutputReference":
        return typing.cast("GoogleCloudfunctions2FunctionBuildConfigOutputReference", jsii.get(self, "buildConfig"))

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
    def event_trigger(
        self,
    ) -> "GoogleCloudfunctions2FunctionEventTriggerOutputReference":
        return typing.cast("GoogleCloudfunctions2FunctionEventTriggerOutputReference", jsii.get(self, "eventTrigger"))

    @builtins.property
    @jsii.member(jsii_name="serviceConfig")
    def service_config(
        self,
    ) -> "GoogleCloudfunctions2FunctionServiceConfigOutputReference":
        return typing.cast("GoogleCloudfunctions2FunctionServiceConfigOutputReference", jsii.get(self, "serviceConfig"))

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
    def timeouts(self) -> "GoogleCloudfunctions2FunctionTimeoutsOutputReference":
        return typing.cast("GoogleCloudfunctions2FunctionTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfig"]:
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfig"], jsii.get(self, "buildConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTriggerInput")
    def event_trigger_input(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionEventTrigger"]:
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionEventTrigger"], jsii.get(self, "eventTriggerInput"))

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
    ) -> typing.Optional["GoogleCloudfunctions2FunctionServiceConfig"]:
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionServiceConfig"], jsii.get(self, "serviceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudfunctions2FunctionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudfunctions2FunctionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1745290447133afd9b3f7176c7a7bbef370b8371308556a05990054144a31ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514069ffdd6d362cdc781a52cc6ba2d26a8d1d66f463f2bfe5245726df8e6d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0738930fe6f227ab68829dd0797224a0e932017d6d2b8620eb9bbf0a199544dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb257383d76edc27593345cc06ab3405510d0fc1a172d38c905d75be1fb7f140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2f3b0bc9ee4a394bf88063c4f1a8da42aae88d8a21ba23ab19d18c7c912f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e58af0fbd0c0f839839998079fca7cbca2ac254b11dcdd3808537626133550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a20f17d3a558fa6d9db7f221c45a0e797911a9c13425558ba3a85955cd0cd1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfig",
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
class GoogleCloudfunctions2FunctionBuildConfig:
    def __init__(
        self,
        *,
        automatic_update_policy: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_repository: typing.Optional[builtins.str] = None,
        entry_point: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_deploy_update_policy: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigSource", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_update_policy: automatic_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#automatic_update_policy GoogleCloudfunctions2Function#automatic_update_policy}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#docker_repository GoogleCloudfunctions2Function#docker_repository}
        :param entry_point: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". For Node.js this is name of a function exported by the module specified in source_location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#entry_point GoogleCloudfunctions2Function#entry_point}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#environment_variables GoogleCloudfunctions2Function#environment_variables}
        :param on_deploy_update_policy: on_deploy_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#on_deploy_update_policy GoogleCloudfunctions2Function#on_deploy_update_policy}
        :param runtime: The runtime in which to run the function. Required when deploying a new function, optional when updating an existing function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#runtime GoogleCloudfunctions2Function#runtime}
        :param service_account: The fully-qualified name of the service account to be used for building the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account GoogleCloudfunctions2Function#service_account}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#source GoogleCloudfunctions2Function#source}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#worker_pool GoogleCloudfunctions2Function#worker_pool}
        '''
        if isinstance(automatic_update_policy, dict):
            automatic_update_policy = GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy(**automatic_update_policy)
        if isinstance(on_deploy_update_policy, dict):
            on_deploy_update_policy = GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy(**on_deploy_update_policy)
        if isinstance(source, dict):
            source = GoogleCloudfunctions2FunctionBuildConfigSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b13f81b593ed52fb41f1bc3f63af0996e4eedd2d5d4e5f895ac05b76904ef9d)
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
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy"]:
        '''automatic_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#automatic_update_policy GoogleCloudfunctions2Function#automatic_update_policy}
        '''
        result = self._values.get("automatic_update_policy")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy"], result)

    @builtins.property
    def docker_repository(self) -> typing.Optional[builtins.str]:
        '''User managed repository created in Artifact Registry optionally with a customer managed encryption key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#docker_repository GoogleCloudfunctions2Function#docker_repository}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#entry_point GoogleCloudfunctions2Function#entry_point}
        '''
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-provided build-time environment variables for the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#environment_variables GoogleCloudfunctions2Function#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_deploy_update_policy(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy"]:
        '''on_deploy_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#on_deploy_update_policy GoogleCloudfunctions2Function#on_deploy_update_policy}
        '''
        result = self._values.get("on_deploy_update_policy")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy"], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''The runtime in which to run the function. Required when deploying a new function, optional when updating an existing function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#runtime GoogleCloudfunctions2Function#runtime}
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified name of the service account to be used for building the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account GoogleCloudfunctions2Function#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#source GoogleCloudfunctions2Function#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSource"], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Build Custom Worker Pool that should be used to build the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#worker_pool GoogleCloudfunctions2Function#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionBuildConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc622e2fedda005cb91a243712597547f986284407bdb3ca02a5a69b9da6ccf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0587af76d3682caa6ea9ee9a2736b98f4c7c8ded9e9626b4f433145a970f2d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bcde48df26aec0191f10cff039d311c1de9904f0ddd7f51f11c73cb0a7cc3a3)
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
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be54efda18729cd4481c22b60dc554cd3520b103cf87dbc8e4fbddc22c26359a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctions2FunctionBuildConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da4a23780960cad7907f6806c57d99d85289a2b13deb5a649b1f3e5a143400d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutomaticUpdatePolicy")
    def put_automatic_update_policy(self) -> None:
        value = GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy()

        return typing.cast(None, jsii.invoke(self, "putAutomaticUpdatePolicy", [value]))

    @jsii.member(jsii_name="putOnDeployUpdatePolicy")
    def put_on_deploy_update_policy(self) -> None:
        value = GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy()

        return typing.cast(None, jsii.invoke(self, "putOnDeployUpdatePolicy", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        repo_source: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#repo_source GoogleCloudfunctions2Function#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#storage_source GoogleCloudfunctions2Function#storage_source}
        '''
        value = GoogleCloudfunctions2FunctionBuildConfigSource(
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
    ) -> GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference:
        return typing.cast(GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference, jsii.get(self, "automaticUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildAttribute"))

    @builtins.property
    @jsii.member(jsii_name="onDeployUpdatePolicy")
    def on_deploy_update_policy(
        self,
    ) -> GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference:
        return typing.cast(GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference, jsii.get(self, "onDeployUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "GoogleCloudfunctions2FunctionBuildConfigSourceOutputReference":
        return typing.cast("GoogleCloudfunctions2FunctionBuildConfigSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="automaticUpdatePolicyInput")
    def automatic_update_policy_input(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy], jsii.get(self, "automaticUpdatePolicyInput"))

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
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy], jsii.get(self, "onDeployUpdatePolicyInput"))

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
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSource"]:
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f293fd0d1b704ba7add1e3164b32b4f5bac1dc61aed25707da6d62481ea32e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryPoint")
    def entry_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryPoint"))

    @entry_point.setter
    def entry_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b9986748f52d922271768dac19fffbceba59e28435240e72e68ada5554b2f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73afab2a28afddcd84f200b0db49959374738c8d59514b8db253d712ef7fcc16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69eb1a187ebbcd37ac8c26cafe73f51f388d791658c5dd8dc73283490641e4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47174e4c83122dc4b23267b4b843fdcd7e1e04446d9e5b6d89d52de4250038b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8685f07a13fed06e9b00df902c070b6f93d168260d183fd431f09866fcf9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfig]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2145c9703fa056e718cacf5812febb55ad091431aae007aebf65e4c6132acb08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigSource",
    jsii_struct_bases=[],
    name_mapping={"repo_source": "repoSource", "storage_source": "storageSource"},
)
class GoogleCloudfunctions2FunctionBuildConfigSource:
    def __init__(
        self,
        *,
        repo_source: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_source: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repo_source: repo_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#repo_source GoogleCloudfunctions2Function#repo_source}
        :param storage_source: storage_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#storage_source GoogleCloudfunctions2Function#storage_source}
        '''
        if isinstance(repo_source, dict):
            repo_source = GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource(**repo_source)
        if isinstance(storage_source, dict):
            storage_source = GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource(**storage_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6458671a264c95aa4f54d5e851e5a46fc4985d7ab3b9ddeeb19c3974c121a8)
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
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource"]:
        '''repo_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#repo_source GoogleCloudfunctions2Function#repo_source}
        '''
        result = self._values.get("repo_source")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource"], result)

    @builtins.property
    def storage_source(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource"]:
        '''storage_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#storage_source GoogleCloudfunctions2Function#storage_source}
        '''
        result = self._values.get("storage_source")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionBuildConfigSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionBuildConfigSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0875eb7116f2f6566c385f47b583fd11cc547174b47aba22dcdead7eed0ff998)
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
        :param branch_name: Regex matching branches to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#branch_name GoogleCloudfunctions2Function#branch_name}
        :param commit_sha: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#commit_sha GoogleCloudfunctions2Function#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#dir GoogleCloudfunctions2Function#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#invert_regex GoogleCloudfunctions2Function#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project_id GoogleCloudfunctions2Function#project_id}
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#repo_name GoogleCloudfunctions2Function#repo_name}
        :param tag_name: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#tag_name GoogleCloudfunctions2Function#tag_name}
        '''
        value = GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource(
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
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#bucket GoogleCloudfunctions2Function#bucket}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#generation GoogleCloudfunctions2Function#generation}
        :param object: Google Cloud Storage object containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#object GoogleCloudfunctions2Function#object}
        '''
        value = GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource(
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
    ) -> "GoogleCloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference":
        return typing.cast("GoogleCloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference", jsii.get(self, "repoSource"))

    @builtins.property
    @jsii.member(jsii_name="storageSource")
    def storage_source(
        self,
    ) -> "GoogleCloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference":
        return typing.cast("GoogleCloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference", jsii.get(self, "storageSource"))

    @builtins.property
    @jsii.member(jsii_name="repoSourceInput")
    def repo_source_input(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource"]:
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource"], jsii.get(self, "repoSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSourceInput")
    def storage_source_input(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource"]:
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource"], jsii.get(self, "storageSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSource]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388f447608536f44148605d7b8e8eba76d73bfb30c1470f087266ebd5a46cfeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource",
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
class GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource:
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
        :param branch_name: Regex matching branches to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#branch_name GoogleCloudfunctions2Function#branch_name}
        :param commit_sha: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#commit_sha GoogleCloudfunctions2Function#commit_sha}
        :param dir: Directory, relative to the source root, in which to run the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#dir GoogleCloudfunctions2Function#dir}
        :param invert_regex: Only trigger a build if the revision regex does NOT match the revision regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#invert_regex GoogleCloudfunctions2Function#invert_regex}
        :param project_id: ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project_id GoogleCloudfunctions2Function#project_id}
        :param repo_name: Name of the Cloud Source Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#repo_name GoogleCloudfunctions2Function#repo_name}
        :param tag_name: Regex matching tags to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#tag_name GoogleCloudfunctions2Function#tag_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b6b17ae31b90959fd7afa3d4cda814e46787809caa7b9c2370fcca9ec840f6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#branch_name GoogleCloudfunctions2Function#branch_name}
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_sha(self) -> typing.Optional[builtins.str]:
        '''Regex matching tags to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#commit_sha GoogleCloudfunctions2Function#commit_sha}
        '''
        result = self._values.get("commit_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''Directory, relative to the source root, in which to run the build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#dir GoogleCloudfunctions2Function#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only trigger a build if the revision regex does NOT match the revision regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#invert_regex GoogleCloudfunctions2Function#invert_regex}
        '''
        result = self._values.get("invert_regex")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''ID of the project that owns the Cloud Source Repository. If omitted, the project ID requesting the build is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project_id GoogleCloudfunctions2Function#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Source Repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#repo_name GoogleCloudfunctions2Function#repo_name}
        '''
        result = self._values.get("repo_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_name(self) -> typing.Optional[builtins.str]:
        '''Regex matching tags to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#tag_name GoogleCloudfunctions2Function#tag_name}
        '''
        result = self._values.get("tag_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9d8da4e728d95e64d951d3fad6d0796879e8fca87b3e9b7e571d7ae946c0d28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a19c2d56fcc4945d2f95e259fbb014d117b29d7c5c1e880c163923b4d629c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @commit_sha.setter
    def commit_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292b73566712f4c5ae1fc76b0717c6090f7be689c8a870f82482046ccbd16cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd05127d3cc6109d40fdadc719358d66122ee5d069b01c221845d40d2dcd3040)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b756f8908dbd13afde0c441ff4adb8fd5a9325d70961097d9b920e4f42f7299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8247f6c34d3dc6d354493ab36da82553bc17485c91b1f7a59a8cdfda910a7d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoName"))

    @repo_name.setter
    def repo_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2986018e1bfe3919a54ccfe613aaf6bb1d4b8f819438e75555d0378fe830095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c53c3c4def598b027e9f6df92d31eff0cd283af8a53b6e905a011469078ca12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10eb756c6fb6bd923023528020f20fc91d1150b0f7c8f52860a5914851ea6fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "generation": "generation", "object": "object"},
)
class GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        generation: typing.Optional[jsii.Number] = None,
        object: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Google Cloud Storage bucket containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#bucket GoogleCloudfunctions2Function#bucket}
        :param generation: Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#generation GoogleCloudfunctions2Function#generation}
        :param object: Google Cloud Storage object containing the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#object GoogleCloudfunctions2Function#object}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c5371bab9a70743488c89a27026c933cd22b216d06e5a9bc9802348be0d1ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#bucket GoogleCloudfunctions2Function#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Google Cloud Storage generation for the object. If the generation is omitted, the latest generation will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#generation GoogleCloudfunctions2Function#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def object(self) -> typing.Optional[builtins.str]:
        '''Google Cloud Storage object containing the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#object GoogleCloudfunctions2Function#object}
        '''
        result = self._values.get("object")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ad480392ba61cd0918e3e12ae849d9edf2d85a45e98c56d4e8849bd1ee7438c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba57aa7d1efa3bc5149652c87a6eaa7edcc331c2898797225347cef1e4a254a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3f73065a0b97e7617aa966b4d1b960bb60e1341fffc7f0d85b230d6eb03988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56784e005cfb5f86ac6f67fb7f0dcea847cfc3c665ac9fcc81eee6b82673f5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74e85899987cc179d8b73e9eedab3ba5876b8a682a7a29fc7d06dd4069c48b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionConfig",
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
class GoogleCloudfunctions2FunctionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        build_config: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_trigger: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_config: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudfunctions2FunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of this cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#location GoogleCloudfunctions2Function#location}
        :param name: A user-defined name of the function. Function names must be unique globally and match pattern 'projects/* /locations/* /functions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#name GoogleCloudfunctions2Function#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#build_config GoogleCloudfunctions2Function#build_config}
        :param description: User-provided description of a function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#description GoogleCloudfunctions2Function#description}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_trigger GoogleCloudfunctions2Function#event_trigger}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#id GoogleCloudfunctions2Function#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. It must match the pattern projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#kms_key_name GoogleCloudfunctions2Function#kms_key_name}
        :param labels: A set of key/value label pairs associated with this Cloud Function. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#labels GoogleCloudfunctions2Function#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project GoogleCloudfunctions2Function#project}.
        :param service_config: service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_config GoogleCloudfunctions2Function#service_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#timeouts GoogleCloudfunctions2Function#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(build_config, dict):
            build_config = GoogleCloudfunctions2FunctionBuildConfig(**build_config)
        if isinstance(event_trigger, dict):
            event_trigger = GoogleCloudfunctions2FunctionEventTrigger(**event_trigger)
        if isinstance(service_config, dict):
            service_config = GoogleCloudfunctions2FunctionServiceConfig(**service_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudfunctions2FunctionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cbe9906ae7b508944e078ef7e073ce25fc08d8ef45ee6e87146bfb9e601fec9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#location GoogleCloudfunctions2Function#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A user-defined name of the function. Function names must be unique globally and match pattern 'projects/* /locations/* /functions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#name GoogleCloudfunctions2Function#name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_config(self) -> typing.Optional[GoogleCloudfunctions2FunctionBuildConfig]:
        '''build_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#build_config GoogleCloudfunctions2Function#build_config}
        '''
        result = self._values.get("build_config")
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionBuildConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description of a function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#description GoogleCloudfunctions2Function#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_trigger(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionEventTrigger"]:
        '''event_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_trigger GoogleCloudfunctions2Function#event_trigger}
        '''
        result = self._values.get("event_trigger")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionEventTrigger"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#id GoogleCloudfunctions2Function#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources.

        It must match the pattern projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#kms_key_name GoogleCloudfunctions2Function#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs associated with this Cloud Function.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#labels GoogleCloudfunctions2Function#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project GoogleCloudfunctions2Function#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_config(
        self,
    ) -> typing.Optional["GoogleCloudfunctions2FunctionServiceConfig"]:
        '''service_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_config GoogleCloudfunctions2Function#service_config}
        '''
        result = self._values.get("service_config")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionServiceConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudfunctions2FunctionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#timeouts GoogleCloudfunctions2Function#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudfunctions2FunctionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionEventTrigger",
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
class GoogleCloudfunctions2FunctionEventTrigger:
    def __init__(
        self,
        *,
        event_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionEventTriggerEventFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_type: typing.Optional[builtins.str] = None,
        pubsub_topic: typing.Optional[builtins.str] = None,
        retry_policy: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        trigger_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_filters: event_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_filters GoogleCloudfunctions2Function#event_filters}
        :param event_type: Required. The type of event to observe. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_type GoogleCloudfunctions2Function#event_type}
        :param pubsub_topic: The name of a Pub/Sub topic in the same project that will be used as the transport topic for the event delivery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#pubsub_topic GoogleCloudfunctions2Function#pubsub_topic}
        :param retry_policy: Describes the retry policy in case of function's execution failure. Retried execution is charged as any other execution. Possible values: ["RETRY_POLICY_UNSPECIFIED", "RETRY_POLICY_DO_NOT_RETRY", "RETRY_POLICY_RETRY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#retry_policy GoogleCloudfunctions2Function#retry_policy}
        :param service_account_email: Optional. The email of the trigger's service account. The service account must have permission to invoke Cloud Run services. If empty, defaults to the Compute Engine default service account: {project_number}-compute@developer.gserviceaccount.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account_email GoogleCloudfunctions2Function#service_account_email}
        :param trigger_region: The region that the trigger will be in. The trigger will only receive events originating in this region. It can be the same region as the function, a different region or multi-region, or the global region. If not provided, defaults to the same region as the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#trigger_region GoogleCloudfunctions2Function#trigger_region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb10f3cc423a73b49a18d8d62d1f5c30792d63a7f8ab380e504e591081ae1d90)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionEventTriggerEventFilters"]]]:
        '''event_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_filters GoogleCloudfunctions2Function#event_filters}
        '''
        result = self._values.get("event_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionEventTriggerEventFilters"]]], result)

    @builtins.property
    def event_type(self) -> typing.Optional[builtins.str]:
        '''Required. The type of event to observe.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#event_type GoogleCloudfunctions2Function#event_type}
        '''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_topic(self) -> typing.Optional[builtins.str]:
        '''The name of a Pub/Sub topic in the same project that will be used as the transport topic for the event delivery.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#pubsub_topic GoogleCloudfunctions2Function#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional[builtins.str]:
        '''Describes the retry policy in case of function's execution failure.

        Retried execution is charged as any other execution. Possible values: ["RETRY_POLICY_UNSPECIFIED", "RETRY_POLICY_DO_NOT_RETRY", "RETRY_POLICY_RETRY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#retry_policy GoogleCloudfunctions2Function#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The email of the trigger's service account. The service account
        must have permission to invoke Cloud Run services. If empty, defaults to the
        Compute Engine default service account: {project_number}-compute@developer.gserviceaccount.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account_email GoogleCloudfunctions2Function#service_account_email}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#trigger_region GoogleCloudfunctions2Function#trigger_region}
        '''
        result = self._values.get("trigger_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionEventTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionEventTriggerEventFilters",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute", "value": "value", "operator": "operator"},
)
class GoogleCloudfunctions2FunctionEventTriggerEventFilters:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        value: builtins.str,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute: 'Required. The name of a CloudEvents attribute. Currently, only a subset of attributes are supported for filtering. Use the 'gcloud eventarc providers describe' command to learn more about events and their attributes. Do not filter for the 'type' attribute here, as this is already achieved by the resource's 'event_type' attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#attribute GoogleCloudfunctions2Function#attribute}
        :param value: Required. The value for the attribute. If the operator field is set as 'match-path-pattern', this value can be a path pattern instead of an exact value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#value GoogleCloudfunctions2Function#value}
        :param operator: Optional. The operator used for matching the events with the value of the filter. If not specified, only events that have an exact key-value pair specified in the filter are matched. The only allowed value is 'match-path-pattern'. `See documentation on path patterns here <https://cloud.google.com/eventarc/docs/path-patterns>`_' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#operator GoogleCloudfunctions2Function#operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21936fa3a69c6e287bb9ea5c95f09b8cf3f04f04a8be1f3e6c2349e322cd4adb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#attribute GoogleCloudfunctions2Function#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Required.

        The value for the attribute.
        If the operator field is set as 'match-path-pattern', this value can be a path pattern instead of an exact value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#value GoogleCloudfunctions2Function#value}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#operator GoogleCloudfunctions2Function#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionEventTriggerEventFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionEventTriggerEventFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionEventTriggerEventFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d9afda72bbdb17930d1b69915f879b5dfdbd5339f4c8a48db0b595ac2cc7550)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudfunctions2FunctionEventTriggerEventFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8a60c7e87453d6bfd46cf177d4306701db6ed9f6a5ed8b3b458abdb822d67b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudfunctions2FunctionEventTriggerEventFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4321927656bac662fdebf76e435e55eeedaa38eff9918643e99d83ec96f957d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__547cdcb23349b4e50290cb996a43d571a6eac51629da65cb7f17f8f5f8441742)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab50537e715afa4b598eb6ac421a61ae30379d8af89904f451c1a5fbe46cb73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionEventTriggerEventFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionEventTriggerEventFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionEventTriggerEventFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8361a82f9147ccf061fdeb182f8bf3b7ed72b421470e1021fcadf212aa4f65f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctions2FunctionEventTriggerEventFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionEventTriggerEventFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2429debb51f519a0728cb0e571460bad84df8297edbfa110588208510fe9d209)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20d9e3b8463b1eecd09db74604043cedc4585ac0d664aeb222f5bf5bbf75e273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3490f01b1c3b311085df6f08a914ad927907f6ba81aaab51e884cd736a7a09d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a4879ade2564010e96c3760de2f253a4b6f326c24ec9a2b9c0e4d7e67827bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionEventTriggerEventFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionEventTriggerEventFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionEventTriggerEventFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95c23d6474321ebf691d2c3152ad236e5e620a051e9d2bf9aafd8ac20ede01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctions2FunctionEventTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionEventTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fc507b0040794b21f0e77c6484bf8b16b4d8bf1caaf152dc51d9b50ffddd14a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEventFilters")
    def put_event_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionEventTriggerEventFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250969cbde9aeff2ddcc78858f186eea1f52decb50b2173e7a5ae02033d83895)
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
    def event_filters(
        self,
    ) -> GoogleCloudfunctions2FunctionEventTriggerEventFiltersList:
        return typing.cast(GoogleCloudfunctions2FunctionEventTriggerEventFiltersList, jsii.get(self, "eventFilters"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="eventFiltersInput")
    def event_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionEventTriggerEventFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionEventTriggerEventFilters]]], jsii.get(self, "eventFiltersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e0deaf3b69faddcf0c068eec11cfd9cd0052e62bd405803d520945bb5660a198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74e6322a85de68906e4ba577cdb0febeb4fcfc0130ab6c8ab73cb37a4cf2477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retryPolicy"))

    @retry_policy.setter
    def retry_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09203f2498e5942d4ee7f82e8e9db4a303b2949c29f57b798d54aff86333d9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74fb57261c5fbec3c363534340a213858a44f6b9eec3da4665fe4e722e4bdcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerRegion")
    def trigger_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerRegion"))

    @trigger_region.setter
    def trigger_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7795f5246630b9f5a9d84a9c1fe54a37cac016265c95def13e39448ab700c793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionEventTrigger]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionEventTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionEventTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e310339c48d8c69add0a4a96c8a7605ebf88a32c3f075c040b828f7c84388f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfig",
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
class GoogleCloudfunctions2FunctionServiceConfig:
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
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        vpc_connector: typing.Optional[builtins.str] = None,
        vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param all_traffic_on_latest_revision: Whether 100% of traffic is routed to the latest revision. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#all_traffic_on_latest_revision GoogleCloudfunctions2Function#all_traffic_on_latest_revision}
        :param available_cpu: The number of CPUs used in a single container instance. Default value is calculated from available memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#available_cpu GoogleCloudfunctions2Function#available_cpu}
        :param available_memory: The amount of memory available for a function. Defaults to 256M. Supported units are k, M, G, Mi, Gi. If no unit is supplied the value is interpreted as bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#available_memory GoogleCloudfunctions2Function#available_memory}
        :param binary_authorization_policy: The binary authorization policy to be checked when deploying the Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#binary_authorization_policy GoogleCloudfunctions2Function#binary_authorization_policy}
        :param environment_variables: Environment variables that shall be available during function execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#environment_variables GoogleCloudfunctions2Function#environment_variables}
        :param ingress_settings: Available ingress settings. Defaults to "ALLOW_ALL" if unspecified. Default value: "ALLOW_ALL" Possible values: ["ALLOW_ALL", "ALLOW_INTERNAL_ONLY", "ALLOW_INTERNAL_AND_GCLB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#ingress_settings GoogleCloudfunctions2Function#ingress_settings}
        :param max_instance_count: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#max_instance_count GoogleCloudfunctions2Function#max_instance_count}
        :param max_instance_request_concurrency: Sets the maximum number of concurrent requests that each instance can receive. Defaults to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#max_instance_request_concurrency GoogleCloudfunctions2Function#max_instance_request_concurrency}
        :param min_instance_count: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#min_instance_count GoogleCloudfunctions2Function#min_instance_count}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret_environment_variables GoogleCloudfunctions2Function#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret_volumes GoogleCloudfunctions2Function#secret_volumes}
        :param service: Name of the service associated with a Function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service GoogleCloudfunctions2Function#service}
        :param service_account_email: The email of the service account for this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account_email GoogleCloudfunctions2Function#service_account_email}
        :param timeout_seconds: The function execution timeout. Execution is considered failed and can be terminated if the function is not completed at the end of the timeout period. Defaults to 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#timeout_seconds GoogleCloudfunctions2Function#timeout_seconds}
        :param vpc_connector: The Serverless VPC Access connector that this cloud function can connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#vpc_connector GoogleCloudfunctions2Function#vpc_connector}
        :param vpc_connector_egress_settings: Available egress settings. Possible values: ["VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED", "PRIVATE_RANGES_ONLY", "ALL_TRAFFIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#vpc_connector_egress_settings GoogleCloudfunctions2Function#vpc_connector_egress_settings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec31863bb443addbfa1108028d35cce7b2c6e9a4e33a844e5b243e778da7338)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#all_traffic_on_latest_revision GoogleCloudfunctions2Function#all_traffic_on_latest_revision}
        '''
        result = self._values.get("all_traffic_on_latest_revision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def available_cpu(self) -> typing.Optional[builtins.str]:
        '''The number of CPUs used in a single container instance. Default value is calculated from available memory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#available_cpu GoogleCloudfunctions2Function#available_cpu}
        '''
        result = self._values.get("available_cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def available_memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory available for a function.

        Defaults to 256M. Supported units are k, M, G, Mi, Gi. If no unit is
        supplied the value is interpreted as bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#available_memory GoogleCloudfunctions2Function#available_memory}
        '''
        result = self._values.get("available_memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_authorization_policy(self) -> typing.Optional[builtins.str]:
        '''The binary authorization policy to be checked when deploying the Cloud Run service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#binary_authorization_policy GoogleCloudfunctions2Function#binary_authorization_policy}
        '''
        result = self._values.get("binary_authorization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables that shall be available during function execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#environment_variables GoogleCloudfunctions2Function#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def ingress_settings(self) -> typing.Optional[builtins.str]:
        '''Available ingress settings. Defaults to "ALLOW_ALL" if unspecified. Default value: "ALLOW_ALL" Possible values: ["ALLOW_ALL", "ALLOW_INTERNAL_ONLY", "ALLOW_INTERNAL_AND_GCLB"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#ingress_settings GoogleCloudfunctions2Function#ingress_settings}
        '''
        result = self._values.get("ingress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The limit on the maximum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#max_instance_count GoogleCloudfunctions2Function#max_instance_count}
        '''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_instance_request_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Sets the maximum number of concurrent requests that each instance can receive. Defaults to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#max_instance_request_concurrency GoogleCloudfunctions2Function#max_instance_request_concurrency}
        '''
        result = self._values.get("max_instance_request_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The limit on the minimum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#min_instance_count GoogleCloudfunctions2Function#min_instance_count}
        '''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]]:
        '''secret_environment_variables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret_environment_variables GoogleCloudfunctions2Function#secret_environment_variables}
        '''
        result = self._values.get("secret_environment_variables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]], result)

    @builtins.property
    def secret_volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumes"]]]:
        '''secret_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret_volumes GoogleCloudfunctions2Function#secret_volumes}
        '''
        result = self._values.get("secret_volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumes"]]], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Name of the service associated with a Function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service GoogleCloudfunctions2Function#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The email of the service account for this function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#service_account_email GoogleCloudfunctions2Function#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''The function execution timeout.

        Execution is considered failed and
        can be terminated if the function is not completed at the end of the
        timeout period. Defaults to 60 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#timeout_seconds GoogleCloudfunctions2Function#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_connector(self) -> typing.Optional[builtins.str]:
        '''The Serverless VPC Access connector that this cloud function can connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#vpc_connector GoogleCloudfunctions2Function#vpc_connector}
        '''
        result = self._values.get("vpc_connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_connector_egress_settings(self) -> typing.Optional[builtins.str]:
        '''Available egress settings. Possible values: ["VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED", "PRIVATE_RANGES_ONLY", "ALL_TRAFFIC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#vpc_connector_egress_settings GoogleCloudfunctions2Function#vpc_connector_egress_settings}
        '''
        result = self._values.get("vpc_connector_egress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionServiceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29ee28d897310114f6d5707208070cd46bbf61554d0c09a205d5f840d67d0bcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretEnvironmentVariables")
    def put_secret_environment_variables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2441b2504d5ddb40501fe6e345ed5be6073218da94ea48c844bce8b8afbcf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretEnvironmentVariables", [value]))

    @jsii.member(jsii_name="putSecretVolumes")
    def put_secret_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3fb388247115d6239980598fa29cca330c7b89a79d8c69981983144b20b740)
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
    ) -> "GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList":
        return typing.cast("GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList", jsii.get(self, "secretEnvironmentVariables"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumes")
    def secret_volumes(
        self,
    ) -> "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesList":
        return typing.cast("GoogleCloudfunctions2FunctionServiceConfigSecretVolumesList", jsii.get(self, "secretVolumes"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables"]]], jsii.get(self, "secretEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumesInput")
    def secret_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumes"]]], jsii.get(self, "secretVolumesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2cde05793f05e47872e5acb9b0bf8006937f79cecc07762f3f37bd29a2456bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allTrafficOnLatestRevision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableCpu")
    def available_cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availableCpu"))

    @available_cpu.setter
    def available_cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92832fe51f578453f309cb0c936fb47d722992884de4b0aba6d5b7d87f19d739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableCpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableMemory")
    def available_memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availableMemory"))

    @available_memory.setter
    def available_memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19792c5b46474e88d352addf1e0fa26f977a139ddf2f2e1aac28410234a4c647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableMemory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationPolicy")
    def binary_authorization_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryAuthorizationPolicy"))

    @binary_authorization_policy.setter
    def binary_authorization_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bae862c37583c56077353e463f83cf1f6bfe8d3eb1e18894c394e1c825d075e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__728b4c988ff65fc5fd8a1e834eae51080974e1ed683eba85051995efb2b927a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressSettings")
    def ingress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressSettings"))

    @ingress_settings.setter
    def ingress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffa86fe817ca697ac93026052801acac8612c4ad6a2fd0151a491f5aab22343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47268d1119dc101af4ac6c6aebed3913aea84f853b5404a64f11093ea5bf1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceRequestConcurrency")
    def max_instance_request_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceRequestConcurrency"))

    @max_instance_request_concurrency.setter
    def max_instance_request_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3f4fcb4ae737306b8b9b847082280c8cb52e01213544e3c97bb8b415ba5de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceRequestConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb046a399bbc97fb5ce7ba839c55bf4d8fc2eed6d5a081b3d6df4759b8d5fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607ef50c9d14d51be5ce02c82713e2907a1f951c749dbeb805e98db2974af2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7006e394830fca45e9a29ec7bf9f922da02888416a1a5e99fc31ea5e97d847c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e3ae6b10730bd73794c3f3e204b5f58b54a8a31982875eed3de6ab3c374da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnector")
    def vpc_connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnector"))

    @vpc_connector.setter
    def vpc_connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3e8db12c61b842704afd32c6302159f4f4e2000c3b54d26ec112bc4cd92501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorEgressSettings")
    def vpc_connector_egress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorEgressSettings"))

    @vpc_connector_egress_settings.setter
    def vpc_connector_egress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfa6b5f10bdb355b1c6a3c768bbd2357e3ea3e94c0eeeaaba64d9275782e0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectorEgressSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctions2FunctionServiceConfig]:
        return typing.cast(typing.Optional[GoogleCloudfunctions2FunctionServiceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctions2FunctionServiceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7c720a94e42d29b01f76ce611fa58f97a76af5cf893fd295d765caaab14214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "project_id": "projectId",
        "secret": "secret",
        "version": "version",
    },
)
class GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables:
    def __init__(
        self,
        *,
        key: builtins.str,
        project_id: builtins.str,
        secret: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param key: Name of the environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#key GoogleCloudfunctions2Function#key}
        :param project_id: Project identifier (preferably project number but can also be the project ID) of the project that contains the secret. If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project_id GoogleCloudfunctions2Function#project_id}
        :param secret: Name of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret GoogleCloudfunctions2Function#secret}
        :param version: Version of the secret (version number or the string 'latest'). It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new instances start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#version GoogleCloudfunctions2Function#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f718c8f31e39ebf4bbdeda1f79c41b4d238e373094df02a8847ca92a04906ff9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#key GoogleCloudfunctions2Function#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Project identifier (preferably project number but can also be the project ID) of the project that contains the secret.

        If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project_id GoogleCloudfunctions2Function#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''Name of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret GoogleCloudfunctions2Function#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string 'latest').

        It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new instances start.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#version GoogleCloudfunctions2Function#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0142d6bb0fd0d82bbffaee21fb5149547368c5b601183674a8eb874c89a305ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e4444ead01ba2808101a5f64bb345608ec365a05eddfa0f754efcbc6d28601)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423f9e1a72fcaf8a8286fe06a88779b5b1774de6ec83b215c03a69c956193da7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f947468a4f10abf98174dda748510e64c5b4b02a3d92440b2b37b2dbad55df12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b87a9274e1a05f73768a527a44e1dca08f21f2f0dc9b53d93af2081327d465cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d41af66e02a92258406f30fab29ba89d895c3381dcbe3289e32e257dfe8c9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5edd128d90a6f5584abd42be6c0f9a4246891a7c7b4be14cc514eee33f88202a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a62df824629e54e686be54b17ba6738fdc1ed48363d4428dee715b19df77ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce8013e724c96a52d65f2076292b34724ba53db1345943e43973cd517a97397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918c64b296a9d958b5d1f3a84db6de64f4191fc42cac9fdd62fb4f4efb4adb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a668f69c9db8534c243171fe3488445eac58a3b38c057769722e22e1d97d38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccf8ebca2c8746e375a642167b5fe8ecbafa67ae4ba0376399c028b2df5baf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "mount_path": "mountPath",
        "project_id": "projectId",
        "secret": "secret",
        "versions": "versions",
    },
)
class GoogleCloudfunctions2FunctionServiceConfigSecretVolumes:
    def __init__(
        self,
        *,
        mount_path: builtins.str,
        project_id: builtins.str,
        secret: builtins.str,
        versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mount_path: The path within the container to mount the secret volume. For example, setting the mountPath as /etc/secrets would mount the secret value files under the /etc/secrets directory. This directory will also be completely shadowed and unavailable to mount any other secrets. Recommended mount path: /etc/secrets Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#mount_path GoogleCloudfunctions2Function#mount_path}
        :param project_id: Project identifier (preferably project number but can also be the project ID) of the project that contains the secret. If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project_id GoogleCloudfunctions2Function#project_id}
        :param secret: Name of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret GoogleCloudfunctions2Function#secret}
        :param versions: versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#versions GoogleCloudfunctions2Function#versions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2890221d1f61b04c83c8ad15c31df373f3ca72571e9eb9197e0a06041c607c9f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#mount_path GoogleCloudfunctions2Function#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Project identifier (preferably project number but can also be the project ID) of the project that contains the secret.

        If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#project_id GoogleCloudfunctions2Function#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''Name of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#secret GoogleCloudfunctions2Function#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def versions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]]:
        '''versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#versions GoogleCloudfunctions2Function#versions}
        '''
        result = self._values.get("versions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionServiceConfigSecretVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionServiceConfigSecretVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6084fe224900a4aa096a52dba08782293ada42a77a94ac4a7a9beac43acad20c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fc7a481167222a5e02ec67b2774761fcbcd8a3f440675535c6ddf2bd5e853b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudfunctions2FunctionServiceConfigSecretVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a914b7537b367eb15b37cf4027e7bc3916a9060990a727ad8d959cc2a7934d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4d21fc4e032c9b48bf4bf4690d7f50b9a32a4c6d0a49afdfb01aca4a0345963)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c09b19b22a9758dab956ceb6c40b878312ef75f90b9032d195b8a290a4721c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c31cdc9e8ac84e37ae70499d5a76a1d87bf92f2316587105b7273c007efe1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctions2FunctionServiceConfigSecretVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e54d6a159277e4b1f462f9e4e165200e406ee733b7e4b160b78c08581e44d36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVersions")
    def put_versions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f952b47d1bc61d976ddfa48ab725daf5bd170d44a002a823ccd4e15c41662ecd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVersions", [value]))

    @jsii.member(jsii_name="resetVersions")
    def reset_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersions", []))

    @builtins.property
    @jsii.member(jsii_name="versions")
    def versions(
        self,
    ) -> "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsList":
        return typing.cast("GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsList", jsii.get(self, "versions"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions"]]], jsii.get(self, "versionsInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24795cb759aac5559fe258a22184f966367c01f6f6998e8ece263e3a96d3e241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4941938b4ec10c272d77c454bdfabd941ba10151a4a3d739f05c4d018d554879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd74f16cabdb5597744f5ba3dc3fc522d7b15a3a4408a8715cdf157146f66cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df98e26211e205dfa51c41ea298eafaa3027a711fa51a0a08b181615b53abf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "version": "version"},
)
class GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions:
    def __init__(self, *, path: builtins.str, version: builtins.str) -> None:
        '''
        :param path: Relative path of the file under the mount path where the secret value for this version will be fetched and made available. For example, setting the mountPath as '/etc/secrets' and path as secret_foo would mount the secret value file at /etc/secrets/secret_foo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#path GoogleCloudfunctions2Function#path}
        :param version: Version of the secret (version number or the string 'latest'). It is preferable to use latest version with secret volumes as secret value changes are reflected immediately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#version GoogleCloudfunctions2Function#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5505f3fd55577ec62f4c2675265db8722c7691f72bc7e54163e31963e96c664e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#path GoogleCloudfunctions2Function#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string 'latest').

        It is preferable to use latest version with secret volumes as secret value changes are reflected immediately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#version GoogleCloudfunctions2Function#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29753a17ac329290f76b40f277d26e16faf407d4c458f358c1e7ef5ca2f11ae3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8c13444aeb344b0b6c9ea569eceac7ea8c6c1d6a9c8dab25ef021dfee1e2b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eacdf836ee3c75d6515172e9da8a29c233ee99446addb7e2c731a13df9303cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b84818fe668e7891be6c99c7e1cce386957f4bbc20df92ae09b35b154edad175)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a1651808c75101eaac1b05b469a005e9e7012b432ff0f33c92d5d789f5250fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00f5acc7c3643aa7c24f5f659b654d94fe3d757ecc4bc7b73a50b942d4324d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1960d8a38ab0e42b2e8ae94ae40d0ead884faa729eaf109e25727505320fd5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67de382c96bb25c7f9b28646356aa4027efcbb0a957916a7be99d687240a6420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98291a80480217a0572029a513894effdb85fecbad70bc9e02a82f76fd907256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee31b33186ce5b7dfe1890fa804079149c6c60cb8db413a81ee54157c55b4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudfunctions2FunctionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#create GoogleCloudfunctions2Function#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#delete GoogleCloudfunctions2Function#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#update GoogleCloudfunctions2Function#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33bc25bb91729331633861284ea8041de63c125c6b29686eb4d935b9fdf355ae)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#create GoogleCloudfunctions2Function#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#delete GoogleCloudfunctions2Function#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions2_function#update GoogleCloudfunctions2Function#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctions2FunctionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctions2FunctionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctions2Function.GoogleCloudfunctions2FunctionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4e90ffadc5112fe50c7e69cec33ff1da4113a30a9ecbc34b7b96a673a7a605f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5237c8a6592969bf05ae52452b8154f5688b32669a5a22d353ac5341c0b8082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2826a96f5f5d20803035a4cbcec660b08a9031592082e0ca78f3a28f388537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06eef55428097f1696fbd5e2d2e5f75530de38b1a847c1b53f5d2e2f212cedea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e04f816fe16a2593e112c6ef112f1a38a93acb0cc4fe50cfb85614cc5190cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudfunctions2Function",
    "GoogleCloudfunctions2FunctionBuildConfig",
    "GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy",
    "GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicyOutputReference",
    "GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy",
    "GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicyOutputReference",
    "GoogleCloudfunctions2FunctionBuildConfigOutputReference",
    "GoogleCloudfunctions2FunctionBuildConfigSource",
    "GoogleCloudfunctions2FunctionBuildConfigSourceOutputReference",
    "GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource",
    "GoogleCloudfunctions2FunctionBuildConfigSourceRepoSourceOutputReference",
    "GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource",
    "GoogleCloudfunctions2FunctionBuildConfigSourceStorageSourceOutputReference",
    "GoogleCloudfunctions2FunctionConfig",
    "GoogleCloudfunctions2FunctionEventTrigger",
    "GoogleCloudfunctions2FunctionEventTriggerEventFilters",
    "GoogleCloudfunctions2FunctionEventTriggerEventFiltersList",
    "GoogleCloudfunctions2FunctionEventTriggerEventFiltersOutputReference",
    "GoogleCloudfunctions2FunctionEventTriggerOutputReference",
    "GoogleCloudfunctions2FunctionServiceConfig",
    "GoogleCloudfunctions2FunctionServiceConfigOutputReference",
    "GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables",
    "GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesList",
    "GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariablesOutputReference",
    "GoogleCloudfunctions2FunctionServiceConfigSecretVolumes",
    "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesList",
    "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesOutputReference",
    "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions",
    "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsList",
    "GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersionsOutputReference",
    "GoogleCloudfunctions2FunctionTimeouts",
    "GoogleCloudfunctions2FunctionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__98bef043b215fc2370a92aa5f04d946c9339441ddb18e11e817e32bbb52ea87e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    build_config: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_trigger: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_config: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bf828c5158b5dd228a569f0d658aaecb8185fd3169a99d209f16a09f0b9af293(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1745290447133afd9b3f7176c7a7bbef370b8371308556a05990054144a31ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514069ffdd6d362cdc781a52cc6ba2d26a8d1d66f463f2bfe5245726df8e6d7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0738930fe6f227ab68829dd0797224a0e932017d6d2b8620eb9bbf0a199544dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb257383d76edc27593345cc06ab3405510d0fc1a172d38c905d75be1fb7f140(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2f3b0bc9ee4a394bf88063c4f1a8da42aae88d8a21ba23ab19d18c7c912f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e58af0fbd0c0f839839998079fca7cbca2ac254b11dcdd3808537626133550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a20f17d3a558fa6d9db7f221c45a0e797911a9c13425558ba3a85955cd0cd1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b13f81b593ed52fb41f1bc3f63af0996e4eedd2d5d4e5f895ac05b76904ef9d(
    *,
    automatic_update_policy: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_repository: typing.Optional[builtins.str] = None,
    entry_point: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    on_deploy_update_policy: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfigSource, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc622e2fedda005cb91a243712597547f986284407bdb3ca02a5a69b9da6ccf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0587af76d3682caa6ea9ee9a2736b98f4c7c8ded9e9626b4f433145a970f2d3(
    value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigAutomaticUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcde48df26aec0191f10cff039d311c1de9904f0ddd7f51f11c73cb0a7cc3a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be54efda18729cd4481c22b60dc554cd3520b103cf87dbc8e4fbddc22c26359a(
    value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigOnDeployUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4a23780960cad7907f6806c57d99d85289a2b13deb5a649b1f3e5a143400d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f293fd0d1b704ba7add1e3164b32b4f5bac1dc61aed25707da6d62481ea32e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b9986748f52d922271768dac19fffbceba59e28435240e72e68ada5554b2f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73afab2a28afddcd84f200b0db49959374738c8d59514b8db253d712ef7fcc16(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69eb1a187ebbcd37ac8c26cafe73f51f388d791658c5dd8dc73283490641e4e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47174e4c83122dc4b23267b4b843fdcd7e1e04446d9e5b6d89d52de4250038b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8685f07a13fed06e9b00df902c070b6f93d168260d183fd431f09866fcf9e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2145c9703fa056e718cacf5812febb55ad091431aae007aebf65e4c6132acb08(
    value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6458671a264c95aa4f54d5e851e5a46fc4985d7ab3b9ddeeb19c3974c121a8(
    *,
    repo_source: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_source: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0875eb7116f2f6566c385f47b583fd11cc547174b47aba22dcdead7eed0ff998(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388f447608536f44148605d7b8e8eba76d73bfb30c1470f087266ebd5a46cfeb(
    value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b6b17ae31b90959fd7afa3d4cda814e46787809caa7b9c2370fcca9ec840f6(
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

def _typecheckingstub__c9d8da4e728d95e64d951d3fad6d0796879e8fca87b3e9b7e571d7ae946c0d28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a19c2d56fcc4945d2f95e259fbb014d117b29d7c5c1e880c163923b4d629c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292b73566712f4c5ae1fc76b0717c6090f7be689c8a870f82482046ccbd16cad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd05127d3cc6109d40fdadc719358d66122ee5d069b01c221845d40d2dcd3040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b756f8908dbd13afde0c441ff4adb8fd5a9325d70961097d9b920e4f42f7299(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8247f6c34d3dc6d354493ab36da82553bc17485c91b1f7a59a8cdfda910a7d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2986018e1bfe3919a54ccfe613aaf6bb1d4b8f819438e75555d0378fe830095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c53c3c4def598b027e9f6df92d31eff0cd283af8a53b6e905a011469078ca12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10eb756c6fb6bd923023528020f20fc91d1150b0f7c8f52860a5914851ea6fb3(
    value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceRepoSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c5371bab9a70743488c89a27026c933cd22b216d06e5a9bc9802348be0d1ed(
    *,
    bucket: typing.Optional[builtins.str] = None,
    generation: typing.Optional[jsii.Number] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad480392ba61cd0918e3e12ae849d9edf2d85a45e98c56d4e8849bd1ee7438c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba57aa7d1efa3bc5149652c87a6eaa7edcc331c2898797225347cef1e4a254a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3f73065a0b97e7617aa966b4d1b960bb60e1341fffc7f0d85b230d6eb03988(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56784e005cfb5f86ac6f67fb7f0dcea847cfc3c665ac9fcc81eee6b82673f5b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74e85899987cc179d8b73e9eedab3ba5876b8a682a7a29fc7d06dd4069c48b6(
    value: typing.Optional[GoogleCloudfunctions2FunctionBuildConfigSourceStorageSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cbe9906ae7b508944e078ef7e073ce25fc08d8ef45ee6e87146bfb9e601fec9(
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
    build_config: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_trigger: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_config: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudfunctions2FunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb10f3cc423a73b49a18d8d62d1f5c30792d63a7f8ab380e504e591081ae1d90(
    *,
    event_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionEventTriggerEventFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_type: typing.Optional[builtins.str] = None,
    pubsub_topic: typing.Optional[builtins.str] = None,
    retry_policy: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    trigger_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21936fa3a69c6e287bb9ea5c95f09b8cf3f04f04a8be1f3e6c2349e322cd4adb(
    *,
    attribute: builtins.str,
    value: builtins.str,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9afda72bbdb17930d1b69915f879b5dfdbd5339f4c8a48db0b595ac2cc7550(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8a60c7e87453d6bfd46cf177d4306701db6ed9f6a5ed8b3b458abdb822d67b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4321927656bac662fdebf76e435e55eeedaa38eff9918643e99d83ec96f957d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547cdcb23349b4e50290cb996a43d571a6eac51629da65cb7f17f8f5f8441742(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab50537e715afa4b598eb6ac421a61ae30379d8af89904f451c1a5fbe46cb73(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8361a82f9147ccf061fdeb182f8bf3b7ed72b421470e1021fcadf212aa4f65f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionEventTriggerEventFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2429debb51f519a0728cb0e571460bad84df8297edbfa110588208510fe9d209(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d9e3b8463b1eecd09db74604043cedc4585ac0d664aeb222f5bf5bbf75e273(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3490f01b1c3b311085df6f08a914ad927907f6ba81aaab51e884cd736a7a09d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a4879ade2564010e96c3760de2f253a4b6f326c24ec9a2b9c0e4d7e67827bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95c23d6474321ebf691d2c3152ad236e5e620a051e9d2bf9aafd8ac20ede01f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionEventTriggerEventFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc507b0040794b21f0e77c6484bf8b16b4d8bf1caaf152dc51d9b50ffddd14a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250969cbde9aeff2ddcc78858f186eea1f52decb50b2173e7a5ae02033d83895(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionEventTriggerEventFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0deaf3b69faddcf0c068eec11cfd9cd0052e62bd405803d520945bb5660a198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74e6322a85de68906e4ba577cdb0febeb4fcfc0130ab6c8ab73cb37a4cf2477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09203f2498e5942d4ee7f82e8e9db4a303b2949c29f57b798d54aff86333d9dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74fb57261c5fbec3c363534340a213858a44f6b9eec3da4665fe4e722e4bdcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7795f5246630b9f5a9d84a9c1fe54a37cac016265c95def13e39448ab700c793(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e310339c48d8c69add0a4a96c8a7605ebf88a32c3f075c040b828f7c84388f(
    value: typing.Optional[GoogleCloudfunctions2FunctionEventTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec31863bb443addbfa1108028d35cce7b2c6e9a4e33a844e5b243e778da7338(
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
    secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionServiceConfigSecretVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
    vpc_connector: typing.Optional[builtins.str] = None,
    vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ee28d897310114f6d5707208070cd46bbf61554d0c09a205d5f840d67d0bcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2441b2504d5ddb40501fe6e345ed5be6073218da94ea48c844bce8b8afbcf9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3fb388247115d6239980598fa29cca330c7b89a79d8c69981983144b20b740(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionServiceConfigSecretVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cde05793f05e47872e5acb9b0bf8006937f79cecc07762f3f37bd29a2456bfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92832fe51f578453f309cb0c936fb47d722992884de4b0aba6d5b7d87f19d739(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19792c5b46474e88d352addf1e0fa26f977a139ddf2f2e1aac28410234a4c647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bae862c37583c56077353e463f83cf1f6bfe8d3eb1e18894c394e1c825d075e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728b4c988ff65fc5fd8a1e834eae51080974e1ed683eba85051995efb2b927a3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffa86fe817ca697ac93026052801acac8612c4ad6a2fd0151a491f5aab22343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47268d1119dc101af4ac6c6aebed3913aea84f853b5404a64f11093ea5bf1e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3f4fcb4ae737306b8b9b847082280c8cb52e01213544e3c97bb8b415ba5de2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb046a399bbc97fb5ce7ba839c55bf4d8fc2eed6d5a081b3d6df4759b8d5fb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607ef50c9d14d51be5ce02c82713e2907a1f951c749dbeb805e98db2974af2b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7006e394830fca45e9a29ec7bf9f922da02888416a1a5e99fc31ea5e97d847c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e3ae6b10730bd73794c3f3e204b5f58b54a8a31982875eed3de6ab3c374da1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3e8db12c61b842704afd32c6302159f4f4e2000c3b54d26ec112bc4cd92501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfa6b5f10bdb355b1c6a3c768bbd2357e3ea3e94c0eeeaaba64d9275782e0ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7c720a94e42d29b01f76ce611fa58f97a76af5cf893fd295d765caaab14214(
    value: typing.Optional[GoogleCloudfunctions2FunctionServiceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f718c8f31e39ebf4bbdeda1f79c41b4d238e373094df02a8847ca92a04906ff9(
    *,
    key: builtins.str,
    project_id: builtins.str,
    secret: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0142d6bb0fd0d82bbffaee21fb5149547368c5b601183674a8eb874c89a305ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e4444ead01ba2808101a5f64bb345608ec365a05eddfa0f754efcbc6d28601(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423f9e1a72fcaf8a8286fe06a88779b5b1774de6ec83b215c03a69c956193da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f947468a4f10abf98174dda748510e64c5b4b02a3d92440b2b37b2dbad55df12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87a9274e1a05f73768a527a44e1dca08f21f2f0dc9b53d93af2081327d465cf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d41af66e02a92258406f30fab29ba89d895c3381dcbe3289e32e257dfe8c9d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edd128d90a6f5584abd42be6c0f9a4246891a7c7b4be14cc514eee33f88202a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a62df824629e54e686be54b17ba6738fdc1ed48363d4428dee715b19df77ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce8013e724c96a52d65f2076292b34724ba53db1345943e43973cd517a97397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918c64b296a9d958b5d1f3a84db6de64f4191fc42cac9fdd62fb4f4efb4adb52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a668f69c9db8534c243171fe3488445eac58a3b38c057769722e22e1d97d38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccf8ebca2c8746e375a642167b5fe8ecbafa67ae4ba0376399c028b2df5baf8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretEnvironmentVariables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2890221d1f61b04c83c8ad15c31df373f3ca72571e9eb9197e0a06041c607c9f(
    *,
    mount_path: builtins.str,
    project_id: builtins.str,
    secret: builtins.str,
    versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6084fe224900a4aa096a52dba08782293ada42a77a94ac4a7a9beac43acad20c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fc7a481167222a5e02ec67b2774761fcbcd8a3f440675535c6ddf2bd5e853b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a914b7537b367eb15b37cf4027e7bc3916a9060990a727ad8d959cc2a7934d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d21fc4e032c9b48bf4bf4690d7f50b9a32a4c6d0a49afdfb01aca4a0345963(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09b19b22a9758dab956ceb6c40b878312ef75f90b9032d195b8a290a4721c5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c31cdc9e8ac84e37ae70499d5a76a1d87bf92f2316587105b7273c007efe1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e54d6a159277e4b1f462f9e4e165200e406ee733b7e4b160b78c08581e44d36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f952b47d1bc61d976ddfa48ab725daf5bd170d44a002a823ccd4e15c41662ecd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24795cb759aac5559fe258a22184f966367c01f6f6998e8ece263e3a96d3e241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4941938b4ec10c272d77c454bdfabd941ba10151a4a3d739f05c4d018d554879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd74f16cabdb5597744f5ba3dc3fc522d7b15a3a4408a8715cdf157146f66cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df98e26211e205dfa51c41ea298eafaa3027a711fa51a0a08b181615b53abf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5505f3fd55577ec62f4c2675265db8722c7691f72bc7e54163e31963e96c664e(
    *,
    path: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29753a17ac329290f76b40f277d26e16faf407d4c458f358c1e7ef5ca2f11ae3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8c13444aeb344b0b6c9ea569eceac7ea8c6c1d6a9c8dab25ef021dfee1e2b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eacdf836ee3c75d6515172e9da8a29c233ee99446addb7e2c731a13df9303cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84818fe668e7891be6c99c7e1cce386957f4bbc20df92ae09b35b154edad175(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1651808c75101eaac1b05b469a005e9e7012b432ff0f33c92d5d789f5250fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00f5acc7c3643aa7c24f5f659b654d94fe3d757ecc4bc7b73a50b942d4324d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1960d8a38ab0e42b2e8ae94ae40d0ead884faa729eaf109e25727505320fd5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67de382c96bb25c7f9b28646356aa4027efcbb0a957916a7be99d687240a6420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98291a80480217a0572029a513894effdb85fecbad70bc9e02a82f76fd907256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee31b33186ce5b7dfe1890fa804079149c6c60cb8db413a81ee54157c55b4eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionServiceConfigSecretVolumesVersions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bc25bb91729331633861284ea8041de63c125c6b29686eb4d935b9fdf355ae(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e90ffadc5112fe50c7e69cec33ff1da4113a30a9ecbc34b7b96a673a7a605f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5237c8a6592969bf05ae52452b8154f5688b32669a5a22d353ac5341c0b8082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2826a96f5f5d20803035a4cbcec660b08a9031592082e0ca78f3a28f388537(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06eef55428097f1696fbd5e2d2e5f75530de38b1a847c1b53f5d2e2f212cedea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e04f816fe16a2593e112c6ef112f1a38a93acb0cc4fe50cfb85614cc5190cbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctions2FunctionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
