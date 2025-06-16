r'''
# `google_cloudfunctions_function`

Refer to the Terraform Registry for docs: [`google_cloudfunctions_function`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function).
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


class GoogleCloudfunctionsFunction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function google_cloudfunctions_function}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        runtime: builtins.str,
        available_memory_mb: typing.Optional[jsii.Number] = None,
        build_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        build_service_account: typing.Optional[builtins.str] = None,
        build_worker_pool: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        docker_registry: typing.Optional[builtins.str] = None,
        docker_repository: typing.Optional[builtins.str] = None,
        entry_point: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        event_trigger: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        https_trigger_security_level: typing.Optional[builtins.str] = None,
        https_trigger_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ingress_settings: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        source_archive_bucket: typing.Optional[builtins.str] = None,
        source_archive_object: typing.Optional[builtins.str] = None,
        source_repository: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionSourceRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_http: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc_connector: typing.Optional[builtins.str] = None,
        vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function google_cloudfunctions_function} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A user-defined name of the function. Function names must be unique globally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#name GoogleCloudfunctionsFunction#name}
        :param runtime: The runtime in which the function is going to run. Eg. "nodejs20", "python37", "go111". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#runtime GoogleCloudfunctionsFunction#runtime}
        :param available_memory_mb: Memory (in MB), available to the function. Default value is 256. Possible values include 128, 256, 512, 1024, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#available_memory_mb GoogleCloudfunctionsFunction#available_memory_mb}
        :param build_environment_variables: A set of key/value environment variable pairs available during build time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_environment_variables GoogleCloudfunctionsFunction#build_environment_variables}
        :param build_service_account: The fully-qualified name of the service account to be used for the build step of deploying this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_service_account GoogleCloudfunctionsFunction#build_service_account}
        :param build_worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_worker_pool GoogleCloudfunctionsFunction#build_worker_pool}
        :param description: Description of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#description GoogleCloudfunctionsFunction#description}
        :param docker_registry: Docker Registry to use for storing the function's Docker images. Allowed values are ARTIFACT_REGISTRY (default) and CONTAINER_REGISTRY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#docker_registry GoogleCloudfunctionsFunction#docker_registry}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. If specified, deployments will use Artifact Registry for storing images built with Cloud Build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#docker_repository GoogleCloudfunctionsFunction#docker_repository}
        :param entry_point: Name of the function that will be executed when the Google Cloud Function is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#entry_point GoogleCloudfunctionsFunction#entry_point}
        :param environment_variables: A set of key/value environment variable pairs to assign to the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#environment_variables GoogleCloudfunctionsFunction#environment_variables}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#event_trigger GoogleCloudfunctionsFunction#event_trigger}
        :param https_trigger_security_level: The security level for the function. Defaults to SECURE_OPTIONAL. Valid only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#https_trigger_security_level GoogleCloudfunctionsFunction#https_trigger_security_level}
        :param https_trigger_url: URL which triggers function execution. Returned only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#https_trigger_url GoogleCloudfunctionsFunction#https_trigger_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#id GoogleCloudfunctionsFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_settings: String value that controls what traffic can reach the function. Allowed values are ALLOW_ALL and ALLOW_INTERNAL_ONLY. Changes to this field will recreate the cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#ingress_settings GoogleCloudfunctionsFunction#ingress_settings}
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#kms_key_name GoogleCloudfunctionsFunction#kms_key_name}
        :param labels: A set of key/value label pairs to assign to the function. Label keys must follow the requirements at https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#labels GoogleCloudfunctionsFunction#labels}
        :param max_instances: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#max_instances GoogleCloudfunctionsFunction#max_instances}
        :param min_instances: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#min_instances GoogleCloudfunctionsFunction#min_instances}
        :param project: Project of the function. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#project GoogleCloudfunctionsFunction#project}
        :param region: Region of function. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#region GoogleCloudfunctionsFunction#region}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret_environment_variables GoogleCloudfunctionsFunction#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret_volumes GoogleCloudfunctionsFunction#secret_volumes}
        :param service_account_email: If provided, the self-provided service account to run the function with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#service_account_email GoogleCloudfunctionsFunction#service_account_email}
        :param source_archive_bucket: The GCS bucket containing the zip archive which contains the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_archive_bucket GoogleCloudfunctionsFunction#source_archive_bucket}
        :param source_archive_object: The source archive object (file) in archive bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_archive_object GoogleCloudfunctionsFunction#source_archive_object}
        :param source_repository: source_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_repository GoogleCloudfunctionsFunction#source_repository}
        :param timeout: Timeout (in seconds) for the function. Default value is 60 seconds. Cannot be more than 540 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#timeout GoogleCloudfunctionsFunction#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#timeouts GoogleCloudfunctionsFunction#timeouts}
        :param trigger_http: Boolean variable. Any HTTP request (of a supported type) to the endpoint will trigger function execution. Supported HTTP request types are: POST, PUT, GET, DELETE, and OPTIONS. Endpoint is returned as https_trigger_url. Cannot be used with trigger_bucket and trigger_topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#trigger_http GoogleCloudfunctionsFunction#trigger_http}
        :param vpc_connector: The VPC Network Connector that this cloud function can connect to. It can be either the fully-qualified URI, or the short name of the network connector resource. The format of this field is projects/* /locations/* /connectors/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#vpc_connector GoogleCloudfunctionsFunction#vpc_connector} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param vpc_connector_egress_settings: The egress settings for the connector, controlling what traffic is diverted through it. Allowed values are ALL_TRAFFIC and PRIVATE_RANGES_ONLY. Defaults to PRIVATE_RANGES_ONLY. If unset, this field preserves the previously set value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#vpc_connector_egress_settings GoogleCloudfunctionsFunction#vpc_connector_egress_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310860b61821063dde4c42272cd4db5cbdc52dfaff823d3a9d93a846da034198)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudfunctionsFunctionConfig(
            name=name,
            runtime=runtime,
            available_memory_mb=available_memory_mb,
            build_environment_variables=build_environment_variables,
            build_service_account=build_service_account,
            build_worker_pool=build_worker_pool,
            description=description,
            docker_registry=docker_registry,
            docker_repository=docker_repository,
            entry_point=entry_point,
            environment_variables=environment_variables,
            event_trigger=event_trigger,
            https_trigger_security_level=https_trigger_security_level,
            https_trigger_url=https_trigger_url,
            id=id,
            ingress_settings=ingress_settings,
            kms_key_name=kms_key_name,
            labels=labels,
            max_instances=max_instances,
            min_instances=min_instances,
            project=project,
            region=region,
            secret_environment_variables=secret_environment_variables,
            secret_volumes=secret_volumes,
            service_account_email=service_account_email,
            source_archive_bucket=source_archive_bucket,
            source_archive_object=source_archive_object,
            source_repository=source_repository,
            timeout=timeout,
            timeouts=timeouts,
            trigger_http=trigger_http,
            vpc_connector=vpc_connector,
            vpc_connector_egress_settings=vpc_connector_egress_settings,
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
        '''Generates CDKTF code for importing a GoogleCloudfunctionsFunction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudfunctionsFunction to import.
        :param import_from_id: The id of the existing GoogleCloudfunctionsFunction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudfunctionsFunction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b49ef227bace9f957db83c6cf5b3e40b1aadb2cee99b5e38f074f6fe3b847f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventTrigger")
    def put_event_trigger(
        self,
        *,
        event_type: builtins.str,
        resource: builtins.str,
        failure_policy: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionEventTriggerFailurePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event_type: The type of event to observe. For example: "google.storage.object.finalize". See the documentation on calling Cloud Functions for a full reference of accepted triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#event_type GoogleCloudfunctionsFunction#event_type}
        :param resource: The name or partial URI of the resource from which to observe events. For example, "myBucket" or "projects/my-project/topics/my-topic". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#resource GoogleCloudfunctionsFunction#resource}
        :param failure_policy: failure_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#failure_policy GoogleCloudfunctionsFunction#failure_policy}
        '''
        value = GoogleCloudfunctionsFunctionEventTrigger(
            event_type=event_type, resource=resource, failure_policy=failure_policy
        )

        return typing.cast(None, jsii.invoke(self, "putEventTrigger", [value]))

    @jsii.member(jsii_name="putSecretEnvironmentVariables")
    def put_secret_environment_variables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2387dbae7bc0a675ae0676ebe60b6cbe70941469f246207a12288095d35c7dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretEnvironmentVariables", [value]))

    @jsii.member(jsii_name="putSecretVolumes")
    def put_secret_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4926d2d2a74af2fbaaa5ff04030f3a39a3820529c853336766ef4a3eb85e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretVolumes", [value]))

    @jsii.member(jsii_name="putSourceRepository")
    def put_source_repository(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL pointing to the hosted repository where the function is defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#url GoogleCloudfunctionsFunction#url}
        '''
        value = GoogleCloudfunctionsFunctionSourceRepository(url=url)

        return typing.cast(None, jsii.invoke(self, "putSourceRepository", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#create GoogleCloudfunctionsFunction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#delete GoogleCloudfunctionsFunction#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#read GoogleCloudfunctionsFunction#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#update GoogleCloudfunctionsFunction#update}.
        '''
        value = GoogleCloudfunctionsFunctionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvailableMemoryMb")
    def reset_available_memory_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableMemoryMb", []))

    @jsii.member(jsii_name="resetBuildEnvironmentVariables")
    def reset_build_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildEnvironmentVariables", []))

    @jsii.member(jsii_name="resetBuildServiceAccount")
    def reset_build_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildServiceAccount", []))

    @jsii.member(jsii_name="resetBuildWorkerPool")
    def reset_build_worker_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildWorkerPool", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDockerRegistry")
    def reset_docker_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerRegistry", []))

    @jsii.member(jsii_name="resetDockerRepository")
    def reset_docker_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerRepository", []))

    @jsii.member(jsii_name="resetEntryPoint")
    def reset_entry_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntryPoint", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetEventTrigger")
    def reset_event_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventTrigger", []))

    @jsii.member(jsii_name="resetHttpsTriggerSecurityLevel")
    def reset_https_trigger_security_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsTriggerSecurityLevel", []))

    @jsii.member(jsii_name="resetHttpsTriggerUrl")
    def reset_https_trigger_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsTriggerUrl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIngressSettings")
    def reset_ingress_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressSettings", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxInstances")
    def reset_max_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstances", []))

    @jsii.member(jsii_name="resetMinInstances")
    def reset_min_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstances", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecretEnvironmentVariables")
    def reset_secret_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretEnvironmentVariables", []))

    @jsii.member(jsii_name="resetSecretVolumes")
    def reset_secret_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVolumes", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @jsii.member(jsii_name="resetSourceArchiveBucket")
    def reset_source_archive_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceArchiveBucket", []))

    @jsii.member(jsii_name="resetSourceArchiveObject")
    def reset_source_archive_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceArchiveObject", []))

    @jsii.member(jsii_name="resetSourceRepository")
    def reset_source_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRepository", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTriggerHttp")
    def reset_trigger_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerHttp", []))

    @jsii.member(jsii_name="resetVpcConnector")
    def reset_vpc_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConnector", []))

    @jsii.member(jsii_name="resetVpcConnectorEgressSettings")
    def reset_vpc_connector_egress_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConnectorEgressSettings", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="eventTrigger")
    def event_trigger(
        self,
    ) -> "GoogleCloudfunctionsFunctionEventTriggerOutputReference":
        return typing.cast("GoogleCloudfunctionsFunctionEventTriggerOutputReference", jsii.get(self, "eventTrigger"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvironmentVariables")
    def secret_environment_variables(
        self,
    ) -> "GoogleCloudfunctionsFunctionSecretEnvironmentVariablesList":
        return typing.cast("GoogleCloudfunctionsFunctionSecretEnvironmentVariablesList", jsii.get(self, "secretEnvironmentVariables"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumes")
    def secret_volumes(self) -> "GoogleCloudfunctionsFunctionSecretVolumesList":
        return typing.cast("GoogleCloudfunctionsFunctionSecretVolumesList", jsii.get(self, "secretVolumes"))

    @builtins.property
    @jsii.member(jsii_name="sourceRepository")
    def source_repository(
        self,
    ) -> "GoogleCloudfunctionsFunctionSourceRepositoryOutputReference":
        return typing.cast("GoogleCloudfunctionsFunctionSourceRepositoryOutputReference", jsii.get(self, "sourceRepository"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudfunctionsFunctionTimeoutsOutputReference":
        return typing.cast("GoogleCloudfunctionsFunctionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @builtins.property
    @jsii.member(jsii_name="availableMemoryMbInput")
    def available_memory_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "availableMemoryMbInput"))

    @builtins.property
    @jsii.member(jsii_name="buildEnvironmentVariablesInput")
    def build_environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "buildEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="buildServiceAccountInput")
    def build_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="buildWorkerPoolInput")
    def build_worker_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildWorkerPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerRegistryInput")
    def docker_registry_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerRegistryInput"))

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
    @jsii.member(jsii_name="eventTriggerInput")
    def event_trigger_input(
        self,
    ) -> typing.Optional["GoogleCloudfunctionsFunctionEventTrigger"]:
        return typing.cast(typing.Optional["GoogleCloudfunctionsFunctionEventTrigger"], jsii.get(self, "eventTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsTriggerSecurityLevelInput")
    def https_trigger_security_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsTriggerSecurityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsTriggerUrlInput")
    def https_trigger_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsTriggerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressSettingsInput")
    def ingress_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingressSettingsInput"))

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
    @jsii.member(jsii_name="maxInstancesInput")
    def max_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstancesInput")
    def min_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvironmentVariablesInput")
    def secret_environment_variables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretEnvironmentVariables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretEnvironmentVariables"]]], jsii.get(self, "secretEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumesInput")
    def secret_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumes"]]], jsii.get(self, "secretVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceArchiveBucketInput")
    def source_archive_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceArchiveBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceArchiveObjectInput")
    def source_archive_object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceArchiveObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRepositoryInput")
    def source_repository_input(
        self,
    ) -> typing.Optional["GoogleCloudfunctionsFunctionSourceRepository"]:
        return typing.cast(typing.Optional["GoogleCloudfunctionsFunctionSourceRepository"], jsii.get(self, "sourceRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudfunctionsFunctionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudfunctionsFunctionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerHttpInput")
    def trigger_http_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "triggerHttpInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorEgressSettingsInput")
    def vpc_connector_egress_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectorEgressSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorInput")
    def vpc_connector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="availableMemoryMb")
    def available_memory_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableMemoryMb"))

    @available_memory_mb.setter
    def available_memory_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ee8ac04b4b348228c73f3450fede3abd8f43c03372959c14a3484edd85beba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableMemoryMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildEnvironmentVariables")
    def build_environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "buildEnvironmentVariables"))

    @build_environment_variables.setter
    def build_environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa8bc3d2af576b4d77dff1c4e12931fc8943bea9fd0a6f2e806e5e33b38a88b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildEnvironmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildServiceAccount")
    def build_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildServiceAccount"))

    @build_service_account.setter
    def build_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928410746c7d342d5d427112e775259ba144377d5cd2b97aa9478b4ed8344b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildWorkerPool")
    def build_worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildWorkerPool"))

    @build_worker_pool.setter
    def build_worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca87806aa91eab247b25b862a4706088dd678b3eebef6c79960abf264047402c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildWorkerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57699ca04ceb2c2080aabf89b64e28665d74718784501e8bd616c0a255fe2ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerRegistry")
    def docker_registry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerRegistry"))

    @docker_registry.setter
    def docker_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11d50e3d26b8b318b494bfa00d66b8e168efb4ab7bfe9f8c4e5d4fbfe145c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRegistry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerRepository")
    def docker_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerRepository"))

    @docker_repository.setter
    def docker_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad68406f7c27090ef76e936c7a80ba9bf2345f5e5c3008426cd6c106c6ad3ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryPoint")
    def entry_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryPoint"))

    @entry_point.setter
    def entry_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81146bd8e061fd362a4adc07666ee68b88b4da142b87faab28d93ecc7ba9e80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2692a195cab2e4767c23141cda1e8abee8bc3bc07fd0034f8378ddca006910c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsTriggerSecurityLevel")
    def https_trigger_security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsTriggerSecurityLevel"))

    @https_trigger_security_level.setter
    def https_trigger_security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5dcecd7ed8bd33ed0ba8277655b18a140aa1fbc4b4fe95cc9b7af5403173478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsTriggerSecurityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsTriggerUrl")
    def https_trigger_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsTriggerUrl"))

    @https_trigger_url.setter
    def https_trigger_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e800d85cfe825cfe2939e59bfe0cbda7a7a3422fbd2f06d90658e0e1d471bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsTriggerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e20c8580799dfcb0f669efd5bc8eddaaf3cb295ca486c4d78e8c681ae5c5b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressSettings")
    def ingress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressSettings"))

    @ingress_settings.setter
    def ingress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7e12873ca17a81545740ab7c3e3061a4c5fc93a5c5d04b1d865542e27e8dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9557180cbe33bf6e47de5dc243c44a0f610f8545de0dd9aa1a996e4dd6d6fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f6a8f5d2066668b50b4651b0927ec1853ea778a78fcd1b123eebf55d35b83d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f8d364ba605210fd7fa2964d22ed1ec81bc531746aec50e769e25abd3c0f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @min_instances.setter
    def min_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66284978ca557754c0c6ae68e54091f084eba0b319115e057598af489568e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0c247b3bcfed9f1e97189e959b9c00d2d2e614bea13a1fa0a99e3f9883a3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98621bf0132d6bf799d37b532bdeff0873102a5867b79540f2cf1734b5738f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcb684ba51f0830b93f181972a46bec4e27dcf7de5f0363b62defe309e176d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__decb700af80784aa1f9baf9dc97aefd7fb34f765de27372a5042f6c98951ac03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871bbf67aaab28e5f1b2b026a1fbf46a890ee4b4e4506b1d111068cad49603fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceArchiveBucket")
    def source_archive_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceArchiveBucket"))

    @source_archive_bucket.setter
    def source_archive_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971de6e660efb1e4b814dde816147998c35d05c1a969d93309d5120158689912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArchiveBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceArchiveObject")
    def source_archive_object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceArchiveObject"))

    @source_archive_object.setter
    def source_archive_object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea6cbfabad4d825cf1e08af1d2b31a2b6ad42c19a0168b2b9449c1f18f3e3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArchiveObject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815c47f59af7e1c0def3636b790f432f70249cd47f0abf090a8889e5d3991e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerHttp")
    def trigger_http(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "triggerHttp"))

    @trigger_http.setter
    def trigger_http(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5443829e07afc07e1de8a22e40f04b05f56ae8e4b149b8cb73a7cd3fdae5bc6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerHttp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnector")
    def vpc_connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnector"))

    @vpc_connector.setter
    def vpc_connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a47cd611e542d12896a38bb494f2d23d759155d5482c8989c227901b1b8a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorEgressSettings")
    def vpc_connector_egress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorEgressSettings"))

    @vpc_connector_egress_settings.setter
    def vpc_connector_egress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5daadbf497b5abc10fac09bd05f63a263c28a422fb37f98d0ffade595638b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectorEgressSettings", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionConfig",
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
        "runtime": "runtime",
        "available_memory_mb": "availableMemoryMb",
        "build_environment_variables": "buildEnvironmentVariables",
        "build_service_account": "buildServiceAccount",
        "build_worker_pool": "buildWorkerPool",
        "description": "description",
        "docker_registry": "dockerRegistry",
        "docker_repository": "dockerRepository",
        "entry_point": "entryPoint",
        "environment_variables": "environmentVariables",
        "event_trigger": "eventTrigger",
        "https_trigger_security_level": "httpsTriggerSecurityLevel",
        "https_trigger_url": "httpsTriggerUrl",
        "id": "id",
        "ingress_settings": "ingressSettings",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "max_instances": "maxInstances",
        "min_instances": "minInstances",
        "project": "project",
        "region": "region",
        "secret_environment_variables": "secretEnvironmentVariables",
        "secret_volumes": "secretVolumes",
        "service_account_email": "serviceAccountEmail",
        "source_archive_bucket": "sourceArchiveBucket",
        "source_archive_object": "sourceArchiveObject",
        "source_repository": "sourceRepository",
        "timeout": "timeout",
        "timeouts": "timeouts",
        "trigger_http": "triggerHttp",
        "vpc_connector": "vpcConnector",
        "vpc_connector_egress_settings": "vpcConnectorEgressSettings",
    },
)
class GoogleCloudfunctionsFunctionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        runtime: builtins.str,
        available_memory_mb: typing.Optional[jsii.Number] = None,
        build_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        build_service_account: typing.Optional[builtins.str] = None,
        build_worker_pool: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        docker_registry: typing.Optional[builtins.str] = None,
        docker_repository: typing.Optional[builtins.str] = None,
        entry_point: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        event_trigger: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
        https_trigger_security_level: typing.Optional[builtins.str] = None,
        https_trigger_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ingress_settings: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        source_archive_bucket: typing.Optional[builtins.str] = None,
        source_archive_object: typing.Optional[builtins.str] = None,
        source_repository: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionSourceRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger_http: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc_connector: typing.Optional[builtins.str] = None,
        vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: A user-defined name of the function. Function names must be unique globally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#name GoogleCloudfunctionsFunction#name}
        :param runtime: The runtime in which the function is going to run. Eg. "nodejs20", "python37", "go111". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#runtime GoogleCloudfunctionsFunction#runtime}
        :param available_memory_mb: Memory (in MB), available to the function. Default value is 256. Possible values include 128, 256, 512, 1024, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#available_memory_mb GoogleCloudfunctionsFunction#available_memory_mb}
        :param build_environment_variables: A set of key/value environment variable pairs available during build time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_environment_variables GoogleCloudfunctionsFunction#build_environment_variables}
        :param build_service_account: The fully-qualified name of the service account to be used for the build step of deploying this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_service_account GoogleCloudfunctionsFunction#build_service_account}
        :param build_worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_worker_pool GoogleCloudfunctionsFunction#build_worker_pool}
        :param description: Description of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#description GoogleCloudfunctionsFunction#description}
        :param docker_registry: Docker Registry to use for storing the function's Docker images. Allowed values are ARTIFACT_REGISTRY (default) and CONTAINER_REGISTRY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#docker_registry GoogleCloudfunctionsFunction#docker_registry}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. If specified, deployments will use Artifact Registry for storing images built with Cloud Build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#docker_repository GoogleCloudfunctionsFunction#docker_repository}
        :param entry_point: Name of the function that will be executed when the Google Cloud Function is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#entry_point GoogleCloudfunctionsFunction#entry_point}
        :param environment_variables: A set of key/value environment variable pairs to assign to the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#environment_variables GoogleCloudfunctionsFunction#environment_variables}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#event_trigger GoogleCloudfunctionsFunction#event_trigger}
        :param https_trigger_security_level: The security level for the function. Defaults to SECURE_OPTIONAL. Valid only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#https_trigger_security_level GoogleCloudfunctionsFunction#https_trigger_security_level}
        :param https_trigger_url: URL which triggers function execution. Returned only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#https_trigger_url GoogleCloudfunctionsFunction#https_trigger_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#id GoogleCloudfunctionsFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_settings: String value that controls what traffic can reach the function. Allowed values are ALLOW_ALL and ALLOW_INTERNAL_ONLY. Changes to this field will recreate the cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#ingress_settings GoogleCloudfunctionsFunction#ingress_settings}
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#kms_key_name GoogleCloudfunctionsFunction#kms_key_name}
        :param labels: A set of key/value label pairs to assign to the function. Label keys must follow the requirements at https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#labels GoogleCloudfunctionsFunction#labels}
        :param max_instances: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#max_instances GoogleCloudfunctionsFunction#max_instances}
        :param min_instances: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#min_instances GoogleCloudfunctionsFunction#min_instances}
        :param project: Project of the function. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#project GoogleCloudfunctionsFunction#project}
        :param region: Region of function. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#region GoogleCloudfunctionsFunction#region}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret_environment_variables GoogleCloudfunctionsFunction#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret_volumes GoogleCloudfunctionsFunction#secret_volumes}
        :param service_account_email: If provided, the self-provided service account to run the function with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#service_account_email GoogleCloudfunctionsFunction#service_account_email}
        :param source_archive_bucket: The GCS bucket containing the zip archive which contains the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_archive_bucket GoogleCloudfunctionsFunction#source_archive_bucket}
        :param source_archive_object: The source archive object (file) in archive bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_archive_object GoogleCloudfunctionsFunction#source_archive_object}
        :param source_repository: source_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_repository GoogleCloudfunctionsFunction#source_repository}
        :param timeout: Timeout (in seconds) for the function. Default value is 60 seconds. Cannot be more than 540 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#timeout GoogleCloudfunctionsFunction#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#timeouts GoogleCloudfunctionsFunction#timeouts}
        :param trigger_http: Boolean variable. Any HTTP request (of a supported type) to the endpoint will trigger function execution. Supported HTTP request types are: POST, PUT, GET, DELETE, and OPTIONS. Endpoint is returned as https_trigger_url. Cannot be used with trigger_bucket and trigger_topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#trigger_http GoogleCloudfunctionsFunction#trigger_http}
        :param vpc_connector: The VPC Network Connector that this cloud function can connect to. It can be either the fully-qualified URI, or the short name of the network connector resource. The format of this field is projects/* /locations/* /connectors/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#vpc_connector GoogleCloudfunctionsFunction#vpc_connector} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param vpc_connector_egress_settings: The egress settings for the connector, controlling what traffic is diverted through it. Allowed values are ALL_TRAFFIC and PRIVATE_RANGES_ONLY. Defaults to PRIVATE_RANGES_ONLY. If unset, this field preserves the previously set value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#vpc_connector_egress_settings GoogleCloudfunctionsFunction#vpc_connector_egress_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(event_trigger, dict):
            event_trigger = GoogleCloudfunctionsFunctionEventTrigger(**event_trigger)
        if isinstance(source_repository, dict):
            source_repository = GoogleCloudfunctionsFunctionSourceRepository(**source_repository)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudfunctionsFunctionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78c36e14eb7ca85d3db31c12c173c504d332e330bf2564d04b2617ac87b01f9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument available_memory_mb", value=available_memory_mb, expected_type=type_hints["available_memory_mb"])
            check_type(argname="argument build_environment_variables", value=build_environment_variables, expected_type=type_hints["build_environment_variables"])
            check_type(argname="argument build_service_account", value=build_service_account, expected_type=type_hints["build_service_account"])
            check_type(argname="argument build_worker_pool", value=build_worker_pool, expected_type=type_hints["build_worker_pool"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument docker_registry", value=docker_registry, expected_type=type_hints["docker_registry"])
            check_type(argname="argument docker_repository", value=docker_repository, expected_type=type_hints["docker_repository"])
            check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument event_trigger", value=event_trigger, expected_type=type_hints["event_trigger"])
            check_type(argname="argument https_trigger_security_level", value=https_trigger_security_level, expected_type=type_hints["https_trigger_security_level"])
            check_type(argname="argument https_trigger_url", value=https_trigger_url, expected_type=type_hints["https_trigger_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingress_settings", value=ingress_settings, expected_type=type_hints["ingress_settings"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_instances", value=max_instances, expected_type=type_hints["max_instances"])
            check_type(argname="argument min_instances", value=min_instances, expected_type=type_hints["min_instances"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secret_environment_variables", value=secret_environment_variables, expected_type=type_hints["secret_environment_variables"])
            check_type(argname="argument secret_volumes", value=secret_volumes, expected_type=type_hints["secret_volumes"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument source_archive_bucket", value=source_archive_bucket, expected_type=type_hints["source_archive_bucket"])
            check_type(argname="argument source_archive_object", value=source_archive_object, expected_type=type_hints["source_archive_object"])
            check_type(argname="argument source_repository", value=source_repository, expected_type=type_hints["source_repository"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trigger_http", value=trigger_http, expected_type=type_hints["trigger_http"])
            check_type(argname="argument vpc_connector", value=vpc_connector, expected_type=type_hints["vpc_connector"])
            check_type(argname="argument vpc_connector_egress_settings", value=vpc_connector_egress_settings, expected_type=type_hints["vpc_connector_egress_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "runtime": runtime,
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
        if available_memory_mb is not None:
            self._values["available_memory_mb"] = available_memory_mb
        if build_environment_variables is not None:
            self._values["build_environment_variables"] = build_environment_variables
        if build_service_account is not None:
            self._values["build_service_account"] = build_service_account
        if build_worker_pool is not None:
            self._values["build_worker_pool"] = build_worker_pool
        if description is not None:
            self._values["description"] = description
        if docker_registry is not None:
            self._values["docker_registry"] = docker_registry
        if docker_repository is not None:
            self._values["docker_repository"] = docker_repository
        if entry_point is not None:
            self._values["entry_point"] = entry_point
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if event_trigger is not None:
            self._values["event_trigger"] = event_trigger
        if https_trigger_security_level is not None:
            self._values["https_trigger_security_level"] = https_trigger_security_level
        if https_trigger_url is not None:
            self._values["https_trigger_url"] = https_trigger_url
        if id is not None:
            self._values["id"] = id
        if ingress_settings is not None:
            self._values["ingress_settings"] = ingress_settings
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if max_instances is not None:
            self._values["max_instances"] = max_instances
        if min_instances is not None:
            self._values["min_instances"] = min_instances
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if secret_environment_variables is not None:
            self._values["secret_environment_variables"] = secret_environment_variables
        if secret_volumes is not None:
            self._values["secret_volumes"] = secret_volumes
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email
        if source_archive_bucket is not None:
            self._values["source_archive_bucket"] = source_archive_bucket
        if source_archive_object is not None:
            self._values["source_archive_object"] = source_archive_object
        if source_repository is not None:
            self._values["source_repository"] = source_repository
        if timeout is not None:
            self._values["timeout"] = timeout
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trigger_http is not None:
            self._values["trigger_http"] = trigger_http
        if vpc_connector is not None:
            self._values["vpc_connector"] = vpc_connector
        if vpc_connector_egress_settings is not None:
            self._values["vpc_connector_egress_settings"] = vpc_connector_egress_settings

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
        '''A user-defined name of the function. Function names must be unique globally.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#name GoogleCloudfunctionsFunction#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''The runtime in which the function is going to run. Eg. "nodejs20", "python37", "go111".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#runtime GoogleCloudfunctionsFunction#runtime}
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def available_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''Memory (in MB), available to the function. Default value is 256. Possible values include 128, 256, 512, 1024, etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#available_memory_mb GoogleCloudfunctionsFunction#available_memory_mb}
        '''
        result = self._values.get("available_memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def build_environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value environment variable pairs available during build time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_environment_variables GoogleCloudfunctionsFunction#build_environment_variables}
        '''
        result = self._values.get("build_environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def build_service_account(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified name of the service account to be used for the build step of deploying this function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_service_account GoogleCloudfunctionsFunction#build_service_account}
        '''
        result = self._values.get("build_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_worker_pool(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Build Custom Worker Pool that should be used to build the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#build_worker_pool GoogleCloudfunctionsFunction#build_worker_pool}
        '''
        result = self._values.get("build_worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#description GoogleCloudfunctionsFunction#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_registry(self) -> typing.Optional[builtins.str]:
        '''Docker Registry to use for storing the function's Docker images. Allowed values are ARTIFACT_REGISTRY (default) and CONTAINER_REGISTRY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#docker_registry GoogleCloudfunctionsFunction#docker_registry}
        '''
        result = self._values.get("docker_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_repository(self) -> typing.Optional[builtins.str]:
        '''User managed repository created in Artifact Registry optionally with a customer managed encryption key.

        If specified, deployments will use Artifact Registry for storing images built with Cloud Build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#docker_repository GoogleCloudfunctionsFunction#docker_repository}
        '''
        result = self._values.get("docker_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry_point(self) -> typing.Optional[builtins.str]:
        '''Name of the function that will be executed when the Google Cloud Function is triggered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#entry_point GoogleCloudfunctionsFunction#entry_point}
        '''
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value environment variable pairs to assign to the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#environment_variables GoogleCloudfunctionsFunction#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def event_trigger(
        self,
    ) -> typing.Optional["GoogleCloudfunctionsFunctionEventTrigger"]:
        '''event_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#event_trigger GoogleCloudfunctionsFunction#event_trigger}
        '''
        result = self._values.get("event_trigger")
        return typing.cast(typing.Optional["GoogleCloudfunctionsFunctionEventTrigger"], result)

    @builtins.property
    def https_trigger_security_level(self) -> typing.Optional[builtins.str]:
        '''The security level for the function. Defaults to SECURE_OPTIONAL. Valid only if trigger_http is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#https_trigger_security_level GoogleCloudfunctionsFunction#https_trigger_security_level}
        '''
        result = self._values.get("https_trigger_security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_trigger_url(self) -> typing.Optional[builtins.str]:
        '''URL which triggers function execution. Returned only if trigger_http is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#https_trigger_url GoogleCloudfunctionsFunction#https_trigger_url}
        '''
        result = self._values.get("https_trigger_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#id GoogleCloudfunctionsFunction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_settings(self) -> typing.Optional[builtins.str]:
        '''String value that controls what traffic can reach the function.

        Allowed values are ALLOW_ALL and ALLOW_INTERNAL_ONLY. Changes to this field will recreate the cloud function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#ingress_settings GoogleCloudfunctionsFunction#ingress_settings}
        '''
        result = self._values.get("ingress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#kms_key_name GoogleCloudfunctionsFunction#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to the function. Label keys must follow the requirements at https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#labels GoogleCloudfunctionsFunction#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_instances(self) -> typing.Optional[jsii.Number]:
        '''The limit on the maximum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#max_instances GoogleCloudfunctionsFunction#max_instances}
        '''
        result = self._values.get("max_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''The limit on the minimum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#min_instances GoogleCloudfunctionsFunction#min_instances}
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Project of the function. If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#project GoogleCloudfunctionsFunction#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region of function. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#region GoogleCloudfunctionsFunction#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretEnvironmentVariables"]]]:
        '''secret_environment_variables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret_environment_variables GoogleCloudfunctionsFunction#secret_environment_variables}
        '''
        result = self._values.get("secret_environment_variables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretEnvironmentVariables"]]], result)

    @builtins.property
    def secret_volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumes"]]]:
        '''secret_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret_volumes GoogleCloudfunctionsFunction#secret_volumes}
        '''
        result = self._values.get("secret_volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumes"]]], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''If provided, the self-provided service account to run the function with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#service_account_email GoogleCloudfunctionsFunction#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_archive_bucket(self) -> typing.Optional[builtins.str]:
        '''The GCS bucket containing the zip archive which contains the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_archive_bucket GoogleCloudfunctionsFunction#source_archive_bucket}
        '''
        result = self._values.get("source_archive_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_archive_object(self) -> typing.Optional[builtins.str]:
        '''The source archive object (file) in archive bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_archive_object GoogleCloudfunctionsFunction#source_archive_object}
        '''
        result = self._values.get("source_archive_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_repository(
        self,
    ) -> typing.Optional["GoogleCloudfunctionsFunctionSourceRepository"]:
        '''source_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#source_repository GoogleCloudfunctionsFunction#source_repository}
        '''
        result = self._values.get("source_repository")
        return typing.cast(typing.Optional["GoogleCloudfunctionsFunctionSourceRepository"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for the function. Default value is 60 seconds. Cannot be more than 540 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#timeout GoogleCloudfunctionsFunction#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudfunctionsFunctionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#timeouts GoogleCloudfunctionsFunction#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudfunctionsFunctionTimeouts"], result)

    @builtins.property
    def trigger_http(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean variable.

        Any HTTP request (of a supported type) to the endpoint will trigger function execution. Supported HTTP request types are: POST, PUT, GET, DELETE, and OPTIONS. Endpoint is returned as https_trigger_url. Cannot be used with trigger_bucket and trigger_topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#trigger_http GoogleCloudfunctionsFunction#trigger_http}
        '''
        result = self._values.get("trigger_http")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vpc_connector(self) -> typing.Optional[builtins.str]:
        '''The VPC Network Connector that this cloud function can connect to.

        It can be either the fully-qualified URI, or the short name of the network connector resource. The format of this field is projects/* /locations/* /connectors/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#vpc_connector GoogleCloudfunctionsFunction#vpc_connector}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("vpc_connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_connector_egress_settings(self) -> typing.Optional[builtins.str]:
        '''The egress settings for the connector, controlling what traffic is diverted through it.

        Allowed values are ALL_TRAFFIC and PRIVATE_RANGES_ONLY. Defaults to PRIVATE_RANGES_ONLY. If unset, this field preserves the previously set value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#vpc_connector_egress_settings GoogleCloudfunctionsFunction#vpc_connector_egress_settings}
        '''
        result = self._values.get("vpc_connector_egress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionEventTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "resource": "resource",
        "failure_policy": "failurePolicy",
    },
)
class GoogleCloudfunctionsFunctionEventTrigger:
    def __init__(
        self,
        *,
        event_type: builtins.str,
        resource: builtins.str,
        failure_policy: typing.Optional[typing.Union["GoogleCloudfunctionsFunctionEventTriggerFailurePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event_type: The type of event to observe. For example: "google.storage.object.finalize". See the documentation on calling Cloud Functions for a full reference of accepted triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#event_type GoogleCloudfunctionsFunction#event_type}
        :param resource: The name or partial URI of the resource from which to observe events. For example, "myBucket" or "projects/my-project/topics/my-topic". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#resource GoogleCloudfunctionsFunction#resource}
        :param failure_policy: failure_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#failure_policy GoogleCloudfunctionsFunction#failure_policy}
        '''
        if isinstance(failure_policy, dict):
            failure_policy = GoogleCloudfunctionsFunctionEventTriggerFailurePolicy(**failure_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86892f971d51f59f86d547af4e1c2ef006b040bfe6e70bcc37a59cef3068dc5e)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument failure_policy", value=failure_policy, expected_type=type_hints["failure_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "resource": resource,
        }
        if failure_policy is not None:
            self._values["failure_policy"] = failure_policy

    @builtins.property
    def event_type(self) -> builtins.str:
        '''The type of event to observe.

        For example: "google.storage.object.finalize". See the documentation on calling Cloud Functions for a full reference of accepted triggers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#event_type GoogleCloudfunctionsFunction#event_type}
        '''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(self) -> builtins.str:
        '''The name or partial URI of the resource from which to observe events. For example, "myBucket" or "projects/my-project/topics/my-topic".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#resource GoogleCloudfunctionsFunction#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_policy(
        self,
    ) -> typing.Optional["GoogleCloudfunctionsFunctionEventTriggerFailurePolicy"]:
        '''failure_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#failure_policy GoogleCloudfunctionsFunction#failure_policy}
        '''
        result = self._values.get("failure_policy")
        return typing.cast(typing.Optional["GoogleCloudfunctionsFunctionEventTriggerFailurePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionEventTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionEventTriggerFailurePolicy",
    jsii_struct_bases=[],
    name_mapping={"retry": "retry"},
)
class GoogleCloudfunctionsFunctionEventTriggerFailurePolicy:
    def __init__(
        self,
        *,
        retry: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param retry: Whether the function should be retried on failure. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#retry GoogleCloudfunctionsFunction#retry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6d0257e27025d62a5684483773133ad7d23e9e999b48d90a205c768b0e5fd2)
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retry": retry,
        }

    @builtins.property
    def retry(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the function should be retried on failure. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#retry GoogleCloudfunctionsFunction#retry}
        '''
        result = self._values.get("retry")
        assert result is not None, "Required property 'retry' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionEventTriggerFailurePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctionsFunctionEventTriggerFailurePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionEventTriggerFailurePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c227941f78b12e9b0f74df8dab8400ea1771d7dbbc8b08a3272bec4d7f833b3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="retry")
    def retry(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retry"))

    @retry.setter
    def retry(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a05e497a134105471b83be80ae18fc34c330492480b53f577213c824522ec36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctionsFunctionEventTriggerFailurePolicy]:
        return typing.cast(typing.Optional[GoogleCloudfunctionsFunctionEventTriggerFailurePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctionsFunctionEventTriggerFailurePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e182ecff88afaedcf18fb768a188dab1cf150f130da0d8eb4b2f83b9e24b9d91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctionsFunctionEventTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionEventTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb82c0c409ed035d810dca6fd8484bf3d04a2727f756a44f8ce0cd3a836d709a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFailurePolicy")
    def put_failure_policy(
        self,
        *,
        retry: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param retry: Whether the function should be retried on failure. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#retry GoogleCloudfunctionsFunction#retry}
        '''
        value = GoogleCloudfunctionsFunctionEventTriggerFailurePolicy(retry=retry)

        return typing.cast(None, jsii.invoke(self, "putFailurePolicy", [value]))

    @jsii.member(jsii_name="resetFailurePolicy")
    def reset_failure_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailurePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="failurePolicy")
    def failure_policy(
        self,
    ) -> GoogleCloudfunctionsFunctionEventTriggerFailurePolicyOutputReference:
        return typing.cast(GoogleCloudfunctionsFunctionEventTriggerFailurePolicyOutputReference, jsii.get(self, "failurePolicy"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="failurePolicyInput")
    def failure_policy_input(
        self,
    ) -> typing.Optional[GoogleCloudfunctionsFunctionEventTriggerFailurePolicy]:
        return typing.cast(typing.Optional[GoogleCloudfunctionsFunctionEventTriggerFailurePolicy], jsii.get(self, "failurePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259d2c941594da7503b048dc42e7cd416db717254d864fe20bc3583fed35b435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082453c51a8c5e772c455b7b370c6a9645ca7058098d4759c115b872b7b162af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctionsFunctionEventTrigger]:
        return typing.cast(typing.Optional[GoogleCloudfunctionsFunctionEventTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctionsFunctionEventTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe43846957a1c41bbc98f7eac4c5938a8b2790c2029769e90c185690fb1ce39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretEnvironmentVariables",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "secret": "secret",
        "version": "version",
        "project_id": "projectId",
    },
)
class GoogleCloudfunctionsFunctionSecretEnvironmentVariables:
    def __init__(
        self,
        *,
        key: builtins.str,
        secret: builtins.str,
        version: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Name of the environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#key GoogleCloudfunctionsFunction#key}
        :param secret: ID of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret GoogleCloudfunctionsFunction#secret}
        :param version: Version of the secret (version number or the string "latest"). It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new clones start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#version GoogleCloudfunctionsFunction#version}
        :param project_id: Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret. If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#project_id GoogleCloudfunctionsFunction#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c6c7b9d1f0fb98dcd4f5de42489977bdb3b1448faabb18979e9bf5cc836468)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "secret": secret,
            "version": version,
        }
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def key(self) -> builtins.str:
        '''Name of the environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#key GoogleCloudfunctionsFunction#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''ID of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret GoogleCloudfunctionsFunction#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string "latest").

        It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new clones start.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#version GoogleCloudfunctionsFunction#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret.

        If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#project_id GoogleCloudfunctionsFunction#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionSecretEnvironmentVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctionsFunctionSecretEnvironmentVariablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretEnvironmentVariablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad700cbaae0440e49c8316f6a524b4419890addd8734abbcd1d0aee16492b7e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudfunctionsFunctionSecretEnvironmentVariablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4798fbd71d48592bc1672667fcf12eacac8f117648d3455ebe70aeede4763264)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudfunctionsFunctionSecretEnvironmentVariablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c2cabfb2ec136e460458a7f133b54fc643352a7c8d947bef06aafb886d9bc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db4cfac6cffecc9a9d81e6af2ecefffe0a2e8d60f94508bd1524503c96650019)
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
            type_hints = typing.get_type_hints(_typecheckingstub__195860be8bcf57838cd76578362ec98266c2ff9665287263dc6a6fd198bf8d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretEnvironmentVariables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretEnvironmentVariables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretEnvironmentVariables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b9a9db86abb465fb3d64c3036402a9e62539533b06fe9989f11bb188055e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctionsFunctionSecretEnvironmentVariablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretEnvironmentVariablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__488c6f08f11a301aaf01b30fa164ed9ab0daff1fcf35307b5b09b4789d6b2f78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__488ad83c8b7c15da887095374f700a7fb57555114c4240c22f6df21f80059aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674850d0ec56a8f63867087838b5f02d0002fe5303a6706d0a7ec49615408492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd55db2bed8f79f0fb1e718e9961104eefa3f7a7dd01f7343afa5a47b051d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc01f7685a4e053269d94146426e9a9b5ade624f9b55184e6f19bafe94e43ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretEnvironmentVariables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretEnvironmentVariables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretEnvironmentVariables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8bff73b02f45613da86f4f11d923609e65ce93041d2d4c3b13f92524082334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "mount_path": "mountPath",
        "secret": "secret",
        "project_id": "projectId",
        "versions": "versions",
    },
)
class GoogleCloudfunctionsFunctionSecretVolumes:
    def __init__(
        self,
        *,
        mount_path: builtins.str,
        secret: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
        versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mount_path: The path within the container to mount the secret volume. For example, setting the mount_path as "/etc/secrets" would mount the secret value files under the "/etc/secrets" directory. This directory will also be completely shadowed and unavailable to mount any other secrets. Recommended mount paths: "/etc/secrets" Restricted mount paths: "/cloudsql", "/dev/log", "/pod", "/proc", "/var/log". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#mount_path GoogleCloudfunctionsFunction#mount_path}
        :param secret: ID of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret GoogleCloudfunctionsFunction#secret}
        :param project_id: Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret. If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#project_id GoogleCloudfunctionsFunction#project_id}
        :param versions: versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#versions GoogleCloudfunctionsFunction#versions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb4c0eb37763c035d14a38690593213ce5544a52399b5fa5f4e95e9a99aefc2)
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument versions", value=versions, expected_type=type_hints["versions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mount_path": mount_path,
            "secret": secret,
        }
        if project_id is not None:
            self._values["project_id"] = project_id
        if versions is not None:
            self._values["versions"] = versions

    @builtins.property
    def mount_path(self) -> builtins.str:
        '''The path within the container to mount the secret volume.

        For example, setting the mount_path as "/etc/secrets" would mount the secret value files under the "/etc/secrets" directory. This directory will also be completely shadowed and unavailable to mount any other secrets. Recommended mount paths: "/etc/secrets" Restricted mount paths: "/cloudsql", "/dev/log", "/pod", "/proc", "/var/log".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#mount_path GoogleCloudfunctionsFunction#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''ID of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#secret GoogleCloudfunctionsFunction#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret.

        If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#project_id GoogleCloudfunctionsFunction#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def versions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumesVersions"]]]:
        '''versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#versions GoogleCloudfunctionsFunction#versions}
        '''
        result = self._values.get("versions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumesVersions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionSecretVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctionsFunctionSecretVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cc56e5e6973d92951330ee00d681ee0641348a6f715cf32fa372c9baa4c7e6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudfunctionsFunctionSecretVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060bc52756a8054fc9137a6e1fcce5c9d32cf15e17b3cb8d0620b5633ec5ca87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudfunctionsFunctionSecretVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ec53ae029f3f1c4a2d22ef4a8b779b9f026396b08f3c14876b9478751aebfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82fef000544a86e68581a6fcf9e7d1a4314fa12c66122bb0c2ed6d8b5399f2de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f7708cc163d6ce9586fc43d7d212d4ff64363625d154decf5d3439eb02fbe20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b1795a6ba79198cced34360c309b9f61a33ac816cf27c19b6c7d67fe56bfa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctionsFunctionSecretVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60597188e6663b857b17f0fdc1e4369bce606ee5a272e7d05e36fb3128a1c832)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVersions")
    def put_versions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudfunctionsFunctionSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576b81e6ff19db3c66507f1c1c436445aaed41bd0e224867e9496b3c5c070da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVersions", [value]))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetVersions")
    def reset_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersions", []))

    @builtins.property
    @jsii.member(jsii_name="versions")
    def versions(self) -> "GoogleCloudfunctionsFunctionSecretVolumesVersionsList":
        return typing.cast("GoogleCloudfunctionsFunctionSecretVolumesVersionsList", jsii.get(self, "versions"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumesVersions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudfunctionsFunctionSecretVolumesVersions"]]], jsii.get(self, "versionsInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de92bba460f1faa707a60af3f30713e2b9612971c6faac581f7183ef3e4a658d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a763178564d8ec9d5d7e8015ff55f4f3a3757f6ef224c81e0e1b8c46b4adb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbf25810eb43bbccf6c138bdfc449069bdf5745869e21f9df613f99ebc34ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821d6c91774cfa5a2c47134eb6b576d6bdd500358c5a126b0be812c4120f8ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretVolumesVersions",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "version": "version"},
)
class GoogleCloudfunctionsFunctionSecretVolumesVersions:
    def __init__(self, *, path: builtins.str, version: builtins.str) -> None:
        '''
        :param path: Relative path of the file under the mount path where the secret value for this version will be fetched and made available. For example, setting the mount_path as "/etc/secrets" and path as "/secret_foo" would mount the secret value file at "/etc/secrets/secret_foo". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#path GoogleCloudfunctionsFunction#path}
        :param version: Version of the secret (version number or the string "latest"). It is preferable to use "latest" version with secret volumes as secret value changes are reflected immediately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#version GoogleCloudfunctionsFunction#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7b47bdaef0a51882a0ecf4718fa54ad0a4a4bdc8d288e2671161471828d39b)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "version": version,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Relative path of the file under the mount path where the secret value for this version will be fetched and made available.

        For example, setting the mount_path as "/etc/secrets" and path as "/secret_foo" would mount the secret value file at "/etc/secrets/secret_foo".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#path GoogleCloudfunctionsFunction#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string "latest").

        It is preferable to use "latest" version with secret volumes as secret value changes are reflected immediately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#version GoogleCloudfunctionsFunction#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionSecretVolumesVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctionsFunctionSecretVolumesVersionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretVolumesVersionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95744cb95130d5651d152d0185178482fdc0d139d891e678c93c8004399c30d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudfunctionsFunctionSecretVolumesVersionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8eafd06acc132110553a938934a8af792c4ea55a407c9313e309214b6a5412)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudfunctionsFunctionSecretVolumesVersionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fa83ae8f213ae0c2e3acfc8f2e59df22b2d2cd623a3a0e1064ffb97cb54d29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57b80d41a0b7d0f51f5d65a89d1e6d0ebeb81cbe07a6080165fe7852c990a121)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4500b4449736dc968c14c0fa6e94483a9839122f8bbf26cc3ac04af73b09bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumesVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumesVersions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumesVersions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae0a5a40f96ee341eb4383be74ffe3e6d2b8e6edbe0ceaa09a7c1426100abfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudfunctionsFunctionSecretVolumesVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSecretVolumesVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb242e78235bbbaf68c77e867d75d2aae723eeb188a454757bcd7e7a8c83fb2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7e5cd9914217109722023f833f6a274f142622d8d670f8e71f71618b0bf0f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ab0ef074968a6e13f29e253b0c962234d3c02f6e5efaf0096a0bd1beb17f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumesVersions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumesVersions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumesVersions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5673346a58066edb509cd18d09c9fb87e3850178486598d7dfb0b11525be8c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSourceRepository",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class GoogleCloudfunctionsFunctionSourceRepository:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL pointing to the hosted repository where the function is defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#url GoogleCloudfunctionsFunction#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e474cea1964a541730bfba95e8c2e0f795a9ee04d0700eac52b12686ec6b3617)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL pointing to the hosted repository where the function is defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#url GoogleCloudfunctionsFunction#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionSourceRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctionsFunctionSourceRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionSourceRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44073296dab91908ee986ca45ba6dfd56027b0db9838acbd4667cd2f607b9e2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="deployedUrl")
    def deployed_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployedUrl"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6bd177cacfade610a7e5a50ab4708bc6f904ae9020ef3b532408079fa04b352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudfunctionsFunctionSourceRepository]:
        return typing.cast(typing.Optional[GoogleCloudfunctionsFunctionSourceRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudfunctionsFunctionSourceRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7039dfb924caa8175738054ad14591d2d716d4e3af7e744b161a07996cbf5b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class GoogleCloudfunctionsFunctionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#create GoogleCloudfunctionsFunction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#delete GoogleCloudfunctionsFunction#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#read GoogleCloudfunctionsFunction#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#update GoogleCloudfunctionsFunction#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5317627a6e47f46620a7c0b2e82b287c8f07d2aedb69d9745c6fa5effa722fbb)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#create GoogleCloudfunctionsFunction#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#delete GoogleCloudfunctionsFunction#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#read GoogleCloudfunctionsFunction#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudfunctions_function#update GoogleCloudfunctionsFunction#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudfunctionsFunctionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudfunctionsFunctionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudfunctionsFunction.GoogleCloudfunctionsFunctionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c58721aadeb6f690407edd318c214d030ce5cc46226468c45383714f25a24fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__18ddfa42e8d461967086e64f3a849f7138a170777ddaeca074925cb87aed1da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f754dfdc865317331395ef13e5f7522f55bd83a6cb6d6a9b2da6f84f317426cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4c00aa6610cf8afcbd45d18a5318c371d0d90f364de3b6a2d371b7282890c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2092e95989ac57ee02d7a0d01512cdc196ed6d70c220e725448276f2a54f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef74b86884e87677d349410f98b80f146a08ee9edaee6e619d1fd24d9758b952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudfunctionsFunction",
    "GoogleCloudfunctionsFunctionConfig",
    "GoogleCloudfunctionsFunctionEventTrigger",
    "GoogleCloudfunctionsFunctionEventTriggerFailurePolicy",
    "GoogleCloudfunctionsFunctionEventTriggerFailurePolicyOutputReference",
    "GoogleCloudfunctionsFunctionEventTriggerOutputReference",
    "GoogleCloudfunctionsFunctionSecretEnvironmentVariables",
    "GoogleCloudfunctionsFunctionSecretEnvironmentVariablesList",
    "GoogleCloudfunctionsFunctionSecretEnvironmentVariablesOutputReference",
    "GoogleCloudfunctionsFunctionSecretVolumes",
    "GoogleCloudfunctionsFunctionSecretVolumesList",
    "GoogleCloudfunctionsFunctionSecretVolumesOutputReference",
    "GoogleCloudfunctionsFunctionSecretVolumesVersions",
    "GoogleCloudfunctionsFunctionSecretVolumesVersionsList",
    "GoogleCloudfunctionsFunctionSecretVolumesVersionsOutputReference",
    "GoogleCloudfunctionsFunctionSourceRepository",
    "GoogleCloudfunctionsFunctionSourceRepositoryOutputReference",
    "GoogleCloudfunctionsFunctionTimeouts",
    "GoogleCloudfunctionsFunctionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__310860b61821063dde4c42272cd4db5cbdc52dfaff823d3a9d93a846da034198(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    runtime: builtins.str,
    available_memory_mb: typing.Optional[jsii.Number] = None,
    build_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    build_service_account: typing.Optional[builtins.str] = None,
    build_worker_pool: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    docker_registry: typing.Optional[builtins.str] = None,
    docker_repository: typing.Optional[builtins.str] = None,
    entry_point: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    event_trigger: typing.Optional[typing.Union[GoogleCloudfunctionsFunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    https_trigger_security_level: typing.Optional[builtins.str] = None,
    https_trigger_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ingress_settings: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_instances: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    source_archive_bucket: typing.Optional[builtins.str] = None,
    source_archive_object: typing.Optional[builtins.str] = None,
    source_repository: typing.Optional[typing.Union[GoogleCloudfunctionsFunctionSourceRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudfunctionsFunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_http: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpc_connector: typing.Optional[builtins.str] = None,
    vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__5b49ef227bace9f957db83c6cf5b3e40b1aadb2cee99b5e38f074f6fe3b847f1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2387dbae7bc0a675ae0676ebe60b6cbe70941469f246207a12288095d35c7dd6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4926d2d2a74af2fbaaa5ff04030f3a39a3820529c853336766ef4a3eb85e10(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ee8ac04b4b348228c73f3450fede3abd8f43c03372959c14a3484edd85beba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa8bc3d2af576b4d77dff1c4e12931fc8943bea9fd0a6f2e806e5e33b38a88b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928410746c7d342d5d427112e775259ba144377d5cd2b97aa9478b4ed8344b57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca87806aa91eab247b25b862a4706088dd678b3eebef6c79960abf264047402c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57699ca04ceb2c2080aabf89b64e28665d74718784501e8bd616c0a255fe2ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11d50e3d26b8b318b494bfa00d66b8e168efb4ab7bfe9f8c4e5d4fbfe145c3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad68406f7c27090ef76e936c7a80ba9bf2345f5e5c3008426cd6c106c6ad3ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81146bd8e061fd362a4adc07666ee68b88b4da142b87faab28d93ecc7ba9e80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2692a195cab2e4767c23141cda1e8abee8bc3bc07fd0034f8378ddca006910c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5dcecd7ed8bd33ed0ba8277655b18a140aa1fbc4b4fe95cc9b7af5403173478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e800d85cfe825cfe2939e59bfe0cbda7a7a3422fbd2f06d90658e0e1d471bb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e20c8580799dfcb0f669efd5bc8eddaaf3cb295ca486c4d78e8c681ae5c5b29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7e12873ca17a81545740ab7c3e3061a4c5fc93a5c5d04b1d865542e27e8dc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9557180cbe33bf6e47de5dc243c44a0f610f8545de0dd9aa1a996e4dd6d6fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f6a8f5d2066668b50b4651b0927ec1853ea778a78fcd1b123eebf55d35b83d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f8d364ba605210fd7fa2964d22ed1ec81bc531746aec50e769e25abd3c0f4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66284978ca557754c0c6ae68e54091f084eba0b319115e057598af489568e1e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0c247b3bcfed9f1e97189e959b9c00d2d2e614bea13a1fa0a99e3f9883a3de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98621bf0132d6bf799d37b532bdeff0873102a5867b79540f2cf1734b5738f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcb684ba51f0830b93f181972a46bec4e27dcf7de5f0363b62defe309e176d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decb700af80784aa1f9baf9dc97aefd7fb34f765de27372a5042f6c98951ac03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871bbf67aaab28e5f1b2b026a1fbf46a890ee4b4e4506b1d111068cad49603fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971de6e660efb1e4b814dde816147998c35d05c1a969d93309d5120158689912(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea6cbfabad4d825cf1e08af1d2b31a2b6ad42c19a0168b2b9449c1f18f3e3f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815c47f59af7e1c0def3636b790f432f70249cd47f0abf090a8889e5d3991e4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5443829e07afc07e1de8a22e40f04b05f56ae8e4b149b8cb73a7cd3fdae5bc6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a47cd611e542d12896a38bb494f2d23d759155d5482c8989c227901b1b8a01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5daadbf497b5abc10fac09bd05f63a263c28a422fb37f98d0ffade595638b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78c36e14eb7ca85d3db31c12c173c504d332e330bf2564d04b2617ac87b01f9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    runtime: builtins.str,
    available_memory_mb: typing.Optional[jsii.Number] = None,
    build_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    build_service_account: typing.Optional[builtins.str] = None,
    build_worker_pool: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    docker_registry: typing.Optional[builtins.str] = None,
    docker_repository: typing.Optional[builtins.str] = None,
    entry_point: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    event_trigger: typing.Optional[typing.Union[GoogleCloudfunctionsFunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    https_trigger_security_level: typing.Optional[builtins.str] = None,
    https_trigger_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ingress_settings: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_instances: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    source_archive_bucket: typing.Optional[builtins.str] = None,
    source_archive_object: typing.Optional[builtins.str] = None,
    source_repository: typing.Optional[typing.Union[GoogleCloudfunctionsFunctionSourceRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudfunctionsFunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_http: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpc_connector: typing.Optional[builtins.str] = None,
    vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86892f971d51f59f86d547af4e1c2ef006b040bfe6e70bcc37a59cef3068dc5e(
    *,
    event_type: builtins.str,
    resource: builtins.str,
    failure_policy: typing.Optional[typing.Union[GoogleCloudfunctionsFunctionEventTriggerFailurePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6d0257e27025d62a5684483773133ad7d23e9e999b48d90a205c768b0e5fd2(
    *,
    retry: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c227941f78b12e9b0f74df8dab8400ea1771d7dbbc8b08a3272bec4d7f833b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a05e497a134105471b83be80ae18fc34c330492480b53f577213c824522ec36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e182ecff88afaedcf18fb768a188dab1cf150f130da0d8eb4b2f83b9e24b9d91(
    value: typing.Optional[GoogleCloudfunctionsFunctionEventTriggerFailurePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb82c0c409ed035d810dca6fd8484bf3d04a2727f756a44f8ce0cd3a836d709a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259d2c941594da7503b048dc42e7cd416db717254d864fe20bc3583fed35b435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082453c51a8c5e772c455b7b370c6a9645ca7058098d4759c115b872b7b162af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe43846957a1c41bbc98f7eac4c5938a8b2790c2029769e90c185690fb1ce39(
    value: typing.Optional[GoogleCloudfunctionsFunctionEventTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c6c7b9d1f0fb98dcd4f5de42489977bdb3b1448faabb18979e9bf5cc836468(
    *,
    key: builtins.str,
    secret: builtins.str,
    version: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad700cbaae0440e49c8316f6a524b4419890addd8734abbcd1d0aee16492b7e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4798fbd71d48592bc1672667fcf12eacac8f117648d3455ebe70aeede4763264(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c2cabfb2ec136e460458a7f133b54fc643352a7c8d947bef06aafb886d9bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4cfac6cffecc9a9d81e6af2ecefffe0a2e8d60f94508bd1524503c96650019(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195860be8bcf57838cd76578362ec98266c2ff9665287263dc6a6fd198bf8d09(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b9a9db86abb465fb3d64c3036402a9e62539533b06fe9989f11bb188055e95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretEnvironmentVariables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488c6f08f11a301aaf01b30fa164ed9ab0daff1fcf35307b5b09b4789d6b2f78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488ad83c8b7c15da887095374f700a7fb57555114c4240c22f6df21f80059aaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674850d0ec56a8f63867087838b5f02d0002fe5303a6706d0a7ec49615408492(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd55db2bed8f79f0fb1e718e9961104eefa3f7a7dd01f7343afa5a47b051d52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc01f7685a4e053269d94146426e9a9b5ade624f9b55184e6f19bafe94e43ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8bff73b02f45613da86f4f11d923609e65ce93041d2d4c3b13f92524082334(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretEnvironmentVariables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb4c0eb37763c035d14a38690593213ce5544a52399b5fa5f4e95e9a99aefc2(
    *,
    mount_path: builtins.str,
    secret: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
    versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc56e5e6973d92951330ee00d681ee0641348a6f715cf32fa372c9baa4c7e6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060bc52756a8054fc9137a6e1fcce5c9d32cf15e17b3cb8d0620b5633ec5ca87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ec53ae029f3f1c4a2d22ef4a8b779b9f026396b08f3c14876b9478751aebfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fef000544a86e68581a6fcf9e7d1a4314fa12c66122bb0c2ed6d8b5399f2de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7708cc163d6ce9586fc43d7d212d4ff64363625d154decf5d3439eb02fbe20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b1795a6ba79198cced34360c309b9f61a33ac816cf27c19b6c7d67fe56bfa8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60597188e6663b857b17f0fdc1e4369bce606ee5a272e7d05e36fb3128a1c832(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576b81e6ff19db3c66507f1c1c436445aaed41bd0e224867e9496b3c5c070da4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudfunctionsFunctionSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de92bba460f1faa707a60af3f30713e2b9612971c6faac581f7183ef3e4a658d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a763178564d8ec9d5d7e8015ff55f4f3a3757f6ef224c81e0e1b8c46b4adb17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbf25810eb43bbccf6c138bdfc449069bdf5745869e21f9df613f99ebc34ec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821d6c91774cfa5a2c47134eb6b576d6bdd500358c5a126b0be812c4120f8ea0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7b47bdaef0a51882a0ecf4718fa54ad0a4a4bdc8d288e2671161471828d39b(
    *,
    path: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95744cb95130d5651d152d0185178482fdc0d139d891e678c93c8004399c30d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8eafd06acc132110553a938934a8af792c4ea55a407c9313e309214b6a5412(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fa83ae8f213ae0c2e3acfc8f2e59df22b2d2cd623a3a0e1064ffb97cb54d29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b80d41a0b7d0f51f5d65a89d1e6d0ebeb81cbe07a6080165fe7852c990a121(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4500b4449736dc968c14c0fa6e94483a9839122f8bbf26cc3ac04af73b09bac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae0a5a40f96ee341eb4383be74ffe3e6d2b8e6edbe0ceaa09a7c1426100abfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudfunctionsFunctionSecretVolumesVersions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb242e78235bbbaf68c77e867d75d2aae723eeb188a454757bcd7e7a8c83fb2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e5cd9914217109722023f833f6a274f142622d8d670f8e71f71618b0bf0f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ab0ef074968a6e13f29e253b0c962234d3c02f6e5efaf0096a0bd1beb17f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5673346a58066edb509cd18d09c9fb87e3850178486598d7dfb0b11525be8c20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionSecretVolumesVersions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e474cea1964a541730bfba95e8c2e0f795a9ee04d0700eac52b12686ec6b3617(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44073296dab91908ee986ca45ba6dfd56027b0db9838acbd4667cd2f607b9e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bd177cacfade610a7e5a50ab4708bc6f904ae9020ef3b532408079fa04b352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7039dfb924caa8175738054ad14591d2d716d4e3af7e744b161a07996cbf5b5a(
    value: typing.Optional[GoogleCloudfunctionsFunctionSourceRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5317627a6e47f46620a7c0b2e82b287c8f07d2aedb69d9745c6fa5effa722fbb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c58721aadeb6f690407edd318c214d030ce5cc46226468c45383714f25a24fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ddfa42e8d461967086e64f3a849f7138a170777ddaeca074925cb87aed1da6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f754dfdc865317331395ef13e5f7522f55bd83a6cb6d6a9b2da6f84f317426cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4c00aa6610cf8afcbd45d18a5318c371d0d90f364de3b6a2d371b7282890c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2092e95989ac57ee02d7a0d01512cdc196ed6d70c220e725448276f2a54f49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef74b86884e87677d349410f98b80f146a08ee9edaee6e619d1fd24d9758b952(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudfunctionsFunctionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
